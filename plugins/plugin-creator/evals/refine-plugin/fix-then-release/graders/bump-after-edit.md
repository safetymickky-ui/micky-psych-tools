---
# Steps 4-5: apply the fix, then release with bump.py --write (without --write it is a
# dry run that writes nothing).
type: tool_order
before: { tool: Edit, input_match: "gridgeist" }
after: { tool: Bash, input_match: "bump\\.py[^\"]*--write" }
weight: 2
---
