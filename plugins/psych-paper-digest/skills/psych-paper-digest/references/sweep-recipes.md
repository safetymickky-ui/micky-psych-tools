# Sweep recipes — engines, windows, dedup

Read before the first tool call of a sweep. Two engines, two jobs: PubMed is the
**publication radar**, ClinicalTrials.gov is the **readout radar**. Both are bundled by
this plugin's `.mcp.json` with stable tool prefixes — call them directly, no ToolSearch
hunt:

- `mcp__plugin_psych-paper-digest_pubmed__<tool>`
- `mcp__plugin_psych-paper-digest_clinical-trials__<tool>`

Only external managed connectors get session-varying hashed prefixes; these two are fixed
by the plugin's own name and server keys.

## Windowing

Per domain:

- `date_from = last_swept − 3 days`. The overlap absorbs PubMed's indexing lag (records
  surface days after epub); dedup (below) removes the repeats the overlap causes.
- `date_to = today`.
- `last_swept: null` (never swept) → 14-day inaugural window.
- `last_swept` more than 90 days old → sweep 90 days and name the cap in the digest
  header. A capped window means the stretch between `last_swept` and 90 days ago was never
  screened — that gap must be visible, not silently absorbed.

Never sweep without a window: an unwindowed query returns the domain's whole literature
and the triage drowns.

## PubMed — publication radar

Per domain, one windowed query at the evidence floor:

```
(<domain query from config>) AND (Guideline[Publication Type]
  OR Practice Guideline[Publication Type] OR Meta-Analysis[Publication Type]
  OR systematic[sb] OR Randomized Controlled Trial[Publication Type])
```

`search_articles` args: `query`, `date_from`, `date_to`, `sort: pub_date`,
`max_results: 50`. A domain with `floor: "all"` in config drops the filter block — use
sparingly; it multiplies screening effort 5–10×. No `*` wildcards, no empty query.

Screen titles/abstracts against the domain's **clinical intent** (not keyword
coincidence), then call `get_article_metadata` ONLY for keepers — capture PMID and DOI
(the digest links the DOI; the PMID is for dedup). `convert_article_ids` when a record
lacks its DOI.

**Web fallback** (server down ≠ engine down): E-utilities —
`https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=<query>&mindate=<from>&maxdate=<to>&datetype=edat&retmode=json`,
then `efetch.fcgi?db=pubmed&id=<pmid>&rettype=abstract`. If PubMed is unreachable by both
paths, the run is **fatal**: say so and stop. A registry-only digest misrepresents the
window as quiet.

## ClinicalTrials.gov — readout radar

Three events matter, in this order; everything else is noise *for a digest*:

1. **Results newly posted** in the window — often precedes the publication by months; the
   digest's earliest signal.
2. **Newly completed, nothing posted** — starts the completed-unpublished clock that
   pubmed-research-note's registry check later relies on.
3. **Newly terminated or withdrawn — futility or safety only.** Slow accrual is noise;
   futility on a standard-of-care comparator is Act-tier signal.

MCP path: `search_trials` on the domain's `trials_term` (filter by status: completed,
terminated, has-results), then `get_trial_details` on candidates to read the dates against
the window (results-first-posted, completion, last-update) — the search tool cannot
date-filter directly, so the details call is where the window is enforced.

**Web fallback**: API v2 date-filters directly, e.g.
`https://clinicaltrials.gov/api/v2/studies?query.term=<term>+AND+AREA[ResultsFirstPostDate]RANGE[<from>,<to>]`.

Registry unreachable → **degrade, don't die**: sweep PubMed, and name the registry gap in
the digest header line.

## Dedup — two passes, no seen-ledger

The config keeps no list of seen PMIDs; **the previous digest file is the ledger.**

1. **Against the previous digest:** glob `digest-*.md` in the digest directory, take the
   newest, grep its DOIs/PMIDs/NCTs, and drop matches from this sweep — the 3-day overlap
   guarantees some.
2. **Across domains:** an item matching two watchlist domains appears once, under the
   domain where it triages highest (tie → first in config order), with the other domain
   named in its why-clause.

## Screening discipline

The floor filter is a net, not a judgment. Screening keeps an item when it is (a) genuinely
in-domain — the domain's clinical intent, not keyword coincidence — and (b) new
information, not a re-publication, erratum, or conference restatement of a known result.
Everything dropped is counted into `## Suppressed` per domain. No silent drops: screened
and kept counts both appear in the digest header.
