#!/usr/bin/env bash
# Run a plugin's eval suite with pinned models and a cost cap (spec S12, interface I17).
set -euo pipefail

usage() {
  cat <<'EOF'
usage: bash scripts/eval.sh --smoke <plugin> [--against <ref>] [-- <extra args>]
       bash scripts/eval.sh --release <plugin> [--against <ref>] [-- <extra args>]
       bash scripts/eval.sh --help

  --smoke <plugin>    cases tagged smoke, one arm (--ablation none), --runs 1
  --release <plugin>  two arms, --threshold 0.8, --trust-plugin; --runs 3 for alignment
                      and evidence (gate skills, report writers), --runs 1 otherwise
  --against <ref>     run today's evals/<skill>/ case dirs against the plugin dir that
                      held <skill> at git ref <ref> (a git worktree of <ref>; the old
                      dir is found by skill name, so it works across the W3 family
                      move) and print that run's with-arm score
  -- <extra args>     appended verbatim to `claude plugin eval`
                      (for example: -- --allow-tools Write "Bash(npm test *)")

<plugin> is the bare directory name under plugins/, never a path.
Both modes pass --scaffold (the suites are owner-written).

Environment (all required; unset is a usage error, exit 2):
  EVAL_MODEL        model for the agent under test
  EVAL_JUDGE_MODEL  model for llm graders
  EVAL_BUDGET       USD cap for this run (--max-cost-usd): the smoke-run or the
                    release-run cap recorded in docs/rewrite/baseline.md (S12-W0-9)

Output: --json evals/results/<plugin>-<mode>-<timestamp>.json (repo root).
Exit: the exit code of `claude plugin eval`; 2 on a usage error; 3 when --against
finds no baseline for any skill (no plugin held it at <ref>).
EOF
}

die_usage() { echo "eval.sh: $1" >&2; echo >&2; usage >&2; exit 2; }

mode="" plugin="" against=""
extra=()
if [ $# -eq 0 ]; then usage >&2; exit 2; fi
while [ $# -gt 0 ]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    --smoke|--release)
      [ -z "$mode" ] || die_usage "choose one of --smoke or --release"
      [ $# -ge 2 ] || die_usage "$1 needs a plugin name"
      mode="${1#--}"; plugin="$2"; shift 2 ;;
    --against)
      [ $# -ge 2 ] || die_usage "--against needs a git ref"
      against="$2"; shift 2 ;;
    --) shift; extra=("$@"); break ;;
    *) die_usage "unknown argument: $1" ;;
  esac
done
[ -n "$mode" ] || die_usage "--smoke <plugin> or --release <plugin> is required"
case "$plugin" in
  ''|*/*|.*) die_usage "<plugin> must be a bare directory name under plugins/, got '$plugin'" ;;
esac
for var in EVAL_MODEL EVAL_JUDGE_MODEL EVAL_BUDGET; do
  [ -n "${!var:-}" ] || die_usage "$var is not set"
done

cd "$(dirname "$0")/.."
root="$(pwd)"
[ -f "plugins/$plugin/.claude-plugin/plugin.json" ] || die_usage "no plugin at plugins/$plugin"
mkdir -p evals/results
ts="$(date -u +%Y%m%dT%H%M%SZ)"

flags=()
if [ "$mode" = smoke ]; then
  flags=(--scaffold --tag smoke --ablation none --runs 1
         --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL"
         --max-cost-usd "$EVAL_BUDGET" --no-publish)
else
  case "$plugin" in alignment|evidence) runs=3 ;; *) runs=1 ;; esac
  flags=(--scaffold --runs "$runs" --threshold 0.8
         --model "$EVAL_MODEL" --judge-model "$EVAL_JUDGE_MODEL"
         --max-cost-usd "$EVAL_BUDGET" --trust-plugin --no-publish)
fi

if [ -z "$against" ]; then
  claude plugin eval "plugins/$plugin" "${flags[@]}" \
    --json "evals/results/$plugin-$mode-$ts.json" "${extra[@]}"
  exit $?
fi

# --against <ref>: one run per skill that has case dirs today.
git rev-parse --verify --quiet "$against^{commit}" >/dev/null || die_usage "unknown git ref: $against"
tmp="$(mktemp -d)"
cleanup() { git -C "$root" worktree remove --force "$tmp/wt" >/dev/null 2>&1 || true; rm -rf "$tmp"; }
trap cleanup EXIT
git worktree add --detach --quiet "$tmp/wt" "$against"

refname="$(printf '%s' "$against" | tr -c 'A-Za-z0-9._-' '_')"
status=0 ran=0
for skill_dir in "plugins/$plugin"/skills/*/; do
  skill="$(basename "$skill_dir")"
  cases="plugins/$plugin/evals/$skill"
  [ -d "$cases" ] || continue
  old=""
  for cand in "$tmp/wt"/plugins/*/skills/"$skill"/SKILL.md; do
    [ -f "$cand" ] && old="$(dirname "$(dirname "$(dirname "$cand")")")" && break
  done
  if [ -z "$old" ]; then
    echo "eval.sh: $skill: no plugin held skills/$skill at $against (no baseline)" >&2
    continue
  fi
  arm="$tmp/against-$skill"
  mkdir -p "$arm"
  (cd "$old" && tar --exclude=./evals -cf - .) | (cd "$arm" && tar -xf -)
  mkdir -p "$arm/evals"
  cp -R "$cases" "$arm/evals/$skill"
  # suite-wide material (mocks/, fixtures/) comes along; other skills' case dirs do not
  for shared in "plugins/$plugin"/evals/*/; do
    name="$(basename "$shared")"
    [ -d "plugins/$plugin/skills/$name" ] && continue
    cp -R "$shared" "$arm/evals/$name"
  done
  out="evals/results/$plugin-$mode-against-$refname-$skill-$ts.json"
  echo "eval.sh: $skill at $against ($(basename "$old")) -> $out"
  ran=$((ran + 1))
  set +e
  claude plugin eval "$arm" "${flags[@]}" --json "$out" "${extra[@]}"
  code=$?
  set -e
  [ "$code" -eq 0 ] || status=$code
  # Best effort: the result schema is not documented here, so print every numeric
  # field whose key path names both "with" and "score"; otherwise point at the file.
  python3 - "$out" "$skill" <<'PY' || true
import json, sys
path, skill = sys.argv[1], sys.argv[2]
try:
    data = json.load(open(path, encoding="utf-8"))
except (OSError, ValueError):
    print(f"{skill}: with-arm score unavailable (no readable {path})")
    sys.exit(0)
hits = []
def walk(node, trail):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, trail + [str(k)])
    elif isinstance(node, (int, float)) and not isinstance(node, bool):
        key = ".".join(trail).lower()
        if "with" in key and "score" in key and "without" not in key:
            hits.append((".".join(trail), node))
walk(data, [])
print(f"{skill}: with-arm score " + (", ".join(f"{k}={v}" for k, v in hits[:5]) if hits else f"— see {path}"))
PY
done
[ "$ran" -gt 0 ] || { echo "eval.sh: no baseline at $against for any skill of plugins/$plugin with case dirs" >&2; exit 3; }
exit "$status"
