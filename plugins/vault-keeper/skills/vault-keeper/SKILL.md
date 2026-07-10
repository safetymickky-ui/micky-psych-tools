---
name: vault-keeper
description: >-
  Files, indexes, links, and retrieves any skill's output in the shared vault at the
  marketplace repo root (vault/) — the one Obsidian-style place everything lands. Use
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

## Step 0 — Locate the vault

Do this before every job — never trust a bare relative `vault/`. From the layout reference:

> Resolve it: walk up from cwd to the directory containing `.claude-plugin/marketplace.json`,
> then append `vault/`. From inside a plugin, `${CLAUDE_PLUGIN_ROOT}/../../vault` is equivalent.
> Use the resolved ABSOLUTE path in every Glob/Grep/Read/Write.

Every path operation in every job below uses that resolved absolute path.

## The vault

One vault, at the marketplace repo root: `vault/`. Never anywhere else, never a second copy.
The canonical layout — tree, naming, collision, and index rules — is
[references/vault-layout.md](references/vault-layout.md), the single source of truth every
plugin cites. In brief:

- **Tree is fixed**: `index.md`, `MOCs/`, `notes/`, `artifacts/`, `assets/` — no free-form top-level folders.
- **Naming**: MOCs are `<Topic> MOC.md`; notes `Concept — Qualifier`; artifacts kebab-case.
- **Collision rule**: a derived filename that exists but is NOT the same topic being extended gets ` -2`, ` -3`… — never overwrite.
- **Index determinism**: index regeneration is a pure rebuild, alphabetical by title; multi-topic notes declare `primary-moc:` and that MOC wins; orphans are reported, never moved.

Atomic notes go in `notes/`; long-form or single-file outputs go in `artifacts/`. When unsure,
it is a note if it states one idea another note could link to, an artifact if it is a document
read top-to-bottom. Binaries always land in `assets/` and are referenced from a note.

## Frontmatter — every markdown file carries it

```yaml
---
title: <human title>
created: <YYYY-MM-DD>          # from environment context (currentDate) or ask the user; if neither, omit — never guess
type: note | artifact | moc
source: <origin skill or "manual">
primary-moc: <Topic>   # only for multi-topic notes
tags: [<kebab>, <kebab>]
links: [<Other Note title>, <Another>]   # mirror of the [[wikilinks]] in the body
---
```

Bodies link with Obsidian `[[wikilinks]]` by note title. A link to a note that does not exist
yet is fine — it marks a note worth writing, not an error. Keep the `links:` frontmatter list
in sync with the `[[...]]` used in the body.

## The four jobs

### init — scaffold the vault
Only when the vault is not populated. **Populated means `vault/index.md` exists**;
`.gitkeep`-only dirs do not count as content. Create the canonical tree (see
[references/vault-layout.md](references/vault-layout.md)) and an `index.md` whose body is
`# Vault Index` plus an empty MOC list. Never re-init a populated vault; skip to the real job.

### save — file an artifact
1. Decide `note` vs `artifact` (rule above).
2. **Search first (see query) to avoid a duplicate.** If a fitting note or MOC exists, *extend*
   it rather than create a sibling. This is the rule that keeps the vault from rotting.
3. Kebab the filename for artifacts; use `Concept — Qualifier` for notes. Apply the collision
   rule: an existing filename that is not the same topic being extended gets ` -2`, ` -3`… —
   never overwrite (see [references/vault-layout.md](references/vault-layout.md)).
4. Write frontmatter + body. Merge producer-supplied extra frontmatter fields (e.g. `sources`,
   `board_pearls`, `review_count`) verbatim after the canonical fields; extras never override
   the canonical keys. Add `[[wikilinks]]` to the obvious neighbours already in the vault.
5. Wire it into its topic MOC (create the MOC if the topic is new) and, if the MOC is new, add
   the MOC to `index.md`. When a note belongs to more than one topic, set `primary-moc:` in its
   frontmatter to the chosen primary — that MOC gets the index-checked link; other MOCs may
   link too. A saved file unreachable from `index.md` is a lost file.

### index — maintain the maps
Rebuild or repair `index.md` and the `MOCs/`. Regeneration is deterministic (rules in
[references/vault-layout.md](references/vault-layout.md)): a pure rebuild, alphabetical by
title; multi-topic notes' `primary-moc:` frontmatter decides their one MOC and the index
checks only the primary. Walk the vault, ensure every note is reachable from exactly one MOC
and every MOC from `index.md`, fix stale/broken `[[links]]`, and report orphans (files no MOC
points at) — never move or delete them.

### query — find before you duplicate
`Glob` `<resolved vault root>/**/*.md`, `Grep` titles/tags/body for the topic. Return what exists with paths.
This runs *inside* every save, and standalone when the user asks "what's in the vault about X".

## Rules

- **Never fabricate a write or a path.** If the filesystem is unavailable, say so; write nothing.
- **Never invent `created` dates or content.** Obtain today's date from the environment
  context (currentDate) or ask the user; if neither is available, omit the field rather than
  guess. Missing content → hand back to the source skill.
- **One vault, at repo root.** No second vault, no per-plugin vault, no vault outside the repo.
  Always resolve it per Step 0 — a bare relative `vault/` from the wrong cwd creates a rogue vault.
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
