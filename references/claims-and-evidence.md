# Claims and Evidence

The load-bearing rule of this plugin. Every other reference defers to it.

> **A claim that cannot be traced to a source does not ship.**

This exists because generative copy tooling fails in one specific, predictable way: asked to make a page more persuasive, it invents the persuasion. Statistics, customer counts, testimonials, benchmark numbers, award mentions, and urgency ("limited time", "join thousands of teams") are the most common fabrications, because they are the most conventional ingredients of landing-page copy. They are also the ones that destroy credibility with a technical audience and, depending on jurisdiction and claim, create real legal exposure.

## 1. The four claim classes

Classify every factual assertion before writing it. The class determines what is required.

| Class | Example | Requirement |
|---|---|---|
| **Verifiable in-repo** | "The validator checks dual-host parity." | Point to the file/function. Read it first — do not infer from a filename. |
| **Verifiable externally** | "RFC 2119 defines MUST and SHOULD." | Cite the source inline or in a footnote. Prefer primary sources over summaries. |
| **Attributable opinion** | "The Go team considers formatting non-negotiable." | Name the holder of the opinion. Never launder an opinion into a fact. |
| **Unsupported** | "Teams ship 40% faster." | **Do not write it.** No hedge rescues it — see §3. |

## 2. Never invent

Never originate any of the following. If the user supplies them, use them as given and attribute them; if they are absent, the copy must work without them.

- **Numbers** — percentages, benchmarks, user/customer/download counts, uptime figures, time-to-value, "N× faster".
- **Social proof** — testimonials, quotes, named customers, logos, star ratings, review counts, awards, analyst placements.
- **Endorsement** — implying a standards body, vendor, or person endorses the thing when they have not.
- **Urgency and scarcity** — deadlines, "limited", "act now", countdowns, fake cohort sizes.
- **Comparative superiority** — "the best", "the fastest", "the only", "industry-leading" — unless a cited, reproducible measurement backs the specific comparison.
- **Roadmap as present tense** — describing planned or partial capability as shipped. Use the status vocabulary in §4.

## 3. Hedging is not a fix

Softening an unsupported claim keeps the claim and adds evasion. These are all still violations:

- "Teams report shipping faster" — which teams? reported where?
- "Up to 40% faster" — an unmeasured ceiling is not a measurement.
- "Designed to reduce onboarding time" — intent smuggled in as outcome.
- "Trusted by developers worldwide" — unfalsifiable, therefore meaningless.

The repair is not a weaker verb. It is to **replace the invented outcome with the observable mechanism**:

> ❌ "Cut review time by 40%."
> ✅ "Flags silently-swallowed errors, goroutine leaks, and context misuse — the classes `go vet` and `golangci-lint` do not cover."

The mechanism is checkable, specific, and more persuasive to a technical reader than a number they will assume was fabricated.

## 4. Status vocabulary

State maturity plainly rather than blurring it. Use one word per component and keep it accurate:

`shipped` · `experimental` · `planned` · `deprecated` · `removed`

Do not describe a `planned` component in the present indicative. Do not let a README table claim `shipped` for something absent from the tree — verify against the tree before editing an inventory, because inventories rot faster than prose.

## 5. Inventories rot

Any count, list, or table mirroring real repository contents ("7 skills", "two agents", a component table) must be verified against the source before it is edited or repeated. Prefer generating such a list from the tree over hand-maintaining it. When hand-maintained, the repo's documentation-sync rule must name it so it moves in lockstep.

## 6. Audience calibration

Growth-copy conventions and technical audiences are actively incompatible. Developers, clinicians, and engineers treat unsourced numbers as evidence of unseriousness — the copy pattern that raises conversion on a consumer landing page lowers it here. For technical audiences:

- Lead with **what it does**, not what the reader will feel.
- Prefer a **code block, a command, or a concrete failure it catches** over an adjective.
- Name the **limits and prerequisites** early. Stating what something does not do buys more trust than any superlative.
- Let the reader **verify cheaply** — link the source, the spec, the file.

## 7. Domain ground truth

Where a repository names an authoritative source for its domain facts (a specification, a standards body, a product repo), statements of domain fact come from that source, never from model memory. Look it up. Where a consuming repo's `AGENTS.md` names its ground-truth source, that instruction outranks anything here.

## 8. Review test

For each factual sentence, ask: *if a hostile reader demanded the source, could I produce it in one step?* If not, cut the sentence or downgrade it to the mechanism. Applied consistently this removes most of a page's word count and improves it.
