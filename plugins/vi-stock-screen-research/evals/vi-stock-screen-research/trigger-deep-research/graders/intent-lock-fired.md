---
# Step 0: intent-lock runs before any data call, in both modes.
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?intent-lock"'
arm: both
weight: 1
---
