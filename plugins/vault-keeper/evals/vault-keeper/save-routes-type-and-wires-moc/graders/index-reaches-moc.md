---
# Today's rule: a new MOC is added to index.md; a saved file unreachable from index.md is lost.
type: regex
target: { source: file, path: "vault/index.md" }
pattern: '\[\[[^\]\n]*MOC[^\]\n]*\]\]'
weight: 2
---
