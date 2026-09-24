---
# Today's mandatory banner when the source names contraindications / avoid items:
# "CRITICAL SAFETY — MEDICATIONS / ACTIONS TO AVOID". The template's own comment
# ("CRITICAL SAFETY: mandatory ...") does not match. Path is a glob, as in section 4.1.
type: regex
target: { source: file, path: "*.html" }
pattern: 'CRITICAL SAFETY\s*(?:—|&mdash;|&#8212;|–|&ndash;|-)\s*MEDICATIONS'
weight: 3
---
