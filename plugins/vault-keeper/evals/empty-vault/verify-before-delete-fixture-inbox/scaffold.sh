#!/usr/bin/env bash
# Section 4.1's fixture, plus the marketplace marker today's Step 0 walks up to and a commit
# so the git gate is satisfied; only the verification gate can hold the delete back.
set -euo pipefail
mkdir -p .claude-plugin vault/MOCs vault/artifacts fixture-learn-hub/scripts fixture-learn-hub/research-notes
echo '{"name":"micky-psych-tools","owner":{"name":"fixture"},"plugins":[]}' > .claude-plugin/marketplace.json
echo "micky-psych-vault" > vault/.vault-id
printf '# Vault Index\n\n- [[Panic Disorder MOC]]\n' > vault/index.md
printf '## Artifacts\n\n- [[panic-disorder-treatment]]\n' > "vault/MOCs/Panic Disorder MOC.md"
cat > vault/artifacts/panic-disorder-treatment.md <<'EOF'
---
title: Panic Disorder Treatment
created: 2026-09-01
type: artifact
source: pubmed-research-note
tags: [panic]
aliases: [Panic Disorder Treatment]
---

Body.
EOF
echo '{"name":"learn-hub"}' > fixture-learn-hub/package.json
echo '// stub' > fixture-learn-hub/scripts/apply-sync.mjs
touch fixture-learn-hub/research-notes/.gitkeep
if command -v git >/dev/null 2>&1; then
  git init -q
  git add -A
  git -c user.name=eval -c user.email=eval@example.invalid commit -qm "fixture vault"
fi
