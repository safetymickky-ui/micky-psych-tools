# pubmed-research-note

Research a psychiatry or biomedical topic from primary literature and get back a
verdict-first, quantified evidence report — not an encyclopedia article. The report answers
a decision, then is thrown away; vault notes are opt-in, produced only on request.

## The four decision frames

Every request is classified into exactly one frame before any search runs. The frame picks
the verdict slot, the load-bearing evidence, and which engines are mandatory
(`skills/pubmed-research-note/references/decision-frames.md`):

- **Rx** — treatment choice for a patient in front of the user. Verdict: give / don't /
  give only if X fails first, with a dose and what NOT to promise.
- **Service** — whether to build, change, or fund a service or protocol. Verdict: build /
  don't / build-under-conditions, in throughput and staff-time units.
- **Truth** — whether a specific claim is real; settling a disagreement. Verdict: true /
  false / unsettled, plus why the disagreement exists.
- **Teaching** — what can be safely asserted out loud to trainees. Verdict: the exact
  sentence to speak, with its expiry conditions.

If a request names a topic with no decision attached, or two frames tie on cost, the skill
chains to the separately-installed `intent-lock` plugin rather than guessing — see
`skills/pubmed-research-note/references/intent-lock-pairing.md`.

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
