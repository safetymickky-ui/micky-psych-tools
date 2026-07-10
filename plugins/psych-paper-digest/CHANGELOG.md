# Changelog

## 0.1.0 — 2026-07-10

Initial release. Watchlist-driven literature surveillance: windowed sweeps of PubMed
(publication radar, evidence-floor filtered) and ClinicalTrials.gov (readout radar —
results posted / completed-unpublished / futility-safety terminations), triaged into
Act / Read / Suppressed with a hard Act cap and an explicit all-clear line, rendered as a
dated read-once digest. Config + per-domain `last_swept` state in
`.psych-paper-digest.json` (init interview on first run, vault MOCs offered as watchlist
candidates); previous digest doubles as the dedup ledger. Triage only, never adjudication:
Act items name the decision they raise and hand off to `pubmed-research-note`; vault saves
delegate to `vault-keeper`; deliberately no `intent-lock` chaining. Ships the
`psych-paper-digest` skill, the `/digest [domain]` command, and bundled PubMed +
ClinicalTrials.gov MCP servers with stable prefixes.
