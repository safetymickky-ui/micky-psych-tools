---
# Today's rule: never sweep without a window (Step 1 + sweep-recipes.md: search_articles
# with query, date_from, date_to). Tool name is the plugin-bundled prefix the skill names.
type: tool_used
tool: mcp__plugin_psych-paper-digest_pubmed__search_articles
input_match: '(?=[\s\S]*"date_from"\s*:\s*"\d{4})(?=[\s\S]*"date_to"\s*:\s*"\d{4})'
min: 1
weight: 3
---
