"""Tests for skills/learning-map/scripts/check_map.py.

    python3 -m unittest discover -s plugins/learning-map/tests
"""
import copy
import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "skills", "learning-map", "scripts", "check_map.py")
spec = importlib.util.spec_from_file_location("check_map", SCRIPT)
cm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cm)

SOURCE = ("We pooled 392 participants. Reward sensitivity fell with anhedonia "
          "(r = −0.21, 95% CI −0.33 to −0.08), p < .05, n = 1,204 trials.")


def item(iid, level, needs=(), **extra):
    it = {"id": iid, "level": level, "name": f"Concept {iid}", "field": "statistics",
          "primer": "What it is.", "why": "Table 1 depends on it.", "needs": list(needs)}
    if level == 2:
        it["where"] = "Methods"
    it.update(extra)
    return it


def pearl(text="Reward sensitivity fell with anhedonia.", basis="material", **extra):
    p = {"text": text, "type": "finding", "where": "Results", "basis": basis, "uses": ["a1"]}
    p.update(extra)
    return p


def step(kind="deeper", **extra):
    s = {"topic": "Model comparison", "kind": kind, "why": "It builds on the fitted models.",
         "question": "Which model wins and by how much?", "ladder": ["a1"], "pearls": [1]}
    s.update(extra)
    return s


def good_map():
    return {
        "title": "A test paper", "kind": "paper", "field": "computational psychiatry",
        "date": "2026-10-23", "gist": "It fits models to choices.",
        "source": {"cite": "Doe 2026", "url": "https://example.org/x", "read": "full text"},
        "ladder": [item("a1", 2, ["b1"]), item("a2", 2, ["b1"]), item("a3", 2, ["c1"]),
                   item("b1", 1, ["c1"]), item("c1", 0)],
        "pearls": [pearl(), pearl("We pooled 392 participants."),
                   pearl("The correlation was r = -0.21 (95% CI -0.33 to -0.08)."),
                   pearl("Significance was set at p < 0.05 over 1204 trials."),
                   pearl("My inference is that the effect is small.", basis="inference")],
        "path": [step("deeper"), step("wider"), step("challenge", pearls=[2, 5])],
    }


def errors(m, source=None, map_id=None):
    return cm.check(m, source, map_id)["errors"]


class ValidMap(unittest.TestCase):
    def test_good_map_passes_with_source(self):
        r = cm.check(good_map(), SOURCE, "doe-2026-test")
        self.assertTrue(r["ok"], r["errors"])
        self.assertEqual(r["counts"]["level2"], 3)
        self.assertEqual(r["counts"]["pearls"], 5)

    def test_you_on_all_items_is_fine(self):
        m = good_map()
        for it in m["ladder"]:
            it["you"] = "new"
        self.assertEqual(errors(m), [])


class Ladder(unittest.TestCase):
    def test_upward_edge_fails(self):
        m = good_map()
        m["ladder"][4]["needs"] = ["a1"]
        self.assertTrue(any("lower level" in e for e in errors(m)))

    def test_same_level_edge_fails(self):
        m = good_map()
        m["ladder"][0]["needs"] = ["a2"]
        self.assertTrue(any("lower level" in e for e in errors(m)))

    def test_orphan_lower_item_fails(self):
        m = good_map()
        m["ladder"].append(item("c2", 0))
        self.assertTrue(any("nothing above it needs it" in e for e in errors(m)))

    def test_unknown_need_fails(self):
        m = good_map()
        m["ladder"][0]["needs"] = ["zz"]
        self.assertTrue(any("unknown id" in e for e in errors(m)))

    def test_level2_needs_where(self):
        m = good_map()
        del m["ladder"][0]["where"]
        self.assertTrue(any("need 'where'" in e for e in errors(m)))

    def test_level_counts(self):
        m = good_map()
        m["ladder"] = [it for it in m["ladder"] if it["id"] != "a3"]
        self.assertTrue(any("level 2 has 2 items" in e for e in errors(m)))

    def test_link_in_primer_fails(self):
        m = good_map()
        m["ladder"][1]["primer"] = "See https://example.org for more."
        self.assertTrue(any("concepts only" in e for e in errors(m)))

    def test_bad_you_fails(self):
        m = good_map()
        m["ladder"][0]["you"] = "maybe"
        self.assertTrue(any("you must be" in e for e in errors(m)))


class Pearls(unittest.TestCase):
    def test_number_not_in_source_fails(self):
        m = good_map()
        m["pearls"][1]["text"] = "We pooled 393 participants."
        self.assertTrue(any("393" in e for e in errors(m, SOURCE)))

    def test_inference_numbers_are_not_checked(self):
        m = good_map()
        m["pearls"][4]["text"] = "My inference is that 80% of the effect is noise."
        self.assertEqual(errors(m, SOURCE), [])

    def test_leading_dot_and_thousands_separator_match(self):
        m = good_map()
        m["pearls"][3]["text"] = "Alpha was .05; the task had 1,204 trials."
        self.assertEqual(errors(m, SOURCE), [])

    def test_too_many_inference_pearls(self):
        m = good_map()
        m["pearls"] = [pearl(basis="inference") for _ in range(4)] + [pearl()]
        self.assertTrue(any("inference pearls" in e for e in errors(m)))

    def test_pearl_count(self):
        m = good_map()
        m["pearls"] = m["pearls"][:4]
        self.assertTrue(any("pearls: 4" in e for e in errors(m)))

    def test_unknown_use_fails(self):
        m = good_map()
        m["pearls"][0]["uses"] = ["zz"]
        self.assertTrue(any("unknown ladder id" in e for e in errors(m)))


class Path(unittest.TestCase):
    def test_link_in_path_fails(self):
        m = good_map()
        m["path"][1]["why"] = "Read doi: 10.1000/xyz first."
        self.assertTrue(any("concepts only" in e for e in errors(m)))

    def test_needs_deeper_and_wider_or_challenge(self):
        m = good_map()
        m["path"] = [step("apply"), step("apply"), step("apply")]
        errs = errors(m)
        self.assertTrue(any("'deeper'" in e for e in errs))
        self.assertTrue(any("'wider' or 'challenge'" in e for e in errs))

    def test_pearl_number_out_of_range(self):
        m = good_map()
        m["path"][0]["pearls"] = [9]
        self.assertTrue(any("out of range" in e for e in errors(m)))

    def test_step_count(self):
        m = good_map()
        m["path"] = m["path"][:2]
        self.assertTrue(any("path: 2 steps" in e for e in errors(m)))


class TopLevel(unittest.TestCase):
    def test_bad_map_id(self):
        self.assertTrue(any("map id" in e for e in errors(good_map(), map_id="Bad_Id")))

    def test_bad_kind_and_date(self):
        m = good_map()
        m["kind"], m["date"] = "podcast", "23/10/2026"
        errs = errors(m)
        self.assertTrue(any(e.startswith("kind") for e in errs))
        self.assertTrue(any(e.startswith("date") for e in errs))

    def test_partial_read_warns(self):
        m = good_map()
        m["source"]["read"] = "abstract only"
        r = cm.check(m)
        self.assertTrue(r["ok"])
        self.assertTrue(any("partial" in w for w in r["warnings"]))


class Cli(unittest.TestCase):
    def run_cli(self, m, extra=()):
        with tempfile.TemporaryDirectory() as d:
            mp, sp = os.path.join(d, "m.json"), os.path.join(d, "s.txt")
            with open(mp, "w", encoding="utf-8") as f:
                json.dump(m, f)
            with open(sp, "w", encoding="utf-8") as f:
                f.write(SOURCE)
            out = io.StringIO()
            with redirect_stdout(out):
                code = cm.main([mp, "--source", sp, *extra])
            return code, json.loads(out.getvalue())

    def test_exit_zero_when_ok(self):
        code, res = self.run_cli(good_map(), ["--id", "doe-2026-test"])
        self.assertEqual(code, 0)
        self.assertTrue(res["ok"])

    def test_exit_one_when_broken(self):
        m = good_map()
        m["pearls"][1]["text"] = "We pooled 999 participants."
        code, res = self.run_cli(m)
        self.assertEqual(code, 1)
        self.assertFalse(res["ok"])

    def test_exit_two_on_missing_file(self):
        out = io.StringIO()
        with redirect_stdout(out):
            code = cm.main(["/nonexistent/map.json"])
        self.assertEqual(code, 2)

    def test_does_not_mutate_input(self):
        m = good_map()
        before = copy.deepcopy(m)
        cm.check(m, SOURCE)
        self.assertEqual(m, before)


if __name__ == "__main__":
    unittest.main()
