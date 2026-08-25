# AI Guidelines: Docs Editing Plugin

This file provides guidance to AI coding assistants (Claude Code, Cursor, and compatible tools that read `AGENTS.md`) working in this repository. It is the **canonical** instruction set; `.claude/CLAUDE.md` and any host-specific instruction files defer to it (`.claude/CLAUDE.md` imports this file via `@../AGENTS.md`).

## Project Overview

The **Docs Editing Plugin** (`docs-editing`) is an AI plugin by Cadasto B.V. that teaches AI coding assistants **documentation, editing, and content standards** — technical writing, copy editing, marketing copy, SEO, and AI citability. It targets **both Claude Code and Cursor** from a single shared component set, and is **pure Markdown + JSON** with **no MCP backend**.

It is **general-purpose and stack-agnostic** by design: the components operate on prose (`*.md`, page copy, site metadata, `llms.txt`) and on the target repository's own conventions, so the same skills serve an MkDocs site, a Docusaurus site, and a plain `docs/` tree unchanged.

> **Current status — v0.1.1.** First build, plus a correctness pass on tool grants. Shipped and validating clean (`./scripts/validate.sh` + `claude plugin validate .`): the auto-invoked `docs-editing` **router**; the worker skills `technical-writing`, `copy-editing`, `marketing-copy`, `seo-audit`, `ai-seo`; the user-invoked `/docs-lint-setup`; the report-only `prose-reviewer` and `seo-auditor` agents; four canonical references plus the reference `vale.ini`; the `rules/docs-editing-context.mdc` Cursor rule; and host-agnostic `session-start` + `prose-lint-on-save` hooks. Do not assume a file is present because it is documented here — check first.

## Domain Context

### The load-bearing rule

**A claim that cannot be traced to a source does not ship.** This is not a stylistic preference; it is the plugin's reason to exist, and it outranks everything else in these components.

Generative copy tooling fails in one specific, predictable way: asked to make a page more persuasive, it **invents the persuasion**. Statistics, customer counts, testimonials, benchmark numbers, awards, and urgency devices are the most commonly fabricated elements because they are the most conventional ingredients of landing-page copy. Two consequences follow:

- **It destroys credibility with technical audiences.** Developers, engineers, and domain specialists read an unsourced number as evidence of unseriousness — so the growth-copy move that raises conversion on a consumer page *lowers* trust here.
- **Hedging is not a repair.** "Up to 40%", "designed to reduce", "teams report" all keep the claim and add evasion.

The repair is always the same: **replace the invented outcome with the observable mechanism**, which is both permissible and more persuasive to this reader.

The canonical statement — the four claim classes, the never-invent list, the status vocabulary, the inventory-rot rule, and audience calibration — is **[`references/claims-and-evidence.md`](references/claims-and-evidence.md)**. Components cite it rather than restating it.

### The other three references

Guidance must be grounded in these, not in personal preference. Each is the single home for its rules:

- **[`references/style-guide.md`](references/style-guide.md)** — house style: voice and grammatical person per context, sentence economy, terminology discipline, inclusive language, structure, Markdown mechanics. Names the enforcing tool for every mechanical rule.
- **[`references/doc-types.md`](references/doc-types.md)** — the four document kinds and their boundary rules, based on **Diátaxis** (<https://diataxis.fr>), plus the fixed contracts for `README.md`, `CHANGELOG.md` ([Keep a Changelog](https://keepachangelog.com/en/1.1.0/)), and migration notes — and §3, the agent-instruction files that are deliberately out of scope.
- **[`references/seo-checklist.md`](references/seo-checklist.md)** — on-page essentials, crawlability, content signals, and the AI-citability layer (`llms.txt` per <https://llmstxt.org>, Markdown twins, JSON-LD per schema.org).

**Deterministic beats prose.** Where a tool enforces a rule, run the tool: **Vale** (<https://vale.sh>) owns prose style. The reference config is `references/vale.ini`; `/docs-lint-setup` scaffolds it. A component must never claim a clean lint it did not run.

**Markdown *structure* has no shipped enforcer.** Vale checks prose only. The mechanics in `references/style-guide.md` §6 — heading nesting, fence language tags, trailing whitespace — are conventions applied by judgment. Do not write guidance implying a structural linter ships here, and where a consuming repo runs one, respect its config rather than replacing it.

**The target repository outranks this plugin.** Every component reads the repo being worked on — its `AGENTS.md`/`CLAUDE.md`, style guide, `CONTRIBUTING.md`, and linter configs — *first*, and treats a conflict as the repo's win, reported rather than silently overridden. This matters most for a named **ground-truth source** for domain facts: where a repo names one, domain statements come from it, never from model memory.

### Audience boundary: human-facing prose only

The components write and edit **prose intended for people** — documentation, guides, references, page and marketing copy, changelogs, release notes, site metadata, `llms.txt`.

**Agent-instruction files are out of scope: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, and skill/agent definitions are read for their conventions and never authored or rewritten by these components.** They are a different genre with a different reader, different contracts, and dedicated tooling of their own; a prose editor tuned for human readers will quietly degrade an instruction file by "improving" the imperative voice, cutting the repetition that makes a rule stick, or softening a hard constraint into a suggestion.

The distinction is **read versus write**. Reading a repo's `AGENTS.md` for its terminology, spelling, ground-truth source, and constraints is required — that is how the rule above is honoured. Editing one is someone else's job. When a user asks for an agent-instruction file to be written or revised, say so and point them elsewhere rather than treating it as documentation.

## Repository Layout

This repo supports **both Claude Code and Cursor**; shared assets (skills, agents, references) are used by both. Host-specific manifests and hook configs are separate.

- **Claude manifest**: `.claude-plugin/plugin.json` — `name` (`docs-editing`), `version`, `description`, `author` (an **object** `{name, url}` — `claude plugin validate` rejects a bare string), `license`, `repository`, `keywords`. Claude Code discovers components from the **default folders** (`skills/`, `agents/`, `hooks/`) automatically.
- **Cursor manifest**: `.cursor-plugin/plugin.json` — same metadata **plus** explicit top-level path keys (`skills`, `agents`, `rules`, `hooks`). No `mcpServers` — this plugin has no MCP backend. Keep `name`/`version`/`description`/`author` identical to the Claude manifest.
- **Skills**: `skills/<name>/SKILL.md` — shared by both hosts. The six worker skills carry `argument-hint` + `allowed-tools` so they are both auto-invoked on intent and user-invocable as `/<name>`; `docs-editing` is the always-on router. **Skills use `allowed-tools:` (the Claude Code skill/command key — Cursor reads it too); only agents use `tools:`.**
- **Agents**: `agents/<name>.md` — report-only, context-isolated specialists (`tools:` not `allowed-tools:`). Neither declares `Write`/`Edit`; both declare `Bash` to run the linters, so the no-edit property is a contract in the body, not a sandbox.
- **References**: `references/` — the four canonical rule documents plus the reference linter config (`vale.ini`). Components cite these instead of duplicating rules.
- **Cursor rules**: `rules/*.mdc` — Cursor-only rule guidance (`description` / `globs` / `alwaysApply`), referenced by the Cursor manifest's `rules` path. Shipped: `rules/docs-editing-context.mdc`.
- **Claude hooks**: `hooks/hooks.json` — object `{ "hooks": { "SessionStart": [...], "PostToolUse": [...] } }`; use `${CLAUDE_PLUGIN_ROOT}` in command paths.
- **Cursor hooks**: `hooks/cursor-hooks.json` — object `{ "version": 1, "hooks": { "sessionStart": [...], "afterFileEdit": [...] } }`; the command runs from the plugin root (**workspace-relative**, **not** `${CLAUDE_PLUGIN_ROOT}`).
- **Shared hook scripts**: `hooks/session-start.sh` (detects a docs/content workspace and prints context + the skill surface) and `hooks/prose-lint-on-save.sh` (reports `vale` alerts for the just-edited Markdown file). Both host-agnostic; both exit 0 always.
- **Claude settings**: `.claude/settings.json` enables the maintainer plugins used while developing this repo (skill-creator, superpowers, plugin-dev, claude-md-management) and pre-approves the validate commands; `.claude/CLAUDE.md` imports this file via `@../AGENTS.md`. `.claude/settings.local.json` is gitignored.
- **Validation**: `scripts/validate.sh` (graceful local wrapper — warns and skips if Python is absent) runs `scripts/validate.py`, which checks both manifests, dual-host parity, declared component paths, kebab-case names, hook-config JSON *and script executability*, skill/agent/rule frontmatter, plus the four plugin-specific invariants below. Stdlib-only. CI pins Python, runs the validator strictly, and `bash -n`s both hook scripts ([`.github/workflows/validate.yml`](.github/workflows/validate.yml)).
- **Contributor docs**: `docs/` holds committed human-facing references — [install](docs/install.md), [testing](docs/testing.md), [versioning](docs/versioning.md), [authoring](docs/authoring.md). `.github/` holds issue + PR templates, `copilot-instructions.md`, and the validate workflow. (Planning/research working notes under `docs/plans/` and `docs/research/` are gitignored — not part of the published plugin.)

## Components

Scope is the **human-facing prose and content layer**. Deliberately **not** in scope: **agent-instruction files** (`AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, skill and agent definitions — read for conventions, never authored; see the audience boundary above); source-code review; specification, requirement, and traceability authoring (the `sdd` plugin's layer); and domain facts, which come from the target repo's named ground-truth source. This keeps the surface small and non-colliding.

### Skills (7)

| Skill | Purpose |
|-------|---------|
| `docs-editing` | Auto-invoked router — routes each prose task to the owning skill and the canonical reference; carries the "read the repo's own rules first" instruction and the refusals worth making |
| `technical-writing` | Author new documentation — orient in the repo, pick exactly **one** document kind, draft to the house style, ground every claim, verify (links, commands, lint) before claiming done |
| `copy-editing` | Tighten existing prose — establish the proofread / line-edit / structural **contract** first, run the tools, then six passes large-to-small with claims first; reports what it left alone and why |
| `marketing-copy` | Landing, feature, and announcement copy — substance before words, mechanism instead of invented outcome, explicit self-check before handing over |
| `seo-audit` | Technical and on-page audit of the **published** output; ranked by reader impact, with an honest coverage statement; `--fix` edits source, never build output |
| `ai-seo` | Citability by AI search — `llms.txt` currency, Markdown twins, **validated** JSON-LD, chunk-level self-containment |
| `docs-lint-setup` | Scaffold `.vale.ini`, seed the Vale vocabulary, gitignore `styles/`; never overwrites an existing config unprompted |

### Agents (2, report-only)

| Agent | Purpose |
|-------|---------|
| `prose-reviewer` | Reviews prose for what linters cannot see — unsourced or hedged claims, capability claimed but not shipped, stale inventories, merged document kinds, terminology drift, buried conclusions. Ranked findings + explicit coverage |
| `seo-auditor` | Context-isolated discoverability sweep over a docs tree or live site — per-page essentials, crawlability, orphans, and the AI-citability layer. Mandatory coverage statement |

### Hooks

- **SessionStart** — detects a docs/content workspace (a generated-site config, a prose-linter config, or a `docs/`/`pages/`/`content/` tree containing Markdown) and prints one context line plus the skill and agent surface. A bare `README.md` deliberately does **not** trigger it.
- **PostToolUse** (Claude Code) / **afterFileEdit** (Cursor) — after a `.md`/`.mdx`/`.markdown` edit, runs `vale` on that one file and prints the alerts. **Advisory: it never rewrites the file**, and it is **opt-in** — silent unless the repo carries its own linter config. Output is capped.

## Development

### Testing & validating

No build step — pure Markdown + JSON. Validate and dogfood locally:

```bash
./scripts/validate.sh                          # manifests, parity, frontmatter, reference citations, doc sync
claude plugin validate .                       # manifest + component structure (no Python needed)
claude --plugin-dir /path/to/docs-editing-plugin        # load a working copy (session-scoped)
```

Then exercise the components on a real docs repository and verify skill auto-triggering and both agents on both hosts. Fuller guidance: [`docs/`](docs/).

**The regression test that matters most:** ask any skill to make a technical page "more compelling" with no source material available. Correct behaviour is to **name what it cannot claim** and offer specificity instead. A plausible statistic, a testimonial, or "trusted by teams worldwide" is a **defect in the component**, not a prompt problem — fix it in `references/claims-and-evidence.md`, not only in the skill that slipped.

### File Conventions

- Skills go in `skills/<name>/SKILL.md` (this includes user-invoked slash commands, carrying `argument-hint`/`allowed-tools`); agents in `agents/<name>.md`; Cursor rules in `rules/<name>.mdc`. The legacy `commands/<name>.md` layout is **not** used — host validators treat every `commands/**/*.md` as a command and warn on missing frontmatter.
- Shared reference material lives in top-level **`references/`**, never under `commands/`.
- All Markdown components use YAML frontmatter; frontmatter `name` MUST equal the directory (skills) or filename stem (agents).
- Use **kebab-case** for all directory and file names.
- `allowed-tools:` (skills) pre-approves tools; **agents use `tools:`** — `allowed-tools:` in an agent file is ignored and the agent silently inherits all tools.
- Worker skills are named for the **task**, unprefixed (`copy-editing`, not `docs-copy-editing`) — they read better as `/copy-editing`, and the plugin namespace already disambiguates.
- Skill bodies are imperative and **cite `references/`** rather than restating rules. Every component carries the one-line note that `references/` resolves from the **plugin root**.
- Use `${CLAUDE_PLUGIN_ROOT}` for intra-plugin paths in Claude hook fields — never hardcode absolute paths or `~`.
- **This repo's own human-facing prose follows its own rules.** README, `docs/`, and CHANGELOG are held to `references/style-guide.md` and `references/claims-and-evidence.md`. Dogfooding is the cheapest test the plugin has. This file and the component bodies are agent-instruction prose — the claims rule still binds them, the style guide does not.

### Documentation Sync

When adding or renaming a component, update in lockstep: the **router's routing table** (`skills/docs-editing/SKILL.md`), the announced surface in **`hooks/session-start.sh`**, **AGENTS.md** (component tables), **README.md**, and **CHANGELOG.md**. The first two are **enforced by `scripts/validate.py`** and fail CI if skipped; the rest are on you. The full ordered procedure is in [docs/authoring.md](docs/authoring.md#adding-a-component).

### Versioning

Plugin version (and, for consistency, description and author) must be kept in sync in **both** `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Follow Semantic Versioning; update both manifests and **CHANGELOG.md** when releasing. See [docs/versioning.md](docs/versioning.md).

### CHANGELOG style

- Entries go under `## [Unreleased]` while work is in flight and fold into the next `## [X.Y.Z] - YYYY-MM-DD` section at release.
- Keep a Changelog groups in order: **Added, Changed, Deprecated, Removed, Fixed, Security**. Omit empty groups.
- One line per bullet, leading with the subsystem (`Skills:`, `Agents:`, `References:`, `Hooks:`) and using backticks for file/skill/key names. No rationale (that belongs in commits/PRs).

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/), e.g. `feat(skills): add copy-editing skill`, `fix(agents): correct tools list in prose-reviewer`. Scopes: `skills`, `agents`, `hooks`, `references`, `rules`, `docs`.

### Branching

Use feature branches and pull requests. Validation runs on every push/PR.

## Gotchas

- **Agents use `tools:`, not `allowed-tools:`.** In an agent file `allowed-tools:` is ignored and the agent silently inherits *all* tools. Neither shipped agent may declare `Write`/`Edit` — the validator rejects that outright. Both do declare `Bash`, which is write-capable, so **"report-only" is a contract their bodies keep, not a sandbox**: say report-only, never "read-only", or the docs claim a guarantee the tool grant does not provide.
- **`author` in `plugin.json` must be an object** (`{name, url}`); `claude plugin validate` rejects a bare string.
- **`references/` is plugin-root-relative, and that is a real trap.** A bare `references/x.md` inside `skills/<name>/SKILL.md` is two levels off, so the first Read fails and the component improvises rules instead of grounding in them — the worst possible failure for a plugin whose value *is* its cited rules. Every component carries the resolution note (`${CLAUDE_PLUGIN_ROOT}/references/…`, `../../references/…`, or Glob), and `scripts/validate.py` checks that every cited reference exists.
- **A frontmatter value with an unquoted `: ` silently drops all metadata.** A real YAML parser reads it as a nested mapping, so the component loads with *every* field empty — no error, just an invisible component. Quote the value or use a `>` block scalar (as the agents do). The validator guards this.
- **`${CLAUDE_PLUGIN_ROOT}` is Claude-Code-only.** Cursor hook commands stay workspace-relative (`bash hooks/session-start.sh`) — don't "fix" them to use it. Keep both hook configs in step.
- **The prose-lint hook must never rewrite a file.** Prose is not mechanically formattable the way source code is; an auto-fixing save hook would silently edit an author's voice. It reports and exits 0. Do not "improve" it into `--fix` mode. It is also opt-in on the repo's own linter config, which is what keeps it from firing noisily in every repo with a README.
- **Audit the published output, not the source.** A static site generator can drop a `<title>`, rewrite a link, absorb a heading into a theme partial, or omit a page entirely with **no build warning**. Source Markdown shows intent; only served HTML shows what a crawler sees. `seo-audit` and `seo-auditor` must state which they used and what they could not check — "no issues found" on an unbuilt site is a false statement.
- **`--fix` edits source, never build output.** A fix applied in `site/` disappears on the next build. And never let a fix change a URL — that breaks every inbound link.
- **Invalid JSON-LD is silently ignored.** A syntax error in structured data produces no visible symptom at all, so `ai-seo` parses it rather than eyeballing it.
- **Vale is the only shipped linter.** Markdown structure is unenforced by design (see Domain Context). Resist re-adding a Node-based structural linter: it could not be verified on the maintainer's machine, and a tool this plugin cannot run is a tool it should not prescribe.
- **Vale style-package rules drift.** `references/vale.ini` names rules from the `Google`, `write-good`, `alex`, and `proselint` packages. When a package renames or removes one, `vale` says **nothing at all** — an unknown rule name yields empty stderr and exit 0, so the escalation or suppression quietly stops applying and the config still looks healthy. An unknown *style package* is the loud case (`E100 [loadStyles]`, exit 2), so a broken `Packages =` line fails visibly while a broken rule line does not. Re-check the named rules by hand when bumping a package. Verified against Vale 3.18.0.
- **A large first Vale run is normal — don't gut the config to silence it.** Triage by raising `MinAlertLevel` to `error`, fixing those, then stepping down. Disabling a rule needs a comment saying why, as the reference configs do.
- **Inventories in this repo rot too.** The component tables in README.md and AGENTS.md, and the counts in them, must be verified against the tree before being edited. The plugin's own rule applies to the plugin's own docs.
- **Don't duplicate the `sdd` plugin.** This plugin owns prose and content; requirements, RFC-2119 specifications, ADRs, and traceability belong to `sdd`. When extending, resist adding a spec-authoring or traceability skill that competes.
- **`claude plugin <unknown-subcommand>` prints the general help and exits 0.** It does not error, so a non-existent command reads as working in a script or a doc review. `claude plugin add` does not exist and never did — the real subcommands are `details disable enable eval init install list marketplace prune tag uninstall update validate`. Verify a CLI invocation by running it and checking behaviour, not just the exit code.
- **There is no local-path *install*.** `claude --plugin-dir <path>` loads a working copy for **one session** (repeatable; also takes a `.zip`), and is the dogfooding path. `claude plugin install` resolves names from a configured marketplace, and `claude plugin marketplace add <path>` needs a `.claude-plugin/marketplace.json`, which a single-plugin repo does not have. A persistent install therefore goes through the marketplace.
- **Register in the marketplace separately — and repin it on every release.** Public availability requires an entry in the `cadasto` marketplace, maintained in `Cadasto/plugin-marketplace`. That entry is pinned to a release tag, so tagging here ships nothing until the entry's `version` and `source.ref` are bumped; see [docs/versioning.md](docs/versioning.md#marketplace).
