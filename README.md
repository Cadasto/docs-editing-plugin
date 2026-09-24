# Docs Editing Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://claude.ai/code)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

An AI plugin by **Cadasto B.V.** that teaches AI coding assistants documentation, editing, and content standards: technical writing, copy editing, AI-tell cleanup, marketing copy, SEO, and AI citability. It is for anyone who has an assistant write or edit human-facing docs. It adds eight skills, two report-only review agents, a session-start hook, a prose-lint hook, and a Cursor rule, shared by **Claude Code** and **Cursor** from one component set.

The plugin owns the prose and content layer, and one rule defines it: a claim that cannot be traced to a source does not ship ([why](#the-rule-that-defines-it)). It reads agent-instruction files (`AGENTS.md`, `CLAUDE.md`, rule files, skill and agent definitions) for a repository's conventions but never writes them. It does not review source code, and it leaves specification, requirement, and traceability authoring to the `sdd` plugin. Domain facts come from the target repository's named ground-truth source, never from the plugin.

**Requirements.** A Claude Code or Cursor host; nothing else. The skills apply the standards by judgment with no tooling installed. To make the prose rules machine-enforced, install [Vale](https://vale.sh) and run `/docs-lint-setup` in your repository; see [Host toolchain](docs/install.md#host-toolchain-optional-but-recommended). Without Vale the prose-lint hook stays silent. The plugin is pure Markdown + JSON, with no build step and no MCP server.

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Components](#components)
- [The rule that defines it](#the-rule-that-defines-it)
- [How it decides](#how-it-decides)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Features

- **Evidence before persuasion**: every skill replaces an invented statistic, testimonial, or superlative with the observable mechanism, per [`references/claims-and-evidence.md`](references/claims-and-evidence.md).
- **Writing and editing**: `/technical-writing` drafts new docs in one document kind, `/copy-editing` tightens existing prose under a stated contract, and `/humanize` removes AI tells.
- **Marketing copy**: `/marketing-copy` writes landing, feature, and announcement copy for technical readers, with the anti-fabrication guardrails applied before drafting.
- **Discoverability**: `/seo-audit` audits the published output for search engines; `/ai-seo` covers `llms.txt`, Markdown twins, and JSON-LD.
- **Prose linting**: `/docs-lint-setup` scaffolds Vale with the `ai-tells` style, and the prose-lint hook reports Vale alerts after each Markdown edit without rewriting the file.
- **Independent review**: the report-only `prose-reviewer` and `seo-auditor` agents return ranked findings in an isolated context.

## Installation

**Claude Code**, from the Cadasto marketplace:

```text
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install docs-editing@cadasto
```

Or load a local working copy for a single session: `claude --plugin-dir /path/to/docs-editing-plugin`.

**Cursor**: add this repository through Cursor's plugin flow (Settings → Plugins), from a Git URL or a local path. The repository includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, agents, and references are shared with the Claude plugin.

See [docs/install.md](docs/install.md) for marketplace, local-development, update, and Cursor install details.

## Components

| Component | Status | Purpose |
|-----------|--------|---------|
| Skill `docs-editing` | shipped | Auto-invoked router: sends each prose task to the skill that owns it, and to the canonical rule in `references/`. |
| Skill `/technical-writing` | shipped | Author new documentation: picks exactly one document kind, reads the code before drafting, runs the commands it writes. |
| Skill `/copy-editing` | shipped | Tighten existing prose. Establishes the proofread / line-edit / structural contract first, then works large-to-small; claims pass runs first. |
| Skill `/humanize` | shipped | Remove AI tells from existing prose: signposting, staged contrasts, inflated significance, chatbot residue, decorative formatting. Restates without adding facts, keeps a human author's em dashes, and never judges authorship. |
| Skill `/marketing-copy` | shipped | Landing, feature, and announcement copy for technical audiences, with the anti-fabrication guardrails applied before drafting. |
| Skill `/seo-audit` | shipped | Technical and on-page audit of the **published** output: titles, descriptions, headings, canonicals, sitemap, redirects, orphans. |
| Skill `/ai-seo` | shipped | Citability by AI search: `llms.txt`, Markdown twins, validated JSON-LD, chunk-level self-containment. |
| Skill `/docs-lint-setup` | shipped | Scaffold `.vale.ini`, seed the vocabulary and add the `ai-tells` style; never overwrites an existing config unprompted. |
| Agent `prose-reviewer` | shipped | Report-only prose review for what linters cannot see: unsourced claims, doc-kind bleed, stale inventories, terminology drift. Ranked findings. |
| Agent `seo-auditor` | shipped | Report-only discoverability sweep over a docs tree or live site, with a mandatory coverage statement. |
| Session-start hook | shipped | Detects a docs/content workspace and prints one standards line plus the surface; dual-host. Silent in a repo with only a `README.md`. |
| Prose-lint hook | shipped | After each `.md` edit, reports `vale` alerts. Advisory (**never rewrites**) and opt-in: silent unless the repo carries its own `.vale.ini`. |
| References | shipped | The canonical rules, cited by every component: [claims and evidence](references/claims-and-evidence.md), [house style](references/style-guide.md), [document kinds](references/doc-types.md), [AI tells](references/ai-tells.md), [SEO checklist](references/seo-checklist.md), plus the reference `vale.ini`, its `vocab-accept.txt` seed and the `ai-tells` Vale style. |
| Cursor rule `docs-editing-context.mdc` | shipped | Markdown- and docs-scoped guidance mirroring the router for Cursor. |

## The rule that defines it

> **A claim that cannot be traced to a source does not ship.**

Generative copy tooling fails in one predictable way: asked to make a page more persuasive, it invents the persuasion (statistics, customer counts, testimonials, awards, urgency). Those are the conventional ingredients of landing-page copy, which is why they get fabricated.

For a technical audience they also backfire. Developers, engineers, and clinicians read an unsourced number as evidence of unseriousness, so the growth-copy move that lifts conversion on a consumer page lowers trust here. Every skill in this plugin substitutes the **observable mechanism** instead:

> ❌ "Cuts documentation review time by 40%."
> ✅ "Flags unsourced statistics, doc-kind bleed, and inventories that no longer match the tree."

The mechanism is specific and checkable, and it convinces this reader more than a number they assume was invented. Hedging is no escape: "up to", "designed to", and "teams report" preserve the violation. The full rule, including the never-invent list and the repair pattern, is [`references/claims-and-evidence.md`](references/claims-and-evidence.md).

## How it decides

One constraint comes first: **the repository being worked on outranks this plugin.** Every skill reads the target repo's `AGENTS.md`, style guide, and linter config first, and reports a conflict rather than silently overriding it, including any named ground-truth source for domain facts.

Within that constraint, three principles apply in priority order:

1. **Evidence before persuasion**: [the rule that defines it](#the-rule-that-defines-it). It outranks every stylistic preference.
2. **One document kind per file**: most bad documentation is a tutorial and a reference merged into one page. Decide the kind first ([Diátaxis](https://diataxis.fr)-based; see [`references/doc-types.md`](references/doc-types.md)), then write only that kind.
3. **Deterministic beats prose**: whatever `vale` enforces, run the tool rather than reasoning it out by hand. Markdown *structure* has no shipped enforcer; those conventions are applied by judgment.

The components write **prose for people**: documentation, guides, references, page and marketing copy, changelogs, release notes, site metadata, `llms.txt`. Agent-instruction files address a model rather than a reader, which inverts three of the rules here: repetition becomes deliberate, hard constraints must stay hard, and rigid parallel structure becomes a feature. A prose editor tuned for human readers quietly degrades them, so that genre belongs to tooling built for it.

## Development

No build step: the plugin is pure Markdown + JSON. Validate locally:

```bash
./scripts/validate.sh        # manifests, parity, frontmatter, references, links, tool grants, doc sync
claude plugin validate .     # manifest + component structure
```

Beyond the checks shared with the sibling Cadasto plugins, the validator enforces four invariants specific to this plugin: reference resolution, Markdown links and anchors, tool grants, and doc sync. The [Validation section of docs/testing.md](docs/testing.md#validation) defines each one and the drift it guards against. See [`AGENTS.md`](AGENTS.md) for contributor conventions.

## Documentation

- [docs/install.md](docs/install.md): install on both hosts, and the optional linter toolchain
- [docs/testing.md](docs/testing.md): validate and dogfood
- [docs/versioning.md](docs/versioning.md): SemVer and release steps
- [docs/authoring.md](docs/authoring.md): skill, agent, and rule authoring conventions

## License

[MIT](LICENSE)
