---
# Today's report template puts "*<YYYY-MM-DD> · PubMed N · trials N · books N*" under the
# title. The skill text writes N, so only a filled-in line from the run matches.
type: regex
target: trace
pattern: 'PubMed \d+[^\n]{1,16}trials \d+[^\n]{1,16}books \d+'
weight: 1
---
