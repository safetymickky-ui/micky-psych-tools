---
# The answer exists and is marked: the word Verdict as a bolded line or in a heading, and
# "Confidence:" with one GRADE level (evidence-checks.md section 5).
type: regex
target: { source: file, path: "esketamine-trd.md" }
pattern: '(?=[\s\S]*(?:\*\*Verdict|^#{1,6}[^\n]*Verdict))(?=[\s\S]*Confidence\W{0,6}(?:very low|high|moderate|low)\b)'
flags: im
weight: 3
---
