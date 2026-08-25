---
name: seo-audit
description: Use when asked about search-engine visibility — "run an SEO audit", "fix titles and meta descriptions", "check headings, internal links, sitemap, robots.txt", "why isn't this page indexed?", "find duplicate or orphan pages". Classic SEO, not AI citability (ai-seo).
argument-hint: "<site URL, built output dir, or page path> [--fix]"
allowed-tools: Read, Edit, Glob, Grep, Bash, WebFetch
---

# seo-audit — technical and on-page audit

Audit **$ARGUMENTS**.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

The checklist is `references/seo-checklist.md` §§1–3 and §5. This skill is the procedure around it.

## The rule that makes an audit worth anything

**Audit the published output, not the source.** A static site generator can drop a tag, rewrite a link, absorb a heading into a theme partial, or omit a page entirely with **no build warning at all**. Source Markdown tells you what the author intended; only the served HTML tells you what a crawler sees.

In order of preference:
1. **Fetch the live URL** and inspect the served HTML.
2. **Read the build output directory** (`site/`, `dist/`, `build/`, `public/`) after building.
3. **Read the source** — last resort, and label every finding as unverified against the published output.

Never report a `<title>` or canonical URL as correct on the strength of front matter alone; the theme decides.

## 1 · Scope and gather

1. **Read the repo's instructions** — `AGENTS.md`, `mkdocs.yml` / site config, `CONTRIBUTING.md`. Note the `docs_dir`, the nav source, and any gotcha the repo documents — a failure mode a project has recorded about itself is worth more than any generic check.
2. **Build if needed** — use the repo's own target (`make build`, `make check`, `mkdocs build --strict`, `npm run build`). Do not invent a build command; if you cannot build, say so and downgrade to source-level findings.
3. **Enumerate the page set** — from `sitemap.xml` where one exists, else the built output tree. Note the count.
4. **Note the sample** — if you audit a subset of a large site, say which pages and how they were chosen. A silent sample reads as full coverage.

## 2 · Audit passes

**Pass A — per-page essentials** (`seo-checklist.md` §1). For each page: unique `<title>` (specific term first, ≤ ~60 chars), unique 120–160 char meta description, exactly one `<h1>` that is the page's subject and not the site name, unbroken heading order, self-referencing absolute canonical, `lang` on `<html>`, functional `alt` on images, descriptive link text.

Useful greps over the built output — adapt to the generator:

```bash
grep -rL '<meta name="description"' site --include='*.html'   # pages with no description
grep -rho '<title>[^<]*</title>' site | sort | uniq -d        # duplicated titles
grep -rc '<h1' site --include='*.html' | grep -v ':1$'        # zero or multiple h1
grep -rL 'rel="canonical"' site --include='*.html'            # missing canonical
```

**Pass B — structure and crawlability** (§2). `robots.txt` present, not blocking render-critical assets, naming the sitemap. `sitemap.xml` generated, canonical URLs only, no redirected or `noindex` entries. URLs stable, lowercase, hyphenated. Renamed and removed pages have single-hop `301`s. **No orphans** — every page reachable from the nav or an in-body link. A useful 404.

**Pass C — content signals** (§3). One page per intent — flag pages competing for the same query and propose a merge plus redirect. First paragraph answers. Each `h2` section self-contained enough to survive being extracted. Real terminology, no synonym stuffing.

**Pass D — anti-patterns** (§5). Keyword padding, hidden text, doorway pages, structured data for content not on the page, invented FAQs. An invented FAQ is also a claims violation — `references/claims-and-evidence.md`.

## 3 · Report

Rank by **reader impact**, not by ease of fixing. Report each finding as:

**page · symptom · why it matters · fix**

Group into: **blocks indexing** (noindex, robots block, broken canonical, orphan) → **loses the click** (missing or duplicate title/description) → **degrades comprehension** (heading order, link text, `alt`) → **hygiene**.

Always state:
- **What was audited and how** — live URL, built output, or source; the page count; any sample.
- **What could not be checked**, and why. Coverage claims must be honest; "no issues found" on an unbuilt site is a false statement.

## 4 · Fixing

With `--fix`, apply only the mechanical, unambiguous repairs — a missing `lang`, an untagged image, a heading level, a `robots.txt` sitemap line. **Edit the source, never the build output**; a fix in `site/` disappears on the next build.

Leave to a human: anything that changes a URL (it breaks inbound links), page merges, and any rewrite of copy — hand those to `copy-editing` or `marketing-copy`. Re-build and re-audit the touched pages, and report the before/after.

## 5 · Hand off

`llms.txt`, structured data, Markdown twins, AI citability → `ai-seo` · rewriting a title or description as *copy* → `marketing-copy` or `copy-editing` · a missing page → `technical-writing` · a full context-isolated sweep → the `seo-auditor` agent.
