---
# Depth contract: both load-bearing trials arrive with their effect and CI, from the mocks —
# the n=227 switch RCT (LS mean difference -4.0, 95% CI -7.31 to -0.64) and the n=297
# withdrawal RCT (HR 0.49, 95% CI 0.29-0.84). 7.3 tolerates rounding.
type: regex
target: { source: file, path: "esketamine-trd.md" }
pattern: '(?=[\s\S]*\b227\b)(?=[\s\S]*7\.3)(?=[\s\S]*0\.64)(?=[\s\S]*\b297\b)(?=[\s\S]*0\.49)(?=[\s\S]*0\.29)(?=[\s\S]*0\.84)'
weight: 2
---
