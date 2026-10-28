# Creating images from the source

Every image should help the reader understand or trust the post: show the real product, explain a flow, or make the post recognizable when shared. Decorative stock-style art adds little.

## Choose the image type

| Need | Best option | Notes |
| --- | --- | --- |
| Show how the product does something | Real screenshot | Run the app locally with sample data; crop to the relevant area; 2x resolution |
| Same, but the app can't run | Rebuilt UI mockup (SVG) | Redraw from components and copy in the repo |
| Explain a process, decision or comparison | Diagram (SVG) | Few words, clear direction, one highlighted element |
| Social share / blog card | Featured image (SVG → 1200 × 630) | From `assets/og-template.svg` with brand tokens |
| Quantities | Simple chart (SVG) | Only with real data; label units |

## Real screenshots

If a dev server and a headless browser (e.g. Playwright) are available: seed or use demo data, set viewport (1440 × 900 desktop, 390 × 844 mobile), hide personal data, capture at device scale factor 2, then crop. Never screenshot real customer accounts.

## Rebuilt UI mockups (SVG)

Build from the source so the mockup is faithful:

1. Open the component(s) for the screen (e.g. `components/pricing/PlanCard.tsx`, `app/(app)/customers/page.tsx`).
2. Reuse real structure: layout order, labels, button text, empty states, icons (same icon library style).
3. Apply `brand.json` tokens: colors by role, font family with fallbacks, border radius, border/shadow style.
4. Fill with realistic sample data that matches the product's domain; use obviously fictional names/companies.
5. Frame it simply (browser bar, app window, or phone) on a quiet background using the brand's surface/muted colors.

Rules:

- Sample data only; no real customer names, emails or metrics.
- Don't invent features the product doesn't have; mockups are claims too.
- Keep text real-size (13–16 px equivalents at 1200 px width) so it's readable.
- SVG text doesn't wrap — break lines yourself and leave generous padding, because fallback fonts on other machines are often wider.
- Avoid SVG filters for shadows (renderers differ); use an offset semi-transparent rect.
- Don't draw third-party logos, trademarks or characters. Mention integrations in text instead.

## Diagrams

- Title states the takeaway ("Every question ends in a next step or a gap you can fill"), not the topic.
- 4–8 boxes; one accent color for the key element; arrows in the gaps, not through boxes.
- Use brand ink for text, muted borders, primary color for the highlight.

## Featured image

Edit a copy of `assets/og-template.svg`:

- Replace `{{TITLE_LINE_1}}`, `{{TITLE_LINE_2}}` (break the title into ≤ 2 lines of about 22 characters; render and check for overlap), `{{EYEBROW}}` (blog category), and `{{BRAND_NAME}}`
- Replace color placeholders with `brand.json` values; swap the font family
- Optionally place the product's SVG logo (unaltered) and a small UI fragment on the right
- Keep important content inside the central safe area; platforms crop edges

## Export and checks

```bash
python scripts/render_images.py <images-dir> --webp --png --max-kb 200
```

- Look at every rendered PNG/WebP: clipped text, overflow, overlaps, low contrast (aim for WCAG AA 4.5:1 for body text).
- File names: lowercase, hyphenated, descriptive (`<topic>-<what-it-shows>.webp`).
- Alt text: one sentence describing what the image shows and why it matters in context.
- If any image is AI-generated (not SVG drawn by you), add IPTC `DigitalSourceType` = `TrainedAlgorithmicMedia` metadata where the publishing pipeline allows.
- Tell the user which images are illustrative mockups so they can replace them with real screenshots if they prefer.
