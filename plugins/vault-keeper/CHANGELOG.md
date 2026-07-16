# Changelog — vault-keeper

## 0.5.0 — 2026-07-16
- empty-vault now **migrates infographic assets** instead of deleting them as binaries.
  A self-contained `.html` infographic is handed to learn-hub's new `ingest-infographic`
  skill (→ an `infographics` row that surfaces in the app), paired to its source report's
  topic via the MOC `## Assets` provenance; the handoff runs after that report's
  `digest-report` so the topic FK exists. Only true binaries (PNG previews) are still
  dropped with their topic. Steps 1–6, rules, and failure conditions updated; the delete
  gate now waits on the infographic's landing handshake too.

## 0.2.0 — 2026-07-10
- Step 0 vault resolution (absolute path from marketplace root; fixes wrong-cwd writes)
- Canonical layout extracted to references/vault-layout.md; collision + index determinism rules
- Integration contract README; pubmed-research-note now delegates vault writes here

## 0.1.0
- Initial: single skill, init/save/index/query
