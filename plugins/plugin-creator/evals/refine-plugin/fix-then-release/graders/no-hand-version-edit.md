---
# Never edit a version by hand: bump.py --write writes plugin.json, and the catalog
# carries no version at all.
type: tool_used
tool: Edit
input_match: '"file_path"\s*:\s*"[^"]*(?:plugin|marketplace)\.json"'
min: 0
max: 0
weight: 2
---
