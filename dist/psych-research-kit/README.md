# psych-research-kit

A two-plugin Claude kit by **Thanawat Suharit (Micky)**:

| Plugin | What it does |
|---|---|
| **pubmed-research-note** | Researches a clinical question from primary literature (PubMed + ClinicalTrials.gov) and delivers a **verdict-first, quantified evidence report** — an answer to your decision, not an encyclopedia article. |
| **clinical-infographic** | Turns a sourced evidence report into a **professional, print-ready medical summary infographic** — one self-contained HTML file with color-coded columns, stat tiles, and a mandatory "medications to avoid" safety banner. If no report exists yet, it runs pubmed-research-note first — it never invents a clinical fact. |

They chain naturally: *ask a clinical question → get a sourced report → "make an
infographic of it" → get a printable one-pager.*

## Install in Claude Code (recommended)

1. Unzip this kit anywhere, e.g. `~/psych-research-kit`.
2. In Claude Code, add it as a plugin marketplace and install both plugins:

```
/plugin marketplace add ~/psych-research-kit
/plugin install pubmed-research-note@micky-psych-research-kit
/plugin install clinical-infographic@micky-psych-research-kit
```

3. Restart the session if prompted. `pubmed-research-note` bundles its own MCP servers
   (hosted PubMed and ClinicalTrials.gov at `*.mcp.claude.com`) — approve them when Claude
   Code asks; no API keys needed.

Try it:

```
research whether prazosin is still first-line for PTSD nightmares
/infographic the report above
```

## Use in the Claude app (claude.ai / desktop)

The Claude app takes **skills** rather than plugin marketplaces. Zip each skill folder and
upload it under **Settings → Capabilities → Skills**:

- `plugins/pubmed-research-note/skills/pubmed-research-note/`
- `plugins/clinical-infographic/skills/clinical-infographic/`

(Or use the pre-built per-skill zips if they were sent alongside this kit.) In the app,
enable web search — the research skill falls back to it when the PubMed connector is not
available. The `/infographic` slash command and auto-configured MCP servers are Claude
Code features; in the app just ask in plain words ("make an infographic of this report").

## Standalone notes

These two plugins were extracted from a larger personal marketplace. In their home they
chain to two companions — `intent-lock` (a pre-research interview) and `vault-keeper` (a
knowledge-vault filer). This kit's copies degrade gracefully without them:

- **No intent-lock** → the research skill asks you the few questions needed to lock the
  decision itself, then searches.
- **No vault-keeper** → reports and infographics are simply written to your working
  directory (and shown to you); no vault filing is attempted.

Everything else — the verdict-first report discipline, the citation rules, the infographic
fidelity contract and safety banner — is unchanged from the source plugins
(pubmed-research-note 1.5.0, clinical-infographic 0.2.0).

## Disclaimer

Output is a clinical reference aid, not a substitute for clinical judgment or local
protocol. Reports cite their sources (DOIs / NCT numbers) — audit them before acting.
