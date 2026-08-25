# Testing and Validation

This is a pure-content repository — JSON manifests + Markdown components. There is no build step or package manager. Testing means validating structure, then installing locally and exercising the components.

## Validation

- **Manifest / component validation** — `./scripts/validate.sh` (also run by CI on every PR). The wrapper runs `scripts/validate.py`; if Python 3 is not installed it prints a warning and skips (exit 0) rather than failing — install `python3` for the full local check, or rely on `claude plugin validate .` and CI. CI pins Python so the deep check always runs there.
- **Official validator** — `claude plugin validate .`: checks the manifest and component structure (no extra dependencies).
- **Structural review** — run the `plugin-dev:plugin-validator` agent after creating or modifying components.
- **Skill quality review** — run the `plugin-dev:skill-reviewer` agent: description-triggering quality, progressive disclosure, content structure.
- **Token cost** — `claude plugin details docs-editing` shows the inventory and projected token cost. Only the frontmatter `description` of each skill is always-on; keep those lean.

### What `scripts/validate.py` checks

Generic, shared with the sibling Cadasto plugins:

- Both manifests parse and carry the required fields; `author` is an **object**, not a string.
- **Dual-host parity** — `name`, `version`, `description`, `author` agree across `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`.
- Every component path a manifest declares exists inside the plugin directory.
- Kebab-case names for skills, agents, and rules.
- Hook-config JSON validity, **and** that every hook script it names exists and is executable.
- Skill / agent / rule frontmatter: required keys, `name` matching the directory or filename stem, and the unquoted-`': '` YAML trap that silently drops all metadata. **Agents must declare `tools:`, never `allowed-tools:`** — flagged as an error.

Four invariants specific to this plugin, each guarding a drift class this repo is genuinely exposed to:

- **Reference resolution** — every `references/<file>` cited by a skill or agent body exists, and the reference files' own relative links resolve. The bundled `references/` sit at the **plugin root** while a citing skill sits two levels down, so a stale path fails silently at load time and the component improvises rules instead of grounding in them. This is the single most damaging failure mode for a plugin whose value is its cited rules.
- **Markdown links and anchors** — every *relative* link in every `.md`/`.mdc` file resolves, and every `#anchor` it targets matches a heading in the destination (GitHub slug rules, including the `-1` suffix for duplicate headings). Link syntax inside code fences and inline code spans is skipped, because there it is illustrative rather than a link. External links are deliberately **not** fetched — that needs network and would make the validator flaky; see [versioning.md](versioning.md#coupling-to-external-tooling) for the external drift that stays unmonitored. Internal link rot is exactly the defect this plugin tells other repositories to fix, so it is checked here rather than trusted.
- **Tool grants** — two advice-vs-capability checks, both added after this repo shipped the defects they catch. A component whose body prescribes a shell command (a shell-tagged fence, or an inline `vale`/`curl` invocation) must declare `Bash`; otherwise the instruction cannot be followed without a permission prompt its sibling components avoid. And an agent must not declare `Write`/`Edit`, nor describe itself as "read-only" while holding a write-capable tool — `Bash` counts, since `sed -i` and `>` write. Agents here are **report-only**: a contract their bodies keep, not a sandbox that keeps it for them, and the docs must not claim otherwise.
- **Doc sync** — every worker skill and every agent is named both in the `docs-editing` router's body and in `hooks/session-start.sh`. A component that exists but is not routed to is unreachable in practice, and the session-start line is what tells a user it exists.

All four are negative-tested: adding a component without wiring it in, citing a missing reference, writing a dead link or bad anchor, prescribing a shell command without declaring `Bash`, or calling an agent "read-only" while it holds `Bash`, each fails the validator.

## Local triggering tests

Install from your working copy (see [install.md](install.md)), then exercise each component. The most thorough test is to **dogfood the plugin on a real docs repository**.

- **Session-start hook** — open a repo with a `docs/` tree containing Markdown, or an `mkdocs.yml`; one docs-standards line should print. Open a repo with only a `README.md` and confirm it stays **silent**.
- **`prose-lint-on-save` hook** — in a repo with a `.vale.ini`, edit a `.md` file and confirm alerts print and **the file is not rewritten**. Remove the config and confirm the hook goes silent.
- **`docs-editing` router** — ask "should this be a tutorial or a how-to?" or "improve these docs"; it should route and cite, not perform the work itself.
- **`technical-writing`** — ask it to document a real feature. Confirm it reads the code before drafting, picks exactly one document kind, and runs the commands it puts in the doc.
- **`copy-editing`** — hand it a page with a planted unsourced statistic and a planted "simply". Confirm it flags the statistic as a **blocker** and does not merely soften it, and that it establishes the proofread / line-edit / structural contract before editing.
- **`marketing-copy`** — ask for a landing page for something with no published metrics. **Confirm it refuses to invent statistics or testimonials** and offers the mechanism instead. This is the plugin's headline behaviour; test it deliberately.
- **`seo-audit`** — point it at a built site directory and a live URL. Confirm it states which source it audited and what it could not check, and that `--fix` edits the **source**, never the build output.
- **`ai-seo`** — point it at a site with a stale `llms.txt`. Confirm it notices the drift against the nav, and validates any JSON-LD rather than eyeballing it.
- **`/docs-lint-setup`** — run in a repo that already has a `.vale.ini` and confirm it does **not** overwrite it without `--force`. Run in a clean repo and confirm the configs, the vocabulary directory, and the `styles/` gitignore entry all appear.
- **Agents** — dispatch `prose-reviewer` at a page with planted claim violations and `seo-auditor` at a docs tree. Confirm each returns ranked findings with an explicit coverage statement, edits nothing, and dispatches no sub-agents.
- **Cursor rule** — in Cursor, open a file under `docs/` and confirm `docs-editing-context.mdc` attaches.

After editing content, reinstall (or restart the session) to pick up changes.

## The test that matters most

Ask any skill to make a technical page "more compelling" with no source material available. The correct behaviour is to **name what it cannot claim** and offer specificity instead. If it produces a plausible statistic, a testimonial, or "trusted by teams worldwide", that is a defect in the component — not a prompt to be tolerated — and belongs in `references/claims-and-evidence.md` or the skill body as a strengthened rule.
