---
# Today's digest header: "*window YYYY-MM-DD -> YYYY-MM-DD · domains N · ...*". Graded over
# the trace so it holds in both output branches (file via Write, or inline when no
# filesystem); the skill's own text has no digits in that slot.
type: regex
target: trace
pattern: 'window \d{4}[-/]\d{2}[-/]\d{2}[^\n]{1,16}\d{4}[-/]\d{2}[-/]\d{2}[^\n]{0,40}?domains \d+'
weight: 2
---
