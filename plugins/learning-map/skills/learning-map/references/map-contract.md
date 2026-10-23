# The map contract

A map has four parts: a gist, a ladder, pearls and a path. This file sets what each part must
be. `scripts/check_map.py` enforces the parts that a script can check; the rest is on you.

## Gist

One or two sentences, at most 600 characters: what the material does and what it finds or
argues, in the material's own terms. No verdict on its quality.

## The ladder: prerequisite knowledge as a dependency ladder

### The three levels

- **Level 2 · Assumed here.** Concepts, methods, terms, conventions and facts that the material
  uses without teaching them, or teaches too briefly to learn from. A reader who lacks one
  misreads or cannot follow a specific claim, number or figure.
- **Level 1 · Core.** The ideas the Level 2 items stand on.
- **Level 0 · Foundations.** The base layer a newcomer to the field starts from. The ladder
  stops here; never go below Level 0.

### Build it backward from the material

1. While you read, list every candidate: each term used without a definition, each method
   named without an explanation, each assumption the argument needs, and each figure or table
   convention a reader must know (a forest plot, a log scale, a confusion matrix). Note where
   each first matters.
2. Keep a candidate for Level 2 only when a reader without it would misread a claim, a number
   or a figure. Drop what is only mentioned in passing.
3. Merge near-duplicates: one item per idea, named with its standard English term.
4. For each Level 2 item, ask "what must a reader know to learn this?" Those answers are Level 1
   items. Ask the same of each Level 1 item; those answers are Level 0 items.
5. Share bases. When two items stand on the same idea, it is one item with two dependents.
6. Edges: `needs` points only to items on a lower level (a Level 2 item may need a Level 0 item
   directly). Every Level 0 and Level 1 item must be needed by at least one item above it;
   otherwise drop it or move it.

### Size

- Level 2: 3–10 items. Level 1: 1–10. Level 0: 1–8. At most 25 in all.
- Fewer, decisive items beat a glossary. A short, plain material can have 3, 2 and 1.

### Each item

- `id`: short, lowercase, unique in the map (`p1`, `p2`, … is fine).
- `level`: 0, 1 or 2.
- `name`: the standard English term.
- `field`: the field the item belongs to, in a few words ("statistics", "psychopharmacology",
  "reinforcement learning"). Items often come from several fields; say which.
- `primer`: what it is, in one to three sentences, at the level the reader's level map sets for
  that field. A Specialist field gets the specific nuance the material needs, with no textbook
  basics. A Beginner field starts from the plain definition. Say each symbol in words before
  you use it; write math in Unicode. A primer defines; it never states an effect size, a dose,
  a study result, a citation or a link.
- `why`: the specific claim, number, figure or step in this material that depends on the item.
  "Table 2 reports the learning rate α per group; without α you cannot tell which group
  updated faster" is a why. "It is important for the paper" is not.
- `where`: where in the material it first matters: section, page, figure, table, slide,
  timestamp or line range, as the material labels it. Required on Level 2; optional below.
- `needs`: the ids of the lower-level items it builds on.
- `you` (only when the user's level map is known): an estimate of what the reader owns.
  - `own`: the item's field is a Specialist field for the reader, or an Intermediate field and
    the item is on Level 0.
  - `brush`: the field is Intermediate (Level 1 or 2), or Developing and the item is on Level 0.
  - `new`: anything else, including fields the level map does not name.
  - The page labels these "estimated from your level map". Never ask the user to confirm them.

Order the Level 2 items in the order the material first needs them. Order Level 1 and Level 0
items so that items needed by the same item sit together.

## Pearls

A pearl is a compact takeaway from this material that a reader should still hold a month
later. Each has one type:

- `finding`: a main result with its number (effect size, interval, sample size) as the
  material reports it.
- `method`: a design or analysis choice that changes how to read the result.
- `caveat`: a limit that changes how far the result carries.
- `concept`: a distinction or definition the material draws more sharply than the field
  usually does.
- `practice`: what would change in practice or in a tool if the result holds.

Rules:

- 5–12 pearls, ordered by yield: the one that most changes what a reader understands or does
  comes first.
- A pearl is specific to this material. A statement that is true of every paper in the field is
  not a pearl.
- Copy every number from the material with its unit, interval and sample size. Never round,
  convert or recompute. `check_map.py --source` checks every number in a `material` pearl
  against the text you read.
- `basis: "material"` means the material states it. `basis: "inference"` means it is your own
  reading (a limit the authors do not name, an implication they do not draw), and the sentence
  says so ("my inference is …"). At most 3 inference pearls.
- A dose appears only as what the material used or reported, attributed to it ("the trial
  used …"), never as advice.
- `where`: the place in the material the pearl comes from (same rules as the ladder).
- `uses`: the ids of the ladder items a reader needs to understand this pearl.
- No grades or praise ("landmark", "elegant", "solid"). State what the material shows.

## Path: explore next (concepts only)

- 3–7 steps in order. Each step builds on the material or on an earlier step, so the order is
  the route.
- `kind`, one of:
  - `deeper`: the same idea, one level further.
  - `wider`: a neighbouring idea the material touches or depends on.
  - `apply`: using it: a clinical use, an analysis, a tool.
  - `challenge`: the strongest competing account, a known failure, or the open question.
- Include at least one `deeper` step and at least one `wider` or `challenge` step. Add `apply`
  when the material has a practical side.
- `topic`: the concept, named the way the field names it.
- `why`: why this step comes now, in one or two sentences: what it builds on and what it opens.
- `question`: one question to carry into the step, answerable once the step is learned.
- `ladder` and `pearls`: the ladder ids and the pearl numbers (1-based) the step builds on.
- Concepts only (the user's choice on 2026-10-23): no titles, authors, journals, courses, links
  or DOIs anywhere in the path.
- Start where the material ends. Prefer steps that lead toward the fields the reader is
  learning (Developing and Intermediate on the level map) when the material allows a choice.

## Where the facts come from

- The material is the only source for the gist and the pearls.
- The ladder and the path come from general knowledge. That is why they carry no study
  results, numbers beyond definitions, or citations.
- Never invent a `where` label. When the material has no labels, quote up to eight words or
  give a position ("Discussion, paragraph 3").
