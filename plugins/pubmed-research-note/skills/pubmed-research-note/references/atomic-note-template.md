# Atomic Note Template

**This file is dormant unless the user says "atomize" / "ทำโน้ต" or explicitly asks for a
vault note.** The report is the default and only deliverable. Never produce a note because
the topic "seems noteworthy" — an unrequested atomic note is clutter with a `review_count`
nobody will ever increment.

Note the register shift: the *report* is a verdict-first decision instrument, read once and
discarded. The *note* is the opposite — a durable, atomic, reviewable unit. Do not carry the
report's structure across. Re-atomize the content, and here the ordinary topic headings
(Mechanism, Dosing, Side Effects) are correct, because a note has no decision to spine on.

## One concept per note

A report may collapse into ONE rich concept note, or split into 2–3 when it spans separable
concepts (mechanism vs adverse effects vs dosing). In vault mode, before creating:
`Grep`/`Glob` the vault for an existing note or a fitting `MOC — …` and link/extend it
rather than duplicating. In sandbox mode there is no vault to grep — skip dedup, write to
`<outputs>/vault/`, and say plainly these are downloads, not vault writes.

## Citation rule — differs from the report

The report keeps its prose clean and pushes PMIDs into `## Sources`. **The note does not.**
A note is re-read years later out of context, so it carries `sources:` frontmatter *and* a
`## Sources` section. Inline attribution inside the note body is still unnecessary.

## Frontmatter schema

```yaml
---
type: concept            # concept | mechanism | moc | drug | disorder (match folder)
domain: [psychopharmacology, child-adolescent]   # array of domain tags
related_disorders: [ADHD]
related_drugs: [Atomoxetine]
board_yield: high        # high | medium | low
board_pearls:
  - "One-line, exam-grade fact with the number in it"
  - "Another"
aliases: [Alternative Title, Brand Name]
tags: [psychopharm, board-high-yield]
sources:                 # RESEARCH-NOTE ADDITION — auditable provenance
  - "Author Year. PMID NNNNN. doi:10.xxxx/yyyy"
  - "Kaplan & Sadock's Synopsis, 12e (Open Library OLNNNNNW)"
last_updated: 2026-06-21
review_count: 0
last_reviewed: null
primary_moc: "MOC — Pediatric Psychopharmacology"
---
```

`sources:` is the one field added for research notes — it makes every atomic note trace
back to PubMed/textbook, mirroring the report's citation discipline.

## Body structure

```markdown
> **Chapter MOCs**: [[MOC — Pediatric Psychopharmacology]] · [[MOC — ADHD]]

## Overview
2–4 sentences. What it is, why it matters, the one hallmark fact. Link concepts with [[wikilinks]].

## Mechanism            ← (section headers vary by concept: Mechanism, Dosing,
## <Concept sections>      Pharmacokinetics, Efficacy, Side Effects, Criteria, etc.)
Quantified prose/tables. Effect sizes, NNT, doses, %, named trials — never vague.

## Related Notes
- [[Sibling concept]] · [[Parent disorder]] · [[Comparator drug]]
- Link liberally; a target that doesn't exist yet is a valid stub, not an error.

## Sources
1. Author. Title. Journal Year;vol:pages. PMID NNNNN. doi:10.xxxx/yyyy.
2. Book, Edition, Publisher Year (Open Library OLID).

## Board Pearls
- Mirror the frontmatter board_pearls as a readable list at the bottom.
```

## Optional: Obsidian spaced-repetition button

Include this trailing block **only** for an Obsidian vault that uses the `meta-bind` +
`Templater` plugins. Omit it for plain-Markdown targets, and whenever the target vault's
plugin set is unknown (it does nothing there and just adds noise):

```markdown
---

```meta-bind-button
label: ✅ Mark as Reviewed
style: primary
id: mark-reviewed
hidden: false
action:
  type: runTemplaterFile
  templateFile: Templates/Review Note.md
```
```

## Filename + location (vault mode)

- `<vault_dir>/<Folder>/<Concept — Qualifier>.md`
- Use ` — ` (space, em dash, space) as the separator.
- Put it in the right domain folder — confirm it exists first (`Drugs/`, `Concepts/`,
  `Mechanisms/`, `Adverse Effects/`, `Anxiety Disorders/`, `Geriatric/`, `MOCs/`, …).
- If a note needs a new MOC, either link an existing MOC or create the `MOC — …` note too
  and add the new note to its `## Core Notes` list.

## What distinguishes a research note from a plain vault note

Same skeleton, plus: a populated `sources:` frontmatter list and a `## Sources` body section
with real PMIDs/DOIs. Everything else (atomicity, MOC wiring, pearls, optional button) is
identical — the research note is just an *auditable* member of the same graph.
