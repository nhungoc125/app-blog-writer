#!/usr/bin/env python3
"""Extract brand candidates (colors, fonts, radius, logos) from a codebase.

Usage:
    python extract_brand.py <repo-path>

Prints JSON with:
  css_variables   color-like CSS custom properties (name -> value), light and dark scopes
  theme_colors    named colors from Tailwind/theme/design-token files
  hex_frequency   most used hex colors across styles and components
  fonts           font families from CSS, Google Fonts URLs, next/font imports, Tailwind config
  radius          radius tokens/values found
  logos           logo/icon file candidates
  chosen          empty roles for you to fill after review (primary, accent, ink, surface, muted, font_body, font_heading, radius)
Review the candidates; the brand primary is usually the color on primary buttons and links.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".next", ".nuxt", ".svelte-kit", ".astro", "dist", "build", "out",
             ".output", "coverage", "vendor", "venv", ".venv", "__pycache__", ".turbo", ".cache", "target"}
STYLE_EXT = {".css", ".scss", ".sass", ".less", ".pcss"}
CODE_EXT = {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte", ".astro", ".html", ".json"}

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{3}){1,2}\b")
CSS_VAR_RE = re.compile(r"(--[\w-]+)\s*:\s*([^;}{]+);")
COLOR_VALUE_RE = re.compile(r"^(#(?:[0-9a-fA-F]{3}){1,2}|rgba?\(.+\)|hsla?\(.+\)|oklch\(.+\)|oklab\(.+\)|\d{1,3}(\.\d+)?\s+\d{1,3}(\.\d+)?%\s+\d{1,3}(\.\d+)?%)$")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;}{]+)[;}]")
GOOGLE_FONTS_RE = re.compile(r"fonts\.googleapis\.com/css2?\?([^\"')\s]+)")
NEXT_FONT_RE = re.compile(r"import\s*\{([^}]+)\}\s*from\s*[\"']next/font/(google|local)[\"']")
TW_FONT_RE = re.compile(r"fontFamily\s*:\s*\{([^}]+)\}", re.S)
TW_COLOR_ENTRY_RE = re.compile(r"[\"']?([\w-]+)[\"']?\s*:\s*[\"'](#(?:[0-9a-fA-F]{3}){1,2})[\"']")
RADIUS_RE = re.compile(r"(--radius[\w-]*)\s*:\s*([^;]+);|border-radius\s*:\s*([^;]+);")
LOGO_RE = re.compile(r"(logo|brand|wordmark|mark|icon|favicon)", re.I)


def files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for n in filenames:
            yield Path(dirpath) / n


def read(p, limit=400_000):
    try:
        return open(p, encoding="utf-8", errors="ignore").read(limit)
    except Exception:
        return ""


def norm_hex(h):
    h = h.lower()
    if len(h) == 4:
        h = "#" + "".join(c * 2 for c in h[1:])
    return h


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    root = Path(sys.argv[1]).resolve()
    css_vars = {"light": {}, "dark": {}}
    theme_colors = {}
    hex_counter = Counter()
    fonts = Counter()
    font_sources = defaultdict(set)
    radius = Counter()
    logos = []

    for p in files(root):
        rel = p.relative_to(root).as_posix()
        ext = p.suffix.lower()
        if ext in {".svg", ".png", ".ico", ".webp", ".jpg", ".jpeg"} and LOGO_RE.search(p.name):
            logos.append(rel)
            continue
        if ext not in STYLE_EXT and ext not in CODE_EXT:
            continue
        if ext == ".json" and not re.search(r"(token|theme|color|brand|design|tailwind)", p.name, re.I):
            continue
        text = read(p)
        if not text:
            continue

        for h in HEX_RE.findall(text):
            hex_counter[norm_hex(h)] += 1

        if ext in STYLE_EXT or ext in {".vue", ".svelte", ".astro", ".html"}:
            # split dark scopes roughly
            for scope_match in re.finditer(r"([^{}]+)\{([^{}]*)\}", text):
                selector, body = scope_match.group(1), scope_match.group(2)
                scope = "dark" if re.search(r"\.dark|\[data-theme=['\"]?dark|prefers-color-scheme:\s*dark", selector) else "light"
                for name, value in CSS_VAR_RE.findall(body):
                    value = value.strip()
                    if COLOR_VALUE_RE.match(value) and name not in css_vars[scope]:
                        css_vars[scope][name] = value
                    if name.startswith("--font") and name not in css_vars[scope]:
                        css_vars[scope][name] = value
            for fam in FONT_FAMILY_RE.findall(text):
                first = fam.split(",")[0].strip().strip("'\"")
                if first and not first.startswith("var(") and first.lower() not in {"inherit", "initial"}:
                    fonts[first] += 1
                    font_sources[first].add(rel)

        for q in GOOGLE_FONTS_RE.findall(text):
            for fam in re.findall(r"family=([^&:]+)", q):
                name = fam.replace("+", " ")
                fonts[name] += 3
                font_sources[name].add(rel)
        for names, kind in NEXT_FONT_RE.findall(text):
            for n in names.split(","):
                n = n.strip().split(" as ")[0].replace("_", " ")
                if n:
                    fonts[n] += 5
                    font_sources[n].add(rel + f" (next/font/{kind})")
        if "tailwind" in p.name.lower() or "theme" in p.name.lower() or ext == ".json":
            for block in TW_FONT_RE.findall(text):
                for fam in re.findall(r"[\"']([A-Z][\w ]+)[\"']", block):
                    fonts[fam] += 2
                    font_sources[fam].add(rel)
            for key, val in TW_COLOR_ENTRY_RE.findall(text):
                theme_colors.setdefault(f"{rel}:{key}", norm_hex(val))
        for m in RADIUS_RE.finditer(text):
            val = (m.group(2) or m.group(3) or "").strip()
            if val and len(val) < 30:
                radius[val] += 1

    result = {
        "repo": str(root),
        "css_variables": {k: dict(list(v.items())[:80]) for k, v in css_vars.items()},
        "theme_colors": dict(list(theme_colors.items())[:80]),
        "hex_frequency": dict(hex_counter.most_common(25)),
        "fonts": [{"family": f, "score": s, "sources": sorted(font_sources[f])[:5]} for f, s in fonts.most_common(12)],
        "radius": dict(radius.most_common(8)),
        "logos": sorted(logos)[:30],
        "chosen": {
            "primary": "", "accent": "", "ink": "", "surface": "", "muted": "", "border": "",
            "success": "", "font_body": "", "font_heading": "", "font_fallback": "'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
            "radius": "", "logo": "", "notes": "Fill after reviewing candidates; record why each was chosen in brand-notes.md"
        },
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
