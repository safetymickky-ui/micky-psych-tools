---
name: brainstorm
description: >-
  Runs a structured brainstorm session — grounds against what already exists, diverges
  wide, converges to the 3–7 ideas worth acting on — then routes every kept idea to the
  pipeline that owns its follow-through: clinical decisions to pubmed-research-note,
  whole-disorder reviews to comprehensive-review, watch-this-space items to
  psych-paper-digest, recurring-workflow tooling to plugin-creator, keep-this knowledge to
  vault-keeper, and things-to-learn to the Learn hub vault as sync-ready topic/note stubs.
  Use when the user says "brainstorm", "let's brainstorm", "help me brainstorm", "idea
  dump", "generate ideas", "what should I learn next", "what should I research next",
  "what am I missing", "ระดมสมอง", "ช่วยคิดไอเดีย", or runs /brainstorm. NOT for executing
  any idea it produces (each route's owner does that), not for narrowing an already-chosen
  task to one reading (that is intent-lock), and not for searching the literature
  (pubmed-research-note, psych-paper-digest).
---

# Brainstorm — diverge wide, converge hard, route everything

An idea that leaves the session without an owner is a lost idea. The deliverable is not
the pile — it is a short routed shortlist: 3–7 ideas, each handed to the pipeline that
owns its follow-through. The session generates freely in the middle, but it opens
grounded and it ends routed.

## Prime directive — route, never execute

The failure mode this skill exists to prevent is the **wall of options**: thirty
unweighted bullets the user has to triage themselves. The session does the converging.
The complementary rule: the session never *does* any idea. Running the PubMed search,
writing the review, scaffolding the plugin, syncing the hub — each belongs to the
route's owner. A brainstorm that starts executing has crossed into the wrong skill.

## Step 0 — Seed, and the not-a-brainstorm check

Read the seed (from `/brainstorm` or the conversation). If the request is a formed task
wearing brainstorm clothes, route it instead of brainstorming, and say so:

- "should I use X for Y", "does X work" — a decision → **pubmed-research-note**.
- "review topic X" → **comprehensive-review**; "anything new on X" → **psych-paper-digest**.
- a task already chosen that needs one precise reading → **intent-lock**.

This skill is deliberately NOT intent-lock gated: a brainstorm wants many readings, the
opposite of the lock. At most one clarifying question (what the ideas are *for*) when the
seed is opaque; otherwise start.

## Step 1 — Ground before generating

Ideas should extend what exists, not duplicate it. Scan whichever corpora are reachable,
read-only:

- **Marketplace vault** — MOC titles + recent notes via vault-keeper's query job.
- **Learn hub vault** — `vault/*/_topic.md` in the learn-hub checkout (locate it per
  [references/handoff-map.md](references/handoff-map.md)): topic slugs, domains, books.
  Thin or missing topics are prime seeds.
- **Watchlist** — `.psych-paper-digest.json` domains, if present.

Output: 3–6 one-line observations — what exists, what is thin, what is absent. A corpus
that is not reachable is named as unreachable; never fabricate an inventory.

## Step 2 — Diverge

- Quantity first: **15–30 ideas, one line each.** No evaluation, no killing, no
  paragraphs while generating.
- Force at least four lenses so the pile is not monochrome — default set: clinic
  (patient care), teaching, research, learning (what to master next), tooling/workflow.
  Swap lenses when the seed demands different ones; say which lenses ran.
- Include the ideas the grounding pass exposed (gaps, thin topics) alongside fresh ones.

## Step 3 — Converge

- Cluster the pile and name each cluster.
- Score within clusters against the user's real constraints — clinical impact, teaching
  value, effort — and keep **3–7 total**.
- Discards stay visible as per-cluster counts ("14 discarded across 4 clusters"), never
  itemized. Re-listing the pile defeats the point of converging.

## Step 4 — Route

Every kept idea gets three things: the idea (one line), its **owner** from
[references/handoff-map.md](references/handoff-map.md), and the **handoff seed** — the
first concrete step phrased in the owner's input language (a decision question for
pubmed-research-note, a topic for /comprehensive-review, a watchlist add, a /new-plugin
one-liner, a topic + notes outline for the Learn hub). Render as a table. Offer the
handoffs; take one only when the user picks it — and then the owner runs, not this skill.

## Step 5 — Where output goes

1. **Default:** the routing table inline in chat. No file.
2. **"vault this" / "save this session"** → hand title, body, type `artifact`, and a
   suggested MOC to **vault-keeper**. Never resolve a vault path or write `vault/` from
   this skill.
3. **A picked learning idea** ("scaffold X for the hub") → write Learn-hub topic/note
   **stubs** per the export contract in
   [references/handoff-map.md](references/handoff-map.md), then hand off to
   `/sync-vault` in that repo. Never run the sync, never touch Supabase, never call the
   revalidate webhook.

## Handoffs

- **pubmed-research-note** — kept decisions; seed = the decision question.
- **comprehensive-review** — kept whole-disorder/topic understanding; seed = the topic.
- **psych-paper-digest** — kept "keep an eye on X"; seed = "add X to my watchlist".
- **plugin-creator** — kept recurring-workflow tooling; seed = a /new-plugin one-liner.
- **vault-keeper** — session save, or a kept insight worth keeping as-is.
- **Learn hub (`/sync-vault`)** — kept things-to-learn; stubs per the export contract.
- **intent-lock** — when the user commits to building one kept idea, lock it first.

## Close

Two or three lines in chat: the seed, `N generated → K kept`, routes grouped by owner,
any unreachable corpus — and, if stubs were written, their paths plus the `/sync-vault`
reminder.

## Failure conditions

This skill has failed if:

- Ideas left the session without owners, or the "routing table" is just a list.
- More than 7 ideas were kept, or discards were itemized instead of counted.
- It executed a route: ran a literature search, wrote the review, scaffolded the plugin,
  ran the sync, or wrote Supabase.
- It wrote into either vault directly (the marketplace vault belongs to vault-keeper;
  Learn-hub stubs go only through the export contract, only for a picked idea).
- A grounding inventory was claimed for a corpus that was never read.
- A formed decision or task was brainstormed instead of routed (Step 0).
- The two vaults were confused — session output filed into the Learn hub, or Learn-hub
  frontmatter written into the marketplace vault.
