---
# Today's failure condition: "A file was written outside vault/". Any created path that
# does not run through vault/ fails the case.
type: regex
target: files
pattern: '^(?!.*(?:^|/)vault/).+$'
flags: m
match: not_contains
weight: 2
---
