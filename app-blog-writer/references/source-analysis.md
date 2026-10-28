# Reading a product from its source code

Goal: a product brief where every claim has file evidence, plus brand tokens and voice notes. Start with `scripts/scan_repo.py`, then open the files it lists. Read for meaning, not volume — 20–40 well-chosen files usually tell the whole story.

## Where facts usually live

| What you need | Where to look |
| --- | --- |
| What the product is, positioning | README, homepage component, `<title>`/meta description, `metadata` exports, Open Graph tags, `package.json` description |
| Features | Marketing pages, feature/solution pages, i18n strings, route names, API route folders, feature flags, onboarding flows, docs folder, CHANGELOG |
| Who it's for | Copy on homepage and solution pages, pricing tier names and limits, integrations, sample/demo data, onboarding questions |
| Pricing | `pricing` pages/components, plan constants (`plans.ts`, `pricing.json`), billing integration config (Stripe price IDs with names), i18n strings |
| Languages/markets | Locale folders (`locales/`, `messages/`, `i18n/`, `lang/`), hreflang, currency formatting |
| Integrations | Env var names (`*_API_KEY`), SDK dependencies, webhook handlers, OAuth providers |
| Limits and honesty checks | Feature flags, `TODO`/`FIXME`, "coming soon", stubbed handlers, disabled routes, plan gates |
| Existing content | `content/`, `posts/`, `blog/`, `src/content/` (Astro collections), MDX files, CMS seed data |
| SEO setup | `robots.txt`, sitemap generators, `next-sitemap`, canonical/hreflang logic, structured data components |

## Framework hints

- **Next.js (app router):** `app/**/page.tsx`, `app/**/layout.tsx` (`export const metadata`), `app/sitemap.ts`, `app/robots.ts`, `next.config.*`, `messages/*.json` (next-intl). Pages router: `pages/**`, `next-seo` config.
- **Nuxt:** `pages/**`, `nuxt.config.*` (`app.head`), `content/` (Nuxt Content), `locales/`.
- **Astro:** `src/pages/**`, `src/content/config.ts` (collection schema = blog frontmatter), `astro.config.*`.
- **Remix / React Router:** `app/routes/**` with `meta` exports.
- **SvelteKit:** `src/routes/**/+page.svelte`, `+page.ts`, `svelte.config.js`.
- **Gatsby/Hugo/Jekyll/11ty:** `content/`, `_posts/`, front matter conventions in existing posts; site config for permalinks.
- **Rails:** `config/routes.rb`, `app/views/**`, `config/locales/*.yml`.
- **Laravel:** `routes/web.php`, `resources/views/**`, `lang/**`.
- **Django:** `urls.py`, `templates/**`, `locale/**`.
- **Mobile apps:** store listing text, `Info.plist`/`strings.xml`, onboarding screens; the "website" may be a separate repo — ask.

## Writing the product brief

Use this structure:

```markdown
# Product brief — <Product>

## What it is
<one sentence, ideally the product's own words> (src/app/page.tsx:14)

## Who it's for
- Primary: ... (evidence)
- Secondary: ...

## Verified features
| Feature | Plain-language description | Evidence |
| --- | --- | --- |

## Pricing
| Plan | Price | Key limits | Evidence |

## Languages and markets

## Differentiators (supported by the code)

## Claims to confirm before publishing
- "<copy claim>" — copy says X, but <file> shows Y / no implementation found
```

## Brand from code

`scripts/extract_brand.py` gives candidates; you choose. Tips:

- **Colors:** prefer semantic tokens (`--primary`, `--brand`, `colors.brand.500`, `--accent`). If there are many hex values, the brand color is usually the one used on primary buttons and links. Note dark-mode variants.
- **Type:** the `font-family` on `body`/headings, Google Fonts URLs, `next/font` imports. Images rendered server-side need installed fonts; list fallbacks (system sans/serif) in `brand-notes.md`.
- **Logo:** `public/logo*.svg`, `brand/`, `assets/`; favicon/app icons. Use the SVG directly in featured images when appropriate; never alter its proportions or colors beyond documented variants.
- **Shape language:** border radius, shadows, borders vs fills, icon library (lucide, heroicons, material) — mockups should reuse these.
- **Voice:** collect strings from i18n files, hero copy, empty states, error messages, button labels. Note: person (we/you), formality, sentence length, capitalization style (sentence case vs title case), terms the product uses for its own features.

## When source is partial

- **Backend-only repo:** product facts come from API routes and docs; ask for the marketing site or brand assets.
- **Monorepo:** find the marketing/web app package first (`apps/web`, `apps/marketing`, `packages/ui` for tokens).
- **Live URL only:** fetch key pages (home, pricing, features, docs) and treat claims as lower-confidence; say so in the brief.
