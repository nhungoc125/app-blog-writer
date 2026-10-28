# Post brief, structure and pre-publish checklist

## Brief (`posts/<slug>/brief.md`)

```markdown
# Brief — <working title>
- Target query (validated? y/n, source): 
- Secondary queries:
- Search intent: learn / compare / buy / how-to
- Reader: <persona from product brief>
- What the top results do well / miss:
- Our non-commodity angle:
- Proof assets from the product: <screens, flows, data, code decisions> (evidence paths)
- Outline (H2s):
- Images: <type, what it shows, source screen/file>
- Internal links: <pages/posts>
- CTA: <real next step in the product>
- Claims to avoid: <from product brief>
```

## Post structure

```markdown
---
<frontmatter matching the repo's existing posts exactly; if none exist, use:>
title: "<title, ~50–60 chars>"
description: "<meta description, ~140–160 chars>"
slug: "<short-descriptive-slug>"
date: "YYYY-MM-DD"
updated: "YYYY-MM-DD"
author: "<real person>"
image: "/blog/images/<slug>-featured.webp"
imageAlt: "<alt text>"
tags: ["<cluster>"]
---

# <H1>

<Opening: answer the core question in 2–3 sentences. Then one sentence on what the post covers.>

![<alt>](images/<slug>-featured.webp)

## <H2 that names a sub-question or step>
...

## <H2>
...

## <Optional: FAQ with 3–5 real questions; plain H3 + short answers>

## <CTA heading>
<One paragraph and one link/button to the product's real next step.>
```

Deliver alongside the post:

- `meta.json` — title, description, slug, canonical URL, OG image, JSON-LD (BlogPosting + BreadcrumbList)
- `images/` — SVG sources plus exported WebP/PNG, each with alt text listed in `meta.json`

## Matching an existing blog

`scan_repo.py` lists existing posts and their frontmatter keys. Open two recent posts and copy:

- Folder and filename pattern (e.g. `src/content/blog/<slug>/index.mdx`, `posts/YYYY-MM-DD-slug.md`)
- Frontmatter keys, value types and date format; required fields in content-collection schemas (`src/content/config.ts`)
- Image location and reference style (`/images/blog/...`, co-located `./cover.png`, imported components)
- MDX components they use (callouts, `<Image>`), heading levels (some layouts render the H1 from frontmatter — then start body at H2)
- Category/tag vocabulary already in use

## Pre-publish checklist

- [ ] Answers the query in the first 2–3 sentences
- [ ] Non-commodity angle is clearly present (something only this product's team could say)
- [ ] Every product claim traces to the product brief; nothing from "claims to confirm"
- [ ] No invented statistics, customers, quotes, ratings or results
- [ ] Title ~50–60 chars, unique; meta description ~140–160 chars
- [ ] One H1; logical H2/H3 order
- [ ] 1–3 internal links with descriptive anchors; external links to sources actually opened
- [ ] Every image has a descriptive file name and alt text; WebP exported; sizes reasonable
- [ ] Mockups use sample data only; no third-party logos or characters
- [ ] Structured data matches visible content and validates
- [ ] Frontmatter matches the repo's format; build/preview runs if possible
- [ ] `check_post.py` passes (or remaining warnings are explained)
- [ ] Author named; dates set
