---
# Lazy data-URI images stay blank in print and previews.
type: regex
target: { source: file, path: "notes.html" }
pattern: 'loading\s*='
match: not_contains
weight: 1
---
