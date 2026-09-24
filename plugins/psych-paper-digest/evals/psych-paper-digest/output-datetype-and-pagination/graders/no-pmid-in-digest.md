---
# Today's item discipline: the link is the DOI and nothing else; no PMID in the digest body.
type: regex
target: { source: file, path: "digest-*.md" }
pattern: 'PMID:?\s*\d{5,}'
match: not_contains
weight: 1
---
