# Writing style

The post should read as if a knowledgeable person on the product team wrote it for a busy reader: specific, honest, and in the product's own voice (see `brand-notes.md`).

## Principles

- **Lead with the answer.** The first 2–3 sentences resolve the searcher's question; the rest explains, proves and expands.
- **Specific beats general.** Name real screens, buttons, settings and steps from the source. "Open **Work Areas** in the left sidebar and select **Add Work Area**" beats "navigate to the relevant section".
- **Show, don't claim.** Replace "powerful", "seamless", "cutting-edge" with what actually happens and for whom.
- **Honest trade-offs.** Say when the product isn't the right fit and where alternatives are stronger. It builds trust and matches how buyers compare.
- **Short paragraphs** (1–3 sentences), sentences mostly under 25 words, plain words, active voice.
- **Headings people would scan for** — questions or steps, not clever puns.
- **Lists only for parallel items or real steps.** Prose for reasoning.
- **Match the product voice:** same person (we/you), formality, capitalization and feature names as the UI.
- **Write in the target language natively.** For a second-language version, rewrite for that market (examples, currency, search terms) instead of translating literally.

## Non-commodity techniques

- Walk through the product's real workflow for the reader's task, with screens
- Explain *why* something works the way it does, using decisions visible in the code
- Use the product's own anonymized patterns or the team's support experience (only with permission and real numbers)
- Compare options with a clear, fair verdict per situation
- Give templates, scripts, checklists the reader can use immediately

## Claim discipline

- Every statement about the product must trace to the product brief's evidence.
- Unverified capability → remove it or use the safer wording recorded in the brief.
- No fabricated numbers. If you cite a statistic, it comes from a source you opened, linked in the post.
- No fake testimonials, customer names, logos, awards or ratings.
- "Never wrong", "guaranteed", "100%" claims about AI accuracy or results are not allowed.
- Competitor facts: check their current site, date the comparison, link it.

## Phrases to cut

These read as filler or as machine-written; replace them with something concrete or delete:

"In today's fast-paced world", "In the ever-evolving landscape", "unlock the power of", "game-changer", "revolutionize", "seamlessly", "leverage" (as a verb for "use"), "delve into", "it's important to note that", "whether you're a … or a …", "look no further", "take your X to the next level", "a testament to", "navigate the complexities", "in conclusion".

`check_post.py` flags these automatically.

## Editing pass

1. Read the opening alone — does it answer the query?
2. Delete any paragraph a reader could find in every competitor post.
3. Check each claim against the brief.
4. Read headings alone — do they tell the story?
5. Cut 10–20% of words.
