---
name: docs-editing
description: Documentation and content router — technical writing, copy editing, marketing copy, SEO, and AI citability. This skill should be used when a prose task spans several of those areas, is unspecified, or the question is which standard applies — it routes to the focused skill that owns it (technical-writing, copy-editing, marketing-copy, seo-audit, ai-seo). Also the entry point for "improve these docs", "review this page", or "what should this document be?". For one already-identified task load that skill directly. Not for source-code review or domain facts.
allowed-tools: Read, Grep, Glob, Bash
---

# docs-editing — documentation and content router

Route the prose task to the standard that owns it. This skill is a router, not a style guide.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

Three principles drive every route:

- **Evidence before persuasion.** A claim that cannot be traced to a source does not ship. This is the plugin's hard rule and it outranks every stylistic preference — `references/claims-and-evidence.md`.
- **Decide the document kind first.** Most bad documentation is two kinds of document in one file. Pick the kind, then write only that kind — `references/doc-types.md`.
- **Deterministic beats prose.** Whatever `vale` enforces, run the tool rather than reasoning it out by hand. Scaffold it with `/docs-lint-setup`. Markdown *structure* has no shipped enforcer — apply `references/style-guide.md` §6 by judgment.

## Routing table

| The task | Run now (deterministic) | Skill that owns it |
|---|---|---|
| Write new docs — README, guide, reference, tutorial | `vale` on the result | `technical-writing` |
| Tighten, review, or restructure existing prose | `vale .` on the file | `copy-editing` |
| Landing page, feature page, positioning, announcement | `vale .` | `marketing-copy` |
| Titles, metadata, headings, links, sitemap, crawlability | fetch the **published** page | `seo-audit` |
| `llms.txt`, structured data, Markdown twins, citability | fetch the published page | `ai-seo` |
| Set up prose linting in a repo | — | `/docs-lint-setup` |
| Which document kind is this? | — | this skill → `references/doc-types.md` |
| May I write this claim? | — | this skill → `references/claims-and-evidence.md` |
| Sentence-level style, voice, person, headings | `vale .` | `references/style-guide.md` |

## Read the repo's own rules first

A consuming repository's instructions outrank this plugin. Before writing or editing, check for and follow:

1. **`AGENTS.md` / `CLAUDE.md`** — especially a named **ground-truth source** for domain facts, and any public-safety or "do not duplicate" constraint. Read these; they are never edit targets (see Scope).
2. **A repo style guide or `CONTRIBUTING.md`** — if it sets voice, spelling, or terminology, it wins over `references/style-guide.md`.
3. **`.vale.ini`, or any linter config the repo ships** — its own enforced rules. Run them; do not argue with them.
4. **Existing neighbouring pages** — match their structure and terminology. Consistency beats improvement in isolation.

## Refusals worth making

Route these to a conversation rather than to prose:

- **A requested claim with no source.** Offer the mechanism instead (`claims-and-evidence.md` §3), and say plainly that the number, testimonial, or superlative would have to be invented.
- **A rewrite that would merge two document kinds.** Propose the split.
- **A "make it more compelling" request on technical copy.** The usual growth-copy moves lower trust with this audience — `claims-and-evidence.md` §6. Offer specificity instead.
- **Duplicating prose that already has a canonical home.** Link it; a second copy will drift.

## Scope

Owns **prose written for people**: documentation, guides, references, page and marketing copy, changelogs, READMEs, release notes, site metadata, `llms.txt`.

Does **not** own:

- **Agent-instruction files** — `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, skill and agent definitions. **Read** them for the repo's conventions; never author or rewrite them. They address a model, not a reader, and several rules here invert for that genre (`references/doc-types.md` §3). Dedicated tooling owns them — route the request there.
- **Source-code review** — use a code-review skill or agent.
- **Specifications, requirements, ADRs, and traceability** — the `sdd` plugin's layer.
- **Domain facts** — those come from the repo's named ground-truth source, never from memory.

## Agents

For a context-isolated pass, dispatch rather than inlining:

- **`prose-reviewer`** — report-only review of a document or page set: claim violations, doc-kind bleed, terminology drift, structure, style. Returns ranked findings.
- **`seo-auditor`** — report-only discoverability and citability audit over a docs tree or published site.
