---
name: ai-seo
description: Making content citable by AI search and retrieval systems. This skill should be used when the user asks to "add or update llms.txt", "make this site citable by AI / LLMs", "add structured data / JSON-LD / schema.org markup", "serve Markdown twins", "optimise for AI search or RAG retrieval", or "why does the AI summarise our docs wrongly?" — it audits and improves machine-readability and attribution. Not for classic search SEO — titles, sitemaps, crawlability (seo-audit) — nor for writing the copy (technical-writing, marketing-copy).
argument-hint: "<site URL, built output dir, or docs tree> [llms.txt | structured-data | twins]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# ai-seo — citability by AI search and retrieval

Work on **$ARGUMENTS**.

> **`references/…` paths resolve from the plugin root** (beside `skills/`, two levels up — not under this skill): `${CLAUDE_PLUGIN_ROOT}/references/…` on Claude Code, `../../references/…` relative, or Glob for the installed copy.

The checklist is `references/seo-checklist.md` §4 (with §3 for content signals). This skill is the procedure.

## The model to hold

A retrieval system does not read your page — it reads **a chunk of it**, out of context, and then decides whether it can attribute the chunk to you. Everything below follows from that:

- **Chunks must stand alone.** An `h2` section that says "this" or "the above" is useless once extracted. Resolve pronouns and expand acronyms **per section**, not once per page.
- **The opening sentence is what gets quoted.** Put the definition there. History and motivation come after.
- **Plain structure survives; chrome does not.** Tables, lists, and fenced code extract intact. Nested theme markup, tabbed panes, and JS-rendered content often do not.
- **Attribution needs a stable surface** — a canonical URL, a title, an organisation. Anonymous content gets paraphrased without credit.

Note honestly what is and is not established here: `llms.txt` is an **emerging convention** (<https://llmstxt.org>) with no guarantee any given system consumes it, and retrieval pipelines are largely undocumented. Recommend the cheap, no-downside measures; do not claim a ranking effect you cannot cite (`references/claims-and-evidence.md`).

## 1 · `llms.txt`

A Markdown index at the site root: what the site is, then curated links with a one-line description each.

Audit: does it exist at `/llms.txt`? Is it served as `text/plain` or `text/markdown` and reachable? **Does it still match the nav?** A stale `llms.txt` is worse than none — it confidently points at pages that moved.

Shape:

```markdown
# <Project name>

> One or two sentences: what this is, who it is for, what it does.

## Documentation
- [Install](https://example.org/install/): install on both supported hosts
- [Reference](https://example.org/reference/): every parameter and default

## Optional
- [Changelog](https://example.org/changelog/): release history
```

Rules: absolute URLs; canonical URLs only; one line per link, describing the page rather than repeating its title; group by reader intent; put lower-value material under `## Optional` so a fetcher can skip it. Keep it generated from, or checked against, the nav — and name it in the repo's documentation-sync rule so it moves in lockstep.

## 2 · Markdown twins

Where the generator can serve a `.md` alongside each HTML page, do it. Plain Markdown is the cheapest possible source for a retrieval system and skips theme chrome entirely.

Check: is the twin reachable at a predictable URL (`/page/` → `/page.md` or `/page/index.md`)? Does it carry the **body** content and not just front matter? Is it in the sitemap or linked from the HTML page (`<link rel="alternate" type="text/markdown">`)?

Caveat worth stating when you recommend it: a Markdown twin drops per-class tables and other content that only the HTML rendering produces. Where the source of truth is richer than the Markdown, say so rather than presenting the twin as complete.

## 3 · Structured data (JSON-LD)

JSON-LD in `<head>`. Pick the type from what the page actually is:

| Page | Type |
|---|---|
| Documentation / guide | `TechArticle` |
| Blog / announcement | `Article` or `BlogPosting` |
| A tool or library | `SoftwareSourceCode` / `SoftwareApplication` |
| Nav hierarchy | `BreadcrumbList` |
| Visible Q&A that genuinely exists | `FAQPage` |

Hard rules:

- **Never mark up content that is not visible on the page.** It is a policy violation, and inventing a FAQ to win a rich result is also a claims violation (`claims-and-evidence.md`).
- **Validate it.** Invalid JSON-LD is silently ignored — a syntax error produces no visible symptom at all. Parse it: `python3 -c "import json,sys;json.load(sys.stdin)"`.
- Include `@context`, `@type`, `name`/`headline`, `description`, `url` (canonical), and a `publisher`/`author` so attribution has somewhere to land.
- One primary entity per page. Do not stack unrelated types.

## 4 · Content shape for retrieval

Apply while auditing or editing (`seo-checklist.md` §3):

- Each `h2` self-contained; acronyms expanded within the section.
- Definition in the opening sentence of the page and of each major section.
- The reader's question as the heading where they arrive with one.
- Tables and lists for parameters, comparisons, and steps.
- **Primary content in the served HTML** — not gated, not JS-rendered. What is not served is, for most pipelines, not there.

## 5 · Verify and report

Fetch the published artefacts rather than trusting the source:

```bash
curl -sI  https://example.org/llms.txt          # exists? content type?
curl -s   https://example.org/llms.txt          # still matches the nav?
curl -s   https://example.org/page/ | grep -A20 'application/ld+json'
```

Report as **artefact · symptom · fix**, ranked by effect on citability: **absent or stale index** → **content not extractable** (JS-rendered, gated, chrome-heavy) → **no attribution surface** → **missing or invalid structured data** → **chunk-level fixes**. State what you fetched, what you could not check, and — for each recommendation — whether it is established practice or an emerging convention.

## 6 · Hand off

Titles, canonicals, sitemap, crawlability, orphans → `seo-audit` · rewriting a section so it stands alone → `copy-editing` · a missing page → `technical-writing` · a full context-isolated sweep → the `seo-auditor` agent.
