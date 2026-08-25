# Skill, agent, and rule authoring conventions

The detailed companion to [AGENTS.md](../AGENTS.md) (which is authoritative); this expands on the *how*. The shipped components are the reference examples.

## Naming & layout

- **Components are kebab-case** and namespaced `<plugin>:<component>` (for example `docs-editing:copy-editing`). A component's frontmatter `name` MUST equal its directory (skills) or filename stem (agents); `scripts/validate.py` enforces this.
- `skills/<name>/SKILL.md` (includes user-invoked slash commands) · `agents/<name>.md` · `rules/<name>.mdc`. Shared reference material lives in top-level **`references/`**. The legacy `commands/<name>.md` layout is not used — host validators treat every `commands/**/*.md` as a command and warn on missing frontmatter.
- The router skill is named `docs-editing`, the same as the plugin, so it resolves as `docs-editing:docs-editing`. Worker skills are named for the **task**, not prefixed (`copy-editing`, not `docs-copy-editing`) — they read better as `/copy-editing` and the plugin namespace already disambiguates.

## Skill vs agent vs rule

- **Skill (auto-invoked router)** — `docs-editing`: always-on `description`, routes intent, performs no work itself. Keep its body lean; it is the most frequently loaded component.
- **Skill (worker)** — one task each. All carry `argument-hint` + `allowed-tools`, so each is both auto-invoked on intent and user-invocable as `/<name>`. Bodies are imperative, procedural, and **cite `references/`** rather than restating rules.
- **Agent** — a context-isolated, **report-only** specialist (`prose-reviewer`, `seo-auditor`). Never declare `Write`/`Edit` (the validator rejects it). `Bash` is permitted so an agent can run the linters, but it is write-capable — so write "report-only", never "read-only": the no-edit property is a contract the body keeps, not one the tool grant enforces. Use **`tools:`** (a YAML block list), **never** `allowed-tools:` — in an agent that key is silently ignored and the agent inherits *all* tools. Write the `description` in the **prose-summary** form — conditions + 2–4 named trigger scenarios + a "See *When to invoke* in the agent body" pointer — and put the worked scenarios in a `When to invoke` body section, not an `<example>` block in frontmatter. The body is the agent's **system prompt**: open it in second person ("You are a report-only specialist that…"), then continue imperatively.
- **Cursor rule** — a Cursor-only `.mdc` with `description` / `globs` / `alwaysApply`, mirroring the router. See `rules/docs-editing-context.mdc`.

## The `description` (the trigger)

For skills the `description` is always-on metadata: keep it lean and third person — *what + scope*, then 3–5 representative triggers as **quoted phrases a user would actually type** ("write a README", "tighten this copy", "add llms.txt"), then a short **"Not for …"** anti-trigger disambiguating it from its neighbours. The five worker skills sit close together, so the anti-trigger is what stops the wrong one loading: `technical-writing` vs `copy-editing` is *new* vs *existing*; `seo-audit` vs `ai-seo` is *crawlers* vs *retrieval*; `marketing-copy` vs `technical-writing` is *persuasion* vs *documentation*.

**YAML gotcha:** a `description` value with an unquoted `: ` (colon-space) makes a real YAML parser read it as a nested mapping, so the component loads with *empty* metadata — every field silently dropped. `claude plugin validate` catches this, and `scripts/validate.py` guards against it too. Quote the value, or use a `>` block scalar (as the agents do).

## Body

- **Cite the references; do not re-derive them.** The single source of truth for the rules is `references/`: `claims-and-evidence.md` (the hard rule), `style-guide.md`, `doc-types.md`, `seo-checklist.md`. A skill body states *its procedure* and points at the canonical reference for the rules. This keeps skills lean and the rules in one place — when a rule changes, one file changes.
- **`references/` is plugin-root-relative.** A bare `references/x.md` inside `skills/<name>/SKILL.md` is two levels off, so every component carries the one-line resolution note (`${CLAUDE_PLUGIN_ROOT}/references/…`, `../../references/…`, or Glob). The validator checks that every cited reference exists; it cannot check that a reader resolves the path, which is why the note is mandatory.
- **The repo being worked on outranks this plugin.** Every skill instructs reading the target repo's `AGENTS.md` / style guide / linter config first, and treats a conflict as the repo's win, reported rather than silently overridden.
- **Deterministic beats prose.** Where `vale` enforces a rule, the skill runs the tool and reports its real output. Markdown structure has no shipped enforcer — do not write guidance implying one. A skill must never claim a clean lint it did not run.
- **Verification is part of the skill.** A skill that lands prose runs the linters, checks the links, and runs the commands it wrote into the doc — then reports what it actually did and what it could not check.

## The audience boundary

Components act on **prose written for people**. Agent-instruction files — `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `rules/*.mdc`, `.github/copilot-instructions.md`, and skill or agent definitions — are **read** for a repo's conventions and **never authored or rewritten**.

That genre addresses a model rather than a reader, which inverts rules the style guide treats as load-bearing: repetition is deliberate rather than waste, hard constraints must stay hard, and rigid parallel structure is a feature. A prose editor tuned for human readers degrades such a file while appearing to improve it. Dedicated tooling owns them.

When adding or editing a component, keep the read/write distinction explicit in its body, and make it refuse rather than improvise when asked to write one. The canonical statement is `references/doc-types.md` §3.

## The house rule that outranks style

`references/claims-and-evidence.md` is the plugin's reason to exist. When authoring or editing any component, hold the line that generative copy tooling most reliably crosses: **never originate statistics, testimonials, customer names, awards, urgency, or superlatives**, and never accept a hedge as a repair. A component that produces "trusted by teams worldwide" has a defect, not a prompt problem. Strengthen the rule in `references/` — not only in the skill that slipped.

## Dual-host parity

Skills, agents, and rules are shared by both hosts. The **Cursor** manifest (`.cursor-plugin/plugin.json`) declares each component path; **Claude** discovers the default folders automatically. Keep the two manifests' `name`/`version`/`description`/`author` identical (`scripts/validate.py` checks parity), and keep Cursor hook commands **workspace-relative** (`bash hooks/session-start.sh`), never `${CLAUDE_PLUGIN_ROOT}` (a Claude-Code-only variable).

## Adding a component

The validator enforces the wiring, so work in this order:

1. Create `skills/<name>/SKILL.md` (or `agents/<name>.md`) with frontmatter whose `name` matches.
2. Add it to the **routing table** (or Agents section) in `skills/docs-editing/SKILL.md`.
3. Add it to the announced surface in **`hooks/session-start.sh`**.
4. Update **README.md** (component table), **AGENTS.md**, and **CHANGELOG.md**.
5. Run `./scripts/validate.sh` — steps 2 and 3 fail CI if skipped.

## Before committing

Run `./scripts/validate.sh` and `claude plugin validate .`, then test triggering locally — see [testing.md](testing.md). Include the claims-refusal test from that document; it is the behaviour most worth regression-testing by hand.
