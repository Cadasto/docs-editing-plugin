#!/usr/bin/env bash
# PostToolUse / afterFileEdit hook (host-agnostic): lint the just-edited Markdown file.
#
# Advisory only — it REPORTS, it never rewrites. Prose is not mechanically formattable the
# way source code is, so an auto-fixing save hook would silently edit an author's voice.
# Findings go to stdout, which the assistant reads.
#
# Deliberately opt-in: runs only when the repo carries its own linter config (.vale.ini or
# .markdownlint*), so the hook is silent in a repo that has not asked for prose linting.
# Scaffold those configs with /docs-lint-setup. Silent no-op when the tool is not installed,
# and ALWAYS exits 0 so it can never block an edit.
#
# File-path resolution, in order:
#   1. $CLAUDE_FILE_PATH          — set by Claude Code for Write/Edit hooks (fast path).
#   2. tool payload JSON on stdin — Claude (`tool_input.file_path`) or Cursor
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
[ -f "$f" ] || exit 0                                    # path not resolvable from here — skip

out=""

# Vale: prose style. Only when the repo opted in with its own config.
if [ -f .vale.ini ] || [ -f _vale.ini ]; then
  if command -v vale >/dev/null 2>&1; then
    v="$(vale --output=line "$f" 2>/dev/null | head -n "$MAX_LINES")" || true
    [ -n "$v" ] && out="${out}${v}"$'\n'
  fi
fi

# markdownlint: structure. Same opt-in rule.
# Test each candidate individually: `ls a b c` exits non-zero when ANY operand is
# missing, so a combined `ls` would report "no config" whenever one variant was absent
# -- i.e. almost always -- silently disabling this half of the hook.
has_markdownlint_config=0
for c in .markdownlint.json .markdownlint.jsonc .markdownlint.yaml .markdownlint.yml \
         .markdownlint-cli2.jsonc .markdownlint-cli2.yaml .markdownlint-cli2.json; do
  if [ -f "$c" ]; then
    has_markdownlint_config=1
    break
  fi
done

if [ "$has_markdownlint_config" -eq 1 ]; then
  ml=""
  if command -v markdownlint-cli2 >/dev/null 2>&1; then
    ml="$(markdownlint-cli2 "$f" 2>&1 | grep -E '^\S+:[0-9]+' | head -n "$MAX_LINES")" || true
  elif command -v markdownlint >/dev/null 2>&1; then
    ml="$(markdownlint "$f" 2>&1 | head -n "$MAX_LINES")" || true
  fi
  [ -n "$ml" ] && out="${out}${ml}"$'\n'
fi

if [ -n "${out//[$'\n't ]/}" ]; then
  echo "› prose lint — $f"
  printf '%s' "$out"
  echo "  (advisory; nothing was rewritten. Style rules: docs-editing references/style-guide.md)"
fi

exit 0
