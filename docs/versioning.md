# Versioning and releases

This plugin uses [Semantic Versioning](https://semver.org), adapted to skill / agent / rule / reference content:

| Bump | When |
|------|------|
| **Major** | A skill/agent/rule is removed or renamed, or its behaviour/scope changes incompatibly; a rule in `references/` changes in a way that invalidates existing usage |
| **Minor** | A new component is added, or an existing one's coverage meaningfully expands |
| **Patch** | Typos, clarifications, reference/source fixes — no behaviour change |

While on the `0.x` line, treat the plugin as pre-stable: a breaking change may still ship in a minor bump.

## Release steps

1. Bump `version` in **both** manifests (they must agree): `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`. Keep `description` and `author` identical across both — `scripts/validate.py` enforces this parity.
2. Run `./scripts/validate.sh` and `claude plugin validate .`.
3. **Dogfood:** load a working copy (`claude --plugin-dir /path/to/docs-editing-plugin`) and exercise the components on a real docs repository on **both** hosts — see [testing.md](testing.md). Include the claims-refusal test.
4. Fold the accumulated `## [Unreleased]` notes into a dated `## [X.Y.Z] - YYYY-MM-DD` section in [CHANGELOG.md](../CHANGELOG.md) (Keep a Changelog — groups in order Added, Changed, Deprecated, Removed, Fixed, Security; see [AGENTS.md](../AGENTS.md#changelog-style)).
5. Sync the docs surface (AGENTS.md, README.md) with what shipped. The router body and `hooks/session-start.sh` are checked mechanically by the validator, so a missed component fails CI rather than shipping quietly.
6. Commit (`chore(release): vX.Y.Z`) and tag: `git tag -a vX.Y.Z -m "docs-editing-plugin vX.Y.Z"`.
7. Push commits and the tag: `git push origin main --follow-tags`.
8. **Update the marketplace entry** — the release is not live until this lands. See below.

## Coupling to external tooling

The reference linter config (`references/vale.ini`) pins no tool version, but it does name **style packages** (`Google`, `write-good`, `alex`, `proselint`) whose rule sets change upstream. When a package renames or removes a rule the config disables or escalates, the config breaks **silently**: an unknown rule name produces no warning at all — empty stderr, exit 0 — so the escalation or suppression quietly stops applying. An unknown *style package* is the opposite, failing loudly with `E100 [loadStyles]` and exit 2, so a broken `Packages =` line is caught for you and a broken rule line is not. Re-check the named rules by hand when bumping a package, and treat a rule rename as a **patch** fix. (Verified against Vale 3.18.0.)

## No MCP coupling

This plugin has **no companion MCP server**, so there is no server-compatibility version to align.

## Marketplace

Public install is via the [Cadasto marketplace](https://github.com/Cadasto/plugin-marketplace) as `docs-editing@cadasto`. The catalog **pins every entry to a release tag**, so tagging and pushing a release here does not ship it — users see nothing until the marketplace entry moves.

After step 7, update the entry in `Cadasto/plugin-marketplace`:

1. Bump that entry's `version` to `X.Y.Z` and `source.ref` to `vX.Y.Z` together (validation there rejects a mismatch).
2. Bump the catalog's own `metadata.version` — a plugin minor/major is a catalog **minor**, a plugin patch is a catalog **patch**.
3. Add a dated `## [X.Y.Z] - YYYY-MM-DD` section in the catalog `CHANGELOG.md`, then run `python3 scripts/validate.py --fix`.

See the catalog's [docs/versioning.md](https://github.com/Cadasto/plugin-marketplace/blob/main/docs/versioning.md).

The catalog copies `description`, `version`, and `keywords` verbatim from `.claude-plugin/plugin.json`. Fix those in this repo and copy them into the catalog when the next release is pinned.
