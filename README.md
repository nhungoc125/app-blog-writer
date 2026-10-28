# app-blog-writer

A Claude skill that reads a product's source code, plans SEO blog content, writes the posts after you approve the plan, and creates on-brand images (UI mockups, diagrams, featured images) from the same source.

## What it does

1. Builds a product brief from the code, with file evidence for every feature
2. Extracts brand colors, fonts, logo and voice
3. Researches competitors and search results
4. Writes a content plan and **waits for your approval**
5. Writes each post, checks every claim against the code, runs an SEO pass
6. Creates images: real screenshots when the app runs, otherwise SVG mockups rebuilt from your components, plus diagrams and a featured image
7. Saves posts in your blog's existing format and logs progress in `.blog-writer/`

SEO rules follow Google Search Central guidance as of October 2026 (see `app-blog-writer/references/seo-2026.md`).

## Install

**Claude Code:** copy the skill folder into your skills directory.

```bash
cp -r app-blog-writer ~/.claude/skills/
```

**Claude.ai:** zip the `app-blog-writer` folder (or use the packaged `.skill` file) and upload it in Settings → Capabilities → Skills.

## Use

Open your project and ask, for example:

> Plan our blog content from this codebase, then write the first post with images.

Scripts need Python 3 with `cairosvg` and `Pillow` for image export:

```bash
pip install cairosvg Pillow
```

## Layout

```
app-blog-writer/
├── SKILL.md
├── references/   SEO 2026 guide, source analysis, templates, style, image guide
├── scripts/      scan_repo.py, extract_brand.py, render_images.py, check_post.py
└── assets/       og-template.svg
```
