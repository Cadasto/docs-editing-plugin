---
name: copy-editing
description: Use when asked to improve prose that already exists — "edit this", "tighten this", "review this page", "proofread", "cut this down", "fix the tone", "why does this read badly?". Line-edits to house style and flags unsupported claims. Editing, not drafting (technical-writing).
argument-hint: "<file, page, or pasted prose> [--report-only]"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# copy-editing — tighten existing prose

Edit the prose in **$ARGUMENTS**.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

## 0 · Establish the contract first

Ask — or infer from the request — **which edit this is**, because the three differ enormously in licence:

| Edit | Licence | Use when |
|---|---|---|
| **Proofread** | Fix errors only: typos, grammar, broken links, inconsistent terms. Voice untouched. | Late-stage, someone else's voice |
| **Line edit** | Rewrite sentences for clarity and economy. Meaning and structure preserved. | The default |
| **Structural edit** | Reorder, merge, split, cut sections. | The document does not work, not just the sentences |

Default to a **line edit**. Never silently escalate — a structural edit on a proofread request destroys work. If the document needs restructuring, say so and ask.

With `--report-only`, produce findings and do not touch the file.

## 1 · Run the tools first

```bash
vale "<file>"                  # prose style (references/vale.ini)
```

Fix what the tool flags before spending judgment on what it cannot see. If the repo ships its own `.vale.ini` — or any other linter config — that wins: run it and do not argue with it. If Vale is not installed, say so and proceed by hand rather than silently skipping.

## 2 · The passes, in this order

Order matters: cutting a paragraph makes its sentences moot, so work large to small.

**Pass 1 — claims.** `references/claims-and-evidence.md`. This is the highest-value pass and the one a human reviewer most often misses.
- Flag every unsourced number, benchmark, testimonial, customer name, award, superlative, and urgency device. **Do not soften them — hedging is not a fix.** Replace the invented outcome with the observable mechanism, or cut it and report it.
- Check maturity language: is anything `planned` described as shipped?
- **Verify every inventory** — counts, component tables, feature lists — against the tree. They rot fastest.
- Domain facts: confirm against the repo's named ground-truth source, never from memory.

**Pass 2 — kind and structure.** `references/doc-types.md`. Is this one document kind or two? Does each section answer first? Can a reader arriving at an `h2` act without reading upward? Report a needed split; do not perform one under a line-edit contract.

**Pass 3 — paragraph.** One idea per paragraph. Delete the throat-clearing opener. Is the topic sentence actually first? Are two adjacent paragraphs making the same point?

**Pass 4 — sentence.** `references/style-guide.md` §2: one idea per sentence, active voice, present tense, cut nominalisations and filler intensifiers, prefer the short word. Target ≤ 25 words as a smell test, not a rule.

**Pass 5 — word.** Terminology fixed and consistent (no synonym rotation for variety), acronyms expanded once, spelling per repo, **never** "simply"/"just"/"obviously", no ableist metaphors, `they/them` for unstated gender. `references/style-guide.md` §§3–4.

**Pass 6 — mechanics.** Headings sentence case and correctly nested, one `h1`, fences tagged, links on nouns, no bare URLs in body prose, no trailing whitespace.

## 3 · Preserve what you must not touch

- **Code, commands, identifiers, CLI flags, and cited API names** — never "correct" their spelling, casing, or wording. `color` stays `color`.
- **Quotations and cited text** — verbatim.
- **The author's voice**, under a proofread or line-edit contract. Tighten how it is said; do not replace who is saying it.
- **Legal, licence, and safety text** — flag, never edit.
- **Meaning.** If a sentence is unclear because the underlying fact is unclear, ask. Do not guess and write something plausible — a confident rewrite of a fact you invented is worse than the muddle you replaced.

## 4 · Report

Always report, whether or not you edited. Lead with the highest-impact findings:

1. **Claim violations** — quote the text, name the class, give the repair. These first, always.
2. **Structural findings** — kind bleed, a needed split, sections that do not stand alone.
3. **What changed** — grouped by pass, with counts. A diff is not a report; say what class of problem was fixed.
4. **Left alone deliberately** — and why (out of contract, ambiguous fact, repo style wins, needs the author).
5. **Open questions for the author** — facts you could not verify.

Re-run `vale` after editing and report the result. Do not claim the prose is clean without having run it. Markdown mechanics (pass 6) have no shipped linter — check them by eye.

## 5 · Hand off

New documentation to draft → `technical-writing` · landing/positioning copy → `marketing-copy` · titles, metadata, links → `seo-audit` · `llms.txt`, structured data → `ai-seo` · an independent second pass → the `prose-reviewer` agent.
