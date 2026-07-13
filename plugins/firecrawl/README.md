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

## Boundaries in this marketplace

- **Biomedical literature is not Firecrawl's job here** — PubMed / ClinicalTrials.gov
  questions belong to `pubmed-research-note`, `comprehensive-review`, and
  `psych-paper-digest`. Firecrawl covers the general web.
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
