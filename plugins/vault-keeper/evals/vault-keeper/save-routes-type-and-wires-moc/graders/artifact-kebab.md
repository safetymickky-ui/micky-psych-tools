---
# Today's routing: a document read top-to-bottom is an artifact, kebab-case, in artifacts/.
type: regex
target: files
pattern: '(?:^|/)vault/artifacts/[a-z0-9]+(?:-[a-z0-9]+)*\.md$'
flags: m
weight: 1
---
