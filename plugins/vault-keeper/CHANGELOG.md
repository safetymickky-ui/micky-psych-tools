# Changelog — vault-keeper

## 0.5.0 — 2026-07-19
- empty-vault routes HTML assets by kind: infographic HTML → learn-hub's
  `ingest-infographic`, animation HTML → its `ingest-animation` (new), each deleted only
  after its own row-landed handshake; reports still digest first so the topic FK exists
- Other binaries (preview PNGs, decks) keep the old behavior — deleted with their topic,
  git-recoverable; new eval `assets-route-by-kind`

## 0.2.0 — 2026-07-10
- Step 0 vault resolution (absolute path from marketplace root; fixes wrong-cwd writes)
- Canonical layout extracted to references/vault-layout.md; collision + index determinism rules
- Integration contract README; pubmed-research-note now delegates vault writes here

## 0.1.0
- Initial: single skill, init/save/index/query
