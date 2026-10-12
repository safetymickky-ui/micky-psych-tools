# Changelog

## 0.2.0 — 2026-10-12

- The guess before a why/what-if idea is now an `AskUserQuestion` picker instead of a one-line
  text prompt: header = chunk id, three short predictions (the fitting one mixed in with common
  wrong ones, none marked), `Just tell me`, and his own words through "Other". It is never
  scored, and the lesson follows in the same turn. The text prompt stays only as a fallback when
  no picker exists; unattended runs skip the guess.
- `guess.a` on a saved lesson holds the option he picked or the text he typed (`null` when he
  skipped). The guess eval now checks that the picker was used.

## 0.1.0 — 2026-10-12

- Initial release, built after a brainstorm and a three-round interview with Micky. The locked
  contract: answer-first chunks; a one-line guess only before why/what-if ideas; no quizzes,
  checks or reviews; worked code that really ran; exercises only on request, with a fading
  scaffold; every lesson saved to the Tutor tracker page.
- Tutor tracker page (`skills/tutor/assets/tracker.html`): an artifact with a shared database,
  holding track cards, chunk maps and saved lessons. It uses the Clinical Minimal palette and is
  read-only by design.
- Four domain packs with seeds computed in Python and resources opened on 2026-10-12:
  computational psychiatry (`cp`, 43 chunks, CPC Zurich 2026 tags), Python and R (`py`, 45),
  neural-network architectures (`dl`, 45), math and statistics notation (`ms`, 45).
- `/tutor` command; trigger and near-miss eval cases.
