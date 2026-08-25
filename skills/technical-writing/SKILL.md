---
name: technical-writing
description: Authoring new technical documentation. This skill should be used when the user asks to "write documentation", "write a README", "document this feature/API", "write a how-to / tutorial / reference page", "structure the docs", "write release notes / a changelog entry", or "what should this document contain?" — it picks the document kind, drafts to the house style, and grounds every claim. Not for editing existing prose (copy-editing), landing/marketing pages (marketing-copy), or discoverability (seo-audit).
argument-hint: "<what to document> [target file or doc kind]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# technical-writing — author new documentation

Draft documentation for **$ARGUMENTS**.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

## 1 · Orient before drafting

Never draft from the request alone.

1. **Read the repo's instructions** — `AGENTS.md` / `CLAUDE.md` / `CONTRIBUTING.md`: the ground-truth source for domain facts, public-safety constraints, "do not duplicate" rules, spelling and voice. **Read only** — these are not files this skill edits.
2. **Read the thing you are documenting.** The code, the config, the manifest, the actual command output. A filename is not evidence of behaviour; a function name is not evidence of what it returns. Run the command if you can.
3. **Read two neighbouring pages.** Match their structure, heading depth, and terminology. Consistency with siblings beats local improvement.
4. **Find the canonical home.** If this content already exists somewhere, extend or link it — do not create a second copy that will drift.

## 2 · Pick exactly one document kind

Decide before the first sentence, using `references/doc-types.md`:

| Reader is… | Kind | Contract |
|---|---|---|
| New, learning by doing | **Tutorial** | One path, no branches, pinned versions, works verbatim end to end |
| Competent, has a goal | **How-to** | One real problem, may branch, links fundamentals instead of teaching them |
| Looking a fact up | **Reference** | Exhaustive, indicative, structure mirrors the code, no narrative |
| Trying to understand | **Explanation** | Context, alternatives, trade-offs — the only kind allowed to argue |

If the answer is "both", that is two documents. Say so and propose the split rather than writing a hybrid.

`README.md`, `CHANGELOG.md`, and migration notes have fixed contracts — use the shapes in `references/doc-types.md` §2.

**Do not author or rewrite agent-instruction files** — `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, or skill/agent definitions. They are written for a model, not a reader, and the rules here invert for them (`references/doc-types.md` §3). Asked to write one, say it is out of scope and point elsewhere.

## 3 · Draft

Apply `references/style-guide.md` (voice, person, sentence economy, headings, Markdown mechanics). The rules that matter most while drafting:

- **Answer first.** Each section opens with the conclusion, the command, or the definition. Background never precedes it.
- **Sections stand alone.** A reader arriving at an `h2` must be able to act without reading upward.
- **Show the command, not a description of the command.** Language-tagged fences, no `$` prompt, copy-pasteable.
- **Name the prerequisites and the limits early.** What it does not do buys more trust than any adjective.
- **Cross-reference; never duplicate.** One home per fact.
- **State maturity plainly** — `shipped` / `experimental` / `planned` / `deprecated`. Never describe planned behaviour in the present indicative.

## 4 · Ground every claim

`references/claims-and-evidence.md` is the hard rule. While drafting:

- Every factual sentence must be traceable in one step — to a file you read, a command you ran, or a cited source.
- **Never originate** numbers, benchmarks, testimonials, customer names, awards, urgency, or superlatives. If the user has not supplied them, the doc works without them.
- Domain facts come from the repo's named ground-truth source. Look them up.
- **Verify every inventory** — counts, component tables, feature lists — against the tree before writing or editing it.

## 5 · Verify before claiming done

```bash
vale "<file>"                  # prose style (see references/vale.ini)
```

Then check by hand:

- **Every command in the doc actually runs**, as written, in order. Run them.
- **Every link resolves** — including anchors and relative paths from the file's own location.
- **A tutorial works from a clean state.** If you cannot verify that, say so explicitly instead of implying it.
- **The doc is registered** where the site expects it — nav, index, sitemap, `llms.txt`. An unlinked page is an invisible page.

If the repo has a docs build (`make check`, `mkdocs build --strict`, a site linter), run it. Report what you ran and what it said; do not claim a doc is correct because it looks correct.

## 6 · Hand off

- Existing prose needs tightening → `copy-editing`
- The page is a landing or positioning page → `marketing-copy`
- Titles, metadata, internal links, sitemap → `seo-audit`
- `llms.txt`, structured data, Markdown twins → `ai-seo`
- Independent review of the result → the `prose-reviewer` agent
