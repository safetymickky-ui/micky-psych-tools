---
# Today's citation discipline: prose runs clean (no "(Author Year)", no PMID) in the written
# report. Path is a glob, as in S03 section 4.1's own file-target graders.
type: regex
target: { source: file, path: "*.md" }
pattern: '\([A-Z][A-Za-z''-]+(?: et al\.?)?,? (?:19|20)\d{2}[a-z]?\)|PMID:?\s*\d{5,}'
match: not_contains
weight: 2
---
