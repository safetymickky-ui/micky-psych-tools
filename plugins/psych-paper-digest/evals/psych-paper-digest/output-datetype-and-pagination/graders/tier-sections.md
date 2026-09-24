---
# Today's digest shape (Step 4): digest-YYYY-MM-DD.md with the four sections in order.
type: regex
target: { source: file, path: "digest-*.md" }
pattern: '## Act[\s\S]*## Read[\s\S]*## Registry watch[\s\S]*## Suppressed'
weight: 1
---
