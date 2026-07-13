# Source Tool Catalog

Read before your first tool call. Five engines, five jobs. PubMed and ClinicalTrials.gov have
an **MCP path** — this plugin bundles both servers in its own `.mcp.json` — and a **web
fallback**. Open Library has **no MCP server wired by this plugin**; it is web-fallback only
(WebSearch/WebFetch), unless an external Open Library connector happens to be installed.
Firecrawl rides the **firecrawl plugin / CLI** (keyless fallback exists) and is optional on
every run. A missing server never blocks the run — except PubMed, whose absence is fatal and
must be stated rather than worked around.

**Bundled servers have stable prefixes — no hunting required.** This plugin's own two MCP
servers resolve to fixed tool-name prefixes, not hashes:

- `mcp__plugin_pubmed-research-note_pubmed__<tool>`
- `mcp__plugin_pubmed-research-note_clinical-trials__<tool>`

Only **external managed connectors** (servers installed outside this plugin, e.g. a
user-connected Open Library or Wikipedia MCP) get session-varying hashed prefixes — never
hardcode those; resolve them at runtime with `ToolSearch` / `tool_search`.

---

## 1. PubMed — the backbone

Bundled server — call the tools directly with the stable prefix
`mcp__plugin_pubmed-research-note_pubmed__<tool>` (e.g.
`mcp__plugin_pubmed-research-note_pubmed__search_articles`). No ToolSearch step. Available
tools (reference list):

```
search_articles · get_article_metadata · get_full_text_article
find_related_articles · convert_article_ids · lookup_article_by_citation
```

| Tool | Use | Key args |
|------|-----|----------|
| `search_articles` | Find papers. The workhorse. | `query` (field tags `[Title]`, `[Author]`, `[MeSH Terms]`, `[Publication Type]`, boolean AND/OR/NOT), `max_results`, `sort` (`relevance` / `pub_date`), `date_from` / `date_to`. No `*` wildcards, no empty query. |
| `get_article_metadata` | Full record — **capture PMID, title, journal, year, DOI**. | `pmids: ["...", "..."]` |
| `get_full_text_article` | PMC full text (~6M articles). Use for the 2–3 papers the verdict actually hinges on. | `pmc_ids: ["PMC..."]` |
| `find_related_articles` | Close gaps; find full-text availability. | `pmids`, `link_type` |
| `convert_article_ids` | PMID ↔ PMCID ↔ DOI. | ids |
| `lookup_article_by_citation` | Resolve a half-remembered citation. | citation fields |

**High-evidence recipe** (the backbone query):
```
<topic> AND (Guideline[Publication Type] OR Meta-Analysis[Publication Type]
  OR systematic[sb] OR Randomized Controlled Trial[Publication Type])
```
Widen only if thin. Then run **one deliberately adversarial query** — search for the
negative or null result explicitly (`AND (negative OR null OR "failed to")`, or search the
known large trial by name). A verdict built only from the positive literature is the
publication bias, restated.

**Web fallback.** WebSearch `pubmed.ncbi.nlm.nih.gov`, WebFetch the article page, capture
PMID + DOI (both printed). Or E-utilities:
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<query>&retmode=json`
then `efetch.fcgi?db=pubmed&id=<pmid>&rettype=abstract`.

**Scope guard.** PubMed indexes biomedical/life-sciences only. Never source a clinical claim
from a blog. If PubMed is unreachable entirely, say so and stop — do not downgrade the
evidence base and proceed.

---

## 2. ClinicalTrials.gov — the publication-bias check

**Load-bearing whenever an action is at stake — a treatment choice or a service/protocol
decision — and high-yield on a contested claim.** Its only job: *what evidence exists that is
not in the published record, and would it change the verdict?*

Bundled server — call the tools directly with the stable prefix
`mcp__plugin_pubmed-research-note_clinical-trials__<tool>` (e.g.
`mcp__plugin_pubmed-research-note_clinical-trials__search_trials`). No ToolSearch step.
Available tools (reference list):

```
search_trials · get_trial_details · search_by_sponsor
analyze_endpoints · search_by_eligibility
```

| Tool | Use |
|------|-----|
| `search_trials` | Trials on the intervention. Filter by status. |
| `get_trial_details` | Full record for one `NCT` — design, n, endpoints, dates, results-posted flag. |
| `analyze_endpoints` | Primary vs secondary outcome measures — catches endpoint-switching. |
| `search_by_sponsor` | Industry-sponsored terminated trials. A cluster of them is a finding. |
| `search_by_eligibility` | Does the trial population resemble the patient in front of you? |

**Three things to look for, in this order:**

1. **Completed, no publication.** Completion date > 2 years ago, no linked results, nothing
   in PubMed. This is the single most common reason a confident positive verdict is wrong.
2. **Ongoing, large, reading out soon.** Belongs with the forward-looking evidence — what
   would change the verdict — with the expected readout date. For a service decision this can
   be the whole answer — *wait*.
3. **Terminated / withdrawn, and why.** Slow accrual is noise. Futility or safety is signal.

**Web fallback.** WebFetch `https://clinicaltrials.gov/api/v2/studies?query.term=<term>`.

Report every NCT you cite in `## Sources` as `NCT NNNNNNNN — status, n, endpoint, readout`.

---

## 3. Open Library — the textbook-vs-evidence gap

**Load-bearing when the decision is what to teach** — what a trainee can be told and examined
on. Optional elsewhere. Its job is not to source a clinical claim — it is to establish *what
the trainee has been taught*, so the report can name where the canon and the evidence diverge.

**Web-fallback only — no MCP server is wired for this engine.** `.mcp.json` declares just
`pubmed` and `clinical-trials`; there is no bundled or preferred `open-library` MCP path.
Use WebSearch/WebFetch directly. (If the user has separately connected an external Open
Library MCP connector, its prefix is a session-varying hash — resolve via `ToolSearch`,
never hardcode it; do not assume it exists.)

**Web fallback.** WebFetch `https://openlibrary.org/search.json?title=<title>` — read
edition, OLID, ISBN from the JSON.

A textbook citation without an **edition** is not a citation. Kaplan & Sadock 11e and 12e
disagree about things.

---

## 4. Wikipedia — terminology only

Resolve synonyms, brand names, scale full-names, abbreviations. That is the entire remit.

**It is barred from shaping the report outline.** Do not read its section list. Do not
derive sub-questions from it. Never cite it. If a term is unambiguous, skip it entirely —
this engine is optional on every run.

Its historical role in this skill (generating 3–6 sub-questions that became the report's
H2 headings) is the specific defect this version exists to remove.

---

## 5. Firecrawl — the general-web document engine

**Load-bearing when the verdict hinges on a document that is not in PubMed or the
registry** — a regulator's label or safety communication (FDA, EMA, MHRA), a guideline
body's full text on its own site (NICE, APA, WFSBP), gray literature or a preprint the
decision genuinely needs. Optional on every other run.

**Path.** The `firecrawl` plugin owns the how-to (install, auth, keyless fallback). In
practice: `firecrawl search "<query>"` when the URL is unknown, `firecrawl scrape <url>`
when it is known — clean markdown back, provenance attached. **Web fallback:**
WebSearch/WebFetch; a missing CLI or key never blocks the run.

**Scope guard — this engine widens *where*, never *what*.** The evidence bar is
unchanged: never source a clinical claim from a blog, a vendor page, or an unattributed
site. A scraped document must be an authoritative primary document — regulator,
guideline body, registry — and it feeds the verdict the same way any other source does.
Firecrawl fetches; this skill adjudicates.

**Citation.** A scraped document keeps its exact URL and access date. In `## Sources`:
`<topic it supports> — <URL> (accessed YYYY-MM-DD)`. A DOI link stays preferred whenever
one exists.
