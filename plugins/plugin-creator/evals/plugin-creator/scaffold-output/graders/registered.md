---
# Step 4: the catalog gains the new plugin's entry, sourced from ./plugins/citation-format.
type: regex
target: { source: file, path: ".claude-plugin/marketplace.json" }
pattern: '"source"\s*:\s*"\./plugins/citation-format"'
weight: 1
---
