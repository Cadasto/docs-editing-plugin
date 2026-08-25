# Document Kinds and Their Boundaries

Most bad documentation is not badly written — it is **two kinds of document in one file**. A tutorial that stops to explain architecture loses the beginner; a reference page that tells a story cannot be scanned. Decide the kind first, then write only that kind.

The four-kind split follows **Diátaxis** (Daniele Procida) — <https://diataxis.fr>. The repo-shape contracts in §2 are conventions rather than Diátaxis. All of it concerns prose written **for people**; §3 records what is deliberately out of scope.

## 1. The four kinds

|  | **Tutorial** | **How-to guide** | **Reference** | **Explanation** |
|---|---|---|---|---|
| Serves | Study | Work | Work | Study |
| Reader wants | To learn by doing | To achieve a goal | To look something up | To understand why |
| Form | A lesson | A recipe | A description | A discussion |
| Voice | "We will build…" / imperative | Imperative | Indicative, third person | Discursive |
| Success | The reader completed it | The reader's task is done | The fact was found fast | The reader can reason about it |
| Completeness | Deliberately narrow | Goal-scoped | **Exhaustive** | Bounded by the question |
| Order | Fixed sequence | Fixed sequence | Structure mirrors the code | Argument order |

### Boundary rules

- **A tutorial must work end to end, exactly as written.** No choices, no branches, no "depending on your setup". Pin versions. One path.
- **A how-to assumes competence.** It solves one real problem and may branch. It does not teach fundamentals — it links to them.
- **Reference does not instruct.** It describes what is there: every parameter, every field, every error, every default. Its structure mirrors the code's structure so a reader can navigate by guessing. No opinions, no tutorials, no worked narratives.
- **Explanation does not instruct either.** It supplies context, alternatives considered, trade-offs, history. It is the only kind allowed to argue.

### The four failure modes

| Symptom | Actual problem | Fix |
|---|---|---|
| Tutorial keeps digressing into *why* | Explanation leaked in | Move it out; link to it |
| Reference page has a worked example that grew a plot | Tutorial leaked in | Extract to a how-to |
| How-to starts by installing the toolchain | Tutorial leaked in | Link to the tutorial as a prerequisite |
| Explanation contains the authoritative parameter list | Reference leaked in | Reference owns it; explanation links |

## 2. Repo-shape documents

These have fixed contracts in these repositories.

### README.md

The front door, for someone who has not decided yet. In order:

1. **What it is**, in one or two sentences — the noun, the audience, the mechanism.
2. **Install** — the shortest working path, copy-pasteable.
3. **Component surface / what it does** — a table, verified against the tree.
4. **Prerequisites** — what must already be on the host, and what happens without it.
5. **Development** — how to validate and contribute, linked not inlined.
6. **License.**

A README is not a manual. When a section outgrows a screen, it becomes a page in `docs/` and the README links it.

### CHANGELOG.md

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format, [SemVer](https://semver.org). Entries accumulate under `## [Unreleased]` and fold into a dated `## [X.Y.Z] - YYYY-MM-DD` section at release. Groups in fixed order — **Added, Changed, Deprecated, Removed, Fixed, Security** — omitting empty ones. One line per bullet, leading with the subsystem, backticks around file/component names. **No rationale and no PR links** — those belong in the commit body and the PR. A changelog answers "what changed for me?", not "why did you do it?".

### Migration / upgrade notes

Every breaking change gets: what broke, the exact error the reader will see, the mechanical fix, and — if one exists — the automated path. Order by likelihood of being hit, not by module.

## 3. Not documentation: agent-instruction files

`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, and skill or agent definitions are **not** in any of the four kinds above, and are **out of scope** for these standards. Their reader is a model, not a person, which inverts several rules that are otherwise load-bearing:

| Human-facing prose | Agent-instruction file |
|---|---|
| Cut repetition — say it once, link the rest | Repetition is deliberate; a rule stated once is a rule frequently missed |
| Prefer the shorter, softer verb | Hard constraints stay hard; "should" where "MUST" was meant changes behaviour |
| Vary sentence structure for readability | Rigid, parallel structure is a feature |
| Trim to what a reader will actually read | Enumerating the failure mode explicitly is the point |

Editing one of these files with a prose editor's instincts quietly degrades it. **Read them** — for terminology, spelling, the named ground-truth source, and constraints to obey — and leave authoring them to the tooling that owns them.

## 4. Choosing, in one question

> **Is the reader trying to *do* something right now, or trying to *understand* something?**

Doing → how-to (competent) or tutorial (new). Understanding → reference (a specific fact) or explanation (the shape of it).

If the answer is "both", that is two documents.

## 5. Where the other rules live

- Sentence-level style, voice, headings → [style-guide.md](style-guide.md)
- Whether a claim is permitted → [claims-and-evidence.md](claims-and-evidence.md)
- Titles, metadata, discoverability → [seo-checklist.md](seo-checklist.md)
