# egm-conductor

Master controller for Google's [Elephant-Goldfish Model](https://github.com/google/elephant-goldfish-model)
(`egm@egm`). One command takes a feature from idea to code and keeps checking
it against its spec:

```
preflight → [bootstrap] → brainstorm → draft → review (+resolve) → human gate → implement → drift
```

EGM still does the work of every stage; the conductor runs them in order,
hands each stage's artifact to the next, and saves progress in
`.egm-conductor/state.json` so you can stop and resume.

## Requires

- Claude Code 2.1.271 or later
- `egm@egm` installed and enabled:
  ```
  claude plugin marketplace add google/elephant-goldfish-model
  claude plugin install egm@egm
  ```
- Python 3.10+ on `PATH` (for `scripts/egm_status.py`)

## Install

```
claude plugin install egm-conductor@micky-psych-tools
```

Restart Claude Code after installing.

## Use

| Command | Does |
|---|---|
| `/egm-conductor:conduct <idea>` | Start a new feature at brainstorm |
| `/egm-conductor:conduct docs/designs/x.md` | Start at review for an existing design |
| `/egm-conductor:conduct --from drift` | Jump to a phase |
| `/egm-conductor:conduct --auto` | Skip conductor confirmations; review runs uninterrupted |
| `/egm-conductor:conduct` | Resume from saved state |
| `/egm-conductor:status` | Show install health, artifacts, next phase |

`--auto` never skips EGM's own questions in brainstorm and draft, or the human
approval gate before implementation.

## Why the conductor reads EGM skill files

EGM marks its skills `disable-model-invocation: true`, so another skill cannot
call them through the Skill tool. As EGM's own `docs/claude.md` directs, the
conductor reads each `SKILL.md` from the installed EGM path (found in
`~/.claude/plugins/installed_plugins.json`) and follows it in the main thread,
spawning the registered `egm:egm-*` Goldfish agents for reviews.
