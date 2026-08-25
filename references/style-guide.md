# House Style

The canonical style rules for **human-facing** prose this plugin writes or edits. Skills cite this file; they do not restate it. Where a consuming repository ships its own style guide, **that repo's guide wins** — read it first and treat this as the fallback.

Agent-instruction files (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, rule and skill definitions) are **out of scope** — they are written for a model, not a person, and several rules here invert for them. See [doc-types.md §3](doc-types.md).

Rules that a tool can enforce name that tool, so advice and tooling stay in step. **Vale** owns the prose rules (`references/vale.ini`; scaffold with `/docs-lint-setup`). The Markdown-mechanics rules in §6 have no shipped enforcer — apply them by judgment.

## 1. Voice and grammatical person

| Context | Person | Example |
|---|---|---|
| User-facing docs (tutorials, how-tos) | **Second person, imperative** | "Run `make check`." |
| Reference material | **Third person, indicative** | "`sync` fetches the pinned docs." |
| Marketing copy | **Second person for benefit, third for mechanism** | "You get a ranked diff. The auditor reads the tree." |

Never use first-person plural ("we recommend") in reference docs — it hides who is speaking. In marketing copy it is acceptable when the speaker is genuinely the organisation.

**Active voice by default.** Passive is correct when the actor is genuinely unknown or irrelevant ("the file is created at build time"), not as a way to avoid naming a responsible party.

**Present tense.** Describe what the system does, not what it will do. Reserve future tense for genuinely future events.

## 2. Sentence economy

- **One idea per sentence.** Two independent clauses joined by "and" usually want to be two sentences.
- **Cut the throat-clearing.** "It is important to note that", "In order to", "As you can see", "Simply", "Just", "Basically" — delete. `Vale` flags these.
- **Prefer the short word** where meaning is unchanged: use/utilise, help/facilitate, before/prior to, about/approximately, start/commence, after/subsequent to, so/therefore.
- **Kill nominalisations.** "perform a validation of" → "validate". "make a decision" → "decide".
- **No filler intensifiers.** "very", "really", "extremely", "incredibly", "seamlessly", "effortlessly", "robust", "powerful", "cutting-edge". If a thing is fast, say how fast and cite it (see [claims-and-evidence.md](claims-and-evidence.md)).
- **Target ≤ 25 words per sentence**, not as a hard limit but as a smell test — longer usually means a buried second sentence.

## 3. Word-level conventions

- **Terminology is fixed per repo.** Pick one term per concept and never alternate for variety — if it is a "record", it is not also a "row", an "entry", and an "item". Elegant variation is a virtue in prose and a defect in documentation. Maintain the list in the repo's Vale vocabulary (`styles/config/vocabularies/`).
- **Expand an acronym once**, at first use, then use the acronym: "Command Line Interface (CLI)".
- **Spelling** follows the repo. These repos use **British spelling in prose** (`behaviour`, `initialise`, `licence` as noun) while **code identifiers, CLI flags, and cited API names keep their own spelling** (`color`, `initialize`, `--license`). Never "correct" an identifier.
- **Oxford comma**: use it.
- **Em dashes** — spaced or unspaced consistently per repo; these repos use spaced em dashes for parenthetical breaks.
- **Sentence case for headings.** Not Title Case. Proper nouns keep their capitals.
- **No emoji in reference documentation.** Acceptable sparingly in changelogs or marketing if the repo already does it.

## 4. Inclusive and precise language

- **Never** "simply", "just", "obviously", "trivially", "everyone knows" — they tell a stuck reader the fault is theirs.
- Prefer **they/them** for a person of unstated gender.
- Replace ableist metaphors used as judgements ("crazy", "insane", "blind to", "cripples").
- Use **allowlist/denylist**, **primary/replica**, **placeholder** over the legacy terms.
- Say **"unsupported"** or **"not implemented"** rather than "unfortunately".

## 5. Structure

- **Answer first.** Put the conclusion, the command, or the definition in the first sentence of a section. Background follows; it never precedes.
- **One `H1` per document**, matching the title. Do not skip heading levels.
- **Sections are scannable**: a reader jumping to a heading must be able to act without reading upward.
- **Lists** for parallel items, **tables** for comparisons across a fixed set of dimensions, **prose** for reasoning. A table with one column of real content is a list.
- **Front-load links.** Put the link on the noun that names the destination, never on "click here", "this", "here", or a bare URL in body prose. The link text alone should say where it goes.
- **Code blocks carry a language tag.** Commands show the command only — no `$` prompt — so the reader can copy them.
- **Cross-reference rather than duplicate.** One home per fact; a second copy will drift. If two documents need the same rule, one owns it and the other links.

## 6. Markdown mechanics

**Not tool-enforced.** Vale checks prose, not Markdown structure, and this plugin ships no structural linter — so these are conventions to apply while writing and to check by eye when reviewing. Where a repo already runs a Markdown linter, that config wins; run it and do not argue with it.

- ATX headings (`##`), not underlines.
- Fenced code blocks with a language tag, not indented blocks. An untagged fence loses syntax highlighting silently.
- Blank line around headings, lists, and fences.
- No trailing whitespace; single trailing newline.
- Reference-style or inline links consistently, not mixed.
- One `H1`, matching the title; no skipped heading levels (see §5).
- Line length is deliberately **unconstrained** — semantic line breaks (one clause per line) are welcome and make diffs readable.

## 7. What this guide does not cover

- **Whether a claim may be made at all** → [claims-and-evidence.md](claims-and-evidence.md).
- **Which document kind you are writing, and what belongs in it** → [doc-types.md](doc-types.md).
- **Discoverability and machine-readability** → [seo-checklist.md](seo-checklist.md).
