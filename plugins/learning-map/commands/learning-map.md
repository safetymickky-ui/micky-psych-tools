---
description: Map a material's prerequisite knowledge (dependency ladder), its learning pearls and what to explore next, saved to Learn
argument-hint: [paper, chapter, URL, DOI/PMID, PDF path, or pasted text]
---

Run the `learning-map` skill now.

- `$ARGUMENTS` names or holds a material (a path, a URL, a DOI or PMID, pasted text) → map it.
  Several materials → one map each, in order.
- `$ARGUMENTS` is empty and nothing is attached → ask for the material in one line and stop.
- `$ARGUMENTS` is "open" or "list" → find the Learn page and open it.

The skill owns the whole procedure: read the material in full → build the ladder (Level 0
foundations, Level 1 core, Level 2 what the material assumes), the pearls and the path →
`check_map.py` → save to the "Learn" artifact → reply with the link, the items to learn first
and numbered next options. This command is only the manual trigger.
