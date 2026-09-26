---
# Numbers keep their units: the BP target with mmHg (a stat tile may split value and unit
# across tags, hence the 160-character reach) and the doxazosin ceiling in mg.
type: regex
target: { source: file, path: "ppgl-infographic.html" }
pattern: '(?=[\s\S]*130/80[\s\S]{0,160}?mmHg)(?=[\s\S]*\b32\s*(?:&nbsp;|&#160;)?\s*mg)'
weight: 2
---
