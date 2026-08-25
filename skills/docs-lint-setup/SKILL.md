---
name: docs-lint-setup
description: Scaffold prose and Markdown linting into a repository. This skill should be used when the user runs `/docs-lint-setup` or asks to "set up Vale", "add prose linting", "configure markdownlint", "add a docs lint CI job", or "bootstrap the docs linters" — it writes the plugin's reference `.vale.ini` and `.markdownlint.jsonc` and will not overwrite an existing config unprompted. For what the rules mean, use `copy-editing` or `references/style-guide.md`. Not for non-prose linting.
argument-hint: "[target dir] [--ci] [--force]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# docs-lint-setup — scaffold the prose linters

Scaffold prose linting into **$ARGUMENTS** (default: the repo root).

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

Two tools, complementary and both non-negotiable once installed — they exist so that the mechanical half of `references/style-guide.md` never costs a reviewer's attention:

| Tool | Owns | Config |
|---|---|---|
| **Vale** (<https://vale.sh>) | Prose style: voice, hedges, weasel words, condescension, terminology | `references/vale.ini` → `.vale.ini` |
| **markdownlint** | Markdown structure: headings, fences, whitespace, link form | `references/markdownlint.jsonc` → `.markdownlint.jsonc` |

## Procedure

1. **Look before writing.** Check for an existing `.vale.ini`, `_vale.ini`, `.markdownlint.{json,jsonc,yaml,yml}`, or `.markdownlint-cli2.*`.
   - **Present** → do **not** overwrite. Read it, report what it already covers, and offer a diff of the additions the reference config would make. Apply only with `--force` or explicit confirmation. A repo's own config always wins.
   - **Absent** → continue.

2. **Copy the reference configs**, resolving them host-agnostically (`${CLAUDE_PLUGIN_ROOT}/references/…`, `../../references/…`, or Glob):

   ```bash
   cp "<plugin-root>/references/vale.ini"            .vale.ini
   cp "<plugin-root>/references/markdownlint.jsonc"  .markdownlint.jsonc
   ```

3. **Seed the vocabulary.** Vale's `Vocab = Cadasto` needs the directory to exist or `vale sync` warns:

   ```bash
   mkdir -p styles/config/vocabularies/Cadasto
   touch styles/config/vocabularies/Cadasto/accept.txt
   touch styles/config/vocabularies/Cadasto/reject.txt
   ```

   Populate `accept.txt` with the repo's canonical terms and product names (this is what keeps naming fixed per `references/style-guide.md` §3) and `reject.txt` with banned vocabulary — the filler intensifiers and marketing words the style guide bans, so the linter catches them instead of a reviewer. Seed both from terminology already used in the repo's docs; do not invent terms.

4. **Gitignore the downloaded styles.** `StylesPath = styles` holds downloadable packages, not source:

   ```gitignore
   styles/
   ```

   Add it if absent. Keep `styles/config/vocabularies/` tracked — negate it (`!styles/config/`, `!styles/config/**`) since the vocabulary *is* source.

5. **Sync and run.** Report the real output; do not claim a clean run you did not see.

   ```bash
   vale sync                      # download the packages named in .vale.ini
   vale .                         # lint
   markdownlint-cli2 "**/*.md"    # structure
   ```

   Neither tool installed? Say so and stop after writing the configs — do not report a passing lint. Install hints: `vale` via Homebrew/`go install`/release binary; `markdownlint-cli2` via `npm i -g markdownlint-cli2`.

6. **Expect a large first run, and do not "fix" it by gutting the config.** A repo linted for the first time produces hundreds of alerts. Triage in this order: raise `MinAlertLevel` to `error` to get a shippable baseline, fix the errors, then step down to `warning` and `suggestion`. Disable a rule only when it is genuinely wrong for the repo — and leave a comment saying why, as the reference configs do.

7. **CI, with `--ci`.** Add a job that runs both linters on pull requests. Match the repo's existing workflow style rather than importing a new one; pin the tool versions. Do not add a CI job that fails on the pre-existing backlog — gate on changed files, or land the baseline first.

## Report

State: which configs were written or skipped (and why), whether the vocabulary directory was seeded, whether `styles/` was gitignored, whether each tool is installed, the **actual** first-run alert counts by severity, and the recommended triage order.

## Hand off

What the rules mean and how to apply them → `copy-editing` (editing) or `technical-writing` (authoring); the rules themselves → `references/style-guide.md`.
