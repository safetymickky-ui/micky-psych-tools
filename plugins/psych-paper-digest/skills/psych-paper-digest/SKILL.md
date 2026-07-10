---
name: psych-paper-digest
description: >-
  Sweeps every domain on the user's watchlist for literature published since the last sweep
  and delivers a triaged, read-once digest — practice-changing first, then worth-reading,
  plus registry trial readouts; noise suppressed with counts. Use when the user says "paper
  digest", "today's digest", "what's new in the literature", "anything new this week",
  "อัปเดตงานวิจัย", "มีเปเปอร์ใหม่ไหม", runs /digest, or asks to manage the watchlist ("add X
  to my watchlist", "show my watchlist"). Initializes its .psych-paper-digest.json config on
  first run. Triage only, never adjudication: each practice-changing item names the decision
  it raises and offers a pubmed-research-note handoff for the verdict-first report. NOT for:
  answering a clinical decision or researching one named topic (pubmed-research-note);
  non-biomedical monitoring (deep-research); writing into the vault directly (content is
  handed to vault-keeper on explicit request only).
---

# Watchlist → Radar Sweep

You are not reviewing the literature. You are answering one question: **did anything appear
since the last sweep that should change what the user does, prescribes, or teaches?** The
digest is read once over coffee and thrown away. On most sweeps the honest answer is
"nothing" — and an explicit all-clear is a successful digest, not a failed one.

## Prime directive — triage, never adjudicate

The failure mode this skill exists to prevent is **triage inflation**: padding the
practice-changing section so the sweep looks useful. The Act section spends the user's
clinical attention; when unsure between Act and Read, choose Read. When unsure between Read
and Suppressed, choose Suppressed.

The complementary rule: the digest never carries a verdict. It flags that a new result
*raises* a decision — whether that result should actually change practice, at what dose, for
whom, is adjudication, and adjudication belongs to `pubmed-research-note`. A digest item
that answers its own question has crossed into the wrong skill.

## Step 0 — Resolve the watchlist

Config is `.psych-paper-digest.json` in the working directory — schema, init flow, and
sanity rules in [references/config-schema.md](references/config-schema.md).

- **Present** → load `domains[]` (each: name, label, query, trials_term, floor, last_swept).
- **Absent** → run **init**: elicit 3–8 watchlist domains (when a vault exists, offer its
  MOC titles as candidates), confirm the drafted queries once, write the config with every
  `last_swept: null`, then run the inaugural sweep in the same turn.
- **Scoped run** — `/digest <domain>` or "sweep only X" limits the sweep to that domain;
  every other domain's `last_swept` is untouched.
- **Watchlist management** — "add X to my watchlist" / "remove X" / "show my watchlist"
  edits or prints the config and stops. No sweep unless one was asked for.

## Step 1 — Window

Per domain: `date_from = last_swept − 3 days` (indexing-lag overlap; dedup absorbs the
repeats), `date_to = today`.

- `last_swept: null` → 14-day inaugural window.
- `last_swept` more than 90 days old → sweep 90 days and name the cap in the digest header;
  the uncovered gap must be visible, not silently skipped.
- Never sweep without a window.

## Step 2 — Sweep two engines

Read [references/sweep-recipes.md](references/sweep-recipes.md) before the first call. The
plugin bundles both servers with stable prefixes — no ToolSearch hunt:
`mcp__plugin_psych-paper-digest_pubmed__<tool>` and
`mcp__plugin_psych-paper-digest_clinical-trials__<tool>`.

- **PubMed — publication radar.** One windowed query per domain at its evidence floor;
  screen titles/abstracts against the domain's clinical intent; fetch metadata (PMID → DOI)
  only for keepers.
- **ClinicalTrials.gov — readout radar.** Three events only: results newly posted; newly
  completed with nothing posted; newly terminated for futility or safety (accrual is noise).
- **Dedup** against the newest previous digest file (its DOIs/PMIDs/NCTs are the seen-ledger)
  and across domains (one appearance, under the domain where the item triages highest).
- **PubMed unreachable = fatal**: say so and stop — a registry-only digest misrepresents the
  window as quiet. Registry unreachable = degrade: sweep PubMed and name the registry gap in
  the digest header.

## Step 3 — Triage

Three tiers, full criteria and examples in
[references/triage-rubric.md](references/triage-rubric.md):

- **Act** — would change drug choice, dose, monitoring, a service decision, or a taught
  sentence for patients the user actually sees: reversals, guideline updates,
  regulator-grade safety signals, pivotal readouts. Floor: RCT / meta-analysis / guideline.
  **Hard cap 5** — more means the window was too long; keep the top 5 by clinical
  consequence and say the cap bit.
- **Read** — solid new in-domain evidence that informs but changes nothing yet.
  Confirmatory positives live here, never in Act.
- **Suppressed** — below floor or off-domain. Counted per domain, never listed.

## Step 4 — Render, then mark swept

Write `digest-YYYY-MM-DD.md` (collision → ` -2`, never overwrite) to the working directory
or `digest_dir` from config. Then — and only then — set each swept domain's `last_swept` to
today. A failed or partial run leaves `last_swept` untouched so the next run re-covers the
window.

## The digest

```markdown
# Paper digest — YYYY-MM-DD
*window YYYY-MM-DD → YYYY-MM-DD · domains N · screened N → kept N · trials N*
*(name any capped window or unreachable registry here — one clause)*

## Act
- **<claim with its one number — design, n>** — why it matters to <domain>; raises: <the
  decision it raises, phrased as a question>. → full report: pubmed-research-note.
  [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)

(empty → the single line: "Nothing practice-changing this window — all clear.")

## Read
- **<claim with its number>** — one clause on what it adds to <domain>.
  [doi:10.xxxx/yyyy](https://doi.org/10.xxxx/yyyy)

## Registry watch
- NCT NNNNNNNN — <results posted | completed unpublished | terminated-futility>, n=NNN,
  <readout or completion date>, <domain>.

## Suppressed
- <domain>: N below floor · <domain>: N below floor
```

Item discipline, inherited from the house citation contract: **every item carries its
number** (effect size, n, or event rate — "positive trial" is a failure); the link is the
DOI and nothing else — no authors, journal, year, or PMID in the digest body; NCT entries
carry status and n. No sub-headings inside any section; no per-domain H3 ladders — the tier
is the structure, the domain is a word inside the item.

## Where output goes

1. **Default:** the digest file lands in the working directory, or `digest_dir` from config.
2. **Vault, only on explicit request** ("vault this digest"): hand title, body, target
   type `artifact`, and a suggested MOC topic to the **vault-keeper** skill — it owns paths,
   dedup, MOC wiring, and the index. Never resolve a vault path or write into `vault/` from
   this skill.
3. **No filesystem:** render the digest inline, state that nothing was written and that
   `last_swept` was not advanced.

Never fabricate a write, a path, or an advanced watchlist state.

## Handoffs

- **pubmed-research-note** — the adjudicator. Every Act item ends with the handoff; when the
  user takes it, pass the raised decision (the question the item names) as the seed. Never
  run the decision report inside the digest.
- **vault-keeper** — vault saves, on request only, per Where output goes.
- **intent-lock — deliberately not chained.** A sweep has no decision to lock; the only
  elicitation this skill owns is init's watchlist interview.

## Close

Two lines in chat: the file written, `domains N · kept N of N screened · trials N`, the Act
count (or the all-clear), and any engine gap or capped window. Append a watchlist-health
nudge only when [references/config-schema.md](references/config-schema.md) sanity rules
fire (a starved or flooding domain). The digest file is the deliverable — never restate it
inline.

## Failure conditions

This skill has failed if:

- An Act item would not change action for a patient population the user actually sees
  (triage inflation).
- Any item, in any tier, lacks a number.
- The digest carries a verdict, a dose recommendation, or an adjudication between trials.
- An empty Act section is padded, apologized for, or missing its explicit all-clear line.
- A suppressed item is listed, or suppression happens without a per-domain count.
- The sweep ran unwindowed, or `last_swept` advanced after a failed or partial run, or a
  scoped run advanced an unswept domain.
- A vault path was resolved or written by this skill instead of vault-keeper.
- The registry went unswept without the gap being named in the digest header.
- A decision question ("should I…", "is X better than Y…") was answered with a digest
  instead of routing to pubmed-research-note.
- The previous digest was not checked and an already-delivered item reappeared as new.
- An author, journal name, year, or PMID appeared in the digest body.
