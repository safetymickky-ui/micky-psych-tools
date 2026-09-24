---
# Today's rule: one self-contained file; no external CSS, JS, fonts, images or CDN.
# Plain <a href> links (the DOI footer) are allowed.
type: regex
target: { source: file, path: "*.html" }
pattern: '<(?:link|script|img|source|iframe)\b[^>]*\b(?:href|src)\s*=\s*["'']?(?:https?:)?//|@import\s+(?:url\()?\s*["'']?(?:https?:)?//|url\(\s*["'']?https?://'
flags: i
match: not_contains
weight: 2
---
