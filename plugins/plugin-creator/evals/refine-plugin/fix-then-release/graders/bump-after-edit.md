---
# Today's Steps 4-5: apply the fix, then bump via scripts/bump.py.
type: tool_order
before: { tool: Edit, input_match: "gridgeist" }
after: { tool: Bash, input_match: "bump\\.py" }
weight: 2
---
