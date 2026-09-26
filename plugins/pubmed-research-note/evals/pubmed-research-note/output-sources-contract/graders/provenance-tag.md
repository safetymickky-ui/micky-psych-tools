---
# This case mocks no full-text or id-conversion tool, so every load-bearing number comes from
# an abstract and must say so in its sentence (evidence-checks.md section 1).
type: regex
target: { source: file, path: "esketamine-trd.md" }
pattern: 'abstract[ -]only'
flags: i
weight: 2
---
