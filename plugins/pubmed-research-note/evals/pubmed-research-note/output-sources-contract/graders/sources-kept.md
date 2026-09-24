---
# Today's contract: a request to drop "## Sources" is declined, and each Sources line is the
# topic phrase then the DOI link. Graded over the trace so it holds whether the report reached
# the user through the Write call or the inline copy; the pattern needs a real DOI right after
# a "## Sources" heading, which the skill's own text never contains.
type: regex
target: trace
pattern: '## Sources(?:\\+n|\s)+- [^\n]{0,400}?(?:doi\.org/|doi:)10\.\d{4,}'
weight: 3
---
