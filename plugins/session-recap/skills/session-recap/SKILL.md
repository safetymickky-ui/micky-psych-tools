---
name: session-recap
description: >-
  Writes a summary of what was done in this session as one page: what is still open, what was
  done with its evidence (files, commits, pull requests, artifacts), what was decided and by
  whom, what was checked, and what was asked. Publishes it as a private artifact, one page per
  session, or writes one HTML file when asked. Use when the user says "summarize this
  session", "session summary", "recap this session", "what did we do in this session",
  "summary of what was done", "wrap up this session", "handoff summary", "สรุป session นี้",
  "สรุปว่าทำอะไรไปบ้าง", "สรุปงานที่ทำ", or runs /recap. Only on request: never offers or
  builds one unasked. Reports only what the session record shows: a failed or skipped step is
  listed as such, and nothing is called verified without a check that ran. Not for
  summarizing a paper or document (bullet-reconstruct), a meeting or email thread, release
  notes or a repo changelog, or updating a memory file.
---

# Session recap

Turns this session into one page the user can read in two minutes and open again later:
what is still open, what was done, what was decided, what was checked, what changed, and
what was asked.

The user locked this shape on 2026-11-10: one page per session, published as a private
artifact, and made only on request.

## The contract

- **Only what the record shows.** Every line comes from the conversation, from a tool
  result in it, or from state read in Step 1. Never fill a gap with what probably happened.
- **Status is exact.** An item is `done`, `partial`, `failed`, `skipped` or `running`. A
  step that failed and was later fixed is one `done` item whose detail names the failure.
- **Verified means a check ran.** An item is verified only when a check in this session
  passed and the recap names it. "It should work" is not a check.
- **State, not praise.** No grades, no "successfully", no opinion on the work or the user.
- **Private things stay out.** No keys, tokens or passwords. No patient-identifiable
  detail: describe clinical material by topic only. No personal details of other people.
- **The page follows [references/recap-contract.md](references/recap-contract.md)**, and
  `scripts/build_recap.py` must exit 0 before the page is shown.
- **The user's standing preferences apply.** Write the recap in the language the user used
  most in the session, with technical terms in English. Short sentences, common words, no
  lead-in labels inside a sentence.

## Step 0. Route

- **"Summarize this session", `/recap`:** the whole session.
- **A focus in the request** ("only the plugin work", `/recap the data cleaning`): the
  whole session is still read; the page holds only the items that belong to the focus, and
  its first line says what was left out.
- **"As a file", "HTML file", "don't publish":** build the file and send it; do not publish.
- **A second request in the same session:** rebuild from the same file path, so the same
  page is updated and the link stays the same.
- **Nothing was done yet** (the request is the first turn): say so in one line and stop.
- **A request to summarize something else** (a paper, a meeting, an email thread, a repo's
  history): this skill does not apply.

Ask nothing. This request is already precise, so intent-lock does not run.

## Step 1. Collect the record

Read the session from its first turn to now, and collect:

1. **Requests.** Each thing the user asked for, in the user's words. Keep a short quote.
2. **Answers and corrections.** Each picker answer the user gave, and each time the user
   corrected the work.
3. **Actions.** Each tool call that changed something: a file written, edited or deleted;
   a command that changed state; a commit, a push, a pull request; an artifact published; a
   message or email sent; a database write; a scheduled task. Record the outcome the tool
   returned, not the outcome intended.
4. **Checks.** Each test, validator, render or read-back that ran, with its command and its
   result.
5. **Decisions.** Each choice that shaped the work, who made it (the user, Claude, or a
   default nobody chose) and the reason given at the time.
6. **Work in progress.** Background commands and agents that have not reported yet.

Then read the state that can be read, and prefer it to the conversation when they differ:

- In a git repository: `git status --short`, `git log --oneline` for the commits made in
  this session, and `git diff --stat` against the commit the session started from.
- A pull request or an artifact made in this session: its URL from the tool result.
- A difference between the conversation and the state (a file the session wrote that is no
  longer there, a commit that was never pushed) is a finding. Put it in the open items.

When earlier turns exist only as a compacted summary, the items from that part are marked
`"from": "summary"`, and the page says so.

## Step 2. Write the recap data

Write `recap.json` to the scratchpad, in the shape
[references/recap-contract.md](references/recap-contract.md) defines. In short:

1. `outcome`: one to three sentences on what exists now that did not exist before the
   session. This is the first thing the user reads.
2. `open`: what is not finished, what needs the user's decision, what is at risk. An empty
   list is a claim that nothing is open; make it only when that is true.
3. `done`: one item per piece of work, in the order it happened, each with its status, its
   evidence and whether a check verified it.
4. `decisions`, `checks`, `changes`, `asked`: as the contract says.

Order `open` by what blocks the user first. Merge steps that served one piece of work into
one item; do not list every tool call.

## Step 3. Build and check

Run, from this skill's directory:

```
python3 scripts/build_recap.py <scratchpad>/recap.json -o <scratchpad>/<slug>-recap.html
```

- The script checks the data first and builds nothing when a rule is broken. Fix every
  error it names and run it again until it exits 0.
- Read its warnings and fix the ones that are real.
- Never weaken a status or delete a failed item to pass. The rules exist to stop that.
- `<slug>` is two to four words for this session's work, in kebab-case
  (`plugin-build-recap.html`). Keep the same path for every rebuild in this session.

## Step 4. Deliver

- **Default:** publish the file with the `Artifact` tool: `icon: "clipboard"`, and a
  one-sentence `description` that names the session's work. The page is private until the
  user shares it. No `capabilities`.
- **File requested, or no `Artifact` tool:** send the HTML file to the user
  (`SendUserFile` when it exists; otherwise give its full path).
- Never publish a recap that holds anything the contract says must stay out. Remove it
  from `recap.json` and rebuild first.

## Step 5. Reply in chat

- First line: the link (or the file).
- Then at most five bullets: the outcome, then each open item that needs the user. When
  nothing is open, say so in one bullet.
- No table, no closing summary, no offer to do more.

## Not for

Summarizing a paper, a chapter or a document (bullet-reconstruct); a meeting, a call or an
email thread; release notes or a changelog for a repository (the repo's own `CHANGELOG.md`
and `MEMORY.md`); saving standing preferences to memory; a mid-task progress update, which
is one or two lines in chat and needs no page.
