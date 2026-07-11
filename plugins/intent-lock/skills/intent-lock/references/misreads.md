# Misread ledger

How Claude has misread **this user**, in this user's words.

Entries are written by the user, never by Claude. Claude may append the factual lines
(`Asked for`, `Got`, `Tell arrived`) and must quote the user verbatim for `Axis missed`
and `Prior`. See the `misread-capture` skill for why.

Read `## Active priors` before reading any request. That is the whole point of this file.

---

## Active priors

Newest first. Cap: 7. Each is a check to run, not a lesson to remember. The Active-priors line must be copied verbatim from the entry's `Prior:` line at append time; cap 7 — retirement follows misread-capture's procedure (ask the user which of the oldest three retires), never silent dropping.

1. When he asks to "research" or "review" a topic, run intent-lock first to lock breadth and frame — never collapse a "comprehensive review" into "just Rx."
2. When he says "craft my prompt," check whether he wants the prompt or the work.

---

## Entries

## 2026-07-11 · comprehensive review, not just Rx
Asked for:    Research + comprehensive review of intermittent explosive disorder
Got:          a verdict-first Rx (treatment-only) decision report; the frame was chosen for him without asking
Axis missed:  breadth/frame — "Comprehensive review (Not just Rx)"
Tell arrived: at delivery — the report was Rx-only when a full-disorder review was wanted
Prior:        When he asks to "research" or "review" a topic, run intent-lock first to lock breadth and frame — never collapse a "comprehensive review" into "just Rx."

## 2026-07-09 · the intent-lock skill itself
Asked for:    a way to make you understand my need without misunderstanding
Got:          a prompt-compiler that interviews, then emits a portable prompt artifact and stops
Axis missed:  deliverable shape — I never wanted a file, I wanted you to just start working
Tell arrived: only at the end, after the .skill was already packaged
Prior:        when he says "craft my prompt," check whether he wants the prompt or the work

<!--
Entry template — copy, fill, append below. Leave a line blank rather than inventing it.

## YYYY-MM-DD · <request in five words>
Asked for:    <your words>
Got:          <what was delivered, factually>
Axis missed:  <your words — the dimension, not the symptom>
Tell arrived: <first line | structure | only at the end>
Prior:        <your words — phrased as a check that fires, not a lesson that sits>
-->
