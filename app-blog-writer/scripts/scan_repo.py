#!/usr/bin/env python3
"""Inventory a product repository for content planning.

Usage:
    python scan_repo.py <repo-path> [--max-items 60]

Prints JSON describing the framework, marketing pages/routes, copy (i18n) files,
pricing candidates, docs, existing blog posts and their frontmatter keys, images
and logo candidates, SEO files, meta titles/descriptions, and integration hints.
It only lists and lightly parses files; read the important ones yourself.
"""
import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {
    ".git", "node_modules", ".next", ".nuxt", ".svelte-kit", ".astro", "dist", "build",
    "out", ".output", "coverage", "vendor", "venv", ".venv", "__pycache__", ".turbo",
    ".cache", "tmp", ".vercel", ".idea", ".vscode", "target", "Pods", ".gradle",
}
TEXT_EXT = {".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".html", ".htm",
            ".md", ".mdx", ".json", ".yml", ".yaml", ".rb", ".php", ".py", ".erb", ".twig",
            ".blade.php", ".liquid", ".njk", ".hbs", ".txt", ".toml", ".css", ".scss"}
IMAGE_EXT = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".avif", ".gif", ".ico"}

ROUTE_PATTERNS = [
    re.compile(r"(^|/)app/.*page\.(tsx|jsx|ts|js|mdx)$"),
    re.compile(r"(^|/)pages/.*\.(tsx|jsx|ts|js|vue|astro|md|mdx|svelte)$"),
    re.compile(r"(^|/)src/pages/.*\.(astro|tsx|jsx|md|mdx|vue|svelte)$"),
    re.compile(r"(^|/)src/routes/.*\+page\.svelte$"),
    re.compile(r"(^|/)app/routes/.*\.(tsx|jsx|ts|js)$"),
    re.compile(r"(^|/)resources/views/.*\.blade\.php$"),
    re.compile(r"(^|/)app/views/.*\.(erb|haml|slim)$"),
    re.compile(r"(^|/)templates/.*\.html$"),
]
I18N_HINTS = re.compile(r"(^|/)(locales?|i18n|messages|lang|translations)(/|$)", re.I)
BLOG_DIR_HINTS = re.compile(r"(^|/)(blog|posts|articles|_posts|content/blog|src/content/blog|news|resources)(/|$)", re.I)
DOC_HINTS = re.compile(r"(^|/)(docs?|documentation|help|guides?)(/|$)", re.I)
LOGO_HINTS = re.compile(r"(logo|brand|mark|icon|favicon|wordmark)", re.I)
PRICE_RE = re.compile(r"(\$|€|£|₫|VND|USD)\s?\d|\d+\s?(/|per)\s?(mo|month|year|yr)\b", re.I)
META_TITLE_RE = re.compile(r"(?:<title>([^<]{3,120})</title>|title\s*[:=]\s*[\"'`]([^\"'`]{3,120})[\"'`])")
META_DESC_RE = re.compile(r"description\s*[:=]\s*[\"'`]([^\"'`]{20,300})[\"'`]|<meta\s+name=[\"']description[\"']\s+content=[\"']([^\"']{20,300})")
ENV_KEY_RE = re.compile(r"^([A-Z][A-Z0-9_]{2,})\s*=", re.M)

FRAMEWORK_DEPS = [
    ("next", "Next.js"), ("nuxt", "Nuxt"), ("astro", "Astro"), ("@remix-run/react", "Remix"),
    ("@sveltejs/kit", "SvelteKit"), ("gatsby", "Gatsby"), ("@11ty/eleventy", "Eleventy"),
    ("vite", "Vite"), ("react", "React"), ("vue", "Vue"), ("svelte", "Svelte"), ("@angular/core", "Angular"),
    ("tailwindcss", "Tailwind CSS"), ("next-intl", "next-intl"), ("i18next", "i18next"),
    ("contentlayer", "Contentlayer"), ("@nuxt/content", "Nuxt Content"), ("next-sitemap", "next-sitemap"),
    ("stripe", "Stripe"), ("@stripe/stripe-js", "Stripe"), ("lucide-react", "lucide icons"),
    ("@heroicons/react", "heroicons"), ("shadcn", "shadcn/ui"), ("@radix-ui/react-dialog", "Radix UI"),
]


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith(".") or d in {".github"}]
        for name in filenames:
            yield Path(dirpath) / name


def read_text(path: Path, limit=200_000):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read(limit)
    except Exception:
        return ""


def frontmatter_keys(text: str):
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end == -1:
        return []
    block = text[3:end]
    keys = []
    for line in block.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:", line)
        if m:
            keys.append(m.group(1))
    return keys


def detect_frameworks(root: Path):
    found = []
    for pkg in list(root.glob("package.json")) + list(root.glob("*/package.json")) + list(root.glob("apps/*/package.json")) + list(root.glob("packages/*/package.json")):
        try:
            data = json.loads(read_text(pkg))
        except Exception:
            continue
        deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
        for dep, label in FRAMEWORK_DEPS:
            if dep in deps and label not in found:
                found.append(label)
    markers = {
        "Gemfile": "Ruby/Rails", "composer.json": "PHP/Laravel", "manage.py": "Django",
        "pyproject.toml": "Python", "requirements.txt": "Python", "hugo.toml": "Hugo",
        "_config.yml": "Jekyll", "pubspec.yaml": "Flutter", "go.mod": "Go",
    }
    for marker, label in markers.items():
        if (root / marker).exists() and label not in found:
            found.append(label)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo")
    ap.add_argument("--max-items", type=int, default=60)
    args = ap.parse_args()
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(json.dumps({"error": f"not a directory: {root}"}))
        sys.exit(1)
    cap = args.max_items

    out = {
        "repo": str(root), "frameworks": detect_frameworks(root),
        "readme": [], "routes": [], "i18n_files": [], "pricing_candidates": [],
        "docs": [], "blog_posts": [], "blog_frontmatter_keys": {}, "images": [],
        "logo_candidates": [], "seo_files": [], "meta_titles": [], "meta_descriptions": [],
        "env_keys": [], "content_config": [], "todo_or_coming_soon": [], "file_count": 0,
        "top_extensions": {},
    }
    ext_counter = Counter()
    fm_counter = Counter()

    for path in walk(root):
        rel = path.relative_to(root).as_posix()
        out["file_count"] += 1
        ext = path.suffix.lower()
        ext_counter[ext] += 1
        name = path.name.lower()

        if name.startswith("readme"):
            out["readme"].append(rel)
        if name in {"robots.txt", "robots.ts", "sitemap.xml", "sitemap.ts", "next-sitemap.config.js", "manifest.json", "site.webmanifest"}:
            out["seo_files"].append(rel)
        if name in {".env.example", ".env.sample", ".env.template", "env.example"}:
            out["env_keys"].extend(ENV_KEY_RE.findall(read_text(path)))
        if re.search(r"content/config\.(ts|js|mjs)$|contentlayer\.config|content\.config", rel):
            out["content_config"].append(rel)

        if ext in IMAGE_EXT:
            if LOGO_HINTS.search(name):
                out["logo_candidates"].append(rel)
            elif re.search(r"(^|/)(public|static|assets|images|img)/", rel):
                out["images"].append(rel)
            continue

        if ext not in TEXT_EXT and not name.endswith(".blade.php"):
            continue

        if any(p.search(rel) for p in ROUTE_PATTERNS):
            out["routes"].append(rel)
        if I18N_HINTS.search(rel) and ext in {".json", ".yml", ".yaml", ".ts", ".js", ".php", ".po"}:
            out["i18n_files"].append(rel)
        if ext in {".md", ".mdx"}:
            if BLOG_DIR_HINTS.search(rel):
                text = read_text(path, 5000)
                keys = frontmatter_keys(text)
                out["blog_posts"].append(rel)
                fm_counter.update(keys)
            elif DOC_HINTS.search(rel):
                out["docs"].append(rel)

        if ext in {".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte", ".astro", ".json", ".html", ".php", ".erb", ".yml", ".yaml"}:
            text = read_text(path)
            if ("pric" in name or "plan" in name or "billing" in name or "tier" in name) or (
                "pricing" in text.lower() and PRICE_RE.search(text)):
                out["pricing_candidates"].append(rel)
            if re.search(r"(layout|head|seo|metadata|_app|_document|index\.html|app\.html|base\.html)", rel, re.I) or "export const metadata" in text:
                for m in META_TITLE_RE.finditer(text):
                    t = (m.group(1) or m.group(2) or "").strip()
                    if t and t not in out["meta_titles"] and len(out["meta_titles"]) < 15:
                        out["meta_titles"].append(t)
                for m in META_DESC_RE.finditer(text):
                    d = (m.group(1) or m.group(2) or "").strip()
                    if d and d not in out["meta_descriptions"] and len(out["meta_descriptions"]) < 15:
                        out["meta_descriptions"].append(d)
            if re.search(r"coming soon|TODO|FIXME|not implemented|featureFlag|feature_flag", text, re.I):
                if len(out["todo_or_coming_soon"]) < cap:
                    out["todo_or_coming_soon"].append(rel)

    out["blog_frontmatter_keys"] = dict(fm_counter.most_common(30))
    out["top_extensions"] = dict(ext_counter.most_common(12))
    out["env_keys"] = sorted(set(out["env_keys"]))
    for key in ["readme", "routes", "i18n_files", "pricing_candidates", "docs", "blog_posts",
                "images", "logo_candidates", "seo_files", "content_config"]:
        items = sorted(set(out[key]))
        out[key + "_total"] = len(items)
        out[key] = items[:cap]
    out["next_steps"] = [
        "Read README and meta titles/descriptions for positioning.",
        "Open routes for home, pricing, features/solutions; read i18n files for real copy.",
        "Open pricing_candidates to confirm plans and limits.",
        "If blog_posts exist, open two recent ones to copy the exact frontmatter and folder pattern.",
        "Check todo_or_coming_soon files before claiming any feature.",
        "Run extract_brand.py for colors, fonts and logos.",
    ]
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
