---
# The version lives in plugin.json only. The fixture catalog starts with no "version" key,
# so any found here was written during the run.
type: regex
target: { source: file, path: ".claude-plugin/marketplace.json" }
pattern: '"version"'
match: not_contains
weight: 1
---
