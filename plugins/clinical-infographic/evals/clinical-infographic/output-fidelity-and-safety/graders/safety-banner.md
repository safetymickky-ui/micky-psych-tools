---
# Today's mandatory banner when the source names contraindications / avoid items:
# "CRITICAL SAFETY — MEDICATIONS / ACTIONS TO AVOID". The template's own comment
# ("CRITICAL SAFETY: mandatory ...") does not match. Literal path: the harness does not glob a file target.
type: regex
target: { source: file, path: "ppgl-infographic.html" }
pattern: 'CRITICAL SAFETY\s*(?:—|&mdash;|&#8212;|–|&ndash;|-)\s*MEDICATIONS'
weight: 3
---
