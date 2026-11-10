# session-recap

Writes a summary of what was done in this session as one page. Ask for it at the end of a
working session; it never runs on its own.

The page reads top to bottom in the order you need it:

- **The outcome:** one to three sentences on what exists now that did not exist before.
- **Still open:** what is not finished, what needs your decision, what is at risk.
- **Done:** each piece of work with its status (done, partly done, failed, skipped, still
  running), its evidence (files, commits, pull requests, artifacts, commands) and the check
  that verified it, when one did.
- **Decisions:** what was chosen, by whom (you, Claude, or a default) and why.
- **Checks:** every test, validator or render that ran, with its result.
- **What changed:** pull requests, artifacts, commits, files, and anything sent outside.
- **What was asked:** your requests, in your words.

## Use

```
/recap
/recap the data cleaning
/recap file
```

Or in chat: "summarize this session", "session summary", "recap this session", "what did we
do in this session", "wrap up this session", "handoff summary", "สรุป session นี้",
"สรุปว่าทำอะไรไปบ้าง".

Each session gets its own private artifact page. Ask for "a file" and you get one
self-contained HTML file instead. A second request in the same session updates the same page.

## What it will not do

- It reports only what the session record shows. A step that failed is listed as failed.
- It calls nothing verified unless a check ran in the session and passed.
- It holds no keys, tokens or passwords: the build fails when the data looks like one.
- It holds no grades or praise, and no patient-identifiable detail.

## Checks

`skills/session-recap/scripts/build_recap.py` checks the recap data before it renders
anything: status words, a passed check behind every "verified", evidence behind every
change, a reason behind every failed or skipped item, and no secrets. It warns on praise
words and email addresses.

```
python3 -m unittest discover -s plugins/session-recap/tests
```

## Install

```
/plugin marketplace add safetymickky-ui/micky-psych-tools
/plugin install session-recap@micky-psych-tools
```

## Files

```
skills/session-recap/SKILL.md                      the contract and the procedure
skills/session-recap/references/recap-contract.md  the data shape and every rule
skills/session-recap/scripts/build_recap.py        checks the data, then renders the page
skills/session-recap/assets/recap.template.html    the page template
commands/recap.md                                  /recap
tests/test_build_recap.py                          45 unit tests
tests/fixtures/recap.json                          a worked example
evals/session-recap/                               trigger and near-miss cases
```

## Boundaries

Condensing a paper or a document is bullet-reconstruct. Release notes and a repo's history
belong in its `CHANGELOG.md` and `MEMORY.md`. A progress update in the middle of a task is
one or two lines in chat and needs no page. Recaps are not filed to the vault.
