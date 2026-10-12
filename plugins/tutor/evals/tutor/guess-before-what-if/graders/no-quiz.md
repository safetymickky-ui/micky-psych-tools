---
# Contract: the tutor never starts a quiz or a check.
type: regex
target: last_message
pattern: '\bquiz|\btest yourself|does that make sense'
flags: i
match: not_contains
weight: 1
---
