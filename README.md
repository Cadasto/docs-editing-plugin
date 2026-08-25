# Docs Editing Plugin

An AI plugin by **Cadasto B.V.** that teaches AI coding assistants **documentation, editing, and content standards** — technical writing, copy editing, marketing copy, SEO, and AI citability — through skills, two report-only review agents, session-start and prose-lint hooks, and a Cursor rule. It targets **both Claude Code and Cursor** from a single shared component set.

Pure Markdown + JSON. No build step and **no MCP server** to wire up.

## The rule that defines it

> **A claim that cannot be traced to a source does not ship.**

Generative copy tooling fails in one predictable way: asked to make a page more persuasive, it invents the persuasion — statistics, customer counts, testimonials, awards, urgency. Those are the conventional ingredients of landing-page copy, which is exactly why they get fabricated.

For a technical audience they also backfire. Developers, engineers, and clinicians read an unsourced number as evidence of unseriousness, so the growth-copy move that lifts conversion on a consumer page lowers trust here. Every skill in this plugin substitutes the same thing instead — the **observable mechanism**:

> ❌ "Cuts documentation review time by 40%."
> ✅ "Flags unsourced statistics, doc-kind bleed, and inventories that no longer match the tree."

Specific, checkable, and more convincing to this reader than a number they will assume was invented. Hedging is not an escape hatch: "up to", "designed to", and "teams report" preserve the violation. The full rule, including the never-invent list and the repair pattern, is [`references/claims-and-evidence.md`](references/claims-and-evidence.md).

## Install

**Claude Code** — from the Cadasto marketplace:

```
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install docs-editing@cadasto
```

Or from a local working copy: `claude plugin add /path/to/docs-editing-plugin`.

**Cursor**: add this repository as a plugin (Settings → Plugins). See [`docs/install.md`](docs/install.md) for both hosts.

**Prerequisites** — none. The skills apply the standards by judgment with no tooling installed. To make the mechanical half machine-enforced, install [Vale](https://vale.sh) and [markdownlint-cli2](https://github.com/DavidAnson/markdownlint-cli2) and run `/docs-lint-setup` in your repo; see [Host toolchain](docs/install.md#host-toolchain-optional-but-recommended).

## Component surface

| Component | Status | Purpose |
|-----------|--------|---------|
| Skill `docs-editing` | shipped | Auto-invoked router: sends each prose task to the skill that owns it, and to the canonical rule in `references/`. |
| Skill `/technical-writing` | shipped | Author new documentation — picks exactly one document kind, reads the code before drafting, runs the commands it writes. |
| Skill `/copy-editing` | shipped | Tighten existing prose. Establishes the proofread / line-edit / structural contract first, then works large-to-small; claims pass runs first. |
| Skill `/marketing-copy` | shipped | Landing, feature, and announcement copy for technical audiences, with the anti-fabrication guardrails applied before drafting. |
| Skill `/seo-audit` | shipped | Technical and on-page audit of the **published** output — titles, descriptions, headings, canonicals, sitemap, redirects, orphans. |
| Skill `/ai-seo` | shipped | Citability by AI search — `llms.txt`, Markdown twins, validated JSON-LD, chunk-level self-containment. |
| Skill `/docs-lint-setup` | shipped | Scaffold `.vale.ini` + `.markdownlint.jsonc` into a repo; never overwrites an existing config unprompted. |
| Agent `prose-reviewer` | shipped | Report-only prose review for what linters cannot see: unsourced claims, doc-kind bleed, stale inventories, terminology drift. Ranked findings. |
| Agent `seo-auditor` | shipped | Report-only discoverability sweep over a docs tree or live site, with a mandatory coverage statement. |
| Session-start hook | shipped | Detects a docs/content workspace and prints one standards line plus the surface; dual-host. Silent in a repo with only a `README.md`. |
| Prose-lint hook | shipped | After each `.md` edit, reports `vale` + `markdownlint` alerts. Advisory — **never rewrites** — and opt-in: silent unless the repo carries its own linter config. |
| References | shipped | The canonical rules, cited by every component: [claims and evidence](references/claims-and-evidence.md), [house style](references/style-guide.md), [document kinds](references/doc-types.md), [SEO checklist](references/seo-checklist.md), plus reference `vale.ini` and `markdownlint.jsonc`. |
| Cursor rule `docs-editing-context.mdc` | shipped | Markdown- and docs-scoped guidance mirroring the router for Cursor. |

## What it covers

**Prose written for people** — documentation, guides, references, page and marketing copy, changelogs, release notes, site metadata, `llms.txt`.

**Not agent-instruction files.** `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, rule files, and skill or agent definitions are **read** for a repo's conventions and never authored or rewritten by these components. They address a model rather than a reader, which inverts several of the rules here — repetition becomes deliberate, hard constraints must stay hard, rigid parallel structure becomes a feature. A prose editor tuned for human readers quietly degrades them, so that genre belongs to tooling built for it. Also out of scope: source-code review, and specification/traceability authoring.

## How it decides

Three principles, in priority order:

1. **Evidence before persuasion** — the rule above. It outranks every stylistic preference.
2. **One document kind per file** — most bad documentation is a tutorial and a reference merged into one page. Decide the kind first ([Diátaxis](https://diataxis.fr)-based; see [`references/doc-types.md`](references/doc-types.md)), then write only that kind.
3. **Deterministic beats prose** — whatever `vale` or `markdownlint` enforces, run the tool rather than reasoning it out by hand.

And one constraint above all three: **the repository being worked on outranks this plugin.** Every skill reads the target repo's `AGENTS.md`, style guide, and linter config first, and reports a conflict rather than silently overriding it — including any named ground-truth source for domain facts.

## Development

No build step — the plugin is pure Markdown + JSON. Validate locally:

```bash
./scripts/validate.sh        # manifests, dual-host parity, frontmatter, reference citations, doc sync
claude plugin validate .     # manifest + component structure
```

Beyond the shared checks, the validator enforces two invariants specific to this plugin: every `references/<file>` a component cites must exist (the bundled references sit at the plugin root, so a stale path fails silently at load time), and every skill and agent must be wired into both the router and the session-start surface. See [`docs/testing.md`](docs/testing.md) for the full validation story and [`AGENTS.md`](AGENTS.md) for contributor conventions.

## Documentation

- [docs/install.md](docs/install.md) — install on both hosts, and the optional linter toolchain
- [docs/testing.md](docs/testing.md) — validate and dogfood
- [docs/versioning.md](docs/versioning.md) — SemVer + release steps
- [docs/authoring.md](docs/authoring.md) — skill / agent / rule authoring conventions

## License

[MIT](LICENSE) © 2026 Cadasto B.V.
