# The recap contract

`recap.json` is one JSON object. `scripts/build_recap.py` checks it against the rules below
and renders the page from it. A rule marked **(checked)** fails the build when it is broken.

## Shape

```json
{
  "title": "Plugin build recap",
  "date": "2026-11-10",
  "lang": "en",
  "focus": "",
  "outcome": "Two new plugins exist on the branch and a pull request is open. Neither is merged.",
  "open": [
    {"what": "Review and merge the pull request.", "kind": "todo", "owner": "user"}
  ],
  "done": [
    {
      "what": "Scaffolded the visual-lock plugin: skill, three references, two page templates.",
      "type": "change",
      "status": "done",
      "verified": "yes",
      "check": "c1",
      "detail": "",
      "evidence": [
        {"kind": "file", "ref": "plugins/visual-lock/skills/visual-lock/SKILL.md"},
        {"kind": "commit", "ref": "1e1976d"}
      ]
    }
  ],
  "decisions": [
    {"what": "Saved guidance lives in an artifact database, not in plugin files.", "by": "claude",
     "why": "Plugin files are a per-session copy and lose every change."}
  ],
  "checks": [
    {"id": "c1", "what": "bash scripts/health.sh", "result": "passed", "detail": "health: OK"}
  ],
  "changes": {
    "files": [{"path": "plugins/visual-lock/README.md", "change": "added"}],
    "commits": [{"sha": "1e1976d", "subject": "feat: add visual-lock plugin"}],
    "prs": [{"title": "Add visual-lock and session-recap", "url": "https://github.com/o/r/pull/1", "state": "open"}],
    "artifacts": [{"title": "Look Book", "url": "https://claude.ai/artifact/abc"}],
    "external": [{"what": "Sent the draft to the review list", "where": "Gmail"}]
  },
  "asked": [
    {"text": "Help me build a plugin to interview users for the look."}
  ],
  "notes": {"compacted": false, "gaps": []}
}
```

## Fields

**`title`** (checked) — the page's name: two to four words, specific to this session's work
("Plugin build recap"). Not a sentence, no colon, no dash.

**`date`** (checked) — `YYYY-MM-DD`, from the session's current date. Never guessed.

**`lang`** (checked) — `"en"` or `"th"`. It sets the language of the page's headings. Write
every text field in the same language, with technical terms in English.

**`focus`** — empty for the whole session. Otherwise the part the user asked for, in a few
words; the page then states that the rest of the session is left out.

**`outcome`** (checked) — one to three sentences, at most 400 characters. What exists now
that did not exist before. State facts: "A pull request is open and not merged", not "the
work went well".

**`open`** (checked: the key must exist) — one entry per thing that is not finished.

- `what`: one sentence that says what remains.
- `kind`: `todo` (work that remains), `question` (the user must decide), `risk` (something
  that may be wrong and was not checked), or `blocked` (work stopped by something outside).
- `owner`: `user`, `claude` or `either`.
- An empty list renders as "Nothing is left open". Every `done` item with status `partial`,
  `failed`, `skipped` or `running` needs a matching open entry (the script warns when the
  list is empty and such an item exists).

**`done`** (checked: at least one item) — one entry per piece of work, in the order it happened.

- `what`: one sentence, past tense, naming the thing ("Added a retry to the upload client").
- `type`: `change` (something outside the chat changed) or `answer` (an explanation, an
  analysis or advice given in the chat).
- `status`: `done`, `partial`, `failed`, `skipped` or `running`.
- `verified`: `yes`, `no` or `n/a`. Use `n/a` only for `type: "answer"`.
- `check`: the `id` of the check that verified it. **(checked)** `verified: "yes"` requires a
  `check` whose result is `passed`.
- `detail`: what a reader needs beyond `what`. **(checked)** required when the status is
  `partial`, `failed` or `skipped`: say what is missing or why.
- `evidence`: where the work can be seen. **(checked)** a `change` with status `done` or
  `partial` needs at least one entry.
  - `kind`: `file`, `commit`, `pr`, `artifact`, `command`, `link` or `other`.
  - `ref`: the path, the short SHA, the title or the command.
  - `url`: optional; **(checked)** must start with `http://` or `https://`.
- `from`: optional; `"summary"` when this item comes from a compacted part of the session.

**`decisions`** — the choices that shaped the work.

- `what`: the choice, as a sentence.
- `by`: `user` (the user chose it), `claude` (Claude chose it), or `default` (nobody chose;
  a default applied).
- `why`: the reason given at the time. Leave it empty rather than invent one.

**`checks`** — every check that ran.

- `id`: a short id (`c1`), unique in the list. **(checked)**
- `what`: the command or the action.
- `result`: `passed`, `failed` or `not run`. A check that was planned and never ran is
  listed as `not run`.
- `detail`: the line of output that shows the result.

**`changes`** — the state the session left behind. Every list is optional.

- `files`: `path` and `change` (`added`, `modified`, `deleted` or `renamed`). List at most
  40; when there are more, list the 40 that matter most and say how many are left out in
  `notes.gaps`.
- `commits`: `sha` (**checked**: 7 to 40 hex characters) and `subject`.
- `prs`: `title`, `url` and `state` (`open`, `merged`, `closed` or `draft`).
- `artifacts`: `title` and `url`.
- `external`: anything that left the session: a message sent, a record written, a task
  scheduled. `what` and `where`.

**`asked`** (checked: at least one item) — the user's requests, in order.

- `text`: the request in the user's words, shortened with "…" when long. Fix nothing in it.
- `note`: optional; how a garbled or ambiguous request was read, when that mattered.

**`notes`**

- `compacted`: `true` when part of the session was read from a compacted summary.
- `gaps`: sentences that say what the recap could not establish ("The test run was started
  and its result was not read").

## Text rules

- **Inline code:** wrap a path, a command or an identifier in backticks. Nothing else is
  formatted; the script escapes all HTML.
- **No secrets (checked).** The build fails on anything that looks like a key, a token, a
  password assignment or a private key. Name the place a secret lives, never its value.
- **No praise (warned).** The script warns on words such as "successfully", "seamlessly",
  "robust" and "perfectly". Remove them; the status already says what happened.
- **No personal details (warned).** The script warns on an email address. Remove it unless
  the user asked for it to be on the page.
- **Clinical material by topic only.** "Reviewed a medication question for an inpatient
  case" is fine. Initials, ages with dates, ward names and hospital numbers are not.

## Order of the page

The script renders the sections in this order, and leaves out a section that has no entries
(except "Still open", which always shows):

1. The title, the date and the outcome, with a one-line count.
2. Still open.
3. Done.
4. Decisions.
5. Checks.
6. What changed (pull requests, artifacts, commits, files, things sent outside).
7. What was asked.
8. Notes on gaps, when there are any.

The user reads to decide what to do next, so what is still open comes before what was done.
