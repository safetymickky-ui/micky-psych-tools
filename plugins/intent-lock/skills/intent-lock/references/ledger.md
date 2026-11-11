# The Misread Ledger

Both skills in this plugin use one ledger. It is an artifact page with its own database,
so it survives between chats and the user can read and edit it on a phone.

- Title: Misread Ledger
- Slug: `2af470bc-0d78-4d63-abe3-0cd473022fca`
- Page: https://claude.ai/artifact/6JeVKcDeh53yvFsNcMt73f

Never write ledger entries into the plugin's own files. Those files are a per-session copy
and every change to them is lost.

## Tools

Use the artifact database tools of this session. Their names differ by app:

- `db_query`, `db_list`, `db_get`, `db_write` on the claude-artifacts server, each with the slug above.
- Or the Artifact tool's `read_db` and `write_db` actions.

The tools may be deferred. Search the tool list for "artifact db" and load them before the first call.

## Collections

`checks`: one document per check.

- `text`: the check, one sentence: "When <trigger>, <thing to verify or ask>".
- `by`: `"user"` when the text is the user's own words, `"claude"` when Claude wrote it.
- `status`: `"active"` or `"retired"`.
- `created`: `YYYY-MM-DD`.
- `fires`: how many times the trigger matched a request.
- `last_fired`: `YYYY-MM-DD`, or `""`.
- `fire_dates`: list of `YYYY-MM-DD`, one per fire. `[]` for a check that never fired.
- `entry`: id of the entry that produced it, or `""`.
- `type`: what the check guards against: `shape`, `frame`, `depth`, `structure` or `other`.
  Copy it from the entry that produced the check.

The page also keeps `merged_into`, `merged_from`, `merge_prev_text` and
`merge_prev_last_fired` on checks the user merged. Never write or remove them.

`entries`: one document per logged mistake.

- `date`: `YYYY-MM-DD`.
- `kind`: `"drift"` (found by the check before delivery), `"correction"` (the user corrected
  delivered work), or `"process"` (an interview error found by the audit).
- `by`: `"user"` or `"claude"`, by who worded the `mismatch` line.
- `request`: the request in about five words.
- `asked`: what the user asked for. Quote the user.
- `got`: what was produced, as plain fact.
- `mismatch`: what differed. Quote the user when the user said it.
- `type`: the kind of mismatch, one of `shape` (wrong kind of deliverable), `frame` (wrong
  breadth or frame), `depth` (too shallow or too deep), `structure` (wrong layout or order),
  `other`. The page groups misreads and judges each check by it.
- `tell`: when it was noticed: before delivery, first line, structure, or only at the end.
- `check`: the text of the check this entry produced or sharpened, or `""`.
- `fixed`: for `drift` entries, whether it was fixed before delivery.

Document ids: `YYYYMMDD-three-word-slug`, lowercase letters, digits and hyphens.

## Reading

Query `checks` where `status` equals `active`. That is the whole read. Do not read `entries`
during a normal run.

## Writing

- Send one `db_write` call per run, with all ops in it.
- A new document needs no `ifVersion`. A change to an existing document needs the version
  from your read of it.
- When a check fires, add 1 to `fires`, set `last_fired` to today, and send `fire_dates`
  as the list you read with today's date added at the end. A list is replaced whole, so
  never send only the new date.
- Give every new entry a `type`, and every new check the `type` of its entry and
  `fire_dates: []`.
- Write a check only when it names a concrete trigger in the request. "Be more careful" is
  not a check. "When he asks to review a topic, ask whether he wants the whole disorder or
  one decision" is a check.
- Before adding a check, look for an active check with the same trigger. If one exists,
  sharpen its `text` and keep its id. Do not add a second one.
- Keep at most 10 active checks. When an eleventh is added, set `status` to `"retired"` on
  the active check with the oldest `last_fired`; use `created` for a check that never fired.
  Never delete a check or an entry. Only the user deletes.
- Use the user's words where the user gave them. Write your own words only for the parts
  the user did not say, and set `by` to match.

## When the ledger cannot be reached

- Reading: use `checks-snapshot.md` in this folder. It is a copy from release time and may be old.
- Writing: say in one sentence that the ledger was not updated and give the entry in one
  line, so the user can add it on the page. In an intent-lock run, this sentence is one of
  the lock lines.
