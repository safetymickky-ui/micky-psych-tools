---
# Step 3: findings in two tagged tiers, blockers ranked first. The planted blocker
# (fire-crawl) must sit after a [BLOCKER] tag and before a [QUALITY] tag, so prose that
# only mentions "blockers" and "quality", or a misfiled finding, no longer passes.
type: regex
target: last_message
pattern: '\[blocker\][\s\S]*?fire-crawl[\s\S]*?\[quality\]'
flags: i
weight: 1
---
