# Changelog

## 1.2.0 — 2026-07-10

- **Portable output.** Dropped the claude.ai-sandbox-only output path (`/mnt/user-data/outputs`)
  and the `present_files` tool, which do not exist in Claude Code. Output goes to the working
  directory (or `report_dir` from `.pubmed-research-note.json`), and renders inline with an
  explicit "nothing was written" when no filesystem is available.
- **Delegated vault writes to `vault-keeper`.** In vault mode the skill hands note content
  (title, body, target type, suggested MOC topic, tags, and optional extra frontmatter) to the
  `vault-keeper` skill, which owns placement, filenames, dedup, and MOC/index wiring. The
  atomic-note template keeps only the note *content* schema; its old path/folder/dedup mechanics
  and the non-canonical `MOC — <Topic>` naming are gone.
- **Truthful tool catalog.** Open Library is documented as web-fallback only (no MCP server is
  wired). The two bundled servers use stable prefixes
  (`mcp__plugin_pubmed-research-note_pubmed__*`, `mcp__plugin_pubmed-research-note_clinical-trials__*`)
  and are called directly — no ToolSearch hunt; the session-hash caveat is scoped to external
  managed connectors.
- **Description** made third-person and trimmed for headroom; the "sole entry point for
  literature research" overclaim softened to "the entry point for decision-driven biomedical
  literature research," consistent with the existing psych-paper-digest / deep-research carve-outs.
- **Docs & tests.** Added `README.md`; the intent-lock pairing section is deduped against its
  reference (with the misread-capture routing and `/intent-lock` override retained inline);
  evals renumbered contiguous with new coverage for the no-filesystem and vault-handoff branches.

## 1.1.1

Initial release. Verdict-first evidence-report skill orchestrating PubMed (backbone),
ClinicalTrials.gov (publication-bias check), Open Library (textbook-vs-evidence gap), and
Wikipedia (terminology only). Four decision frames (Rx / Service / Truth / Teaching), the
citation contract (clean prose, quantified evidence, compressed `## Sources`), and an
opt-in, word-gated atomize flow. Chains to the `intent-lock` plugin for bare-topic and
tied-frame requests. (The manifest has carried this version since the plugin's first commit;
there is no earlier tagged release to reconstruct.)
