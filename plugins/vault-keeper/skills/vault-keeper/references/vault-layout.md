# Canonical vault layout (single source of truth)

Vault root: the `vault/` directory beside `.claude-plugin/marketplace.json` at the
marketplace repo root. NEVER a `vault/` relative to the current working directory.

Resolve it: walk up from cwd to the directory containing `.claude-plugin/marketplace.json`,
then append `vault/`. From inside a plugin, `${CLAUDE_PLUGIN_ROOT}/../../vault` is equivalent.
Use the resolved ABSOLUTE path in every Glob/Grep/Read/Write.

Tree (fixed — no free-form top-level folders):
  vault/index.md          # master index — every MOC listed
  vault/MOCs/<Topic> MOC.md
  vault/notes/<Concept — Qualifier>.md
  vault/artifacts/<kebab-slug>.md
  vault/assets/

Naming: MOC files are `<Topic> MOC.md` (not `MOC — <Topic>`). Notes use
`Concept — Qualifier` title case. Artifacts kebab-case.

Collision rule: if the derived filename exists and is NOT the same topic being
extended, disambiguate with ` -2`, ` -3`… — never overwrite.

MOC internal sections: inside `<Topic> MOC.md`, entries live under type-keyed headings —
`## Artifacts`, `## Assets`, `## Notes`, in that order — each mapping 1:1 to the vault tree
so index regeneration stays a pure rebuild. Include a section when it has content; an empty
section may carry a single placeholder line. Artifacts and notes are linked as
`[[wikilinks]]`; assets are referenced by vault path (`assets/<file>`).

MOC membership: every note reachable from exactly one MOC. Multi-topic notes declare
`primary-moc:` in frontmatter; that MOC wins, other MOCs may link but index checks
only the primary. Index regeneration is a pure rebuild, alphabetical by title;
orphans are REPORTED, never moved.

"Populated" (skip init): `vault/index.md` exists. `.gitkeep`-only dirs do not count
as content.
