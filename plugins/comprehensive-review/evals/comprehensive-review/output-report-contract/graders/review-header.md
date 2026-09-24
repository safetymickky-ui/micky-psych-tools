---
# Today's review template: "*<YYYY-MM-DD> · PubMed N · trials N · sections N*" under the
# title. Graded over the trace (Write input or inline render); the skill text writes N.
type: regex
target: trace
pattern: 'PubMed \d+[^\n]{1,16}trials \d+[^\n]{1,16}sections \d+'
weight: 2
---
