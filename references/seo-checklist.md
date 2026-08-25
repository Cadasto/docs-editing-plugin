# Discoverability Checklist — Search and AI Citability

Two audiences read a documentation site that neither writes nor reviews it: **search crawlers** and **AI retrieval systems**. Both reward the same thing — a page that states plainly what it is about, in one place, in machine-readable form. Neither is served by keyword padding.

Verify against the **published output**, not the source. A statically generated site can drop a tag, rewrite a link, or omit a page without any build warning.

## 1. On-page essentials

| Item | Rule | Common failure |
|---|---|---|
| `<title>` | Unique per page, ≤ ~60 chars, most specific term first, site name last | Every page inherits the site title |
| Meta description | Unique, 120–160 chars, describes *this* page, no keyword stuffing | Absent, or duplicated site-wide |
| One `<h1>` | Matches the page's actual subject; not the site name | Theme renders the site name as `h1` |
| Heading order | `h1` → `h2` → `h3`, no skipped levels | Levels chosen for font size |
| Canonical URL | Set, absolute, self-referencing; one canonical per piece of content | Missing, so `/page` and `/page/` compete |
| `lang` attribute | Set on `<html>` | Absent |
| Image `alt` | Describes function, empty (`alt=""`) for decorative | Filename as alt text |
| Descriptive link text | Link the noun | "click here", bare URLs |

## 2. Structure and crawlability

- **`robots.txt`** — present, does not block assets the page needs to render, references the sitemap.
- **`sitemap.xml`** — generated, lists canonical URLs only, no redirects or `noindex` pages, referenced from `robots.txt`.
- **URLs** — stable, lowercase, hyphenated, no session or tracking parameters in canonical form. A URL is a permanent promise; renaming one costs every inbound link unless redirected.
- **Redirects** — every renamed or removed page has a `301`. Verify the chain resolves in one hop.
- **Internal links** — every page reachable from the nav or an in-body link; no orphans. Deep pages need inbound links from related pages, not only from the sitemap.
- **404 page** — useful, links back into the nav.
- **Pagination / faceted views** — must not multiply near-duplicate URLs.

## 3. Content signals

- **One page per intent.** Two pages competing for the same query cannibalise each other; merge them and redirect.
- **Answer in the first paragraph.** Both search snippets and AI retrieval quote the opening. Put the definition there, not the history.
- **Self-contained sections.** A retrieval system returns *a chunk*, not a page — each `h2` section must make sense pulled out of context. Resolve pronouns and expand acronyms per section, not only per page.
- **The question as the heading.** Where readers arrive with a question, make the heading the question.
- **Real terminology.** Use the words practitioners use, including the acronym and the expansion, once each, naturally. No synonym stuffing.
- **Dates.** Show a meaningful last-updated date where currency matters; do not fake freshness by touching timestamps.

## 4. AI citability

Retrieval-augmented systems favour content they can extract, attribute, and trust.

- **`llms.txt`** — a Markdown index at the site root summarising the site and linking its key pages with one-line descriptions. Emerging convention (<https://llmstxt.org>), cheap to maintain, no downside. Keep it in step with the nav; a stale `llms.txt` is worse than none.
- **Markdown twins** — where the site can serve a `.md` alongside each HTML page, do. Plain Markdown is the cheapest possible source for a retrieval system, and avoids it parsing theme chrome.
- **Structured data** — JSON-LD in `<head>`. `TechArticle` or `Article` for docs pages, `SoftwareSourceCode` / `SoftwareApplication` for a tool, `FAQPage` **only** where visible Q&A really exists, `BreadcrumbList` for hierarchy. Validate it; invalid JSON-LD is silently ignored. Never mark up content that is not on the page.
- **Attribution surface** — a clear canonical URL, an author or organisation, and a stable title give a model something to cite. Anonymous content gets paraphrased without attribution.
- **Tables and lists over prose** for parameters, comparisons, and steps — they survive chunking intact.
- **Do not gate or JS-render the primary content.** What is not in the served HTML is, for most crawlers and many retrieval pipelines, not there.

## 5. What not to do

- Keyword density targets, synonym padding, hidden text, doorway pages.
- Marking up structured data that does not appear on the page.
- Inventing FAQs to win a rich result (also a claims violation — see [claims-and-evidence.md](claims-and-evidence.md)).
- Chasing a word count. Length is an output of scope, never a target.

## 6. Verification

Prefer checking the built artefact:

- Fetch the published page and inspect the served HTML for the tags in §1.
- Fetch `robots.txt`, `sitemap.xml`, and `llms.txt` and confirm they exist and agree with the nav.
- Grep the build output for the assertions the build itself cannot make — a missing stylesheet target or a template-emitted link produces no warning in most generators.
- Report findings as **file · symptom · fix**, ranked by reader impact, not by how easy they are to fix.
