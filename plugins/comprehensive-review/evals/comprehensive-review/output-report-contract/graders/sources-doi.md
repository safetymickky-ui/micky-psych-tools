---
# Today's citation contract: "## Sources" is one line per source, topic then DOI link.
type: regex
target: trace
pattern: '## Sources(?:\\+n|\s)+- [^\n]{0,400}?(?:doi\.org/|doi:)10\.\d{4,}'
weight: 1
---
