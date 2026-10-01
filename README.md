# Docs Editing Plugin

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-blue)](CHANGELOG.md)
[![Claude Code](https://img.shields.io/badge/Claude_Code-plugin-D97757?logo=anthropic&logoColor=white)](https://docs.claude.com/en/docs/claude-code/overview)
[![Cursor](https://img.shields.io/badge/Cursor-plugin-000?logo=cursor&logoColor=white)](https://cursor.com)
[![Keep a Changelog](https://img.shields.io/badge/Keep%20a%20Changelog-1.1.0-E05735)](CHANGELOG.md)

An AI plugin by **Cadasto B.V.** that teaches AI coding assistants documentation, editing, and content standards: technical writing, copy editing, AI-tell cleanup, marketing copy, SEO, and AI citability. It is for anyone who has an assistant write or edit human-facing docs. It adds eight skills, two report-only review agents, and two hooks (session-start, prose-lint) for **[Claude Code](https://docs.claude.com/en/docs/claude-code/overview)** and **[Cursor](https://cursor.com)** from one shared component set, plus a Cursor rule.

The plugin owns the prose and content layer, and one rule defines it: a claim that cannot be traced to a source does not ship ([how it decides](#how-it-decides)). It reads agent-instruction files (`AGENTS.md`, `CLAUDE.md`, rule files, skill and agent definitions) for a repository's conventions but never writes them. It does not review source code, and it leaves specification, requirement, and traceability authoring to the `sdd` plugin. Domain facts come from the target repository's named ground-truth source, never from the plugin.

**Requirements.** A Claude Code or Cursor host. The plugin is pure Markdown + JSON, with no build step and no MCP server, and the skills apply the standards by judgment with no other tooling installed. To have the prose rules checked by a linter, install [Vale](https://vale.sh) and run `/docs-lint-setup` in your repository; until both are in place, the prose-lint hook stays silent. See [Host toolchain](docs/install.md#host-toolchain-optional-but-recommended) for install options.

## Table of contents

- [Features](#features)
- [Installation](#installation)
- [Components](#components)
- [How it decides](#how-it-decides)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Features

- **Routing**: you describe the prose task; the auto-invoked `docs-editing` router picks the skill for it.
- **Evidence before persuasion**: the skills that write or edit prose refuse to invent a statistic, testimonial, or superlative, and `/copy-editing` and `/marketing-copy` replace one they find with the observable mechanism, per [`references/claims-and-evidence.md`](references/claims-and-evidence.md).
- **Writing and editing**: `/technical-writing` drafts new docs in one document kind, `/copy-editing` tightens existing prose under a stated contract, and `/humanize` removes AI tells.
- **Marketing copy**: `/marketing-copy` writes pitch copy for technical readers without invented metrics or testimonials.
- **Discoverability**: `/seo-audit` audits the published output for search engines; `/ai-seo` covers `llms.txt`, Markdown twins, and JSON-LD.
- **Prose linting**: `/docs-lint-setup` scaffolds Vale with the `ai-tells` style, and the prose-lint hook reports Vale alerts after each Markdown edit without rewriting the file.
- **Review**: the report-only `prose-reviewer` and `seo-auditor` agents return ranked findings from an isolated context.
- **Cursor parity**: Cursor gets the same skills, agents, and hooks, plus `rules/docs-editing-context.mdc` mirroring the router.

## Installation

**Claude Code**, from the Cadasto marketplace:

```text
/plugin marketplace add Cadasto/plugin-marketplace
/plugin install docs-editing@cadasto
```

Or load a local working copy for a single session: `claude --plugin-dir /path/to/docs-editing-plugin`.

**Cursor**: add this repository as a plugin (Settings → Plugins, from a Git URL or a local path). The repo includes a Cursor manifest at [`.cursor-plugin/plugin.json`](.cursor-plugin/plugin.json); skills, agents, references, and hook scripts are shared with the Claude plugin.

See [docs/install.md](docs/install.md) for marketplace, local-development, update, and Cursor install details.

## Components

| Component | Purpose |
|-----------|---------|
| Skill `docs-editing` | Auto-invoked router: sends each prose task to the skill that owns it, and to the canonical rule in `references/`. |
| Skill `/technical-writing` | Drafts new documentation in exactly one document kind. Reads the code before drafting and runs the commands it writes. |
| Skill `/copy-editing` | Tightens existing prose. Settles the proofread, line-edit, or structural contract first, then works from large to small, starting with the claims pass. |
| Skill `/humanize` | Removes AI tells from existing prose: signposting, staged contrasts, inflated significance, chatbot residue, decorative formatting. Restates without adding facts, keeps a human author's em dash where its passage has no other tell, and never judges authorship. |
| Skill `/marketing-copy` | Writes landing, feature, and announcement copy for technical readers, with the anti-fabrication guardrails applied before drafting. |
| Skill `/seo-audit` | Audits the **published** output, technical and on-page: titles, descriptions, headings, canonicals, sitemap, redirects, orphans. |
| Skill `/ai-seo` | Audits and improves citability by AI search: `llms.txt`, Markdown twins, validated JSON-LD, chunk-level self-containment. |
| Skill `/docs-lint-setup` | Scaffolds `.vale.ini`, seeds the vocabulary, and adds the `ai-tells` style. Never overwrites an existing config unprompted. |
| Agent `prose-reviewer` | Report-only review of what linters cannot see: unsourced claims, doc-kind bleed, stale inventories, terminology drift. Returns ranked findings. |
| Agent `seo-auditor` | Report-only discoverability sweep over a docs tree or live site, with a mandatory coverage statement. |
| Session-start hook | Detects a docs or content workspace and prints one standards line plus the skill and agent surface; dual-host. Stays silent in a repo with only a `README.md`. |
| Prose-lint hook | After each Markdown edit, reports `vale` alerts for that file; dual-host. Advisory (it **never rewrites** the file) and opt-in: silent unless the repo carries its own `.vale.ini` (or `_vale.ini`). |
| References | The canonical rules the skills, agents, and Cursor rule cite: [claims and evidence](references/claims-and-evidence.md), [house style](references/style-guide.md), [document kinds](references/doc-types.md), [AI tells](references/ai-tells.md), and the [SEO checklist](references/seo-checklist.md). |
| Lint config `references/vale.ini` | The reference Vale config that `/docs-lint-setup` scaffolds from, with its `vocab-accept.txt` vocabulary seed and the `ai-tells` Vale style. |
| Cursor rule `docs-editing-context.mdc` | Markdown- and docs-scoped guidance mirroring the router for Cursor. |

Neither agent's tool grant includes `Write` or `Edit`, but both include `Bash` for read-only commands (Vale for `prose-reviewer`; builds, greps, and fetches for `seo-auditor`), so report-only is a contract their bodies keep rather than a sandbox that enforces it.

The guidance draws on [Diátaxis](https://diataxis.fr) for document kinds, [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org) for changelogs, [Vale](https://vale.sh) with the `Google`, `write-good`, `alex`, and `proselint` style packages for prose style, the [llms.txt proposal](https://llmstxt.org) for AI citability, and Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) for AI tells.

## How it decides

**The repository being worked on outranks this plugin.** Before writing or editing, the `docs-editing` router (and, on Cursor, the rule) has the assistant read the target repo's `AGENTS.md` or `CLAUDE.md`, its style guide, its linter config, and neighbouring pages. Where those conflict with the plugin, the repo wins, and so does any ground-truth source it names for domain facts.

Below that, three principles apply in priority order:

1. **Evidence before persuasion.** A claim that cannot be traced to a source does not ship, and this outranks every stylistic preference. Generative copy tooling fails in one predictable way: asked to make a page more persuasive, it invents the persuasion (statistics, customer counts, testimonials, awards, urgency). Developers, engineers, and clinicians read an unsourced number as evidence of unseriousness, so the growth-copy move that lifts conversion on a consumer page lowers trust here. The writing and editing skills state the observable mechanism instead:

   > ❌ "Cuts documentation review time by 40%."
   > ✅ "Flags unsourced statistics, doc-kind bleed, and inventories that no longer match the tree."

   Hedging is no repair: "up to", "designed to", and "teams report" keep the claim. The full rule, with the never-invent list, is [`references/claims-and-evidence.md`](references/claims-and-evidence.md).
2. **One document kind per file.** Most bad documentation is a tutorial and a reference merged into one page. `/technical-writing` picks the kind before drafting and writes only that kind; `/copy-editing` and `prose-reviewer` report a page that mixes two. The kinds follow [Diátaxis](https://diataxis.fr), per [`references/doc-types.md`](references/doc-types.md).
3. **Deterministic beats prose.** Where Vale enforces a rule, the writing and editing skills run it rather than reasoning the rule out by hand. Markdown *structure* has no shipped enforcer, so those conventions are a matter of judgment.

The components write **prose for people**: documentation, guides, references, page and marketing copy, changelogs, release notes, site metadata, `llms.txt`. Agent-instruction files stay out of scope because they address a model, not a reader, and the rules for human readers invert for them: repetition is deliberate, hard constraints must stay hard, rigid parallel structure is a feature, and spelling out the failure mode is the point. A prose editor tuned for human readers would quietly degrade them ([`references/doc-types.md` §3](references/doc-types.md#3-not-documentation-agent-instruction-files)).

## Development

The plugin has no build step. Validate locally:

```bash
./scripts/validate.sh        # manifests, parity, frontmatter, references, links, tool grants, doc sync
claude plugin validate .     # manifest + component structure
```

Beyond the checks shared with the sibling Cadasto plugins, the validator enforces four invariants specific to this plugin: reference resolution, Markdown links and anchors, tool grants, and doc sync. The [Validation section of docs/testing.md](docs/testing.md#validation) defines each one and the drift it guards against.

## Documentation

- [docs/install.md](docs/install.md): install on both hosts, and the optional linter toolchain
- [docs/testing.md](docs/testing.md): validate and dogfood
- [docs/versioning.md](docs/versioning.md): SemVer policy and release steps
- [docs/authoring.md](docs/authoring.md): skill, agent, and rule authoring conventions

See [AGENTS.md](AGENTS.md) for contributor conventions.

## License

[MIT](LICENSE)
