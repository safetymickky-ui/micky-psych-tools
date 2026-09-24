---
# Today's level rule: a wording change is a patch, 0.1.0 -> 0.1.1 in the catalog.
type: regex
target: { source: file, path: ".claude-plugin/marketplace.json" }
pattern: '"version"\s*:\s*"0\.1\.1"'
weight: 1
---
