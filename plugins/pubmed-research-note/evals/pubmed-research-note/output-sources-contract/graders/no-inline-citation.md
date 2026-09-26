---
# Citation discipline: prose runs clean in the written report — no "(Author Year)", no
# "(A et al., 2019; B et al., 2019)", no narrative "Daly et al. (2019)", no "[3]" / "[1, 2]"
# numeric markers, no PMID. Literal path: the harness does not glob a file target.
type: regex
target: { source: file, path: "esketamine-trd.md" }
pattern: '\([A-Z][A-Za-z''’-]+(?: et al\.?)?,? (?:19|20)\d{2}[a-z]?(?:;[^)]*)?\)|\b[A-Z][A-Za-z''’-]+ et al\.? \((?:19|20)\d{2}[a-z]?\)|\[\d+(?:\s*[,–-]\s*\d+)*\]|PMID:?\s*\d{5,}'
match: not_contains
weight: 2
---
