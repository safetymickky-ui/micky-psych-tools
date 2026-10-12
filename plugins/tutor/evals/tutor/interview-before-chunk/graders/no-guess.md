---
# Contract: no guess or prediction prompt before the teaching (removed in 0.3.0).
type: regex
target: last_message
pattern: 'guess in one line|\bguess\b.*\?|เดา'
flags: i
match: not_contains
weight: 1
---
