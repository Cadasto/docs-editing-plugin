## Summary

<!-- What does this PR change, and why? -->

## Checklist

- [ ] `./scripts/validate.sh` passes (or `claude plugin validate .` if Python is unavailable)
- [ ] `claude plugin validate .` passes
- [ ] Skill / agent triggering tested locally (see [docs/testing.md](../docs/testing.md))
- [ ] Cursor install tested locally when manifest, rule, or hook content changed (see [docs/install.md](../docs/install.md#cursor))
- [ ] Both manifests kept in sync when metadata changed: `.claude-plugin/plugin.json` and `.cursor-plugin/plugin.json`
- [ ] Rules cite `references/` rather than restating them; no rule duplicated across components
- [ ] **No unsourced claim added** — no invented statistics, testimonials, customer names, awards, urgency, or superlatives, in the components or in this repo's own docs (`references/claims-and-evidence.md`)
- [ ] Inventories and counts in README/AGENTS.md verified against the tree
- [ ] New or renamed component wired into the router **and** `hooks/session-start.sh` (the validator enforces this)
- [ ] Version bumped and [CHANGELOG.md](../CHANGELOG.md) updated (if component content changed) — see [docs/versioning.md](../docs/versioning.md)
