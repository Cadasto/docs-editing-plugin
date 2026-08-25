---
name: marketing-copy
description: Writing new marketing and positioning copy. This skill should be used when the user asks to "write the landing page", "write feature/product copy", "position this", "write the announcement or release post", "write the tagline / hero section", or "make the pitch clearer" — it writes benefit-led copy for technical audiences with every claim grounded in a verifiable mechanism. Not for documentation (technical-writing), editing existing prose (copy-editing), or metadata and discoverability (seo-audit).
argument-hint: "<what to position> [page kind: hero | feature | announcement | one-pager]"
allowed-tools: Read, Write, Edit, Glob, Grep, WebFetch
---

# marketing-copy — positioning and page copy

Write copy for **$ARGUMENTS**.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

## The constraint that defines this skill

Read `references/claims-and-evidence.md` **before drafting**, not after. Conversion-optimised copy fails in one predictable way: asked to be more persuasive, it invents the persuasion — statistics, customer counts, testimonials, awards, urgency. For this plugin those are not stylistic choices; they are prohibited outputs.

The audience makes this practical rather than merely ethical. Developers, engineers, and clinicians read an unsourced number as evidence of unseriousness, so **the growth-copy move that raises conversion on a consumer page lowers it here** (`claims-and-evidence.md` §6). The persuasive substitute is always the same: **replace the claimed outcome with the observable mechanism.**

> ❌ "Cut documentation review time by 40%."
> ✅ "Flags unsourced statistics, doc-kind bleed, and terminology drift — the classes a spell-checker cannot see."

Specific, checkable, and more convincing to this reader than any number they will assume was fabricated.

## 1 · Get the substance before the words

Copy cannot be written from a request. Establish, from the repo and the code — not from imagination:

1. **What it actually does.** Read the manifest, the components, the tests. Run it if you can.
2. **Who it is for**, stated as a role plus a situation ("clinical modellers reviewing archetypes before publication"), not a demographic.
3. **The problem, in the reader's words** — what they currently do instead, and what that costs them.
4. **The mechanism** — *how* it solves that. This is the copy's load-bearing element.
5. **The honest limits** — prerequisites, what it does not do, what maturity each part is at.
6. **The one true differentiator.** If you cannot name it from evidence, say so; do not manufacture one.

Anything the user supplies (real metrics, real quotes, real customers) is usable **as given, attributed**. Never extend, round, or embellish it.

## 2 · Structures that work

**Hero** — four elements, in this order:
1. **What it is**, plainly, in one line. The noun and the audience. Not a metaphor, not a question.
2. **The mechanism**, in one or two lines — the specific thing it does that the reader cannot easily do now.
3. **A concrete proof surface** — a command, a code block, a named failure it catches, a screenshot of real output. This does the work a testimonial would do on a consumer page.
4. **One primary action**, honestly labelled ("Install", "Read the docs"). Not "Get started free" if there is nothing to pay for.

**Feature section** — one per real capability: the capability named in the reader's vocabulary, the mechanism, and the observable outcome. Cut any feature you cannot describe mechanically.

**Announcement / release post** — what changed, who it affects, what they must do, then the detail. Link the changelog rather than reproducing it (`references/doc-types.md` §2 — one home per fact).

## 3 · Write

Apply `references/style-guide.md`; for marketing copy specifically:

- **Second person for benefit, third for mechanism.** "You get ranked findings. The auditor reads the whole tree."
- **Front-load.** The most specific word first, in every heading and every line. Readers scan the left edge.
- **Verbs over adjectives.** "Flags", "reads", "refuses" — not "powerful", "robust", "seamless", "cutting-edge", "industry-leading".
- **Concrete nouns over categories.** "`go vet` misses goroutine leaks" beats "improves code quality".
- **Say the limit out loud.** A prerequisites line and a plain `experimental` label buy more trust than a page of superlatives.
- **Shorter than feels finished.** Cut every sentence that does not add a fact. Most technical landing copy is twice as long as it needs to be.
- **No fake voice.** No invented "we've all been there" anecdotes, no imagined user, no rhetorical questions standing in for a claim.

## 4 · Self-check before handing over

Run this list explicitly and report the result:

- [ ] Every number, quote, name, and comparative has a source I can produce in one step.
- [ ] Nothing invented from `claims-and-evidence.md` §2 — no stats, social proof, endorsement, urgency, or superiority claim.
- [ ] No hedged claim standing in for a cut one ("up to", "designed to", "teams report").
- [ ] Every capability described is `shipped`; anything else is labelled.
- [ ] Every inventory and count verified against the tree.
- [ ] Prerequisites and limits stated on the page, not buried in docs.
- [ ] The primary action is honestly labelled.
- [ ] `vale` run on the result.

State plainly what a page would need in order to make a stronger claim ("a published benchmark", "permission to quote a named user") rather than making the claim without it.

## 5 · Hand off

Documentation → `technical-writing` · tightening existing copy → `copy-editing` · titles, metadata, internal links → `seo-audit` · citability and `llms.txt` → `ai-seo` · independent review → the `prose-reviewer` agent.
