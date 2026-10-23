# learning-map

Give it one material: a paper, a chapter, a lecture, slides, a transcript, a URL, a DOI or
PMID, a PDF, or pasted text. It returns a learning map in three parts and saves the map to one
phone-readable **Learn** page:

- **Before you read:** the prerequisite knowledge as a dependency ladder. Level 0 holds the
  foundations, Level 1 the core ideas, Level 2 the concepts the material uses without teaching
  them. Each item has a short primer, the place in the material where it matters and why, and
  the items it builds on. When your level map is known, each item is marked new, brush up or
  likely owned.
- **Pearls:** 5–12 takeaways from the material, highest yield first, each anchored to its
  section, figure or page. Numbers are copied from the material and checked against its text.
- **Explore next:** 3–7 ordered steps of concepts (deeper, wider, apply, challenge), each with a
  question to carry into it. Concepts only: no reading list, no citations.

## Use

```
/learning-map https://doi.org/10.1186/2045-5380-3-12
/learning-map ~/papers/chapter-4.pdf
```

Or in chat: "what do I need to know before reading this", "prerequisites for this paper",
"learning pearls of this", "what should I learn next after this", "ต้องรู้อะไรก่อนอ่าน",
"ควรเรียนอะไรต่อ".

The reply in chat is short: the link to the map in Learn, the Level 2 items that are new to
you, the first pearl and the first path step, and numbered next options (teach an item with
tutor, check a clinical pearl with pubmed-research-note, reconstruct the material with
bullet-reconstruct, or visualize a step). Nothing runs until you pick a number.

## The Learn page

A private artifact titled "Learn" (template in `skills/learning-map/assets/learn.html`). It
lists every map as a card. A map opens with its gist, then:

- a dependency diagram (Level 0 → Level 1 → Level 2 → the material); tap an item to trace what
  it builds on and what needs it, and hide what you likely own;
- the ladder by level, each item with its primer and why;
- the pearls in order, with type, location and the ladder items each one needs;
- the path as a numbered route.

The page only reads. The skill writes each map to the artifact's database (`maps/<map-id>`)
with version pins; see `skills/learning-map/references/learn-page.md`. The skill finds the page
by its title and creates it from the template when it is missing. A link of the form
`<Learn url>#<map-id>` opens one map directly.

## Checks

`skills/learning-map/scripts/check_map.py` runs before every save. It enforces the ladder shape
(edges point down a level, no orphan items, level sizes), pearl and path counts and kinds, no
links in the ladder or path, and, with `--source`, that every number in a pearl drawn from the
material appears in the material's text.

```
python3 -m unittest discover -s plugins/learning-map/tests
```

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install learning-map@micky-psych-tools
```

## Files

```
skills/learning-map/SKILL.md                    the contract and the procedure
skills/learning-map/references/map-contract.md  what the ladder, pearls and path must be
skills/learning-map/references/learn-page.md    find, create and write the Learn page
skills/learning-map/scripts/check_map.py        the pre-save check
skills/learning-map/assets/learn.html           the Learn page template
commands/learning-map.md                        /learning-map
tests/test_check_map.py                         checker tests
evals/learning-map/                             trigger and near-miss cases
```

## Boundaries

Condensing a material into bullets with its figures is bullet-reconstruct. Teaching one concept
step by step, or a curriculum for a field with no material, is tutor. A clinical evidence
verdict is pubmed-research-note. Maps are not filed to the vault; Learn is their home.
