#!/usr/bin/env bash
# SessionStart hook (host-agnostic): print one docs-standards context line when a
# documentation or content workspace is detected. Always exits 0 so the assistant reads
# stdout and is never blocked.
set -u

is_docs_workspace() {
  # A generated docs site, or an opted-in prose-linting config.
  for f in mkdocs.yml mkdocs.yaml .vale.ini _vale.ini llms.txt \
           docusaurus.config.js docusaurus.config.ts docusaurus.config.mjs; do
    [ -f "$f" ] && return 0
  done
  # A docs/ or pages/ tree that actually contains Markdown. Bounded so session start
  # stays fast; a bare README.md deliberately does NOT count (it is in every repo).
  # Group the -name tests: `-o` binds loosely, so an ungrouped
  # `-maxdepth 3 -name '*.md' -o -maxdepth 3 -name '*.mdx'` is two expressions and
  # provokes find's "global option after argument" warning.
  for d in docs pages content; do
    if [ -d "$d" ] && find "$d" -maxdepth 3 \( -name '*.md' -o -name '*.mdx' \) 2>/dev/null | grep -q .; then
      return 0
    fi
  done
  return 1
}

if is_docs_workspace; then
  echo "› Docs/content workspace detected — docs-editing standards available. Claims must be traceable to a source (never invent statistics, testimonials or superlatives); pick one document kind per file. Skills: /technical-writing · /copy-editing · /marketing-copy · /seo-audit · /ai-seo · /docs-lint-setup. Agents: prose-reviewer · seo-auditor. Scope is human-facing prose; agent-instruction files (AGENTS.md, CLAUDE.md, rules) are read for conventions, never rewritten. Read the repo's own AGENTS.md/style guide first — it outranks these defaults."
fi

exit 0
