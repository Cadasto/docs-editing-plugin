#!/usr/bin/env bash
# PostToolUse / afterFileEdit hook (host-agnostic): lint the just-edited Markdown file.
#
# Advisory only -- it REPORTS, it never rewrites. Prose is not mechanically formattable the
# way source code is, so an auto-fixing save hook would silently edit an author's voice.
# Findings go to stdout, which the assistant reads.
#
# Deliberately opt-in: runs only when the repo carries its own Vale config (.vale.ini or
# _vale.ini), so the hook is silent in a repo that has not asked for prose linting. Scaffold
# it with /docs-lint-setup. Silent no-op when Vale is not installed, and ALWAYS exits 0 so it
# can never block an edit.
#
# Vale checks prose, not Markdown structure; this plugin ships no structural linter.
#
# File-path resolution, in order:
#   1. $CLAUDE_FILE_PATH          -- set by Claude Code for Write/Edit hooks (fast path).
#   2. tool payload JSON on stdin -- Claude (`tool_input.file_path`) or Cursor
#      `afterFileEdit` (`file_path`). Extracted without a jq/python dependency.
set -u

MAX_LINES=15   # keep the hook's contribution to the context window bounded

f="${CLAUDE_FILE_PATH:-}"

# Fall back to the JSON the host pipes in on stdin (Cursor; newer Claude payloads).
# Guard on a non-tty stdin so a manual run without a pipe doesn't block on `cat`.
if [ -z "$f" ] && [ ! -t 0 ]; then
  payload="$(cat)"
  f="$(printf '%s' "$payload" \
        | grep -oE '"file_?[Pp]ath"[[:space:]]*:[[:space:]]*"[^"]+"' \
        | head -n1 \
        | sed -E 's/.*"([^"]+)"$/\1/')"
fi

[ -n "$f" ] || exit 0                                   # nothing to lint
case "$f" in *.md|*.mdx|*.markdown) ;; *) exit 0 ;; esac # Markdown only
[ -f "$f" ] || exit 0                                    # path not resolvable from here -- skip

# Opt-in: the repo must ship its own Vale config.
{ [ -f .vale.ini ] || [ -f _vale.ini ]; } || exit 0
command -v vale >/dev/null 2>&1 || exit 0

out="$(vale --output=line "$f" 2>/dev/null | head -n "$MAX_LINES")" || true

if [ -n "${out//[$'\n't ]/}" ]; then
  echo "› prose lint — $f"
  printf '%s\n' "$out"
  echo "  (advisory; nothing was rewritten. Style rules: docs-editing references/style-guide.md)"
fi

exit 0
