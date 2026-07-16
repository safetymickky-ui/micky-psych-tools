---
name: empty-vault
description: >-
  Drains the shared vault at the marketplace repo root (vault/) into the Learn hub:
  inventories artifacts, notes, and infographic assets, hands each report to learn-hub's
  digest-report skill (→ atomic Learn notes) and each infographic HTML to its
  ingest-infographic skill (→ an infographics row that shows in the app), syncs to Supabase,
  and only after that verified sync deletes the moved files, prunes their MOCs, and rebuilds
  index.md. Use when the user says "empty the vault", "drain the vault", "clear the vault",
  "move the vault to the Learn hub", "export the vault to learn-hub", "ship these reports to
  the hub", or asks to migrate vault content into the Learn hub (Thai: "ล้าง vault", "ย้าย
  vault ไป Learn"). Scope to one topic with /empty-vault [topic]. Deletion is double-gated —
  git-committed and explicitly confirmed — and nothing is deleted before the Learn-side sync
  verifies. NOT for filing/indexing/finding vault content (that is vault-keeper), and NOT the
  authoring itself — the learn-hub skills own that.
---

# Empty Vault — drain it into the Learn hub, then wipe it clean

The vault accumulates finished research — evidence reports, reviews, infographic assets —
whose long-term home is the **Learn hub** (`learn-hub` repo), where each report becomes a
chapter of atomic, learnable notes with graph, mastery, and spaced review. Emptying the
vault is a three-beat move: **move → verify → delete**, in that order, never reordered.
Git history is the archive — nothing is ever truly lost, but only if the delete happens
on committed state.

Like vault-keeper, this skill is a librarian, not an author. **It moves and erases; it
never distills.** The note-authoring happens in the Learn repo, owned by its
`digest-report` skill.

## Step 0 — resolve BOTH roots

- **Psych vault root** — exactly as vault-keeper's Step 0: walk up from cwd to the
  directory containing `.claude-plugin/marketplace.json`, append `vault/`, use the
  absolute path everywhere.
- **Learn repo root** — the `learn-hub` checkout: the directory containing
  `.claude/skills/digest-report/` (and `vault/` + `scripts/sync-vault.mjs`). Look for a
  sibling checkout of this marketplace repo first, then the machine's known checkout
  (`C:\Users\User\Desktop\Learn` on the owner's machine). If neither exists, **stop and
  ask for the path**. Never guess one, never create one.

## Step 1 — inventory and manifest

Glob the vault (`artifacts/`, `notes/`, `MOCs/`, `assets/`) and read `index.md`.

Scope: the **whole vault** by default; `/empty-vault <topic>` limits it to one topic —
that MOC's artifacts, notes, and assets only.

Build and show a manifest before anything moves:

- **artifacts** → each handed to `digest-report` (becomes a Learn topic + atomic notes).
- **notes** → handed along with their MOC's artifacts as supplementary source material
  for the same Learn topic; an orphan note with no artifact is digested as a small topic
  of its own.
- **infographic assets** (a self-contained `.html` one-pager, typically from the
  `clinical-infographic` skill) → these DO migrate: each is handed to the Learn repo's
  **`ingest-infographic`** skill (Step 2) and becomes an `infographics` row that shows up in
  the app's Infographics gallery + on its topic page. Pair each infographic to its **source
  report** via the MOC `## Assets` entry ("Source of truth is [[<report>]]") or the HTML's
  leading `Rendered from:` comment — that report's Learn topic is what the infographic attaches
  to. An infographic whose source report is out of scope (or failed to digest) is NOT migrated.
- **binary assets** (`.png`/`.jpg` previews, and any other non-HTML binary) → cannot render
  in the app. They are *removed with their topic* and remain recoverable from git history. A
  `.preview.png` sitting next to a migrated infographic is one of these — the app renders the
  live HTML, not the raster. Name every binary asset in the manifest — they never vanish silently.
- **MOCs + index.md** → not transferred (navigation, not content); pruned/rebuilt in
  Step 5.

## Step 2 — hand off to the Learn repo's ingestion skills

Two handoffs, both into learn-hub — never author or write into the Learn repo's `vault/`
directly (that is the ingestion skills' job):

- **Reports → `digest-report`.** For each artifact in scope, invoke the Learn repo's
  **`digest-report`** skill with the absolute file path plus context: title, topic (its MOC),
  tags, `source` skill, `created`. One report at a time; collect each verification report
  (Learn topic id, note ids, notes written vs counted in Supabase, cache revalidated).
- **Infographics → `ingest-infographic`.** For each infographic HTML asset in scope, invoke
  the Learn repo's **`ingest-infographic`** skill with the absolute `.html` path plus its
  source report (so it resolves the target topic + `source` provenance). Run this **after** the
  source report's `digest-report` handoff, since the infographic's `topic_id` is a foreign key
  onto the topic that report creates. Collect each verification (infographic id, topic id, html
  bytes landed, revalidated). The `ingest-infographic` skill owns the light-lock normalisation
  and the sidecar authoring — do not write the sidecar yourself.

Do **not** author, summarize, or reshape the notes/infographics yourself.

## Step 3 — verify the landing

A report counts as **landed** only when digest-report's handshake confirms it: notes
written == notes counted in Supabase for that report's provenance (`sources[]` carries
the artifact basename). An infographic counts as **landed** only when ingest-infographic's
handshake confirms its `infographics` row exists with the expected `topic_id` and a
non-blank `html`. Any report or infographic that did not verify stays out of the deletable
set — no exceptions. A binary asset (PNG) is deletable only once the topic it belongs to has
landed.

## Step 4 — the deletion gate (double-gated)

Only files whose reports/infographics landed are deletable (a binary asset rides with its
topic). Before deleting anything:

1. **Git gate** — every file about to be deleted must be committed. Deleting uncommitted
   vault content is unrecoverable loss; offer the commit first if needed.
2. **User gate** — show exactly what will be deleted (files, MOC entries, and every
   asset by name) and get an explicit yes. "Empty the vault" starts the pipeline; the
   delete still needs its own confirmation here.

## Step 5 — empty and reindex

Delete the verified files (artifacts, their notes, and their assets — the migrated
infographic HTML once its `infographics` row verified, and the binary previews that rode
with the landed topic). Prune the moved entries from their MOCs; a MOC left with no entries
is deleted too. Rebuild `index.md` exactly per
vault-keeper's **index** job (deterministic rebuild, alphabetical). A whole-vault empty
returns `index.md` to the empty scaffold (`# Vault Index` + empty MOC list); the
`.gitkeep` files stay so the tree survives.

## Step 6 — report

Close with the ledger: what moved (vault report → Learn topic + note ids; vault infographic
→ `infographics` row), what was deleted, and what stayed (failed verification or out of
scope) with the reason. Stop before committing — the commit is the user's call.

## Rules

- **Move first, delete last.** Nothing is deleted that did not verifiably land in the
  Learn hub.
- **Never distill or author.** `digest-report` owns note authoring, `ingest-infographic`
  owns infographic filing + light-locking; this skill only inventories, hands off, verifies,
  deletes, and reindexes.
- **Infographics migrate, only true binaries are dropped.** A self-contained `.html`
  infographic goes to `ingest-infographic` and lands as an `infographics` row; only
  non-renderable binaries (PNG previews, etc.) are removed with their topic. Never delete an
  infographic HTML as if it were a binary — that is the bug this pipeline exists to prevent.
- **Double gate on every delete** — committed to git AND explicitly confirmed.
- **Partial failure → partial empty.** Verified reports/infographics are removed, failed
  ones stay, and the report says which and why.
- **One vault**, resolved per Step 0. Touch nothing outside it except the handoff into
  the Learn repo's skills.
- **Scope is sacred.** A topic-scoped run never touches the other MOCs' content.

## Failure conditions

This skill has failed if:

- A vault file was deleted before its report/infographic verified in Supabase, or without
  the git gate and the explicit user confirmation.
- An infographic HTML asset was deleted (as a binary) instead of being migrated to the hub
  via `ingest-infographic`, or was deleted before its `infographics` row verified.
- It authored/distilled Learn notes itself, or wrote into the Learn repo's `vault/`
  directly instead of invoking `digest-report` / `ingest-infographic`.
- The Learn repo root was guessed or created instead of found or asked for.
- A MOC or `index.md` was left pointing at deleted files, or a surviving file became
  unreachable from `index.md`.
- The whole vault was emptied when the user scoped to one topic (or vice versa).
- An asset was deleted without being named in the manifest and the deletion gate.
