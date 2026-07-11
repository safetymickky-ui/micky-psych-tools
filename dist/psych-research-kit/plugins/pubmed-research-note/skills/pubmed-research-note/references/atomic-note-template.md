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
concepts (mechanism vs adverse effects vs dosing). Dedup, placement, and MOC linking are not
this skill's job — hand each note's title and body to vault-keeper (see below) and let it
decide whether an existing note should be extended instead.

## Citation rule — differs from the report

The report keeps its prose clean and pushes PMIDs into `## Sources`. **The note does not.**
A note is re-read years later out of context, so it carries `sources:` frontmatter *and* a
`## Sources` section. Inline attribution inside the note body is still unnecessary.

## Note data handed to vault-keeper (shown as frontmatter for readability)

This is a description of what data this skill hands to vault-keeper, not a block this
skill writes itself — vault-keeper authors the actual frontmatter (see **Placement is
vault-keeper's job** below). `type`, `tags`, and `primary-moc` map to the contract's core
payload slots (target type, tags-as-data, suggested MOC topic); every other field travels
via the contract's optional extra-frontmatter-fields slot as a flat key: value map.

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
primary-moc: "Pediatric Psychopharmacology MOC"
---
```

`sources:` is the one field added for research notes — it makes every atomic note trace
back to PubMed/textbook, mirroring the report's citation discipline.

## Body structure

MOC wikilinks in the body are suggestions — vault-keeper may rewrite them when it does the
actual MOC wiring.

```markdown
> **Chapter MOCs**: [[Pediatric Psychopharmacology MOC]] · [[ADHD MOC]]

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
- Mirror the board_pearls data (handed to vault-keeper) as a readable list at the bottom.
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

## Placement is vault-keeper's job

Title each note `Concept — Qualifier` (space, em dash, space). Beyond that, this skill does
not resolve a vault path, pick a folder, dedup against existing notes, or wire a MOC.
Placement, filenames, dedup, and MOC wiring are owned by the vault-keeper plugin (see its own
docs when it is installed). **If vault-keeper is not installed**, write each requested note as
a plain md file in the working directory instead — same title and body, no invented vault.

## What distinguishes a research note from a plain vault note

Same skeleton, plus: a populated `sources:` list — handed to vault-keeper as extra
frontmatter data, not written by this skill — and a `## Sources` body section with real
PMIDs/DOIs. Everything else (atomicity, MOC wiring — which vault-keeper owns — pearls,
optional button) is identical — the research note is just an *auditable* member of the
same graph.
