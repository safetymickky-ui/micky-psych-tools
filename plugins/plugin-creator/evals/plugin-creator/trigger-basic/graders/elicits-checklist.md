---
# Today's Step 1: elicit the fixed checklist before anything is written. Section 4.1's
# pattern with the reach widened (80 -> 400 chars) so a numbered list still matches.
type: regex
target: last_message
pattern: '(kebab|name)[\s\S]{0,400}(purpose|category|trigger)'
flags: i
weight: 1
---
