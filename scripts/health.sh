#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
fail() { echo "health: FAIL — $1" >&2; exit 1; }
python3 scripts/validate.py
claude plugin validate --strict .claude-plugin/marketplace.json
for d in plugins/*/; do claude plugin validate --strict "$d"; done
python3 scripts/rewrite_gate.py ratchet verify
python3 scripts/rewrite_gate.py triggers verify
python3 scripts/delivery_log.py check >/dev/null || fail "delivery log: run python3 scripts/delivery_log.py check"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -q || fail "delivery_log tests"
if [ "${1:-}" != "--fast" ]; then
  python3 -m unittest discover -s scripts -p 'test_*.py' -q
  [ -n "${LEARN_HUB_DIR:-}" ] && [ -f "$LEARN_HUB_DIR/package.json" ] && \
    echo "cross-repo checks: not yet available (owner S08, I19 --cross-repo)"
fi
echo "health: OK"
