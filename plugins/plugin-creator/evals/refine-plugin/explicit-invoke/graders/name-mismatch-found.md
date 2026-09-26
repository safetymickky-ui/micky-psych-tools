---
# The planted mechanical blocker is reported: firecrawl's SKILL.md frontmatter says
# name: fire-crawl in directory skills/firecrawl. The wrong name shows up in the report
# only when the audit found it; a bare keyword could not tell a found defect from a
# denied one.
type: regex
target: last_message
pattern: 'fire-crawl'
weight: 2
---
