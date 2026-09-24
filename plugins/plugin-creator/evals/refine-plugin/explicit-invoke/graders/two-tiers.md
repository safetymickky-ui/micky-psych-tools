---
# Today's Step 3: findings in two ranked tiers, [BLOCKER] mechanical then [QUALITY].
# Section 4.1's pattern with the reach widened (400 -> 1500 chars) for before/after blocks.
type: regex
target: last_message
pattern: '(blocker|mechanical)[\s\S]{0,1500}?(quality|trigger)'
flags: i
weight: 1
---
