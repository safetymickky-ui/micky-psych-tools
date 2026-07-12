# vault-keeper

Files, indexes, links, and retrieves any skill's output in the shared Obsidian-style vault
at the marketplace repo root (`vault/`). This README is the integration contract: if your
plugin produces content that should land in the vault, this is how you hand it over.

## The four jobs

| Job | What it does |
|-----|--------------|
| **init** | Scaffold the canonical tree. Skipped when the vault is populated (`vault/index.md` exists — `.gitkeep`-only dirs don't count). |
| **save** | File a note/artifact: query first to avoid duplicates, name it per the layout rules, write frontmatter + wikilinks, wire it into its topic MOC and `index.md`. |
| **index** | Rebuild/repair `index.md` and `MOCs/` deterministically — pure rebuild, alphabetical by title, `primary-moc:` tie-break, orphans reported never moved. |
| **query** | Glob/Grep the resolved vault root to find what exists before anything is duplicated. |

## Canonical layout

The single source of truth for the vault tree, naming, collision, and index rules is
[`skills/vault-keeper/references/vault-layout.md`](skills/vault-keeper/references/vault-layout.md)
— i.e. `plugins/vault-keeper/skills/vault-keeper/references/vault-layout.md` from the repo
root. Every plugin that touches the vault cites that file; do not restate or fork its rules.

Key point: the vault root is resolved by walking up from cwd to the directory containing
`.claude-plugin/marketplace.json`, then appending `vault/` — never a bare relative `vault/`.

## Handoff rule for producer skills

The producer passes:

- **title** (a human title; `Concept — Qualifier` style for notes — vault-keeper derives
  artifact/asset filenames)
- **body** (the content itself; for an `asset`, the file path(s) of the rendered binary instead)
- **target type** (`note` / `artifact` / `asset` / `MOC`)
- **suggested MOC topic**
- **source-skill identity and tags** — as data, not as frontmatter
- **extra frontmatter fields** (optional) — a flat key: value map (e.g. sources, board_pearls, review_count) merged verbatim into the frontmatter vault-keeper writes; reserved keys (title, created, type, source, primary-moc, tags, links) cannot be overridden

**Vault-keeper writes the actual frontmatter block, the filename, and all index/MOC wiring.**
Producers never emit frontmatter, choose paths, invent filenames, or edit `index.md`/MOCs —
hand the payload over and let vault-keeper file it. Conversely, vault-keeper never authors
content: missing content is handed back to the source skill.

For an **asset** (a rendered binary — HTML, PNG, deck), the producer hands the file path(s), a
human title, the suggested MOC topic, and optionally a link to the source artifact and/or a
short companion-note body. Vault-keeper places the binary in `assets/`, references it from the
topic MOC's `## Assets` section (and from the source artifact when one exists), and writes a
companion note only when a body was supplied — the note is optional, not required.
