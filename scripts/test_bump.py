"""Tests for scripts/bump.py (S10-W0-2).

Run: python3 -m unittest discover -s scripts -p 'test_bump.py' -q
Fixtures live in temporary directories; the validator is injected, so no subprocess runs.
"""
import io
import json
import os
import tempfile
import unittest

import bump

DATE = "2026-01-02"


def read(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def snapshot(root):
    files = {}
    for dirpath, _, names in os.walk(root):
        for n in names:
            p = os.path.join(dirpath, n)
            files[os.path.relpath(p, root)] = read(p)
    return files


class BumpTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = self._tmp.name
        os.makedirs(os.path.join(self.root, ".claude-plugin"))
        os.makedirs(os.path.join(self.root, "plugins", "alpha", ".claude-plugin"))
        with open(os.path.join(self.root, ".claude-plugin", "marketplace.json"), "w", encoding="utf-8") as fh:
            json.dump({"name": "t", "plugins": [{"name": "alpha", "source": "./plugins/alpha"}]}, fh)
        self.man = os.path.join(self.root, "plugins", "alpha", ".claude-plugin", "plugin.json")
        with open(self.man, "w", encoding="utf-8") as fh:
            json.dump({"name": "alpha", "version": "1.2.3", "description": "Ünïcode — dash"}, fh)
        self.log = os.path.join(self.root, "plugins", "alpha", "CHANGELOG.md")
        with open(self.log, "w", encoding="utf-8") as fh:
            fh.write("# Changelog\n\n## 1.2.3 — 2025-12-01\n\n- old entry\n")
        self.calls = []

    def tearDown(self):
        self._tmp.cleanup()

    def run_bump(self, argv, codes=(0, 0)):
        codes = list(codes)

        def validator(root):
            self.calls.append(root)
            return codes.pop(0)

        out = io.StringIO()
        code = bump.main(argv, root=self.root, today=DATE, validator=validator, out=out)
        return code, out.getvalue()

    def test_dry_run_changes_nothing(self):
        before = snapshot(self.root)
        code, out = self.run_bump(["alpha", "patch"])
        self.assertEqual(code, 0)
        self.assertIn("alpha: 1.2.3 -> 1.2.4", out)
        self.assertIn("## 1.2.4 — 2026-01-02", out)
        self.assertEqual(snapshot(self.root), before)
        self.assertEqual(self.calls, [])

    def test_write_edits_plugin_json_and_changelog_only(self):
        before = snapshot(self.root)
        code, _ = self.run_bump(["alpha", "minor", "--write"])
        self.assertEqual(code, 0)
        after = snapshot(self.root)
        changed = sorted(k for k in after if after[k] != before.get(k))
        self.assertEqual(changed, [os.path.join("plugins", "alpha", ".claude-plugin", "plugin.json"),
                                   os.path.join("plugins", "alpha", "CHANGELOG.md")])
        text = read(self.man)
        self.assertNotIn("\\u", text)
        self.assertIn("Ünïcode — dash", text)
        self.assertTrue(text.endswith("}\n"))
        self.assertEqual(json.loads(text)["version"], "1.3.0")
        log = read(self.log)
        self.assertTrue(log.startswith("# Changelog\n\n## 1.3.0 — 2026-01-02\n\n## 1.2.3 — 2025-12-01"))
        self.assertEqual(len(self.calls), 2)  # before and after the write

    def test_write_creates_missing_changelog(self):
        os.remove(self.log)
        code, _ = self.run_bump(["alpha", "major", "--write"])
        self.assertEqual(code, 0)
        self.assertEqual(read(self.log), "# Changelog\n\n## 2.0.0 — 2026-01-02\n\n")

    def test_failed_pre_validation_writes_nothing(self):
        before = snapshot(self.root)
        code, out = self.run_bump(["alpha", "patch", "--write"], codes=(1,))
        self.assertEqual(code, 1)
        self.assertIn("nothing written", out)
        self.assertEqual(snapshot(self.root), before)

    def test_failed_post_validation_is_reported_and_files_stay_bumped(self):
        code, out = self.run_bump(["alpha", "patch", "--write"], codes=(0, 1))
        self.assertEqual(code, 1)
        self.assertIn("the files stay bumped", out)
        self.assertEqual(json.loads(read(self.man))["version"], "1.2.4")

    def test_unknown_plugin_and_level_exit_1(self):
        self.assertEqual(self.run_bump(["nope", "patch"])[0], 1)
        self.assertEqual(self.run_bump(["alpha", "huge"])[0], 1)

    def test_bump_levels(self):
        self.assertEqual(bump.bump("1.2.3", "patch"), "1.2.4")
        self.assertEqual(bump.bump("1.2.3", "minor"), "1.3.0")
        self.assertEqual(bump.bump("1.2.3", "major"), "2.0.0")


if __name__ == "__main__":
    unittest.main()
