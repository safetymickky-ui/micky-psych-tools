# psych-paper-digest

Multi-domain literature surveillance on a personal watchlist. Each run sweeps PubMed and
ClinicalTrials.gov for what appeared **since the last sweep** and delivers a triaged,
read-once digest. The digest is a radar screen, not a review: its one question is *did
anything appear that should change what you do, prescribe, or teach?* — and on most sweeps
the honest, explicit answer is "nothing".

## Radar, not adjudicator

This plugin fills the temporal gap next to `pubmed-research-note`:

| | pubmed-research-note | psych-paper-digest |
|---|---|---|
| Trigger | a decision you're about to make | time passing |
| Scope | one question, searched deep | every watchlist domain, swept shallow |
| Output | verdict-first decision report | triaged digest |
| Adjudicates? | yes — that is its job | **never** — it names the decision an item raises and hands it off |

Every practice-changing item in the digest ends with a handoff: run `pubmed-research-note`
on the decision it raises to get the full verdict-first report.

## The three tiers

- **Act** — would change drug choice, dose, monitoring, a service decision, or a taught
  sentence: reversals, guideline updates, regulator-grade safety signals, pivotal
  readouts. Design floor RCT/meta-analysis/guideline; hard cap 5 per digest.
- **Read** — solid new in-domain evidence that informs but changes nothing yet.
- **Suppressed** — below floor; counted per domain, never listed.

An empty Act section renders as an explicit all-clear line — that is the rubric working.
Full criteria: `skills/psych-paper-digest/references/triage-rubric.md`.

## Config

`.psych-paper-digest.json` in the working directory holds the watchlist (3–8 domains, each
with a PubMed query, a ClinicalTrials.gov term, an evidence floor) and per-domain
`last_swept` state. First run with no config triggers an init interview — when a vault
exists, its MOC titles are offered as watchlist candidates. Schema and rules:
`skills/psych-paper-digest/references/config-schema.md`.

`last_swept` is written only by the skill, only after a digest file is written — a failed
run re-covers its window next time. Sweeps window from `last_swept − 3 days` (indexing-lag
overlap), capped at 90 days; the previous digest file doubles as the dedup ledger.

## Scheduling

Claude Code has no built-in cron for skills; schedule the trigger outside and let the
window logic absorb any drift — the sweep covers *since last swept*, so missed days are
caught up automatically:

- **system cron / launchd:** `0 7 * * 1,4 cd ~/clinic && claude -p "/digest"` (Mon + Thu, 07:00)
- **Claude Code on the web:** a Routine that sends `/digest` into a session on this repo.
- **Manual:** `/digest` any time; `/digest <domain>` scopes to one domain.

## MCP setup

The plugin bundles two servers in its own `.mcp.json`, with stable tool prefixes — no
ToolSearch hunt:

| Server key | Backing | Stable tool prefix |
|---|---|---|
| `pubmed` | `https://pubmed.mcp.claude.com/mcp` | `mcp__plugin_psych-paper-digest_pubmed__<tool>` |
| `clinical-trials` | `https://hcls.mcp.claude.com/clinical_trials/mcp` | `mcp__plugin_psych-paper-digest_clinical-trials__<tool>` |

PubMed unreachable (MCP **and** E-utilities fallback) is fatal — the skill says so and
stops rather than shipping a registry-only digest. Registry unreachable degrades: PubMed
still sweeps and the gap is named in the digest header.

## Vault handoff

The digest lands in the working directory (or `digest_dir` from config). Only on explicit
request ("vault this digest") is it handed to the **vault-keeper** skill as an artifact —
vault-keeper owns paths, dedup, MOC wiring, and the index. This skill never writes into
`vault/` itself.

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install psych-paper-digest@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install psych-paper-digest@micky-psych-tools
```
