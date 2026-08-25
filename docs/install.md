# Installing the Docs Editing Plugin

> Pure Markdown + JSON — there is no build step and **no MCP server** to wire up.

Distributed for both [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins) (`.claude-plugin/`) and [Cursor](https://cursor.com/docs/plugins) (`.cursor-plugin/`). Skill, agent, and reference content is shared; only the manifest and hook layer differ.

## Claude Code

### Install (from the Cadasto marketplace)

```
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install docs-editing@cadasto
```

The marketplace name is `cadasto`, so the plugin is addressed as `docs-editing@cadasto`.

### Install (local working copy, for development)

```bash
claude plugin add /path/to/docs-editing-plugin
```

### Inspect / update

```bash
claude plugin validate .                # manifest + component structure
claude plugin details docs-editing      # component inventory + projected token cost
```

```
/plugin marketplace update cadasto
/plugin update docs-editing
```

A session restart is required for an update to take effect.

## Cursor

Add this repository as a plugin (Cursor **Settings → Plugins**, via Git URL or local path). The repo root contains `.cursor-plugin/plugin.json`, which declares the `skills`, `agents`, `rules`, and `hooks` paths. After changing content locally, reload or reinstall the plugin so Cursor picks it up.

> The Cursor hook wiring targets the `sessionStart` and `afterFileEdit` events. If your Cursor version exposes a different post-edit event or payload shape, adjust `hooks/cursor-hooks.json` and the path-extraction in `hooks/prose-lint-on-save.sh` accordingly.

## Host toolchain (optional but recommended)

The plugin installs and its skills work with no tooling at all. Two prose linters make the mechanical half of the house style machine-enforced rather than a reviewer's problem:

| Tool | Owns | Install |
|---|---|---|
| **[Vale](https://vale.sh)** | Prose style — voice, hedges, weasel words, condescension, terminology | `brew install vale`, `go install github.com/errata-ai/vale/v3/cmd/vale@latest`, or a release binary |
| **[markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2)** | Markdown structure — headings, fences, whitespace, link form | `npm install -g markdownlint-cli2` |

Run `/docs-lint-setup` in a repository to scaffold `.vale.ini` and `.markdownlint.jsonc` from the plugin's reference configs, seed the Vale vocabulary, and gitignore the downloaded style packages. Then:

```bash
vale sync     # download the style packages named in .vale.ini
vale .
markdownlint-cli2 "**/*.md"
```

Without either tool the skills still apply the standards by judgment, and the save hook stays silent.

`ai-seo` and `seo-audit` audit the **published** output, so they use `WebFetch` (or `curl`) against a deployed URL, or read a built output directory. Neither needs a network connection to give source-level findings, but both will label such findings as unverified against the published output.

## Hooks

Two host-agnostic hooks ship (Claude `hooks/hooks.json`, Cursor `hooks/cursor-hooks.json`):

- **`session-start.sh`** — on session start, detects a docs/content workspace (a generated-site config, a prose-linter config, or a `docs/`, `pages/`, or `content/` tree containing Markdown) and prints one context line plus the available skill and agent surface. A bare `README.md` deliberately does not count, or the hook would fire in every repository.
- **`prose-lint-on-save.sh`** — after an edit to a `.md`, `.mdx`, or `.markdown` file (Claude `PostToolUse` on `Write`/`Edit`; Cursor `afterFileEdit`), runs `vale` and `markdownlint` on that one file and prints the alerts.

  It is **advisory and never rewrites the file** — prose is not mechanically formattable the way source code is, so an auto-fixing save hook would silently edit an author's voice. It is also **opt-in**: it runs only when the repository carries its own `.vale.ini` or `.markdownlint*`, so it stays silent in a repo that has not asked for prose linting. Output is capped so it cannot flood the context window. It always exits 0 and can never block an edit.
