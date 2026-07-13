# firecrawl

Firecrawl onboarding and routing docs, packaged as a marketplace skill. Firecrawl gives
agents fast, reliable web context — search first, scrape clean markdown, interact with
live pages when plain extraction is not enough, and produce finished deliverables from
web data.

The skill body is Firecrawl's official AI-onboarding guide
(https://docs.firecrawl.dev/ai-onboarding), kept verbatim so it stays a faithful map of
the vendor's install command, skill segments, and usage paths.

## What it routes

| Path | Use it when |
|---|---|
| A — Live web tools | the agent needs web data during this session (search / scrape / interact / crawl / map) |
| B — App integration | Firecrawl is being wired into product code with the SDK + `FIRECRAWL_API_KEY` |
| C — Repeatable deliverables | the goal is a finished artifact (research brief, SEO audit, lead list, knowledge base) |
| D — Account / API key | the human still needs to sign up, sign in, or authorize a key |
| E — REST API directly | nothing should be installed; call `https://api.firecrawl.dev/v2` |
| F — Keyless free tier | no key is obtainable right now (rate-limited fallback) |

One command installs the CLI plus all three vendor skill segments:

```bash
npx -y firecrawl-cli@latest init --all --browser
```

## Deep integration with the pipeline

Firecrawl is the marketplace's **general-web engine** — the complement to the
PubMed/ClinicalTrials.gov pipeline, never its replacement:

| Direction | Contract |
|---|---|
| Inbound — engine for the research plugins | `pubmed-research-note` (fifth engine in its tool catalog) and `comprehensive-review` call it for documents outside PubMed/CT.gov: regulator labels (FDA/EMA/MHRA), guideline full texts (NICE/APA/WFSBP), gray literature. Served as clean markdown + exact URL + access date; fetch only — adjudication stays with the caller, the blog ban stands. |
| Outbound — intent-lock | Path C's "confirm the workflow and final artifact" step runs through the `intent-lock` skill (explicit opt-out only), like every other deliverable-producing plugin. |
| Outbound — vault-keeper | On an explicit "vault this", a finished deliverable is handed to `vault-keeper` (title, body, target type `artifact`, suggested MOC topic) — never a direct `vault/` write. Opt-in, same rule as psych-paper-digest. |
| Not chained | `clinical-infographic` renders sourced clinical reports only; `psych-paper-digest` sweeps PubMed + CT.gov by contract. |

## Boundaries in this marketplace

- **Biomedical literature is not Firecrawl's job here** — PubMed / ClinicalTrials.gov
  questions belong to `pubmed-research-note`, `comprehensive-review`, and
  `psych-paper-digest`. Firecrawl covers the general web, and serves those plugins as an
  engine rather than replacing them. Mixed requests are split, not grabbed.
- **Keys never enter the repo.** `FIRECRAWL_API_KEY` lives in the environment. The
  vendor doc's session-specific key block is deliberately not part of the skill; a key
  that appears in chat or a document is exposed — rotate it in the dashboard.

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install firecrawl@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install firecrawl@micky-psych-tools
```
