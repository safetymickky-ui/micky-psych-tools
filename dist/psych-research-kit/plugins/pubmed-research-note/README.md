# pubmed-research-note

Research a psychiatry or biomedical topic from primary literature and get back a
verdict-first, quantified evidence report — not an encyclopedia article. The report answers
a decision, then is thrown away; vault notes are opt-in, produced only on request.

## The decision brief — built, not chosen

There is no fixed set of frames. Every request is turned into a bespoke **decision brief**
before any search runs, built fresh from the same anatomy every good decision shares
(`skills/pubmed-research-note/references/decision-brief.md`):

- **The decision** — what the user will do differently, in one sentence. Never the topic.
- **The verdict's shape** — what a good answer physically looks like for *this* decision (a
  dose + what not to promise; a build/don't + conditions in the service's units; a
  true/false/unsettled + why; a sentence you can say aloud + its expiry; a probability + a
  threshold). Named for the request, not picked from a list.
- **What settles it / what must be counted** — the load-bearing evidence and the numbers the
  verdict is hollow without.
- **Mandatory checks** — the publication-bias sweep when an action or a claim's live status
  is at stake; the textbook edition when the decision is what to teach.
- **The anti-goal** — the specific way this report would satisfy the words and still fail.

The decision-lock gate runs first on every request — the `intent-lock` plugin when installed,
otherwise a short built-in interview — and fixes the *what-the-user-wants* half of the brief;
the skill derives the evidence-side slots. If a request names a topic with no decision,
or carries two readings that tie on cost, the interview is where that gets settled rather than
guessed — see `skills/pubmed-research-note/references/intent-lock-pairing.md`.

## The report — shaped to the decision

There is no fixed template either. The report is the verdict shown its working, and it takes
whatever shape carries *this* decision from evidence to action in the fewest sections that
earn their place — headings minted from the decision, never the topic; verdict first; numbers
in every section; disagreements adjudicated, not listed; as long as the decision needs and no
longer. The full guide is `skills/pubmed-research-note/references/report-craft.md`.

## Source engines

Four engines, four jobs — PubMed (backbone), ClinicalTrials.gov (publication-bias check),
Open Library (textbook-vs-evidence gap), Wikipedia (terminology only, never cited). Full
tool reference: `skills/pubmed-research-note/references/tool-catalog.md`.

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

This skill never resolves vault paths, dedup-greps, or writes YAML frontmatter itself. When
the user asks to save the report into the vault, or says "atomize" / "ทำโน้ต" to produce
atomic notes, the skill hands the content to the **vault-keeper** skill — title, body,
target type (note/artifact), suggested MOC topic, source-skill tags, and any optional extra
frontmatter fields (sources, board_pearls, review_count, last_reviewed, aliases) as a flat
map. `vault-keeper` owns paths, dedup, MOC wiring, and the index, and reports back where the
content landed.

If vault-keeper is not installed (a standalone install of this kit), the vault step is simply
skipped — reports stay in the working directory and are shown inline; requested atomic notes
are written as plain md files there too.

## Install

From the psych-research-kit folder (see the kit's root README for the full walkthrough):

```
/plugin marketplace add <path-to>/psych-research-kit
/plugin install pubmed-research-note@micky-psych-research-kit
```
