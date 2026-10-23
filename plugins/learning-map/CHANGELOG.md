# Changelog

## 0.1.0 — 2026-10-23

- Initial release. One material in, one learning map out, in three parts: the prerequisite
  knowledge as a dependency ladder (Level 0 foundations, Level 1 core, Level 2 what the material
  assumes), 5–12 learning pearls anchored to the material, and a 3–7 step path of concepts to
  explore next. The owner chose the ladder, the Learn artifact as the home of every map, and a
  concepts-only path on 2026-10-23.
- `check_map.py` checks every map before it is saved: ladder edges point down a level, no
  orphan items, level, pearl and path sizes, no links in the ladder or path, and every number in
  a material pearl found in the material's text. 27 unit tests.
- Learn page (`skills/learning-map/assets/learn.html`): an artifact with a database holding
  `maps/<map-id>`. Map cards, a dependency diagram with chain tracing, the ladder by level with
  new / brush up / likely owned marks and a "hide what I likely own" toggle, pearls and the
  path as a route. Clinical Minimal palette, light and dark.
- `/learning-map` command; trigger and near-miss eval cases.
