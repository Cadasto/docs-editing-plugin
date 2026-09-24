# AI Tells

The canonical catalogue of the patterns that make prose read as machine-drafted, and the rules for removing them. Skills cite this file; they do not restate it. `humanize` applies it end to end; `copy-editing`, `technical-writing`, `marketing-copy` and the `prose-reviewer` agent apply it as one pass among several.

A tell is a **default choice**: the phrasing that fits the widest range of readers and subjects, used where a careful writer would have chosen for one reader and one subject. Removing tells is an editing job about the reader. It is not a verdict on who wrote the text (§8).

Where a consuming repository's style guide conflicts with this file, **the repo wins**, as everywhere in this plugin.

<!-- This file quotes the patterns it catalogues, so the ai-tells style is off for it (§7, quoted or discussed text). -->

<!-- vale ai-tells = NO -->

## 0. How to apply the catalogue

- **Strength decides whether one sighting is enough.** Patterns marked **strong** justify an edit on their own. Patterns marked **weak alone** are ordinary choices a person makes on purpose; act on one only when other tells share the passage. A **passage** is the paragraph, or the list or table, the pattern sits in.
- **Restate; do not swap.** Replacing "delve into" with "dig into" keeps the sentence that asked for it. Find the fact the sentence carries and say that plainly. If there is no fact, cut the sentence.
- **Add no fact; drop no supported fact.** A rewrite keeps every supported claim and introduces no fact, name, number, date, quote or citation that the source or the user did not supply. The never-invent list in [claims-and-evidence.md](claims-and-evidence.md) §2 binds a humanising pass exactly as it binds drafting. If a sentence needs a detail you do not have, write a simpler sentence or ask.
- **Drop nothing by accident.** Shape edits (breaking a triad, merging a closer into its paragraph, removing bold labels) are where claims quietly disappear. Compare before and after for every fact.
- **Vale finds the words; judgment finds the shapes.** The `ai-tells` Vale style (`references/vale-styles/ai-tells/`) flags the phrasings below that a pattern can match without false positives: chatbot residue, tool markup, signposting, stock vocabulary, unsourced attribution, staged contrasts and dashes. The rest are found by reading. Structure (triads, closers, bold-label lists, uniform rhythm) has no deterministic check and is found by reading.

## 1. Leftovers from the chat (strong)

Text addressed to the person who prompted a model, not to the reader. Always a defect in a published page. Vale: `ai-tells.chatbot-residue` and `ai-tells.tool-markup` (error), for the phrasings with no ordinary documentation use. "Let me know if you have any questions" is also a human sign-off, so it is judged, not linted.

| Pattern | Example | Repair |
|---|---|---|
| Chatbot pleasantries | "Great question!", "I hope this helps", "Let me know if you have any questions" | Delete |
| Knowledge-limit disclaimers | "As of my last update", "details may have changed since my training" | Delete; if currency matters, state the date the fact was checked |
| Writing about the previous draft | "Here is the revised version", "In this updated version, I have…" | Delete; the changelog records changes, not the page |
| Tool markup left in | `contentReference`, `oaicite`, `turn0search0`, `[Insert link here]` | Delete, and check the claim it was attached to still has a source |

## 2. Staging instead of stating (strong unless noted)

The sentence performs importance instead of adding a fact. Vale: `ai-tells.signposting` (warning), `ai-tells.negation-contrast` (suggestion).

- **Signposting.** Announcing content instead of delivering it: "Let's dive in", "Here's the thing", "It's worth noting that", "In conclusion". Delete the announcement; the next sentence is the point. This overlaps the throat-clearing rule in [style-guide.md](style-guide.md) §2.
- **Staged contrast.** "It's not X, it's Y", "This isn't just a tool", "more than just". It argues with an opponent nobody raised. State Y. *Weak alone* where a reader really does hold X: "`sync` is not a backup; it overwrites local changes" is a legitimate warning in reference docs.
- **Quotable closer.** A short final line that restates the paragraph as a slogan ("Clarity is the product."). Delete it, or fold its one new fact into the paragraph.
- **Question run-up.** "So what does this mean for you? It means…" or "The result? Faster builds." Ask nothing; state the answer.
- **Colon run-up.** "Here's why:" or "The key insight:" before a point that needs no drumroll. Start with the point.

## 3. Inflation and borrowed authority (strong)

Ordinary facts dressed as significant or expert-backed. Vale: `ai-tells.stock-vocabulary`, `ai-tells.vague-attribution` (both warnings).

- **Significance inflation.** "plays a pivotal role", "marks a turning point", "a testament to", "underscores the importance of". Say what the thing does and let the reader judge its importance.
- **Stock vocabulary.** "delve", "tapestry", "realm", "landscape", "ever-evolving", "embark on", "harness the power", "unlock the potential", "game-changer". Restate per §0; a synonym is not a repair.
- **Vague attribution.** "Experts say", "studies show", "it is widely believed", "teams report". This is a claims defect first: apply [claims-and-evidence.md](claims-and-evidence.md) §3. Cite the source or cut the claim; never soften it.
- **Trailing "-ing" riders.** "…, highlighting its commitment to quality", "…, ensuring a seamless experience". The rider asserts a consequence nobody checked. Cut it, or make the consequence its own sentence with its evidence.
- **Avoiding "is" and "has"** (*weak alone*). "serves as", "stands as", "boasts", "features" where "is" or "has" is the plain verb. Use the plain verb.

## 4. Rhythm by rule (weak alone)

Devices applied everywhere, whether or not the meaning asks for them. No Vale rule except dashes (§6).

- **Forced triads.** Three adjectives, three examples, three parallel clauses, again and again. Keep a list of three when there are three things; otherwise use the number the facts support. Two items often read better.
- **Metronome sentences.** Every sentence the same length and shape, or several sentences in a row opening with the same word. Vary length where the meaning allows; combine or split by sense, not by pattern.
- **Stacked hedges.** "may potentially", "could possibly help to". One qualifier, or none if the statement is true.
- **Synonym rotation.** Calling one thing a "record", an "entry" and an "item" in consecutive sentences. Already a defect under [style-guide.md](style-guide.md) §3.
- **Em dashes as the universal connector.** See §6, which sets the house rule.

## 5. Formatting by rule (weak alone)

Formatting applied to every item rather than where it helps the reader scan. Patterns marked *structural* change sections, not sentences: under a proofread or line-edit contract, report them and leave the fix to the author or a structural edit.

- **Bold as decoration.** Several bolded phrases per paragraph, so nothing stands out. Bold at most the one term a scanning reader must not miss.
- **Bold-label bullets.** `- **Speed:** It is fast.` repeated down a list, where the label restates the sentence. Drop the labels, or turn a list of real attributes into a table.
- **Heading per paragraph** (*structural*). Headings over single short paragraphs, or emoji in headings. Headings mark sections a reader navigates to ([style-guide.md](style-guide.md) §5).
- **Recap section** (*structural*). A closing "Summary" or "Key takeaways" that repeats the body. Delete it; the answer belongs at the top (style-guide §5, answer first).

## 6. The em-dash rule

**Write no em dashes.** In prose the assistant drafts or rewrites, use a comma, a colon, parentheses or a new sentence instead. Do not substitute a spaced en dash (`–`) or a spaced hyphen (`-`); those are the same tell.

**A person's dash is theirs.** An em dash a human author wrote on purpose stays. What happens to an existing dash depends on the pass, whatever the edit contract:

- **Wording the assistant writes** (a draft, a rewritten sentence, a new paragraph): no dashes.
- **An existing dash, in any pass except `humanize`** (copy-editing, drafting around existing text, review): leave it unless the author asked for dashes to go.
- **An existing dash, in a `humanize` pass**: *weak alone*. Replace it where its passage carries other tells; otherwise keep it and list it under "left alone".

**Vale reports, never blocks.** `ai-tells.em-dash` is a **suggestion**, so it never fails a `--minAlertLevel=error` CI gate. An author who wants dashes in one passage can silence the rule there:

```markdown
<!-- vale ai-tells.em-dash = NO -->
A sentence where the dash is deliberate — and stays.
<!-- vale ai-tells.em-dash = YES -->
```

A repo that uses dashes throughout sets `ai-tells.em-dash = NO` in its `.vale.ini`. Unspaced en dashes in ranges (`2020–2026`, `pages 4–7`) are correct typography and are not flagged, and neither is a lone dash standing in a table cell as "none".

## 7. When not to act

- **Quoted, cited or discussed text.** A tell inside a quotation, a title, a proper name, a code span or block, or a passage that talks *about* the phrase (like this file) is not a finding.
- **The repo's own conventions.** If the consuming repo's style guide permits a pattern, it is not a finding. Report the conflict once; do not fight it.
- **Legitimate uses.** Three real items, a contrast a reader genuinely needs, a bolded warning, a heading a reader will jump to. The test is whether the device serves this reader here.
- **The writer's voice.** Keep what marks a person: a specific, unusual detail; honest uncertainty ("I think", "probably"); a real aside or self-correction; a blunt opinion; mixed feelings left unresolved. These are the opposite of the default choice, and removing them makes the text read *more* machine-drafted.
- **Agent-instruction files.** `AGENTS.md`, `CLAUDE.md`, rules and skill definitions are out of scope ([doc-types.md](doc-types.md) §3). Their deliberate repetition and rigid parallel structure are features.

## 8. Not a detector

These patterns describe writing, not writers. Wikipedia's own catalogue calls them "only potential signs of a problem, not the problem itself". People write every one of them, especially under deadline or in a second language, and automated AI detectors have been shown to misclassify non-native English writing as AI-generated (Liang et al., 2023). So:

- **Never state or guess whether a text is AI-written.** Report the patterns found, quoted, with their repair.
- **Never promise a detector outcome.** The goal is prose a reader trusts, not a score from a classifier.

## Sources

- Wikipedia, "[Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)", maintained by WikiProject AI Cleanup; consulted 2026-09-24. The origin of the content, style, communication-with-the-user and markup categories used here.
- W. Liang, M. Yuksekgonul, Y. Mao, E. Wu, J. Zou, "[GPT detectors are biased against non-native English writers](https://arxiv.org/abs/2304.02819)", *Patterns*, 2023.
- The strength ranking (§0) and the edit-versus-report split follow an approach shared by the four English-prose humanising skills with the most GitHub stars on 2026-09-24: [blader/humanizer](https://github.com/blader/humanizer), [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop), [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) and [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing). This catalogue is written independently; no text is taken from them.
