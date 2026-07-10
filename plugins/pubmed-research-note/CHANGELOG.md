# Changelog

## 1.1.1

The manifest has carried this version since the plugin's first commit in this repo — there
is no earlier tagged release to reconstruct, so this entry covers everything landed under
it so far:

- **Initial release.** Verdict-first evidence-report skill orchestrating PubMed (backbone),
  ClinicalTrials.gov (publication-bias check), Open Library (textbook-vs-evidence gap), and
  Wikipedia (terminology only). Four decision frames (Rx / Service / Truth / Teaching), the
  citation contract (clean prose, quantified evidence, compressed `## Sources`), and an
  opt-in, word-gated atomize flow. Pairs with the separately-installed `intent-lock` plugin
  for bare-topic and tied-frame requests.
- **Dropped sandbox-only vault paths.** Removed the `<outputs>/vault/` write path and the
  producer-side dedup-grep from the atomize flow; the skill no longer resolves vault paths
  or writes YAML frontmatter itself.
- **Delegated vault writes to `vault-keeper`.** Atomic-note creation now hands title, body,
  target type, suggested MOC topic, and source-skill tags to the `vault-keeper` skill, which
  owns paths, dedup, MOC wiring, and the index.
- **Extended the handoff contract.** Aligned the note handoff with `vault-keeper`'s
  producer-supplied optional extra frontmatter fields (sources, board_pearls, review_count,
  last_reviewed, aliases), passed as a flat map.
