# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/spec/v2.0.0.html

## [Unreleased]

### Added
- References: `references/vocab-accept.txt` — a seed Vale vocabulary of technical jargon (`repo`, `config`, `frontmatter`, `validator`, `stderr`, `citability`, `crawlability`, …). Entries are case-tolerant regexes (`[Cc]onfigs?`) because `Vale.Terms` demands a term appear exactly as listed: a bare lowercase entry silences the spelling warning and then reports every sentence-initial capital instead. Product names are listed with their exact capitalisation on purpose, so that rule enforces them. Deliberately excludes British/American spelling pairs — Vale's dictionary accepts both. Verified against Vale 3.18.0.

### Changed
- References: `vale.ini` disables `Google.Quotes`. Google's package assumes American punctuation-inside-quotes while the house style is British, so the rule fired on correct prose — 7 error-level false positives on this repo's own docs, now zero. Recorded in the existing deliberate-deviations block, which must sit inside the `[*.{md,mdx,markdown}]` section: a rule set after the `[{CHANGELOG.md,LICENSE}]` header silently applies to that section instead.
- References: the vocabulary is no longer named after an organisation. `Vocab = Cadasto` became `Vocab = Project`, a neutral default a repo can rename, so scaffolding no longer creates a `Cadasto/` directory in someone else's tree. `/docs-lint-setup` takes the name as a `VOCAB` variable used for both the directory and the config value.
- Docs: `AGENTS.md` no longer pins a version (`Current status — v0.1.1`, itself stale by two releases). The version and its changes live in `CHANGELOG.md` and the git tags; repeating them in an instruction file only creates a second copy to rot. The component inventory and the check-the-tree-first warning stay.
- Skills: `/docs-lint-setup` copies the vocabulary seed instead of `touch`ing an empty `accept.txt`, then appends repo-specific terms. Its triage guidance no longer lists `Vale.Spelling` as inherently noisy — spelling noise now means step 3 was skipped, and the fix is to seed the vocabulary rather than disable a genuine check.
- References: `vale.ini` documents where the vocabulary seed comes from and why an empty one is harmful.
- Docs: `docs/versioning.md`, `AGENTS.md` — the `cadasto` catalog pins each entry to a release tag, so a tag here ships nothing until the entry's `version` and `source.ref` move. Repinning is now release step 8.
- Docs: `docs/testing.md`, `docs/versioning.md`, `docs/authoring.md` H1s are sentence case per `references/style-guide.md` §3; product names keep their capitals.
- Docs: opened `docs/install.md`'s no-`claude plugin add` note and `docs/testing.md`'s overview with the conclusion rather than "There is …" (§5, answer first).
- Docs: `docs/authoring.md` uses "for example" over "e.g." (`Google.Latin`).

### Fixed
- Skills: `/docs-lint-setup` claimed a missing vocabulary directory makes `vale sync` warn. It does not — `vale sync` reports success and exits 0, so the config looks healthy; the *lint* then fails hard with `E100 [vocab] … vocabulary not found` and exit 2. Verified against Vale 3.18.0.
- Linting: the reference Vale setup shipped an **empty** vocabulary, so `Vale.Spelling` flagged ordinary jargon and buried every real style finding — 190 spelling alerts across this plugin's own tree, against 11 once seeded (the rest being product names and cited proper nouns, which belong in a repo's own additions). A scaffolded repo now lints clean on first run.
- Docs: `README.md` claimed the validator enforces **two** plugin-specific invariants and named two. It enforces four — reference resolution, markdown links, tool grants, doc sync — which `docs/testing.md` already stated correctly, so the README was the file out of step. Exactly the inventory rot `references/claims-and-evidence.md` §5 warns about, in the plugin's own shop window.
- Docs: `docs/versioning.md`, `AGENTS.md` claimed `vale` "warns but exits 0" for an unknown rule name. It does not warn — an unknown rule yields **empty stderr and exit 0**, which is what makes the drift dangerous, so the gotcha undercut its own point. An unknown *style package* is the loud case (`E100 [loadStyles]`, exit 2). Verified against Vale 3.18.0.
- Docs: fixed the rules the reference `vale.ini` escalates to **error** in this repo's own prose — `Google.Will` (future tense where present belongs, §1) in `README.md` and `docs/install.md`, and `write-good.Weasel` ("several", §2) in `README.md`, replaced with the count the sentence goes on to list.

## [0.2.0] - 2026-08-25

Tightens the plugin to a single prose linter and makes its always-on surface cheap: markdownlint is gone, the agents are honestly described as report-only, and every skill description is rewritten for the skill-listing budget.

### Added
- Validation: tool-grant invariants — a component whose body prescribes a shell command must declare `Bash`; an agent must not declare `Write`/`Edit`, nor call itself "read-only" while holding a write-capable tool. Both are negative-tested against the defects recorded under Fixed.

### Changed
- Skills: all seven skill `description` fields rewritten for the skill-listing budget — trigger phrases and sibling disambiguation kept, the name-restating lead-in and mechanism prose dropped. Total description weight falls from 3,635 to 1,861 characters (measured listing: 35,560 → 33,786), taking the plugin from 10.8% of the listing for 8.3% of the skills to 6.1%. Descriptions are dropped whole (the skill degrades to a bare name, not a truncated sentence) and never-used skills rank last, so length is the only lever a new plugin controls.
- References: `style-guide.md` §6 (Markdown mechanics) no longer claims tool enforcement — those rules are conventions applied by judgment, and a consuming repo's own structural linter takes precedence.
- Hooks: `prose-lint-on-save.sh` is Vale-only and opt-in on `.vale.ini` alone; `session-start.sh` no longer treats a markdownlint config as a docs-workspace signal.
- Docs: `docs/install.md` records Vale's exit codes (`0` clean, `1` findings, `2` config error) and that the release binary is the working install route — `go install` fails to build.
- Skills: the `docs-editing` router declares `allowed-tools: Read, Grep, Glob, Bash`, matching the deterministic checks its routing table tells the assistant to run.

### Removed
- Dropped the **markdownlint** integration entirely: deleted `references/markdownlint.jsonc`, removed the tool from `docs-lint-setup` (now Vale-only), `copy-editing`, `technical-writing`, the `docs-editing` router, `prose-reviewer`, the Cursor rule, and both hooks. It required a Node toolchain that could not be verified, and prescribing an unrunnable tool contradicts the plugin's own advice-equals-tooling principle.

### Fixed
- Skills: `marketing-copy` prescribed `vale` in its pre-handover self-check while declaring no `Bash` in `allowed-tools`, so the instruction could not be followed without a permission prompt its sibling skills avoid.
- Docs: the local install command was `claude plugin add /path/to/docs-editing-plugin`, which **does not exist** — `claude plugin` prints its general help and exits 0 for an unknown subcommand, so the wrong command never failed visibly. Replaced with `claude --plugin-dir <path>` (session-scoped) in `README.md`, `docs/install.md`, `docs/versioning.md` and `AGENTS.md`, with the persistent-install route stated explicitly.
- Agents, docs: `prose-reviewer` and `seo-auditor` were described as **read-only** in their own bodies, the README, `AGENTS.md` and the release notes while declaring `Bash`, which is write-capable. Both are now **report-only** — no `Write`/`Edit` in the tool grant, and no-edit stated as a contract the body keeps rather than a sandbox that enforces it.

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
