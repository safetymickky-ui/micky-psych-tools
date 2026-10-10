# Changelog — vault-keeper

## 0.5.0 — 2026-10-10

- Links follow the Learn hub's rules (new **Links** section in SKILL.md): a link sits inline on
  words the note already uses; only notes that exist (no stub links); `links:` mirrors the
  body's inline note links exactly; a MOC is never a `links:` entry; cross-topic links only where
  the note names the other note's concept. `index` now repairs to these rules (unwrap a link to
  a missing note, drop a MOC from `links:`, reset `links:` to the body) and reports each repair.

## 0.4.0

no contemporaneous entry; see `git log` around this version.

## 0.3.0

no contemporaneous entry; see `git log` around this version.

## 0.2.0 — 2026-07-10
- Step 0 vault resolution (absolute path from marketplace root; fixes wrong-cwd writes)
- Canonical layout extracted to references/vault-layout.md; collision + index determinism rules
- Integration contract README; pubmed-research-note now delegates vault writes here

## 0.1.0
- Initial: single skill, init/save/index/query
