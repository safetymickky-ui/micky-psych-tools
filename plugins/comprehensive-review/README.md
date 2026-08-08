# comprehensive-review

Write a comprehensive, textbook-chapter academic review of a whole psychiatric disorder or
topic from primary literature — the chapter a good textbook would carry if it were
rewritten from this year's papers. The deliverable is an md file filed to the vault via
vault-keeper under the disorder's MOC; chat gets a two-line Close, not the chapter.

## Components

- **`comprehensive-review` skill** — the whole procedure: intent-lock gate → coverage map
  + designed outline → per-domain PubMed/CT.gov search → write → file via vault-keeper.
- **`/comprehensive-review [disorder or topic]`** — the manual trigger for the skill.

## Coverage is the contract, structure is yours

Ten coverage domains — definition & nosology, epidemiology, etiology & pathophysiology,
clinical features & course, diagnosis & assessment, differential & comorbidity, treatment
across all modalities, special populations, prognosis, controversies & future directions —
must each be covered somewhere in the chapter or consciously excluded and named in the
preface. The **structure** that carries them is designed per topic: reorder, split, merge,
rename, nest freely; sub-headings anywhere they help. The one structural rule: treatment
never absorbs the review. The failure mode the skill exists to prevent is *silent
narrowing* — a "comprehensive review" that quietly becomes a treatment essay.

## The depth contract

Load-bearing studies get the full per-study treatment (design, population, n, comparator,
endpoint, effect size with CI — a developed paragraph each); mechanism and background are
woven in; sources are capped by relevance, never by count. A long section is subdivided,
not amputated. Full guide: `skills/comprehensive-review/references/review-arc.md`.

## Boundaries

- A single clinical decision ("should I use X for Y?") belongs to **pubmed-research-note**
  — the review reports the evidence landscape but never issues a patient-level verdict.
- Watchlist surveillance belongs to **psych-paper-digest**.
- Every vault write goes through **vault-keeper** — this skill never resolves vault paths.
- Guideline/regulator full texts outside PubMed/CT.gov are fetched via the **firecrawl**
  plugin.

## MCP setup

This plugin bundles two MCP servers in its own `.mcp.json`:

| Server key | Backing | Stable tool prefix |
|---|---|---|
| `pubmed` | `https://pubmed.mcp.claude.com/mcp` | `mcp__plugin_comprehensive-review_pubmed__<tool>` |
| `clinical-trials` | `https://hcls.mcp.claude.com/clinical_trials/mcp` | `mcp__plugin_comprehensive-review_clinical-trials__<tool>` |

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install comprehensive-review@micky-psych-tools
```
