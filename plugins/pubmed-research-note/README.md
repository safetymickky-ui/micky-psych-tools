# pubmed-research-note

Research a psychiatry or biomedical question from primary literature and get back a
quantified, adjudicated evidence report with a clearly marked verdict and the full evidence
behind it — shown inline and filed to the vault by default; atomic notes are opt-in,
produced only on "atomize". The report takes whatever shape serves the question —
decision-shaped, topic-shaped, or mixed — and load-bearing studies are reported in full
per-study detail, never compressed to clauses.

## The decision brief — built, not chosen

There is no fixed set of frames. Every request is turned into a bespoke **decision brief**
before any search runs, built fresh from the same anatomy every good decision shares
(`skills/pubmed-research-note/references/decision-brief.md`):

- **The question** — what the user will do, or understand, differently, in one sentence.
  Never a bare topic.
- **The verdict's shape** — what a good answer physically looks like for *this* decision (a
  dose + what not to promise; a build/don't + conditions in the service's units; a
  true/false/unsettled + why; a sentence you can say aloud + its expiry; a probability + a
  threshold). Named for the request, not picked from a list.
- **What settles it / what must be counted** — the load-bearing evidence and the numbers the
  verdict is hollow without.
- **Mandatory checks** — the publication-bias sweep when an action or a claim's live status
  is at stake; the textbook edition when the decision is what to teach.
- **The anti-goal** — the specific way this report would satisfy the words and still fail.

`intent-lock` runs first on every request and fixes the *what-the-user-wants* half of the
brief; the skill derives the evidence-side slots. If a request names a topic with no decision,
or carries two readings that tie on cost, the interview is where that gets settled rather than
guessed — see `skills/pubmed-research-note/references/intent-lock-pairing.md`.

## The report — shaped to serve the question

There is no fixed template and no mandated shape. The report is the answer shown its
working, at the depth the evidence deserves: an explicit, marked verdict (leading or
closing — a skimmer finds it in seconds) with its confidence level; structure chosen per
report — topic-domain headings like *Mechanism* or *Adverse effects* are legitimate
whenever they organize the evidence best; numbers in every section, with load-bearing
studies given full per-study detail (design, population, n, comparator, endpoint, effect
size with CI); mechanism and background woven in wherever they illuminate; disagreements
adjudicated, not listed; sources capped by relevance, never by count. The full guide is
`skills/pubmed-research-note/references/report-craft.md`.

## Source engines

Five engines, five jobs — PubMed (backbone), ClinicalTrials.gov (publication-bias check),
Open Library (textbook-vs-evidence gap), Wikipedia (terminology only, never cited),
Firecrawl (general-web documents — regulator labels, guideline full texts, gray literature;
via the `firecrawl` plugin, cited with URL + access date). Full tool reference:
`skills/pubmed-research-note/references/tool-catalog.md`.

## MCP setup

This plugin bundles two MCP servers in its own `.mcp.json`:

| Server key | Backing | Stable tool prefix |
|---|---|---|
| `pubmed` | `https://pubmed.mcp.claude.com/mcp` | `mcp__plugin_pubmed-research-note_pubmed__<tool>` |
| `clinical-trials` | `https://hcls.mcp.claude.com/clinical_trials/mcp` | `mcp__plugin_pubmed-research-note_clinical-trials__<tool>` |

Unlike an externally-connected managed connector (whose prefix is a session-varying hash
you have to resolve with `ToolSearch`), these two prefixes are fixed by the plugin's own
name and server key — no hunting required. If PubMed is unreachable, the skill states that
and stops rather than downgrading the evidence base.

Open Library has **no MCP server wired by this plugin** — it is web-fallback only
(WebSearch/WebFetch), unless the user has separately connected an external Open Library
connector.

## Config: report destination

Drop a `.pubmed-research-note.json` in the working directory to redirect where reports are
written by default:

```json
{ "report_dir": "<path>" }
```

If absent, reports land in the working directory. See "Where output goes" in
`skills/pubmed-research-note/SKILL.md` for the full precedence (working directory /
`report_dir` → vault mode → no-filesystem inline render).

## Vault handoff

This skill never resolves vault paths, dedup-greps, or writes YAML frontmatter itself. The
finished report is handed to the **vault-keeper** skill as an artifact by default (skip only
on an explicit "don't vault this"); "atomize" / "ทำโน้ต" additionally produces atomic notes.
The handoff passes title, body, target type (note/artifact), suggested MOC topic,
source-skill tags, and any optional extra frontmatter fields (sources, board_pearls,
review_count, last_reviewed, aliases) as a flat map. `vault-keeper` owns paths, dedup, MOC
wiring, and the index, and reports back where the content landed.

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install pubmed-research-note@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install pubmed-research-note@micky-psych-tools
```
