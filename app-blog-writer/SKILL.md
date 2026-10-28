---
name: app-blog-writer
description: Plans and writes SEO blog content for a software product by reading its source code, then creates on-brand images (UI mockups, diagrams, featured/OG images) from that same source. Use this skill whenever someone wants a content plan, blog strategy, SEO articles, landing-page copy or blog images for their own app, SaaS, website or product — especially when they share a repo, codebase, zip or folder, say "plug you into the code", "write blog posts for my app", "plan our content", "SEO for our product", or ask for images that match their brand. Also use it to continue an existing plan (a .blog-writer/ folder in the repo) or write the next post in a series.
---

# App Blog Writer

Turn a product's source code into an approved content plan, then into published-ready blog posts with on-brand images. The source code is the single best source of truth about what the product actually does, how it talks, and what it looks like, so everything here starts from it.

The user has delegated decisions to you: choose the audience, topics, angles, structure and visuals yourself, and explain your reasoning briefly. There is exactly **one hard approval gate**: the content plan. Never start writing posts before the user approves the plan (or explicitly says to skip approval).

## Workflow at a glance

1. Locate the source and any saved state
2. Build the product brief from the code (facts with evidence)
3. Extract the brand (colors, type, logo, voice)
4. Research the market and search landscape
5. Write the content plan → **stop and get approval**
6. Write each post (brief → draft → claims check → SEO pass)
7. Create images from the source, export, and place them
8. QA, deliver into the repo's blog format, and log progress

Keep the user informed with one short line per phase ("Reading the codebase…", "Brand extracted: 2 colors, Inter + Fraunces…"). Put long material in files, not chat.

---

## 1. Locate the source and saved state

The source can arrive as a local repo path (Claude Code), an uploaded zip or folder, or a connected GitHub/GitLab repo. Get it onto disk if possible (unzip uploads into a working directory). If you have no source at all, ask for it once; if the user only gives a URL, fetch the live site and proceed with lower confidence, saying so.

Check for a saved state folder at `<repo>/.blog-writer/` (or `./blog-writer-state/` when the repo is read-only). If it exists, read `state.md` first and resume where it left off instead of starting over.

State folder layout (create it as you go):

```
.blog-writer/
├── state.md            # phase, approvals, what's next (update after every phase)
├── product-brief.md    # facts about the product, each with file evidence
├── brand.json          # tokens from extract_brand.py, edited by you
├── brand-notes.md      # voice and visual rules in plain words
├── content-plan.md     # the plan the user approves
├── posts/<slug>/       # brief.md, post.md, images/, meta.json
└── published.md        # log: date, slug, URL, keyword
```

## 2. Build the product brief from the code

Run the inventory script first; it saves you from reading files blindly:

```bash
python scripts/scan_repo.py <repo-path> > .blog-writer/inventory.json
```

It reports the framework, marketing pages and routes, i18n/locale files, pricing-like files, docs, existing blog posts and their frontmatter fields, public images and logos, sitemap/robots/meta tags. Then read the files it points to. `references/source-analysis.md` lists where facts usually live per framework (Next.js, Nuxt, Astro, Remix, SvelteKit, Rails, Laravel, Django, plain HTML) and how to read them.

Write `product-brief.md` with:

- **What it is** in one sentence, in the product's own words where possible
- **Who it is for** (inferred from copy, onboarding, pricing tiers, integrations)
- **Verified features** — each with evidence, e.g. `Lead alerts by email or Telegram — src/i18n/en.json:212, app/api/notify/telegram.ts`
- **Pricing and plans** as the code states them
- **Languages/markets** (locales present)
- **Differentiators** you can support from the code
- **Unverifiable or ambiguous claims** — things marketing copy says that the code does not clearly implement (feature flags off, TODOs, stubs, "coming soon"). Content must not promise these. List them so the user can confirm.

Evidence matters because AI-written content that overstates a product is the fastest way to lose reader trust and to publish something false; Google also asks that AI-assisted content be fact-checked before publishing.

## 3. Extract the brand

```bash
python scripts/extract_brand.py <repo-path> > .blog-writer/brand.json
```

The script collects color tokens (CSS custom properties, Tailwind/theme config, design-token JSON), font families (Google Fonts links, `@font-face`, `next/font`, Tailwind `fontFamily`), logo/icon candidates, and border radius. Review its output: pick the real primary, accent, ink, surface and muted colors (the most-used values in components, not every hex in the repo) and record your choices in `brand.json` under `"chosen"`.

Then write `brand-notes.md`:

- **Visual:** palette roles, fonts (with web-safe fallbacks), corner radius, icon style, logo files to use and where
- **Voice:** read 20–40 strings of real UI and marketing copy. Note person (we/you), formality, sentence length, how features are named, words they use and avoid. Posts should sound like the product, not like a generic blog.

If the repo has no styling (API-only, backend), ask for brand colors/logo once; otherwise choose a restrained palette and say so.

## 4. Research the market and search landscape

Read `references/seo-2026.md` before planning — it summarizes current Google guidance (as of late 2026) and is the basis for the rules below. If that file is more than ~6 months old relative to today's date, run a quick search for new Google core updates or Search Central guidance changes and note anything that changes the rules.

With web search:

1. Identify 3–6 real competitors and what they publish.
2. For each candidate topic, search it and read the top results: who ranks (big brands vs small sites), what format wins (guide, comparison, tool, list), and what is missing.
3. If the user has a keyword tool (Ahrefs, Semrush, GSC data), use real volumes; otherwise label priorities as estimates and tell the user to validate them.

What to look for — the core of current SEO:

- **Non-commodity angles.** Google's guidance favors unique, first-hand, expert content over restated common knowledge. For every topic, ask: *what can only this product's team say?* Sources of that: the product's own workflow, real setup steps, internal data patterns, decisions in the code (why it's built this way), honest trade-offs vs alternatives.
- **Intent fit.** Bottom-of-funnel pages (comparisons, alternatives, use-case and integration pages) bring signups; problem-aware guides build reach. A new site should start with high-intent, winnable topics.
- **One strong page per topic.** Do not create near-duplicate pages for keyword variations or AI "fan-out" queries; that is scaled content abuse under Google's spam policies and also simply doesn't work.

## 5. Write the content plan — then stop for approval

Use `references/content-plan-template.md`. Keep it decisive and short enough to read in five minutes:

- Positioning in one sentence and the primary audience
- Topic clusters (2–4), each tied to a product capability from the brief
- First 8–12 pieces, prioritized, each with: working title, type (post / landing page / comparison), target query (validate), search intent, the non-commodity angle, proof assets from the product, internal links, images planned
- Cadence the team can sustain (1–2 pieces/week is typical; quality beats volume)
- Claims to confirm (from the brief)
- How success is measured (organic signups and qualified leads first; impressions as a leading signal)

Deliver the plan as the most useful format available (a doc/artifact if the environment supports it, otherwise `content-plan.md`), then **ask for approval and stop**. Accept edits, update the plan, and record approval in `state.md` with the date.

## 6. Write each post

After approval, work through the plan in order. For each piece:

1. **Brief** (`posts/<slug>/brief.md`, use `references/post-template.md`): query, intent, reader, angle, outline, proof assets, images, internal links, CTA.
2. **Research** the current top results for the query; note what they miss. Never copy their structure or wording.
3. **Draft** following `references/writing-style.md`:
   - Answer the searcher's question in the first 2–3 sentences
   - Clear H2/H3 structure written for people (no keyword-stuffed headings, no artificial "chunking")
   - Specifics over adjectives: real UI labels, real steps, real constraints from the code
   - Honest comparisons, including where alternatives are stronger
   - One relevant call to action matching the product's real next step (signup, trial, demo)
4. **Claims check:** every feature statement must trace to the product brief. Replace anything unverified with safer wording or remove it. No invented statistics, customers, quotes or results; if a number would help, either cite a real source you opened or leave it out.
5. **SEO pass** (details in `references/seo-2026.md`): unique title (~50–60 chars, keyword near the start), meta description that states the benefit, one H1, descriptive slug, internal links to 1–3 related pages, alt text on every image, structured data that matches visible content (BlogPosting/Article + BreadcrumbList; FAQPage only describes visible Q&A — Google retired FAQ rich results in May 2026, so don't promise a SERP dropdown).
6. Run the linter and fix what it flags:

```bash
python scripts/check_post.py .blog-writer/posts/<slug>/post.md
```

## 7. Create images from the source

Read `references/image-guide.md` before making images. Choose per image, in this order of preference:

1. **Real screenshots** — if the app can be run locally (dev server, Playwright/browser available), capture the actual screens with realistic sample data.
2. **Rebuilt UI mockups in SVG** — when running the app isn't possible, redraw the relevant screen from the source: real component structure, real labels and copy, real colors, fonts and radius from `brand.json`. Use sample data, never real customer data. Label these internally as illustrative.
3. **Diagrams and figures in SVG** — flows, comparisons, before/after, step sequences that explain the post's point.
4. **Featured/OG image** — start from `assets/og-template.svg`, apply brand tokens and the post's title.

Export every SVG to WebP (and PNG if the blog needs it):

```bash
python scripts/render_images.py .blog-writer/posts/<slug>/images --webp --png --max-kb 200
```

Render, look at the result, fix overflow or clipped text, and re-render. Give each image a descriptive file name and alt text that describes what the image shows. Do not draw third-party logos, mascots or copyrighted characters; integrations can be named in text.

## 8. QA, deliver, log

Before handing over, run the pre-publish checklist in `references/post-template.md`. Then deliver in the repo's native format:

- If the repo has a blog (MD/MDX/content collection/CMS seed files), match an existing post exactly: folder, filename/slug pattern, frontmatter keys and types, image path conventions, component usage. `scan_repo.py` reports the frontmatter keys it found.
- If there is no blog yet, deliver `post.md` plus images and a JSON-LD snippet, and suggest where a blog should live (a subfolder on the main domain, e.g. `/blog`).
- Never push to a remote or merge on your own; write files locally or open a branch/PR only if the user asked.

Update `state.md` (what's done, what's next) and append to `published.md` once the user publishes. When the user returns, offer the next post in the plan, and after 8–12 weeks suggest a review: expand what earns impressions and signups, rewrite pages with impressions but few clicks, drop topics with no demand.

---

## Reference files

| File | Read when |
| --- | --- |
| `references/seo-2026.md` | Before planning and during every SEO pass |
| `references/source-analysis.md` | Building the product brief and brand from a codebase |
| `references/content-plan-template.md` | Writing the content plan |
| `references/post-template.md` | Writing each brief and post; pre-publish checklist |
| `references/writing-style.md` | Drafting and editing |
| `references/image-guide.md` | Before creating any image |

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/scan_repo.py` | Inventory a repo: framework, routes, copy, pricing, docs, blog format, assets |
| `scripts/extract_brand.py` | Pull color, font, radius and logo candidates into JSON |
| `scripts/render_images.py` | SVG → WebP/PNG with size reporting (needs `cairosvg`, `Pillow`) |
| `scripts/check_post.py` | Lint a markdown post for SEO basics and leftover placeholders |

Install dependencies if missing: `pip install cairosvg Pillow` (add `--break-system-packages` on managed Linux environments).
