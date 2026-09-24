# Changelog

Repo-level tooling of micky-psych-tools: `scripts/`, `docs/rewrite/`, `CLAUDE.md`,
`README.md` (plan OQ16-a). A plugin's own changes go to `plugins/<name>/CHANGELOG.md`.
Every repo-tooling step of specs S10, S11 and S12 adds its line under `## Unreleased`.

## Unreleased

### W0 tooling (plugin rewrite, specs S10–S12)

- `scripts/validate.py`: every load guarded and every check counted (H13); CRLF-safe
  `yaml.safe_load` frontmatter; stdio MCP servers pass; the 200-char floor is a WARN;
  version parity removed; ratcheted `yaml-parse` entries print WARN (S10-W0-1).
- `scripts/rewrite_gate.py`: ratchet, trigger lock, h-coverage checklist and baseline
  measurements; `docs/rewrite/{ratchet.json,triggers.lock.json,h-coverage.md}` generated
  (S12-W0-1).
- `docs/rewrite/ratchet.json`: the `yaml-parse` entry for intent-lock seeded (S10-W0-1b).
- `.claude-plugin/marketplace.json`: every `version` removed; version lives in
  `plugin.json` only (S10-W0-3).
- `scripts/bump.py`: dry run by default, `--write` validates first, writes `plugin.json`
  only and adds a CHANGELOG entry (S10-W0-2).
- `scripts/route.py`: argparse CLI (`--help` writes nothing); no versions in `ROUTING.md`
  (S10-W0-4).
- `.gitignore`: `.env`, `.firecrawl/`, `plugins/*/evals/results/` (S10-W0-7).
- Every plugin has a README, a LICENSE (MIT, Thanawat Suharit (Micky), 2026; gridgeist
  keeps upstream's) and a CHANGELOG whose top entry equals its `plugin.json` version;
  this file created (S10-W0-8).
- `scripts/health.sh [--fast]`: validate.py, `claude plugin validate --strict` on the
  catalog and every plugin, `ratchet verify`, `triggers verify`; the full mode adds the
  script unit tests (S10-W0-9).
- `.githooks/pre-commit`: runs `bash scripts/health.sh --fast`; enable once per clone with
  `git config core.hooksPath .githooks` (S10-W0-10).
- `CLAUDE.md`: version rule is "plugin.json only" with `bump.py --write`; MEMORY.md and
  ROUTING.md demoted to on-demand reading; the workflow and health check run
  `bash scripts/health.sh`; the layout lists README, CHANGELOG, LICENSE, `hooks/hooks.json`,
  `references/` and `evals/<skill>/<case>/` (S10-W0-5).
