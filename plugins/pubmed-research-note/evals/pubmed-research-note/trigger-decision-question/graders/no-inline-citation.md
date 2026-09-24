---
type: regex
target: last_message
pattern: '\([A-Z][A-Za-z''-]+(?: et al\.?)?,? (?:19|20)\d{2}[a-z]?\)|PMID:?\s*\d{5,}'
match: not_contains
weight: 1
---
