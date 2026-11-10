# Changelog

## 0.1.0 — 2026-11-10

- Initial release. One page per session that says what is still open, what was done with
  its evidence, what was decided and by whom, what was checked, what changed and what was
  asked. The owner chose on 2026-11-10: one private artifact page per session, made only on
  request.
- `build_recap.py` checks the recap data and renders nothing when a rule is broken: status
  and result words, a passed check behind every "verified", evidence behind every change, a
  reason behind every partial, failed or skipped item, a title that is a name, a file cap of
  40, and no keys, tokens or passwords. It warns on praise words and email addresses.
  45 unit tests.
- Page template (`assets/recap.template.html`): one reading column, open items before the
  record of work, each status shown as a mark, a word and a colour. English and Thai
  headings. Clinical Minimal palette, light and dark, prints cleanly. No tables.
- `/recap` command; trigger and near-miss eval cases.
