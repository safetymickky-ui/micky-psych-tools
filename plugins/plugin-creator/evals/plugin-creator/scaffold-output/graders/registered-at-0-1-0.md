---
# Today's Step 4: the catalog entry is added with version 0.1.0, equal to plugin.json.
type: regex
target: { source: file, path: ".claude-plugin/marketplace.json" }
pattern: '\{[^{}]*"name"\s*:\s*"citation-format"[^{}]*"version"\s*:\s*"0\.1\.0"[^{}]*\}|\{[^{}]*"version"\s*:\s*"0\.1\.0"[^{}]*"name"\s*:\s*"citation-format"[^{}]*\}'
weight: 2
---
