---
# A wording change is a patch: bump.py --write moves plugin.json from 0.1.0 to 0.1.1.
type: regex
target: { source: file, path: "plugins/gridgeist/.claude-plugin/plugin.json" }
pattern: '"version"\s*:\s*"0\.1\.1"'
weight: 1
---
