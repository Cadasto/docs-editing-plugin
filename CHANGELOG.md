# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

### Fixed
- Skills: `marketing-copy` prescribed `vale` in its pre-handover self-check while declaring no `Bash` in `allowed-tools`, so the instruction could not be followed without a permission prompt its sibling skills avoid.
- Agents, docs: `prose-reviewer` and `seo-auditor` were described as **read-only** in their own bodies, the README, `AGENTS.md` and the release notes while declaring `Bash`, which is write-capable. Both are now **report-only** — no `Write`/`Edit` in the tool grant, and no-edit stated as a contract the body keeps rather than a sandbox that enforces it.

### Added
- Validation: tool-grant invariants — a component whose body prescribes a shell command must declare `Bash`; an agent must not declare `Write`/`Edit`, nor call itself "read-only" while holding a write-capable tool. Both are negative-tested against the defects above.

### Changed
- Skills: the `docs-editing` router declares `allowed-tools: Read, Grep, Glob, Bash`, matching the deterministic checks its routing table tells the assistant to run.

## [0.1.0] - 2026-08-25

First build — a dual-host (Claude Code + Cursor) documentation, editing, and content surface. Pure Markdown + JSON, stack-agnostic, no MCP backend. Scope is human-facing prose; agent-instruction files (`AGENTS.md`, `CLAUDE.md`, rules) are read for conventions, never authored.

### Added
- Dual-host manifests (`.claude-plugin/plugin.json`, `.cursor-plugin/plugin.json`) with parity-enforced metadata; plugin `name` is `docs-editing`.
- References: `references/claims-and-evidence.md` — the load-bearing rule (claim classes, the never-invent list, why hedging is not a repair, status vocabulary, inventory rot, audience calibration). Every component cites it.
- References: `references/style-guide.md` — voice and person per context, sentence economy, terminology, inclusive language, structure, Markdown mechanics; each mechanical rule names its enforcing tool.
- References: `references/doc-types.md` — the four Diátaxis document kinds and their boundary rules, plus fixed contracts for `README.md`, `CHANGELOG.md`, and migration notes, and the explicit exclusion of agent-instruction files.
- References: `references/seo-checklist.md` — on-page essentials, crawlability, content signals, and the AI-citability layer (`llms.txt`, Markdown twins, JSON-LD).
- References: `references/vale.ini` and `references/markdownlint.jsonc` — the reference linter configs, with the house-style deviations and escalations commented.
- Skills: `docs-editing` — auto-invoked router; routes each prose task to the owning skill and canonical reference, carries the "read the target repo's rules first" instruction and the refusals worth making. Only its `description` is always-on.
- Skills: `technical-writing` — author new documentation; orient in the repo, pick exactly one document kind, draft to the house style, ground every claim, verify links/commands/lint before claiming done.
- Skills: `copy-editing` — tighten existing prose; establishes the proofread / line-edit / structural contract first, runs the tools, then six passes large-to-small with the claims pass first.
- Skills: `marketing-copy` — landing, feature, and announcement copy; substance before words, observable mechanism instead of invented outcome, explicit pre-handover self-check.
- Skills: `seo-audit` — technical and on-page audit of the published output, ranked by reader impact with an honest coverage statement; `--fix` edits source, never build output.
- Skills: `ai-seo` — citability by AI search; `llms.txt` currency against the nav, Markdown twins, validated JSON-LD, chunk-level self-containment.
- Skills: `docs-lint-setup` — scaffold `.vale.ini` + `.markdownlint.jsonc`, seed the Vale vocabulary, gitignore `styles/`; never overwrites an existing config unprompted.
- Agents: `prose-reviewer` — report-only prose review for what linters cannot see (unsourced/hedged claims, capability claimed but not shipped, stale inventories, merged document kinds, terminology drift); ranked findings plus an explicit coverage statement.
- Agents: `seo-auditor` — report-only discoverability sweep over a docs tree or live site; audits published output by preference and states its coverage.
- Hooks: `session-start.sh` — detects a docs/content workspace and prints one standards line plus the surface; a bare `README.md` deliberately does not trigger it. Dual-host.
- Hooks: `prose-lint-on-save.sh` — reports `vale`/`markdownlint` alerts for the just-edited Markdown file. Advisory (never rewrites), opt-in on the repo's own linter config, output capped, always exits 0. Dual-host.
- Cursor rule: `rules/docs-editing-context.mdc` — Markdown- and docs-scoped guidance mirroring the router.
- Validation: `scripts/validate.py` + `scripts/validate.sh` — manifests, dual-host parity, component paths, kebab-case names, hook-config JSON and script executability, and skill/agent/rule frontmatter (agents must declare `tools:`; the unquoted-`': '` metadata trap). Plus three plugin-specific invariants: every `references/<file>` cited by a component exists; every relative Markdown link resolves and every `#anchor` matches a heading in its destination (code fences and inline code spans excluded, external links not fetched); and every skill and agent is wired into both the router body and `hooks/session-start.sh`.
- CI: `.github/workflows/validate.yml` pins Python, runs the validator strictly, and `bash -n`s both hook scripts.
- Contributor docs: `docs/install.md`, `docs/testing.md`, `docs/versioning.md`, `docs/authoring.md`; issue + PR templates and `copilot-instructions.md` under `.github/`.
