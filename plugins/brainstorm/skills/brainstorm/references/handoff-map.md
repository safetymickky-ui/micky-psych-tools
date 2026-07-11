# Handoff map — who owns each kept idea

Route by what the idea **is**, not the words it arrived in. One owner per idea; when two
could claim it, the more specific pipeline wins (a decision inside a learning topic is
still a decision).

| The kept idea is… | Owner | Handoff seed |
| --- | --- | --- |
| A clinical decision — should I / which / for whom / does X work | `pubmed-research-note` skill | the decision phrased as one question |
| Understanding a whole disorder or topic at chapter breadth | `/comprehensive-review <topic>` | the topic |
| "Keep an eye on X" — evolving evidence, no decision yet | `psych-paper-digest` | "add X to my watchlist" |
| A recurring workflow Claude could own end-to-end | `/new-plugin <seed>` | one-line purpose + trigger phrases |
| A fact, framework, or insight worth keeping as-is | `vault-keeper` (save) | title + body + type |
| Something to learn or master — becomes study material | Learn hub — stubs + `/sync-vault` | export contract below |
| One kept idea graduating into a build task, starting now | `intent-lock` | the chosen idea |

## Two vaults — never confuse them

- **Marketplace vault** (`vault/` at the micky-psych-tools repo root) — Obsidian-style
  (title-based wikilinks, MOCs, `index.md`), written **only** by vault-keeper. Brainstorm
  session artifacts land here, via vault-keeper.
- **Learn hub vault** (`vault/` in the learn-hub repo) — frontmatter-typed markdown
  (`type: topic|note`, slug ids) that `/sync-vault` parses and upserts to Supabase, which
  the Learn app renders. Things-to-learn stubs land here.

Writing one format into the other produces a file that is either unreachable (no MOC) or
unsyncable (no `type:`/`id:`). Session notes → marketplace vault. Study stubs → Learn hub.

## Learn hub export contract — things-to-learn only

The Learn hub is a separate repo (`learn-hub`): markdown vault → `/sync-vault` skill →
Supabase → Next.js app (lesson reader, knowledge graph, spaced review, stats). Brainstorm
writes only **sync-ready stubs**; the hub's own pipeline owns everything downstream.

### 1. Locate the checkout

Ask the user for the learn-hub repo path if the session does not already know it; the
checkout is recognizable by `vault/` plus a `CLAUDE.md` titled "Learn — Personal
Knowledge Hub". Unreachable → write the stubs to the working directory, state that
moving them into `learn-hub/vault/` is on the user, and still name the `/sync-vault`
handoff.

### 2. Ground against the existing hub vault

Glob `vault/*/_topic.md` and read the ids, `domain`, and `book` values.

- **Extend over duplicate:** if a topic already covers the idea, append note stubs to it
  (reuse its topic id; do not rewrite its `_topic.md` metadata).
- Reuse existing `domain` spellings **verbatim** (e.g. `Psychiatry`, `Computational
  Psychiatry`, `Neurology`) — the hub groups and colours by exact string.
- Omit `book` for brainstormed standalone topics (`book` is for extracted books).

### 3. Write the stubs

Topic file `vault/<topic-slug>/_topic.md`:

```yaml
---
id: <topic-slug>             # kebab, deterministic from the title
type: topic
title: <Title>
domain: <existing domain spelling>
description: <one line>
icon: "<one fitting emoji>"
color: "#<hex suiting the domain>"
order: <next free integer>
prerequisites: []            # topic ids only, and only if real
status: active
created: <today YYYY-MM-DD>  # from the environment date — never invented
updated: <today YYYY-MM-DD>
---
```

Note stub `vault/<topic-slug>/<note-slug>.md` — one per converged sub-idea, 3–6 per topic:

```yaml
---
id: <topic-slug>-<note-slug>
type: note
topic: <topic-slug>
title: <Note title>
summary: <one-line gist — this is the card and graph-hover text>
order: <1..n reading order>
difficulty: <1-5>
tags: [<kebab concept tags>]
links: []                    # note ids only — in this batch or already in the vault
sources: ["brainstorm YYYY-MM-DD"]
estimated_min: <rough read time>
created: <today YYYY-MM-DD>
updated: <today YYYY-MM-DD>
---

## What this note should cover

- <the 3–6 points the eventual author fills in>

> Stub from a brainstorm session — body to be authored.
```

Stub bodies are outlines by default. Write full note bodies only when the user explicitly
asks for finished notes — and then still in this format, never the marketplace vault's.
Wikilinks `[[note-id]]` may appear only for ids that exist (in this batch or already in
the hub vault) — the sync turns them into graph edges, and a dangling id makes a dead edge.

### 4. Hand off — the hub pipeline owns the rest

Tell the user to run `/sync-vault` in the learn-hub repo: it parses frontmatter +
wikilinks, upserts topics/notes/links to Supabase, prebakes mermaid, and busts the app
cache. This skill never runs the sync, never executes SQL, and never calls the revalidate
webhook. After the sync, the stubs surface in the app (Books, graph, review queue)
exactly like any other note.
