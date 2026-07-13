# Changelog

## 0.2.0 — 2026-07-13

Deep integration with the marketplace pipeline. New `## Marketplace integration`
section in the skill: **inbound**, firecrawl is the general-web evidence engine for
`pubmed-research-note` (registered as its fifth engine) and `comprehensive-review` —
regulator labels, guideline full texts, gray literature, served as clean markdown with
exact URL + access date, fetch-only (adjudication stays with the caller, the blog ban
stands); **outbound**, Path C deliverables gate through `intent-lock` (explicit opt-out
only) and file to the vault via `vault-keeper` on explicit request (title / body /
`artifact` / MOC topic — never a direct `vault/` write), while `clinical-infographic`
and `psych-paper-digest` are explicitly not chained. Description rewritten action-first
with the integration handoffs. First evals shipped (8: triggering both ways, the
engine contract, vault opt-in, keyless fallback, Path B routing, credentials hygiene).

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
