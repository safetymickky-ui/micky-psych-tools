---
# Today's rule: never re-init a populated vault. The scaffolded index.md survives intact.
type: regex
target: { source: file, path: "vault/index.md" }
pattern: '<!-- fixture: populated vault sentinel -->[\s\S]*\[\[Panic Disorder MOC\]\]'
weight: 3
---
