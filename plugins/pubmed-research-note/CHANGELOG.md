# Changelog

## 1.6.0 — 2026-07-13

- **Fifth engine: Firecrawl — the general-web document engine.** Load-bearing when the
  verdict hinges on a document outside PubMed and the registry: regulator labels and
  safety communications (FDA, EMA, MHRA), guideline full texts on org sites (NICE, APA,
  WFSBP), gray literature. Rides the new `firecrawl` plugin (`firecrawl search` /
  `firecrawl scrape`; WebFetch fallback — a missing CLI or key never blocks a run).
  Widens *where* documents come from, never the evidence bar — the blog ban stands, and
  Firecrawl fetches while this skill adjudicates. Scraped sources cite exact URL +
  access date in `## Sources`. Tool catalog, SKILL engines list, description, and README
  updated to five engines; the citation discipline and report-craft admit the
  web-document format (`<topic> — <URL> (accessed YYYY-MM-DD)`, DOI preferred when one
  exists) with "publication year" disambiguated from the access date. README's stale
  opt-in vault framing corrected to the write → show → file default (1.3.0 behavior).

## 1.5.0 — 2026-07-11

- **Removed the four fixed frames.** Rx / Service / Truth / Teaching are gone. In their place
  the skill builds a bespoke **decision brief** for every request from the same six-slot
  anatomy every good decision shares — the decision, the verdict's shape, what settles it,
  what must be counted, the mandatory checks, the anti-goal — filled fresh instead of chosen
  from a menu. `references/decision-frames.md` is replaced by `references/decision-brief.md`.
- **Removed the fixed report template.** The five-heading skeleton (Verdict / What the
  evidence says / Where it breaks / What would change this / Sources) is no longer mandated.
  The report now takes whatever shape carries *this* decision from evidence to action in the
  fewest sections that earn their place, guided by the new `references/report-craft.md`:
  answer first, headings minted from the decision (never the topic), numbers in every section,
  disagreements adjudicated not listed, as long as the decision needs and no longer.
- **Invariants became motivated principles, not enforced rules.** The old hard "Failure
  conditions" and forbidden-headings ban are reframed as *tells that the report has drifted*
  back toward the encyclopedia — taught with the reasoning, so the shape is reconstructed from
  understanding rather than compliance. The citation discipline (clean prose, quantified
  evidence, compressed one-line `## Sources`, decline-to-drop) is retained.
- **De-framed the references.** `intent-lock-pairing.md` now describes the four
  *what-the-user-wants* slots intent-lock must fix (decision, verdict's shape, scope,
  anti-goal) instead of "the frame — Rx/Service/Truth/Teaching"; `tool-catalog.md` ties the
  ClinicalTrials.gov and Open Library mandates to the *decision at stake* rather than to named
  frames. Evals rewritten to test brief-building, verdict-first, decision-shaped headings, and
  adjudication rather than frame classification and the fixed template.

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
