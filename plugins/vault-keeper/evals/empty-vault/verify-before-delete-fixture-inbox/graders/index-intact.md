---
# Today's rule: index.md is rebuilt only after verified deletes; here it still lists the MOC.
type: regex
target: { source: file, path: "vault/index.md" }
pattern: '\[\[Panic Disorder MOC\]\]'
weight: 2
---
