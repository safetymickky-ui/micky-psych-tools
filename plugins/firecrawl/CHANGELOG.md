# Changelog

## 0.1.0 — 2026-07-13

Initial release. Packages Firecrawl's official AI-onboarding guide as a marketplace
skill: the one-command install (`npx -y firecrawl-cli@latest init --all --browser`),
the three vendor skill segments (CLI / build / workflow), and the six usage paths —
live web tools, app-code integration, repeatable deliverables, account/API-key auth,
REST-only, and the keyless free-tier fallback. Two local adaptations: the frontmatter
description gained this marketplace's Use-when / Not-for trigger clauses (biomedical
literature stays with the PubMed-facing plugins), and the vendor doc's session-specific
API-key block was replaced by a credentials-hygiene rule — keys live in the
environment, never in the repo. Ships the `firecrawl` skill only; no commands, agents,
or MCP wiring.
