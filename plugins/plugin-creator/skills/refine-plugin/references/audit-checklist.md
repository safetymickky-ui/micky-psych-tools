# Audit checklist — quality tier

The mechanical tier lives in `../plugin-creator/references/authoring-rules.md` (version
parity, kebab-case, semver, description length, MCP type/url, name==dir). This file is the
**quality tier** — the judgment checks that a rule-passing skill can still fail. Each is a
pass/fail with a concrete fix.

## Skill / agent description (the trigger)

The description is the ONLY thing that decides when a skill or agent fires. Check:

- [ ] **Action-first, third person** — starts with a verb ("Audits…", "Scaffolds…"), not
      "This skill will…" / "Use this to…". Fix: rewrite the opening clause.
- [ ] **Trigger phrases present verbatim** — the literal phrases a user would type appear
      in the description. Fix: pull them in as a "Use when the user says '…', '…'" clause.
- [ ] **Has a Use-when clause AND a Not-for clause** — positive scope alone triggers on
      neighbours; negative scope sharpens it. Fix: add the missing clause.
- [ ] **Length in the sweet spot** — 200–1024 chars (validate.py enforces), but aim
      ~400–900. Under ~200 triggers unreliably even though it passes. Fix: expand with
      more trigger phrasings and scope.
- [ ] **Concrete, not abstract** — names the real objects/verbs it acts on, not "helps
      with tasks". Fix: replace vague nouns with the actual domain terms.

## SKILL.md body

- [ ] **Lean** — heavy reference material lives in `references/`, not inline. Fix: move it
      out and point to it.
- [ ] **Procedure is ordered and followable** — numbered steps, each one action. Fix:
      break prose into steps.
- [ ] **Has an explicit scope / Not-for** — the body states what it does NOT do. Fix: add.
- [ ] **No redundant reference files** — each `references/*` earns its place; none
      duplicate another or the body. Fix: merge or delete.
- [ ] **Frontmatter name matches its directory** — also a blocker, but check it here too.

## Plugin-level

- [ ] **Catalog description matches the plugin's actual components** — if a plugin gained
      or lost a skill, its `marketplace.json` description should reflect it. Fix: update
      the entry description (no version bump needed for description-only if paired with a
      real change that IS bumped).
- [ ] **Keywords are discoverable** — 3–6, real terms someone would search. Fix: derive
      from purpose + trigger phrases.
- [ ] **plugin.json description ≈ catalog description** — they needn't be identical but
      shouldn't contradict. Fix: align.

## Reporting

Rank blockers above quality findings. For every finding: file · problem · before/after.
Never pad the report — "no findings" is a valid, good result.
