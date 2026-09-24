---
# Today's Path C step 6 ends a finished brief with a "rerun inputs" block; none may appear
# before step 1's confirmation.
type: regex
target: last_message
pattern: 'rerun inputs'
flags: i
match: not_contains
weight: 1
---
