---
# Today's Step 5: validate after scaffolding (section 4.1's grader).
type: tool_order
before: { tool: Write, input_match: "citation-format/\\.claude-plugin/plugin\\.json" }
after: { tool: Bash, input_match: "validate\\.py" }
weight: 2
---
