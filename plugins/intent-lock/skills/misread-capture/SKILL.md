---
name: misread-capture
description: >-
  Logs a misread to the Misread Ledger when the user's reply shows that delivered work missed what they wanted, then redoes the work. Use the moment the user corrects delivered work: "this isn't what I wanted", "you misunderstood", "that's not it", "I asked for X and got Y", "you wasted my time", "ไม่ใช่ที่ผมต้องการ", "เข้าใจผิด", "ไม่ใช่แบบนี้", or a request to redo the work as a different kind of output, for a different use, or at a different depth or breadth. Logs without being asked and asks at most one question. Also use when the user asks to see, add, edit or retire their checks. Not for an ordinary follow-up edit that adds a new wish, and not for a correction made while an intent-lock interview is still running.
---

# Misread Capture

A misread is delivered work that missed something the user had already said, something the
lock stated, or the kind, use, depth or breadth the user wanted. This skill logs it and
turns it into a check that the next intent-lock run reads.

The ledger rules are in the `intent-lock` skill of this plugin, in
`../intent-lock/references/ledger.md` relative to this skill's folder. Read that file first.

## Is it a misread?

- **Yes:** the user had said it, the lock stated it, or the work was the wrong kind, for the
  wrong use, or at the wrong depth or breadth.
- **No:** the user adds a new wish to work that matched the request ("make it shorter",
  "add a section on X"). Do the edit and log nothing.

When you cannot tell, treat it as a misread only if the user's words show the work was not
what they wanted.

## Steps

1. Do not defend the work and do not explain what you understood.
2. Ask at most one question, and only when the reply does not say what the user wanted
   instead. Without that, the work cannot be redone. Otherwise ask nothing.
3. Write one `correction` entry to the ledger without asking permission.
   - Quote the user for `asked` and `mismatch` wherever the user gave the words.
   - Write `got` as plain fact, with no justification.
   - Fill the rest yourself and set `by` to match who worded the `mismatch` line.
4. Add or sharpen one check for it, following the ledger rules. The check names a trigger
   that would appear in a future request and the thing to verify or ask.
5. Tell the user in one sentence what check was logged.
6. Redo the work. Write a corrected lock first, and follow Steps 4 to 7 of the
   `intent-lock` skill: work to the lock, check before delivery, put the lock lines on top.

## When the user asks about their checks

- To see them: read the active checks and list them, and give the ledger page link.
- To add, edit or retire one: make that change in the ledger and confirm it in one sentence.
- Only the user deletes entries and checks. They can do it on the ledger page.

## This skill has failed if

- The work was defended, or the reply explained what Claude had understood.
- More than one question was asked.
- A misread was not logged, or a new wish was logged as a misread.
- A check was written with no concrete trigger.
- The entry was written into a plugin file and not into the ledger.
