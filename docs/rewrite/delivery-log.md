# Delivery log

One row per change to how plugins and VM tooling reach an environment, newest last.
To roll back row N: set the same variable in the same environment to row N's `previous`
value, then append a row whose reason is `rollback of #N`.

Format owner: spec S11 (interface I16). Check: `python3 scripts/delivery_log.py check`
(scripts/health.sh runs it). Setup script text: `docs/rewrite/cloud-setup.sh`.

## Environments

| id | configured at | network access |
|---|---|---|
| `cloud:<id>` | claude.ai/code, cloud environment menu in the session title bar, environment `<name>`, Edit | `<level>` |
| `windows:<host>` | user environment variables on `<host>` (`$env:COMPUTERNAME`), set with PowerShell | n/a |

## W0 mechanism checklist

| check | question | answer | evidence | date | fallback taken |
|---|---|---|---|---|---|
| a | Does a new platform-started multi-repo session load `gridgeist@inline`? | pending | | | |
| b | Do a probe plugin's SessionStart and PreToolUse(Bash) hooks fire in that session? | pending | | | |
| c | Does a many-to-one `renames` map validate on a scratch copy of the real catalog? | yes | https://claude.ai/code/session_01DX4DHycbPctqMkDe1aC5r3 — CLI 2.1.281, scratch copy of the W0-day catalog (vault-keeper, firecrawl, gridgeist, plugin-creator + alignment, evidence, visuals; 10 `renames`): `CLAUDE_CONFIG_DIR=$S/cfg claude plugin validate --strict $S` → exit 0; control `renames.alignment = intent-lock` → exit 1, "chain does not resolve (cycle)" | 2026-09-24 | |
| d | Is `claude plugin eval` enabled on the account, with an http MCP mock answering? | pending | | | |
| e | Do learn-hub `.claude/skills` load, and does a `.claude/rules` file with `paths:` load, in a multi-repo session? | pending | | | |
| f | Does `/doctor` report the listing cost, without overflow, in a multi-repo session? | pending | | | |
| g | Windows: CLI at least 2.1.280, micky source type, learn-hub-local state, and does the variable load a canary? | pending | | | |
| h | Does the setup script run before the repos are cloned? | pending | | | |

## Log

| # | date | environment | variable | previous | new | reason | evidence | rollback |
|---|---|---|---|---|---|---|---|---|
