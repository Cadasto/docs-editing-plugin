---
name: docs-lint-setup
description: Scaffold Vale prose linting into a repository. This skill should be used when the user runs `/docs-lint-setup` or asks to "set up Vale", "add prose linting", "bootstrap the docs linter", "add a prose lint CI job", or "why is Vale so noisy?" — it writes the plugin's reference `.vale.ini`, seeds the vocabulary, and will not overwrite an existing config unprompted. For what the rules mean, use `copy-editing` or `references/style-guide.md`. Not for Markdown structure linting, which this plugin does not ship, nor for non-prose linting.
argument-hint: "[target dir] [--ci] [--force]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# docs-lint-setup — scaffold Vale

Scaffold prose linting into **$ARGUMENTS** (default: the repo root).

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill). Resolve host-agnostically: Glob for the installed copy is the reliable method; `${CLAUDE_PLUGIN_ROOT}` is available to hook and MCP command fields, not to tool calls.

**[Vale](https://vale.sh)** is the enforcing tool for the mechanical half of `references/style-guide.md` — voice, hedges, weasel words, condescension, terminology. Config: `references/vale.ini` → `.vale.ini`.

Vale checks **prose**, not Markdown structure. Heading nesting, fence language tags, and trailing whitespace are conventions applied by judgment here (`references/style-guide.md` §6); this plugin ships no structural linter. Where a repo already runs one, respect its config and do not replace it.

## Procedure

1. **Look before writing.** Check for an existing `.vale.ini` or `_vale.ini`.
   - **Present** → do **not** overwrite. Read it, report what it already covers, and offer a diff of what the reference config would add. Apply only with `--force` or explicit confirmation. A repo's own config always wins.
   - **Absent** → continue.

2. **Copy the reference config**, resolving it host-agnostically:

   ```bash
   cp "<plugin-root>/references/vale.ini" .vale.ini
   ```

3. **Seed the vocabulary.** `Vocab = Cadasto` needs the directory to exist or `vale sync` warns:

   ```bash
   mkdir -p styles/config/vocabularies/Cadasto
   touch styles/config/vocabularies/Cadasto/accept.txt
   touch styles/config/vocabularies/Cadasto/reject.txt
   ```

   `accept.txt` holds the repo's canonical terms, product names, and ordinary technical jargon — this is what keeps naming fixed per `references/style-guide.md` §3, **and** what suppresses Vale's spelling and heading-capitalisation false positives on proper nouns. `reject.txt` holds banned vocabulary, so the linter catches marketing words instead of a reviewer. Seed both from terminology already in the repo's docs; do not invent terms.

4. **Gitignore the downloaded styles.** `StylesPath = styles` holds downloadable packages, not source:

   ```gitignore
   styles/
   !styles/config/
   !styles/config/**
   ```

   The negations keep the vocabulary tracked, because the vocabulary *is* source.

5. **Sync and run.** Report the real output; never claim a clean run that was not observed.

   ```bash
   vale sync                      # download the packages named in .vale.ini
   vale .                         # lint
   vale --minAlertLevel=error .   # errors only
   ```

   Vale exits `0` clean, `1` on findings, `2` on a config error. If Vale is not installed, say so and stop after writing the config — do not report a passing lint. Install via the release binary from <https://github.com/vale-cli/vale/releases> (`go install` fails to build).

6. **Expect a loud first run, and do not gut the config to quiet it.** Triage in order: `--minAlertLevel=error` for a shippable baseline, fix those, then step down to `warning` and `suggestion`. Disable a rule only when it is genuinely wrong for the repo, with a comment saying why, as the reference config does.

   Two rules are reliably noisy on technical prose and are the first to reach for: `write-good.E-Prime` (objects to every "is") and `Vale.Spelling` (flags ordinary jargon until the vocabulary is seeded).

7. **CI, with `--ci`.** Add a job running `vale --minAlertLevel=error` on pull requests. Match the repo's existing workflow style; pin the Vale version. Do not gate on the pre-existing backlog — scope to changed files, or land the baseline first.

## Report

State: whether the config was written or skipped and why, whether the vocabulary directory was seeded, whether `styles/` was gitignored, whether Vale is installed, the **actual** first-run alert counts by severity, and the recommended triage order.

## Hand off

What the rules mean and how to apply them → `copy-editing` (editing) or `technical-writing` (authoring); the rules themselves → `references/style-guide.md`.
