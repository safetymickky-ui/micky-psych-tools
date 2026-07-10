# Config schema — .psych-paper-digest.json

One file in the working directory owns the watchlist and the sweep state. The skill
creates it at init and is the **only writer of `last_swept`**; the user edits domains
freely — by hand, or by asking ("add perinatal psychiatry to my watchlist").

```json
{
  "digest_dir": ".",
  "domains": [
    {
      "name": "child-adhd",
      "label": "Child & adolescent ADHD",
      "query": "(ADHD[Title/Abstract] OR \"attention deficit\"[Title/Abstract]) AND (child[Title/Abstract] OR adolescent[Title/Abstract] OR pediatric[Title/Abstract] OR paediatric[Title/Abstract])",
      "trials_term": "ADHD child adolescent",
      "floor": "high",
      "last_swept": "2026-07-03"
    }
  ]
}
```

## Fields

- **`digest_dir`** — optional; where `digest-YYYY-MM-DD.md` lands. Default `"."` (the
  working directory). Same idea as pubmed-research-note's `report_dir`.
- **`domains[].name`** — kebab-case id; what `/digest <domain>` matches.
- **`domains[].label`** — human name; used in the digest's why-clauses.
- **`domains[].query`** — the PubMed query fragment: field-tagged, boolean, **no `*`
  wildcards, no date terms** — the skill windows every sweep itself.
- **`domains[].trials_term`** — plain-language ClinicalTrials.gov search term.
- **`domains[].floor`** — `"high"` (default: the guideline / meta-analysis / systematic /
  RCT filter) or `"all"` (no filter; screening cost 5–10×; use for thin domains only).
- **`domains[].last_swept`** — ISO date the last successful sweep covered through;
  `null` = never swept. **Written only by the skill, only after the digest file is
  written.** A failed or partial run leaves it untouched so the next run re-covers the
  window. A scoped run (`/digest child-adhd`) advances only that domain.

## Init flow (no config present)

1. **Elicit 3–8 domains** — the clinical areas the user actually covers. When a vault
   exists (walk up to the directory holding `.claude-plugin/marketplace.json`, look in
   `vault/MOCs/`), offer the MOC titles as candidates — the vault is the best available
   map of what the user tends.
2. **Draft** each domain's `query` and `trials_term` from its label, and show the drafts
   for one confirm pass — a bad query silently starves its domain forever, which is worth
   one look.
3. **Write** the config with every `last_swept: null`.
4. **Run the inaugural sweep** (14-day window) in the same turn.

## Sanity rules

- **3–8 domains.** Under 3, the user doesn't need a digest; over 8, every sweep is a slog
  and Act inflates.
- A domain returning **0 kept items across 3 consecutive sweeps** → suggest widening its
  query or floor, in the close line.
- A domain suppressing **more than ~40 items per sweep** → suggest narrowing its query,
  in the close line.
