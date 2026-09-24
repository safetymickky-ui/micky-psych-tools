#!/usr/bin/env bash
# One-domain watchlist (the config-schema.md example domain), last swept 7 days ago, so
# today's Step 1 window is (last_swept - 3 days) -> today.
set -euo pipefail
swept="$(date -u -d '7 days ago' +%F 2>/dev/null || date -u -v-7d +%F)"
cat > .psych-paper-digest.json <<JSON
{
  "digest_dir": ".",
  "domains": [
    {
      "name": "child-adhd",
      "label": "Child & adolescent ADHD",
      "query": "(ADHD[Title/Abstract] OR \"attention deficit\"[Title/Abstract]) AND (child[Title/Abstract] OR adolescent[Title/Abstract] OR pediatric[Title/Abstract] OR paediatric[Title/Abstract])",
      "trials_term": "ADHD child adolescent",
      "floor": "high",
      "last_swept": "${swept}"
    }
  ]
}
JSON
