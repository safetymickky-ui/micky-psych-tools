"""Tests for scripts/rewrite_gate.py (S12-W0-1).

Run: python3 -m unittest discover -s scripts -p 'test_rewrite_gate.py' -q
     (or: python3 -m unittest scripts.test_rewrite_gate)
Fixtures live in temporary directories; no network, no wall clock (dates are injected).
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rewrite_gate as g  # noqa: E402

DATE = "2026-01-02"


def write(root, rel, text):
    path = os.path.join(root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    return path


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def skill(root, name, description, plugin="p"):
    return write(root, f"plugins/{plugin}/skills/{name}/SKILL.md",
                 f"---\nname: {name}\ndescription: {description}\n---\n\n# {name}\n")


def ratchet(entries):
    return {"schema": 1, "generated_at": DATE, "repo": "t", "entries": entries}


def entry(check_id, path):
    return {"check_id": check_id, "path": path, "message": "m"}


class Tmp(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name

    def tearDown(self):
        self._tmp.cleanup()


class RatchetTests(Tmp):
    def test_shrink_only_growth_of_existing_check_fails(self):
        base = ratchet([entry("yaml-parse", "a")])
        cur = ratchet([entry("yaml-parse", "a"), entry("yaml-parse", "b")])
        errors = g.compare_ratchet(base, cur)
        self.assertEqual(len(errors), 1)
        self.assertIn("may only shrink", errors[0])

    def test_shrink_and_equal_pass(self):
        base = ratchet([entry("yaml-parse", "a"), entry("R70", "x")])
        self.assertEqual(g.compare_ratchet(base, ratchet([entry("R70", "x")])), [])
        self.assertEqual(g.compare_ratchet(base, base), [])

    def test_first_seed_of_new_check_id_passes(self):
        base = ratchet([])
        cur = ratchet([entry("yaml-parse", "a"), entry("yaml-parse", "b")])
        self.assertEqual(g.compare_ratchet(base, cur), [])
        self.assertEqual(g.compare_ratchet(None, cur), [])

    def test_verify_against_explicit_base(self):
        write(self.root, g.RATCHET, g.dump_json(ratchet([entry("R70", "x"), entry("R70", "y")])))
        res = g.ratchet_verify(self.root, base=ratchet([entry("R70", "x")]), base_given=True)
        self.assertFalse(res["ok"])
        res = g.ratchet_verify(self.root, base=ratchet([entry("R70", "x"), entry("R70", "y"),
                                                        entry("R70", "z")]), base_given=True)
        self.assertTrue(res["ok"], res)

    def test_verify_rejects_bad_schema_and_duplicates(self):
        data = ratchet([entry("R70", "x"), entry("R70", "x")])
        data["schema"] = 2
        write(self.root, g.RATCHET, json.dumps(data))
        res = g.ratchet_verify(self.root, base=None, base_given=True)
        self.assertFalse(res["ok"])
        self.assertTrue(any("schema" in e for e in res["errors"]))
        self.assertTrue(any("duplicates" in e for e in res["errors"]))

    def test_init_seed_close_round_trip(self):
        write(self.root, ".claude-plugin/marketplace.json", json.dumps({"name": "t"}))
        skill(self.root, "bad", "Colon: inside: an unquoted value")
        skill(self.root, "good", "Plain words only")
        g.ratchet_init(self.root, write=True, date=DATE)
        with self.assertRaises(g.Refused):
            g.ratchet_init(self.root, write=True, date=DATE)
        res = g.ratchet_seed(self.root, "yaml-parse", write=True, date=DATE)
        self.assertEqual([a["path"] for a in res["added"]], ["plugins/p/skills/bad/SKILL.md"])
        with self.assertRaises(g.Refused):  # a second seed of the same check id would grow it
            g.ratchet_seed(self.root, "yaml-parse", write=True, date=DATE)
        g.ratchet_close(self.root, "yaml-parse", "plugins/p/skills/bad/SKILL.md", write=True, date=DATE)
        self.assertEqual(g.load_ratchet(self.root)["entries"], [])
        with self.assertRaises(g.Refused):
            g.ratchet_close(self.root, "yaml-parse", "plugins/p/skills/bad/SKILL.md", date=DATE)

    def test_seed_dry_run_writes_nothing(self):
        skill(self.root, "bad", "Colon: inside: an unquoted value")
        g.ratchet_init(self.root, write=True, date=DATE)
        before = read(os.path.join(self.root, g.RATCHET))
        g.ratchet_seed(self.root, "yaml-parse", write=False, date=DATE)
        self.assertEqual(read(os.path.join(self.root, g.RATCHET)), before)

    def test_seed_from_file_and_unknown_check_without_file(self):
        g.ratchet_init(self.root, write=True, date=DATE)
        src = write(self.root, "v.json", json.dumps([{"path": "a/b", "message": "no evals"}]))
        res = g.ratchet_seed(self.root, "R70", source=src, write=True, date=DATE)
        self.assertEqual(res["added"][0]["check_id"], "R70")
        with self.assertRaises(g.UsageError):
            g.ratchet_seed(self.root, "R71", date=DATE)

    def test_verify_warns_on_fixed_entry(self):
        skill(self.root, "ok", "Plain words")
        write(self.root, g.RATCHET, g.dump_json(ratchet([entry("yaml-parse", "plugins/p/skills/ok/SKILL.md")])))
        res = g.ratchet_verify(self.root, base=None, base_given=True)
        self.assertTrue(res["ok"])
        self.assertTrue(any("close it" in w for w in res["warnings"]))


class TriggerTests(Tmp):
    def test_quoted_and_slash_extraction(self):
        text = ('Use when the user says "interview me", “lock the goal”, or runs /new-plugin. '
                'Reads references/x.md and https://example.com/path, and/or `/critique-plan`. '
                'Not "/quoted-slash" twice.')
        found = g.phrases_in(text)
        self.assertIn(("interview me", "quoted"), found)
        self.assertIn(("lock the goal", "quoted"), found)
        self.assertIn(("/new-plugin", "slash"), found)
        self.assertIn(("/critique-plan", "slash"), found)
        self.assertIn(("/quoted-slash", "quoted"), found)
        self.assertNotIn(("/quoted-slash", "slash"), found)
        slashes = [p for p, k in found if k == "slash"]
        self.assertEqual(sorted(slashes), ["/critique-plan", "/new-plugin"])

    def test_raw_line_fallback_for_invalid_yaml(self):
        skill(self.root, "broken", 'Gate. Use when "interview me" or "ask me": then build. Runs /lock.')
        rows, modes = g.scan_repo(self.root)
        self.assertEqual(modes["broken"], "raw-line")
        self.assertIn("interview me", [r["phrase"] for r in rows])
        self.assertIn("/lock", [r["phrase"] for r in rows])

    def test_folded_block_description(self):
        write(self.root, "plugins/p/skills/f/SKILL.md",
              '---\nname: f\ndescription: >-\n  Folded. Use when "fold me"\n  or runs /fold.\n---\nbody\n')
        rows, modes = g.scan_repo(self.root)
        self.assertEqual(modes["f"], "yaml")
        self.assertEqual(sorted(r["phrase"] for r in rows), ["/fold", "fold me"])

    def test_extract_verify_remove_cycle(self):
        path = skill(self.root, "a", 'Use when "one" or "two".')
        skill(self.root, "empty", "No phrases here at all")
        res = g.triggers_extract(self.root, write=True)
        self.assertEqual(res["added"], 2)
        self.assertEqual(res["no_phrases"], ["empty"])
        self.assertTrue(g.triggers_verify(self.root)["ok"])
        # silent drop of "two" fails verify
        write(self.root, os.path.relpath(path, self.root), '---\nname: a\ndescription: Use when "one".\n---\n')
        res = g.triggers_verify(self.root)
        self.assertFalse(res["ok"])
        self.assertIn("'two'", res["errors"][0])
        # retiring it through remove makes verify pass and keeps a ledger row
        g.triggers_remove(self.root, "narrowed in test", "a", phrase="two", write=True, date=DATE)
        self.assertTrue(g.triggers_verify(self.root)["ok"])
        lock = g.load_lock(self.root)
        self.assertEqual(lock["removed"][0]["phrase"], "two")
        self.assertEqual(lock["removed"][0]["reason"], "narrowed in test")

    def test_new_phrase_warns_and_extract_adds_it(self):
        path = skill(self.root, "a", 'Use when "one".')
        g.triggers_extract(self.root, write=True)
        write(self.root, os.path.relpath(path, self.root), '---\nname: a\ndescription: Use when "one" or "new".\n---\n')
        res = g.triggers_verify(self.root)
        self.assertTrue(res["ok"])
        self.assertTrue(res["warnings"])
        self.assertEqual(g.triggers_extract(self.root, write=True)["added"], 1)

    def test_remove_whole_skill_and_missing_skill_fails_verify(self):
        path = skill(self.root, "gone", 'Use when "x" or "y".')
        g.triggers_extract(self.root, write=True)
        os.remove(path)
        self.assertFalse(g.triggers_verify(self.root)["ok"])
        res = g.triggers_remove(self.root, "skill deleted", "gone", write=True, date=DATE)
        self.assertEqual(len(res["removed"]), 2)
        self.assertTrue(g.triggers_verify(self.root)["ok"])
        with self.assertRaises(g.UsageError):
            g.triggers_remove(self.root, " ", "gone")

    def test_extract_one_skill_only(self):
        skill(self.root, "a", 'Use when "one".')
        skill(self.root, "b", 'Use when "two".')
        res = g.triggers_extract(self.root, skill="b", write=True)
        self.assertEqual(res["added"], 1)
        self.assertEqual([p["skill"] for p in g.load_lock(self.root)["phrases"]], ["b"])


APPENDIX = """## Appendix A

| H | Inventory id | Defect (short) | Evidence | Fix | Wave |
|---|---|---|---|---|---|
| H01 | a-1 | first defect | x | y | W3 |
| H07 | b-1 | split defect | x | y | W1/W3 |
| H13 | c-1 | tooling | x | y | W0 |
"""


class HCoverageTests(Tmp):
    def test_round_trip(self):
        src = write(self.root, "arch.md", APPENDIX)
        res = g.h_coverage_seed(self.root, src, write=True)
        self.assertEqual(res["rows"], 4)
        text = read(os.path.join(self.root, g.HCOV))
        self.assertEqual(text.count("\n- [ ] "), 4)
        self.assertIn("- [ ] H07a b-1 — split defect — closed: no — wave: W1", text)
        self.assertIn("- [ ] H07b b-1 — split defect — closed: no — wave: W3", text)
        with self.assertRaises(g.Refused):
            g.h_coverage_seed(self.root, src, write=True)
        with self.assertRaises(g.Refused):
            g.h_coverage_close(self.root, "H13", "W1", write=True)
        with self.assertRaises(g.UsageError):
            g.h_coverage_close(self.root, "H07", "W1", write=True)
        g.h_coverage_close(self.root, "H13", "W0", write=True)
        text = read(os.path.join(self.root, g.HCOV))
        self.assertIn("- [x] H13 c-1 — tooling — closed: yes — wave: W0\n", text)
        self.assertTrue(text.endswith("\n"))
        with self.assertRaises(g.Refused):
            g.h_coverage_close(self.root, "H13", "W0", write=True)
        open_rows = [line for line in text.split("\n") if line.startswith("- [ ]") and line.endswith("wave: W0")]
        self.assertEqual(open_rows, [])

    def test_bad_row_is_usage_error(self):
        src = write(self.root, "arch.md", "| H99 | a | b | W1 |\n")
        with self.assertRaises(g.UsageError):
            g.h_coverage_seed(self.root, src)


DETAILS = """gridgeist 0.1.0
Projected token cost
  Always-on:   ~1.2k tok   added to every session

Per-component (rounded)
  component  always-on  on-invoke
  gridgeist       ~280      ~1.5k

  On-invoke cost is paid each time a skill or agent fires.
"""


class BaselineTests(Tmp):
    def test_degrades_to_manual_without_claude_learn_hub_or_synced(self):
        write(self.root, "CLAUDE.md", "# x\n")
        write(self.root, "plugins/p/.claude-plugin/plugin.json", json.dumps({"name": "p"}))
        skill(self.root, "s", "A description long enough.")
        res = g.baseline_measure(self.root, "W0", learn_hub=os.path.join(self.root, "nope"),
                                 claude=None, synced_dir=os.path.join(self.root, "none"),
                                 write=True, date=DATE)
        section = res["section"]
        self.assertTrue(section.startswith(f"## W0 — {DATE}\n"))
        self.assertIn("| micky always-on (plugin details sum) | MANUAL", section)
        self.assertIn("| /doctor listing cost and overflow | MANUAL", section)
        self.assertIn("| claude.ai-synced listing | MANUAL", section)
        self.assertIn("| micky CLAUDE.md | 4 B / 1 lines / ~1 tok |", section)
        self.assertIn("| ROUTING.md | absent |", section)

    def test_section_replace_keeps_owner_sections(self):
        existing = ("# Baseline\n\n## W0 — 2025-01-01\n\nold\n\n## W0 smoke\n\nkeep me\n\n"
                    "## Owner records\n\n- r\n")
        text = g.replace_section(existing, "W0", "## W0 — 2026-01-02\n\nnew\n")
        self.assertNotIn("old", text)
        self.assertIn("new", text)
        self.assertIn("## W0 smoke\n\nkeep me", text)
        self.assertIn("## Owner records\n\n- r", text)
        self.assertEqual(text.count("## W0 —"), 1)
        appended = g.replace_section(text, "W3", "## W3 — 2026-02-01\n\nw3\n")
        self.assertIn("## W0 — 2026-01-02", appended)
        self.assertTrue(appended.endswith("## W3 — 2026-02-01\n\nw3\n"))

    def test_parse_details(self):
        info = g.parse_details(DETAILS)
        self.assertEqual(info["always_on"], 1200)
        self.assertEqual(info["components"], [("gridgeist", 280, 1500)])
        self.assertIsNone(g.parse_details("no numbers here"))


class CliTests(Tmp):
    def test_help_has_no_side_effects_and_bad_usage_exits_2(self):
        cwd = os.getcwd()
        os.chdir(self.root)
        sink = io.StringIO()
        try:
            with contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
                self.assertEqual(g.main(["ratchet", "--help"]), 0)
                self.assertEqual(g.main([]), 2)
                self.assertEqual(g.main(["ratchet", "seed"]), 2)
        finally:
            os.chdir(cwd)
        self.assertEqual(os.listdir(self.root), [])


if __name__ == "__main__":
    unittest.main()
