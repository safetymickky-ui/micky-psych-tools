---
name: empty-vault
description: >-
  Drains the shared vault at the marketplace repo root (vault/) into the Learn hub:
  inventories artifacts, notes, and assets; hands each report to learn-hub's
  digest-report skill (atomic Learn notes synced to Supabase), each infographic HTML
  asset to ingest-infographic, and each animation HTML asset to ingest-animation; and
  only after those verified syncs deletes the moved files, prunes their MOCs, and
  rebuilds index.md — leaving a clean scaffold. Use when the user
  says "empty the vault", "drain the vault", "clear the vault", "move the vault to the
  Learn hub", "export the vault to learn-hub", "ship these reports to the hub", or asks
  to migrate vault content into Learn (Thai: "ล้าง vault", "ย้าย vault ไป Learn"). Scope
  to one topic with /empty-vault [topic]. Deletion is double-gated (git-committed +
  explicit confirm), never before the Learn-side sync verifies. NOT for filing,
  indexing, or finding vault content (vault-keeper), and NOT the authoring —
  learn-hub's skills own the distillation and ingestion.
---

# Empty Vault — drain it into the Learn hub, then wipe it clean

The vault accumulates finished research — evidence reports, reviews, infographic and
animation assets — whose long-term home is the **Learn hub** (`learn-hub` repo), where
each report becomes a chapter of atomic, learnable notes with graph, mastery, and spaced
review, and each rendered HTML asset becomes a row in the app's Visualizations gallery.
Emptying the vault is a three-beat move: **move → verify → delete**, in that order, never
reordered. Git history is the archive — nothing is ever truly lost, but only if the
delete happens on committed state.

Like vault-keeper, this skill is a librarian, not an author. **It moves and erases; it
never distills and never ingests by hand.** The Learn-side writing is owned by the Learn
repo's skills: `digest-report` (report → atomic notes), `ingest-infographic`
(infographic HTML → `infographics` row), `ingest-animation` (animation HTML →
`animations` row).

## Step 0 — resolve BOTH roots

- **Psych vault root** — exactly as vault-keeper's Step 0: walk up from cwd to the
  directory containing `.claude-plugin/marketplace.json`, append `vault/`, use the
  absolute path everywhere.
- **Learn repo root** — the `learn-hub` checkout: the directory containing
  `.claude/skills/digest-report/` (plus `ingest-infographic/`, `ingest-animation/`,
  `vault/`, and `scripts/sync-vault.mjs`). Look for a sibling checkout of this
  marketplace repo first, then the machine's known checkout
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
- **assets** → routed **by kind** — name every asset in the manifest with its routing;
  they never vanish silently:
  - **infographic HTML** (a static, print-ready one-pager, no scripts — typically from
    `clinical-infographic`) → handed to learn-hub's `ingest-infographic` skill (becomes
    an `infographics` row on its Learn topic).
  - **animation HTML** (a self-contained document that *plays* — inline JS scene
    controller, player controls, reduced-motion fallback — typically from
    `concept-animation`) → handed to learn-hub's `ingest-animation` skill (becomes an
    `animations` row on its Learn topic).
  - **everything else** (preview `.png`s, decks, other binaries) → cannot enter the hub.
    *Removed with their topic*, recoverable from git history. A `.preview.png` companion
    of an ingested HTML asset is a share/export artifact — the ingest skills do not take
    it; it is deleted here with its topic.

  Route by what the document **is**, not its filename: a scripted, playing document is
  an animation; a static sheet is an infographic. The two land in different tables with
  different render sandboxes — the wrong skill means the wrong sandbox.
- **MOCs + index.md** → not transferred (navigation, not content); pruned/rebuilt in
  Step 5.

## Step 2 — hand off to the Learn repo's skills

**Reports first, then assets.** An asset's Learn row needs its topic to already exist
(FK), and the topic is created by digesting the report — so never ingest an asset before
its topic's report has landed.

1. For each artifact in scope, invoke the Learn repo's **`digest-report`** skill with the
   absolute file path plus context: title, topic (its MOC), tags, `source` skill,
   `created`. One report at a time; collect each verification report (Learn topic id,
   note ids, notes written vs counted in Supabase, cache revalidated).
2. For each HTML asset in scope, invoke **`ingest-infographic`** or **`ingest-animation`**
   (per the manifest's routing) with the absolute file path plus context: title, the
   source report/concept, and the Learn topic id from step 1 (or the already-existing
   topic for an asset whose report was digested on an earlier run). Collect each
   ingest handshake.

Do **not** author, summarize, or reshape the notes yourself, do not inline or edit the
asset HTML, and do not bypass the Learn skills by writing into the Learn repo's `vault/`
directly.

## Step 3 — verify the landing

- A **report** counts as **landed** only when digest-report's handshake confirms it:
  notes written == notes counted in Supabase for that report's provenance (`sources[]`
  carries the artifact basename).
- An **HTML asset** counts as **landed** only when its ingest skill's handshake confirms
  it: the row's id + topic id + a non-trivial `html` byte count verified in the
  `infographics` / `animations` table.

Anything that did not verify stays out of the deletable set — no exceptions. If a
report failed, its topic's assets are not ingested (no topic to attach to) and stay in
the vault with it.

## Step 4 — the deletion gate (double-gated)

Only files whose reports (or, for HTML assets, whose ingest handshakes) landed are
deletable. Before deleting anything:

1. **Git gate** — every file about to be deleted must be committed. Deleting uncommitted
   vault content is unrecoverable loss; offer the commit first if needed.
2. **User gate** — show exactly what will be deleted (files, MOC entries, and every
   asset by name) and get an explicit yes. "Empty the vault" starts the pipeline; the
   delete still needs its own confirmation here.

## Step 5 — empty and reindex

Delete the verified files (artifacts, their notes, their assets). Prune the moved entries
from their MOCs; a MOC left with no entries is deleted too. Rebuild `index.md` exactly per
vault-keeper's **index** job (deterministic rebuild, alphabetical). A whole-vault empty
returns `index.md` to the empty scaffold (`# Vault Index` + empty MOC list); the
`.gitkeep` files stay so the tree survives.

## Step 6 — report

Close with the ledger: what moved (vault file → Learn topic + note ids; asset → Learn
`infographics`/`animations` row id), what was deleted, and what stayed (failed
verification or out of scope) with the reason. Stop before committing — the commit is
the user's call.

## Rules

- **Move first, delete last.** Nothing is deleted that did not verifiably land in the
  Learn hub.
- **Never distill, never ingest by hand.** digest-report owns the note authoring;
  ingest-infographic / ingest-animation own the asset ingestion; this skill only
  inventories, hands off, verifies, deletes, and reindexes.
- **Route assets by kind.** Scripted, playing HTML → ingest-animation; static sheet →
  ingest-infographic. Never swap them — the two render under different sandboxes.
- **Double gate on every delete** — committed to git AND explicitly confirmed.
- **Partial failure → partial empty.** Verified reports/assets are removed, failed ones
  stay, and the report says which and why.
- **One vault**, resolved per Step 0. Touch nothing outside it except the handoffs into
  the Learn repo's skills.
- **Scope is sacred.** A topic-scoped run never touches the other MOCs' content.

## Failure conditions

This skill has failed if:

- A vault file was deleted before its report — or, for an HTML asset, its ingest
  handshake — verified in Supabase, or without the git gate and the explicit user
  confirmation.
- It authored/distilled Learn notes or ingested/edited asset HTML itself, or wrote into
  the Learn repo's `vault/` directly instead of invoking digest-report /
  ingest-infographic / ingest-animation.
- An animation was handed to ingest-infographic, or an infographic to ingest-animation.
- The Learn repo root was guessed or created instead of found or asked for.
- A MOC or `index.md` was left pointing at deleted files, or a surviving file became
  unreachable from `index.md`.
- The whole vault was emptied when the user scoped to one topic (or vice versa).
- An asset was deleted without being named in the manifest and the deletion gate.
