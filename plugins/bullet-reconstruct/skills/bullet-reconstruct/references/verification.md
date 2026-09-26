# Verification: units, anchors, scoring, the gate

The gate is only as honest as the unit list. Three rules keep it honest: the list is
written from the source **before** the bullets, every unit that can carry an anchor
does, and the script, not the writer, has the last word on anchors and numbers.

## units.json

```json
{
  "source": "McIntyre & Wong 2026, CNS Spectrums 31:e37",
  "units": [
    {"id": 1, "unit": "sleep disorder has the highest T2DM prevalence of any mental disorder: 39.7% (95% CI 34.9-44.7), meta-analysis of 245 observational studies",
     "anchors": ["39.7", "34.9", "44.7", "245"], "status": "present"},
    {"id": 2, "unit": "suvorexant lowered hepatic Pepck, Pgc-1a and G6Pase mRNA in db/db mice",
     "anchors": ["Pepck", "G6Pase", "db/db"], "status": "present"},
    {"id": 3, "unit": "pancreas APPEARS to make more orexin 1 than orexin 2 (hedged in source)",
     "anchors": ["appears", "orexin 1"], "status": "partial", "note": "hedge dropped"}
  ]
}
```

Fields: `id`, `unit` (one checkable fact), `anchors` (optional list), `status`, `note`
(optional).

## One unit per what

- One unit per distinct claim, relationship, definition, or mechanism step.
- Each number with its unit and interval is its own unit, or part of the claim it
  qualifies. Never a single unit "the statistics".
- Each named entity the source relies on (drug, receptor, gene, region, scale, dataset).
- Each table row and each item of a boxed list.
- The qualifier travels with its claim: hedge, species, design, population. "In db/db
  mice" and "a one-page letter" are part of the unit, not decoration.

Coarse units hide loss: "Table 2's four mechanisms" as one unit lets three of them vanish
at a cost of zero. The script reports units per 1,000 source words. One calibration
point: a 6-page perspective (5,690 words of text including references) gave 115 units,
about 20 per 1,000. The WARN floor is 10, half of that. It is one data point, not a norm.

## Anchors

- 1–3 exact strings per unit that must appear in the notes if the unit survived.
- Best anchors: numbers as the notes will write them (`39.7`, `245`), names (`Pepck`,
  `seltorexant`), distinctive terms (`dawn phenomenon`).
- For a hedged or tier-specific unit, anchor the qualifier (`appears`, `mice`, `letter`).
- Avoid words the notes will legitimately paraphrase. A unit with no stable string gets
  no anchors and stays self-graded; the report counts those units.
- Matching ignores case, HTML tags, markdown emphasis (`**`, `*`, backticks, `\*`
  escapes), repeated spaces and dash style (`34.9–44.7` equals `34.9-44.7`).

## Statuses

| status | meaning | loss |
|---|---|---|
| present | the unit is in the notes, with its qualifiers | 0 |
| partial | the gist is there; a number, name, hedge, species or design was lost | 0.5 |
| missing | not in the notes | 1 |
| distorted | in the notes but changed: a number, a name, a direction, a tier upgraded | 1 |

The anchor check can only lower a score: a `present` unit with some anchors absent
becomes `partial`, and one with none present becomes `missing`.

## Scoring by a fresh subagent (sources over ~5,000 words)

The writer remembers what it meant to keep and reads that into the notes. For long
sources, hand the scoring to a subagent that did not write them:

> You did not write these notes. For each unit in units.json, find it in notes.md and set
> its status: present, partial (a number, name, hedge, species or design was lost),
> missing, or distorted (changed). Do not edit notes.md. Do not add units. Return the
> updated units.json with a short note on every unit that is not present.

## Reading the gate output

- `Downgraded by the anchor check`: the scoring claimed more than the notes contain.
  Fix the notes (or the anchor, if it was a poor choice), then re-run.
- `Units to reinstate or correct`: put the fact back, or correct the distortion.
- `Numbers: NOT in source`: a number was changed or invented. Correct it. If the notes
  derive a number on purpose (a sum, a conversion), pass it with `--allow`.
- `Unit density ... WARN`: split the coarse units and re-score.
- Exit 0 = PASS. Only PASS clears delivery. Report the final line of numbers with it.
