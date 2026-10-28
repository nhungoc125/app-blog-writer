#!/usr/bin/env python3
"""Lint a markdown/MDX blog post for SEO basics and leftover placeholders.

Usage:
    python check_post.py <post.md> [--body-h1-from-frontmatter]

Checks: frontmatter title/description length, single H1, heading order, opening
length, images without alt text, internal/external link counts, filler phrases,
placeholders ([TODO], {{...}}, lorem ipsum, XX%), word count.
Exit code 1 if any ERROR is found; WARN lines are advisory.
Use --body-h1-from-frontmatter when the blog layout renders the H1 from the title
(then the body should have no H1).
"""
import re
import sys
from pathlib import Path

FILLER = [
    "in today's fast-paced world", "ever-evolving landscape", "unlock the power", "game-changer",
    "game changer", "revolutionize", "seamlessly", "delve into", "it's important to note",
    "whether you're a", "look no further", "to the next level", "a testament to",
    "navigate the complexities", "in conclusion", "leverage the power", "cutting-edge",
    "harness the power", "in the realm of", "elevate your",
]
PLACEHOLDERS = re.compile(r"\[(TODO|TK|TBD|PLACEHOLDER|IMAGE[^\]]*)\]|\{\{[^}]+\}\}|lorem ipsum|XX%|\bTKTK\b", re.I)


def parse(text):
    fm = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^([\w-]+)\s*:\s*(.*)$", line)
                if m:
                    fm[m.group(1)] = m.group(2).strip().strip("\"'")
            body = text[end + 4:]
    return fm, body


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    path = Path(sys.argv[1])
    h1_from_fm = "--body-h1-from-frontmatter" in sys.argv
    text = path.read_text(encoding="utf-8")
    fm, body = parse(text)
    errors, warns, info = [], [], []

    # strip code blocks for analysis
    clean = re.sub(r"```.*?```", "", body, flags=re.S)

    title = fm.get("title", "")
    desc = fm.get("description", "") or fm.get("excerpt", "") or fm.get("summary", "")
    if not title:
        warns.append("No frontmatter title (fine if the repo stores titles elsewhere).")
    elif not 30 <= len(title) <= 65:
        warns.append(f"Title is {len(title)} chars; aim for ~50-60.")
    if not desc:
        warns.append("No meta description/excerpt in frontmatter.")
    elif not 110 <= len(desc) <= 165:
        warns.append(f"Description is {len(desc)} chars; aim for ~140-160.")

    headings = re.findall(r"^(#{1,6})\s+(.+)$", clean, re.M)
    h1s = [h for h in headings if len(h[0]) == 1]
    if h1_from_fm:
        if h1s:
            errors.append("Body has an H1 but the layout renders the H1 from frontmatter.")
    elif len(h1s) != 1:
        errors.append(f"Expected exactly one H1, found {len(h1s)}.")
    prev = 1 if not h1_from_fm else 1
    for hashes, txt in headings:
        lvl = len(hashes)
        if lvl > prev + 1 and lvl > 2:
            warns.append(f"Heading level jumps to H{lvl}: '{txt[:50]}'")
        prev = lvl

    paras = [p.strip() for p in re.split(r"\n\s*\n", clean) if p.strip() and not p.strip().startswith(("#", "!", "<", "|", "-", "*", "1."))]
    if paras:
        first_words = len(paras[0].split())
        if first_words > 80:
            warns.append(f"Opening paragraph is {first_words} words; answer the query in 2-3 sentences.")

    images = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", body)
    html_imgs = re.findall(r"<(?:img|Image)\b[^>]*>", body)
    for alt, src in images:
        if not alt.strip():
            errors.append(f"Image without alt text: {src}")
    for tag in html_imgs:
        if not re.search(r"\balt=\S", tag):
            errors.append(f"Image tag without alt: {tag[:60]}")
    if not images and not html_imgs:
        warns.append("No images found.")

    links = re.findall(r"(?<!!)\[([^\]]+)\]\(([^)]+)\)", clean)
    internal = [l for l in links if l[1].startswith(("/", "#", "./", "../")) or not re.match(r"https?://", l[1])]
    external = [l for l in links if re.match(r"https?://", l[1])]
    if len(internal) < 1:
        warns.append("No internal links; add 1-3 to related pages/posts.")
    for anchor, _ in links:
        if anchor.strip().lower() in {"here", "click here", "this", "link", "read more"}:
            warns.append(f"Non-descriptive link text: '{anchor}'")

    low = clean.lower()
    for phrase in FILLER:
        if phrase in low:
            warns.append(f"Filler phrase: '{phrase}'")
    for m in PLACEHOLDERS.finditer(text):
        errors.append(f"Placeholder left in post: '{m.group(0)}'")

    words = len(re.findall(r"\b\w+\b", re.sub(r"[#>*_`|\-]", " ", clean)))
    info.append(f"Words: {words} | H2s: {sum(1 for h in headings if len(h[0]) == 2)} | images: {len(images) + len(html_imgs)} | internal links: {len(internal)} | external links: {len(external)}")

    for line in info:
        print("INFO ", line)
    for line in warns:
        print("WARN ", line)
    for line in errors:
        print("ERROR", line)
    if not errors:
        print("OK   no blocking issues")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
