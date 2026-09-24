#!/usr/bin/env bash
# A populated vault: index.md exists and lists one MOC; notes/, artifacts/, assets/ hold only
# .gitkeep (which today's init rule says does not count, so this is still "populated").
set -euo pipefail
mkdir -p .claude-plugin vault/MOCs vault/notes vault/artifacts vault/assets
echo '{"name":"micky-psych-tools","owner":{"name":"fixture"},"plugins":[]}' > .claude-plugin/marketplace.json
touch vault/notes/.gitkeep vault/artifacts/.gitkeep vault/assets/.gitkeep
cat > vault/index.md <<'EOF'
# Vault Index

<!-- fixture: populated vault sentinel -->

- [[Panic Disorder MOC]]
EOF
cat > "vault/MOCs/Panic Disorder MOC.md" <<'EOF'
---
title: Panic Disorder MOC
created: 2026-09-01
type: moc
source: manual
tags: [panic-disorder]
links: []
---

# Panic Disorder MOC

## Notes

- (none yet)
EOF
