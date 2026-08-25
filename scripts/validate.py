#!/usr/bin/env python3
"""Validate this plugin's manifests, component frontmatter, and doc-sync invariants.

This is a single-plugin repository (the plugin lives at the repo root), supporting both
Claude Code (``.claude-plugin/plugin.json``) and Cursor (``.cursor-plugin/plugin.json``).

Generic checks:
  * both manifests parse as JSON and carry the required fields;
  * dual-host parity (name/version/description/author agree across manifests);
  * every component path declared in a manifest exists inside the plugin dir;
  * kebab-case directory/file names for skills, agents, commands, and rules;
  * hook-config JSON validity, and that every hook script it names exists and is executable;
  * SKILL.md / agent / command frontmatter -- required keys, and ``name`` matching the
    directory/filename. Agents MUST declare ``tools:`` (never ``allowed-tools:``, which
    Claude Code silently ignores so the agent inherits *all* tools -- flagged as an error).

Plugin-specific invariants (the drift classes this repo is actually exposed to):
  * REFERENCE RESOLUTION -- every ``references/<file>`` cited by a skill or agent body
    exists. The bundled ``references/`` sits at the plugin root, but a reader resolves a
    bare ``references/x.md`` inside ``skills/<name>/SKILL.md`` relative to the *skill*
    directory, so a typo or a moved file fails silently at load time and the agent
    improvises rules instead of grounding in them.
  * MARKDOWN LINKS -- every *relative* link in every ``.md``/``.mdc`` file resolves, and
    every ``#anchor`` it targets exists as a heading in the destination. Internal link rot
    is the failure this plugin tells other repos to fix, so leaving it unchecked here would
    be embarrassing as well as wrong. External (http/https/mailto) links are deliberately
    NOT fetched -- that needs network and would make the validator flaky.
  * DOC SYNC -- every worker skill and every agent is named in the ``docs-editing`` router's
    body AND in ``hooks/session-start.sh``. Adding a skill without wiring it into the router
    and the session-start surface is the drift this repo will hit first, and nothing else
    catches it.

This plugin has no MCP backend, so there is intentionally no ``.mcp.json`` check.

Dependency-free (stdlib only) so the ``scripts/validate.sh`` soft-skip is the *only*
reason it wouldn't run. Usage: python3 scripts/validate.py   (from the repo root)
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
errors = []

PLUGIN_NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
# Component-path fields a manifest may declare (Cursor lists them explicitly). No
# `mcpServers` -- this plugin bundles no MCP server.
MANIFEST_PATH_FIELDS = ("logo", "rules", "skills", "agents", "commands", "hooks")
# Fields that must agree across the Claude and Cursor manifests.
SYNCED_FIELDS = ("name", "version", "description", "author")
# The always-on router skill: it must name every other component.
ROUTER_SKILL = "docs-editing"


def err(msg):
    errors.append(msg)


def load_json(path: Path, label: str):
    try:
        return json.loads(path.read_text())
    except Exception as e:
        err(f"{path.relative_to(ROOT)}: cannot parse JSON ({label}): {e}")
        return None


def check_kebab(name: str, label: str):
    if not KEBAB_RE.match(name):
        err(f"{label}: name '{name}' is not kebab-case")


def check_frontmatter_scalars(front: str, rel: str):
    """Stdlib-only guard for the most common frontmatter YAML breakage: an unquoted scalar
    value containing a ': ' (colon-space) or ' #', which a real YAML parser reads as a nested
    mapping / comment -- so at runtime the component loads with EMPTY metadata (every field
    silently dropped). This is NOT a full YAML parser (`claude plugin validate` does that); it
    exists because CI runs only this Python validator, so this class of error must fail here too."""
    in_block = False
    for line in front.splitlines():
        # A block scalar (`description: >`) carries its value on following indented lines,
        # which are prose and legitimately contain ': '. Skip them.
        if in_block:
            if line.startswith((" ", "\t")) or not line.strip():
                continue
            in_block = False
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if not m:
            continue
        value = m.group(2).strip()
        if value in (">", "|", ">-", "|-", ">+", "|+"):
            in_block = True
            continue
        if not value:
            continue
        if value[:1] in ('"', "'", "[", "{", "&", "*", "#"):
            continue  # quoted or structured -- trust the author / real parser
        if ": " in value:
            err(f"{rel}: frontmatter '{m.group(1)}' has an unquoted ': ' in its value -- "
                f"quote the value or YAML parses it as a nested mapping (metadata silently dropped)")
        if " #" in value:
            err(f"{rel}: frontmatter '{m.group(1)}' has an unquoted ' #' in its value -- quote the value")


def split_frontmatter(text: str):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None, text
    return m.group(1), text[m.end():]


def validate_skills():
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        return
    for skill_dir in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        check_kebab(skill_dir.name, f"skills/{skill_dir.name}")
        skill_md = skill_dir / "SKILL.md"
        rel = skill_md.relative_to(ROOT)
        if not skill_md.is_file():
            err(f"{rel}: missing SKILL.md")
            continue
        front, _ = split_frontmatter(skill_md.read_text())
        if front is None:
            err(f"{rel}: missing YAML frontmatter")
            continue
        check_frontmatter_scalars(front, str(rel))
        for field in ("name", "description"):
            if not re.search(rf"^{field}:", front, re.MULTILINE):
                err(f"{rel}: frontmatter missing '{field}'")
        fm_name = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
        if fm_name and fm_name.group(1) != skill_dir.name:
            err(f"{rel}: frontmatter name '{fm_name.group(1)}' != directory '{skill_dir.name}'")


def validate_md_components(subdir: str, *, require_name: bool, is_agent: bool = False):
    """Validate flat .md components (agents/, commands/): kebab-case filename, frontmatter
    present with the required fields, and any `name` matching the filename stem. Non-recursive,
    so nested material is intentionally skipped (shared reference material lives in top-level
    references/). Agents are additionally checked for the `allowed-tools:` foot-gun."""
    comp_dir = ROOT / subdir
    if not comp_dir.is_dir():
        return
    for md in sorted(comp_dir.glob("*.md")):
        rel = md.relative_to(ROOT)
        check_kebab(md.stem, str(rel))
        front, _ = split_frontmatter(md.read_text())
        if front is None:
            err(f"{rel}: missing YAML frontmatter")
            continue
        check_frontmatter_scalars(front, str(rel))
        for field in (("name", "description") if require_name else ("description",)):
            if not re.search(rf"^{field}:", front, re.MULTILINE):
                err(f"{rel}: frontmatter missing '{field}'")
        fm_name = re.search(r"^name:\s*(\S+)", front, re.MULTILINE)
        if fm_name and fm_name.group(1) != md.stem:
            err(f"{rel}: frontmatter name '{fm_name.group(1)}' != filename '{md.stem}'")
        if is_agent:
            if re.search(r"^allowed-tools:", front, re.MULTILINE):
                err(f"{rel}: agents must declare 'tools:' not 'allowed-tools:' "
                    f"('allowed-tools:' is silently ignored, so the agent inherits ALL tools)")
            if not re.search(r"^tools:", front, re.MULTILINE):
                err(f"{rel}: agent frontmatter missing 'tools:' (the agent would inherit ALL tools)")


def validate_rules():
    """Cursor rule files (rules/*.mdc): kebab-case filename plus a `description` in
    frontmatter. Rules carry their own frontmatter contract (description/alwaysApply/globs)."""
    rules_dir = ROOT / "rules"
    if not rules_dir.is_dir():
        return
    for rule in sorted(rules_dir.glob("*.mdc")):
        rel = rule.relative_to(ROOT)
        check_kebab(rule.stem, str(rel))
        front, _ = split_frontmatter(rule.read_text())
        if front is None:
            err(f"{rel}: missing YAML frontmatter")
            continue
        check_frontmatter_scalars(front, str(rel))
        if not re.search(r"^description:", front, re.MULTILINE):
            err(f"{rel}: frontmatter missing 'description'")


def validate_manifest_paths(manifest: dict, label: str):
    for field in MANIFEST_PATH_FIELDS:
        value = manifest.get(field)
        if value is None:
            continue
        paths = [value] if isinstance(value, str) else value if isinstance(value, list) else []
        for path_value in paths:
            if not isinstance(path_value, str) or path_value.startswith(("http://", "https://")):
                continue
            resolved = (ROOT / path_value).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                err(f"{label}: {field} path '{path_value}' escapes the plugin directory")
                continue
            if not resolved.exists():
                err(f"{label}: {field} references missing path '{path_value}'")


def validate_hook_config(path: Path, label: str):
    """Hook configs must be valid JSON, and every script they invoke must exist and be
    executable -- a hook naming a missing or non-executable script fails silently at runtime."""
    if not path.is_file():
        return
    data = load_json(path, label)
    if data is None:
        return
    for script in sorted(set(re.findall(r"hooks/([A-Za-z0-9._-]+\.sh)", json.dumps(data)))):
        target = ROOT / "hooks" / script
        if not target.is_file():
            err(f"{label}: references missing hook script 'hooks/{script}'")
        elif not os.access(target, os.X_OK):
            err(f"{label}: hook script 'hooks/{script}' is not executable (chmod +x)")


def _component_bodies():
    """(relative path, body-after-frontmatter) for every skill and agent."""
    out = []
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        _, body = split_frontmatter(skill_md.read_text())
        out.append((str(skill_md.relative_to(ROOT)), body))
    for agent_md in sorted((ROOT / "agents").glob("*.md")):
        _, body = split_frontmatter(agent_md.read_text())
        out.append((str(agent_md.relative_to(ROOT)), body))
    return out


def validate_reference_citations():
    """Every `references/<file>` cited in prose by a skill or agent must exist. The bundled
    references/ live at the PLUGIN ROOT while the citing skill sits two levels down, so a stale
    path fails silently at load time and the component improvises rules instead of grounding in
    them. (Markdown *links* to those files are covered by validate_markdown_links.)"""
    refs_dir = ROOT / "references"
    cite_re = re.compile(r"references/([A-Za-z0-9][A-Za-z0-9._/-]*\.[A-Za-z0-9]+)")

    for rel, body in _component_bodies():
        for cited in sorted(set(cite_re.findall(strip_code(body)))):
            if not (refs_dir / cited).is_file():
                err(f"{rel}: cites 'references/{cited}' which does not exist")


# --- Markdown link / anchor checking -------------------------------------------------

# Fenced blocks first (``` or ~~~, closed by a fence of at least the same length), then
# inline code spans. Both are stripped before scanning, because link syntax inside them is
# ILLUSTRATIVE, not a link: a `docs-lint-setup` example or an `ai-seo` llms.txt sample
# legitimately shows `[Install](https://example.org/install/)` as literal text.
FENCE_RE = re.compile(r"^(?P<f>```+|~~~+)[^\n]*\n.*?^(?P=f)[^\n]*$\n?", re.M | re.S)
CODESPAN_RE = re.compile(r"(?<!`)(`+)(?!`).*?(?<!`)\1(?!`)", re.S)
# A markdown inline link. Captures the target plus any #fragment; external targets are
# filtered out in the loop below, not here.
LINK_RE = re.compile(r"\[(?:[^\[\]]|\[[^\[\]]*\])*\]\(\s*<?([^)>\s]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$", re.M)
# Protocol-relative URLs, plus any explicit URL scheme (http:, mailto:, tel:, ftp:, data:, …).
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def strip_code(text: str) -> str:
    """Blank out fenced blocks and inline code spans, preserving line count so reported
    line numbers stay accurate."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    return CODESPAN_RE.sub(blank, FENCE_RE.sub(blank, text))


def heading_anchors(text: str) -> set:
    """GitHub-compatible heading anchors for a Markdown document.

    Mirrors GitHub's slugger: drop inline markup, lowercase, strip anything that is not
    alphanumeric / space / hyphen / underscore, then spaces -> hyphens. Repeated slugs get
    the '-1', '-2', ... suffixes GitHub appends, so a doc with two identical headings still
    validates. Headings inside code fences are excluded (strip_code runs first)."""
    seen, out = {}, set()
    for _, raw in HEADING_RE.findall(strip_code(text)):
        t = re.sub(r"<[^>]+>", "", raw)                        # inline HTML
        t = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", t)       # links/images -> text
        t = re.sub(r"[`*_~]", "", t)                           # emphasis / code marks
        slug = re.sub(r"[^\w\s-]", "", t.lower()).strip()
        slug = re.sub(r"\s+", "-", slug)
        if not slug:
            continue
        n = seen.get(slug, 0)
        seen[slug] = n + 1
        out.add(slug if n == 0 else f"{slug}-{n}")
    return out


def validate_markdown_links():
    """Every relative Markdown link resolves, and every '#anchor' exists in its destination.

    Internal link rot is precisely the defect this plugin tells other repositories to fix, so
    it is checked here rather than trusted. External links are NOT fetched -- that needs
    network access and would make the validator flaky and slow."""
    docs = sorted(
        p for p in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.mdc"))
        if not any(part in {".git", "node_modules", "styles", "site", ".fetched"} for part in p.parts)
    )
    anchor_cache = {}

    def anchors_for(path: Path):
        key = str(path)
        if key not in anchor_cache:
            try:
                anchor_cache[key] = heading_anchors(path.read_text())
            except OSError:
                anchor_cache[key] = set()
        return anchor_cache[key]

    for doc in docs:
        rel = doc.relative_to(ROOT)
        text = doc.read_text()
        stripped = strip_code(text)
        for target in sorted(set(LINK_RE.findall(stripped))):
            if target.startswith("//") or SCHEME_RE.match(target):
                continue                           # external -- deliberately not fetched
            path_part, _, frag = target.partition("#")

            if not path_part:                      # same-page anchor
                if frag and frag not in anchors_for(doc):
                    err(f"{rel}: anchor '#{frag}' has no matching heading in this file")
                continue

            dest = (doc.parent / path_part).resolve()
            if not dest.exists():
                err(f"{rel}: relative link '{target}' does not resolve")
                continue
            if frag and dest.is_file() and dest.suffix.lower() in {".md", ".mdc"}:
                if frag not in anchors_for(dest):
                    err(f"{rel}: anchor '#{frag}' has no matching heading in '{path_part}'")


def validate_doc_sync():
    """Every worker skill and agent must be named in the router skill's body AND in
    hooks/session-start.sh. A component that exists but is not routed to is unreachable in
    practice, and the session-start surface is what tells a user it exists."""
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        return

    workers = sorted(d.name for d in skills_dir.iterdir() if d.is_dir() and d.name != ROUTER_SKILL)
    agents = sorted(a.stem for a in (ROOT / "agents").glob("*.md"))

    router_md = skills_dir / ROUTER_SKILL / "SKILL.md"
    if not router_md.is_file():
        err(f"skills/{ROUTER_SKILL}/SKILL.md: missing router skill (doc-sync cannot be checked)")
    else:
        _, router_body = split_frontmatter(router_md.read_text())
        for name in workers + agents:
            if name not in router_body:
                err(f"skills/{ROUTER_SKILL}/SKILL.md: router does not mention '{name}' "
                    f"-- add it to the routing table (or the Agents section) so it is reachable")

    hook = ROOT / "hooks" / "session-start.sh"
    if not hook.is_file():
        err("hooks/session-start.sh: missing (doc-sync cannot be checked)")
    else:
        hook_text = hook.read_text()
        for name in workers + agents:
            if name not in hook_text:
                err(f"hooks/session-start.sh: does not advertise '{name}' "
                    f"-- keep the announced surface in step with the components")


def main():
    manifests = {}
    for subdir, label in ((".claude-plugin", "Claude manifest"), (".cursor-plugin", "Cursor manifest")):
        manifest_path = ROOT / subdir / "plugin.json"
        if not manifest_path.is_file():
            err(f"missing {manifest_path.relative_to(ROOT)}")
            continue
        data = load_json(manifest_path, label)
        if data is None:
            continue
        manifests[subdir] = data

        name = data.get("name")
        if not name or not PLUGIN_NAME_RE.match(name):
            err(f"{label}: 'name' must be lowercase alphanumerics, hyphens, and periods")
        for field in ("name", "version", "description"):
            if not data.get(field):
                err(f"{label}: required field '{field}' is missing or empty")
        # `claude plugin validate` rejects a bare-string author.
        if "author" in data and not isinstance(data["author"], dict):
            err(f"{label}: 'author' must be an object {{name, url}}, not a string")
        validate_manifest_paths(data, label)

    # Cross-manifest agreement (dual-host parity).
    if len(manifests) == 2:
        claude, cursor = manifests[".claude-plugin"], manifests[".cursor-plugin"]
        for field in SYNCED_FIELDS:
            if claude.get(field) != cursor.get(field):
                err(f"manifests disagree on '{field}': "
                    f"claude={claude.get(field)!r} cursor={cursor.get(field)!r}")

    validate_hook_config(ROOT / "hooks" / "hooks.json", "Claude hooks")
    validate_hook_config(ROOT / "hooks" / "cursor-hooks.json", "Cursor hooks")

    validate_skills()
    validate_md_components("agents", require_name=True, is_agent=True)
    validate_md_components("commands", require_name=False)
    validate_rules()
    validate_reference_citations()
    validate_markdown_links()
    validate_doc_sync()


if __name__ == "__main__":
    main()
    if errors:
        print(f"FAIL: {len(errors)} problem(s)")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print("OK: manifests, dual-host parity, component paths, kebab-case names, hook configs "
          "and scripts, skills, agents, rules, reference citations, markdown links/anchors, "
          "and doc sync are valid")
