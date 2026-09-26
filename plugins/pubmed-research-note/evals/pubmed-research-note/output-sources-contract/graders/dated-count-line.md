---
# The report puts "*<YYYY-MM-DD> · PubMed N · trials N · books N*" under the title. Graded on
# the written file (the Close line in the trace would also match, so the trace is not used).
type: regex
target: { source: file, path: "esketamine-trd.md" }
pattern: 'PubMed \d+[^\n]{1,16}trials \d+[^\n]{1,16}books \d+'
weight: 1
---
