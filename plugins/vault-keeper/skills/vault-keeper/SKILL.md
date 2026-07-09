---
name: vault-keeper
description: >-
  Full manager for the shared Obsidian-style knowledge vault at the marketplace repo root
  (vault/). The one place any skill's output gets saved, indexed, linked, and retrieved. Use
  when the user says "save this to the vault", "vault this", "add to my vault", "file this
  note", "put this in the vault", "index the vault", "rebuild the index", "link these notes",
  "make a MOC", "query the vault", "search my vault", "what's in the vault", or asks to store,
  organize, or find any artifact a skill produced — reports, atomic notes, decks, data. Thai
  triggers: "เก็บลง vault", "เพิ่มใน vault", "ค้น vault", "ทำ index". Four jobs: init (scaffold
  the vault), save (write an artifact with YAML frontmatter, kebab name, wikilinks), index
  (maintain index.md + topic MOCs), query (grep/glob to find and read before duplicating). NOT
  for producing the artifact itself — the source skill does that; this only files it and finds
  it again.
---

# Vault Keeper — the one drawer everything goes in

Skills in this marketplace produce artifacts — evidence reports, atomic notes, decks, data
dumps — and then lose them. This skill is where they land, stay findable, and connect. You
are a librarian, not an author. **You do not write the artifact. You file it.** If the user
hasn't produced the content yet, that is the source skill's job; hand off, don't invent.

## The vault

One vault, at the marketplace repo root: `vault/`. Never anywhere else, never a second copy.

```
vault/
  index.md                       # root MOC — links every topic MOC. The front door.
  MOCs/<Topic> MOC.md            # one map-of-content per topic; links its notes
  notes/<Concept — Qualifier>.md # atomic notes — one idea each
  artifacts/<kebab-name>.md      # whole-file outputs (reports, decks, transcripts)
  assets/                        # binaries (images, pdfs, csv)
```

Atomic notes go in `notes/`; long-form or single-file outputs go in `artifacts/`. When unsure,
it is a note if it states one idea another note could link to, an artifact if it is a document
read top-to-bottom. Binaries always land in `assets/` and are referenced from a note.

## Frontmatter — every markdown file carries it

```yaml
---
title: <human title>
created: <YYYY-MM-DD>          # ask the user or use the known current date; never fabricate
type: note | artifact | moc
source: <origin skill or "manual">
tags: [<kebab>, <kebab>]
links: [<Other Note title>, <Another>]   # mirror of the [[wikilinks]] in the body
---
```

Bodies link with Obsidian `[[wikilinks]]` by note title. A link to a note that does not exist
yet is fine — it marks a note worth writing, not an error. Keep the `links:` frontmatter list
in sync with the `[[...]]` used in the body.

## The four jobs

### init — scaffold the vault
Only when `vault/` is missing or empty. Create the tree above and an `index.md` whose body is
`# Vault Index` plus an empty MOC list. Do not re-init a populated vault; if it exists, skip to
the real job.

### save — file an artifact
1. Decide `note` vs `artifact` (rule above).
2. **Search first (see query) to avoid a duplicate.** If a fitting note or MOC exists, *extend*
   it rather than create a sibling. This is the rule that keeps the vault from rotting.
3. Kebab the filename for artifacts; use `Concept — Qualifier` for notes.
4. Write frontmatter + body. Add `[[wikilinks]]` to the obvious neighbours already in the vault.
5. Wire it into its topic MOC (create the MOC if the topic is new) and, if the MOC is new, add
   the MOC to `index.md`. A saved file unreachable from `index.md` is a lost file.

### index — maintain the maps
Rebuild or repair `index.md` and the `MOCs/`. Walk the vault, ensure every note is reachable
from exactly one MOC and every MOC from `index.md`, fix stale/broken `[[links]]`, report
orphans (files no MOC points at) rather than silently deleting them.

### query — find before you duplicate
`Glob` `vault/**/*.md`, `Grep` titles/tags/body for the topic. Return what exists with paths.
This runs *inside* every save, and standalone when the user asks "what's in the vault about X".

## Rules

- **Never fabricate a write or a path.** If the filesystem is unavailable, say so; write nothing.
- **Never invent `created` dates or content.** Missing content → hand back to the source skill.
- **One vault, at repo root.** No second vault, no per-plugin vault, no vault outside the repo.
- **Extend over duplicate.** Two notes on one idea is the failure this skill exists to prevent.
- **Everything is reachable from `index.md`.** Save that skips MOC wiring is incomplete.

## Failure conditions

This skill has failed if:

- It authored artifact content instead of filing content the user already has.
- A file was written outside `vault/`, or a second vault was created.
- A saved file is unreachable from `index.md`.
- A duplicate note was created when an existing one should have been extended.
- Frontmatter is missing, or `created` was fabricated.
- A write was claimed that did not happen, or a vault path was invented.
