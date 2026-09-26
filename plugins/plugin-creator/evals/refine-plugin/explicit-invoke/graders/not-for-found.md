---
# The planted quality gap is reported as a gap: the Not-for clause is called missing
# (or a fix adds one). A report that calls it present, or only names the words, fails.
type: regex
target: last_message
pattern: '(?:\bno\b|missing|lacks?|lacking|without|absent|\badds?\b|\badding\b)[^.\n]{0,15}not[\s-]*for|not[\s-]*for[^.\n]{0,30}(?:missing|absent|lack(?:s|ing)?|\bnone\b)'
flags: i
weight: 1
---
