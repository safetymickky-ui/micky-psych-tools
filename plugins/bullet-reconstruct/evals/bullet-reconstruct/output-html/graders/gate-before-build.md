---
# Process: only a passing gate clears the HTML build.
type: tool_order
before: { tool: Bash, input_match: 'coverage_check\.py' }
after: { tool: Bash, input_match: 'build_html\.py' }
weight: 1
---
