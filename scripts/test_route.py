"""Tests for scripts/route.py (S10-W0-4).

Run: python3 -m unittest discover -s scripts -p 'test_route.py' -q
The generator's input and output paths are pointed at a temporary directory.
"""
import contextlib
import io
import json
import os
import tempfile
import unittest

import route


class RouteTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        root = self._tmp.name
        os.makedirs(os.path.join(root, ".claude-plugin"))
        skill = os.path.join(root, "plugins", "alpha", "skills", "alpha")
        os.makedirs(skill)
        with open(os.path.join(skill, "SKILL.md"), "w", encoding="utf-8") as fh:
            fh.write("---\nname: alpha\ndescription: Does alpha. Use when the user says alpha.\n---\n")
        self.mkt = os.path.join(root, ".claude-plugin", "marketplace.json")
        with open(self.mkt, "w", encoding="utf-8") as fh:
            json.dump({"name": "t", "plugins": [{"name": "alpha", "source": "./plugins/alpha",
                                                 "version": "9.9.9", "description": "Alpha.",
                                                 "category": "tools"}]}, fh)
        self.out = os.path.join(root, "ROUTING.md")
        self._saved = (route.ROOT, route.MKT, route.OUT)
        route.ROOT, route.MKT, route.OUT = root, self.mkt, self.out

    def tearDown(self):
        route.ROOT, route.MKT, route.OUT = self._saved
        self._tmp.cleanup()

    def test_help_writes_nothing(self):
        with open(self.out, "w", encoding="utf-8") as fh:
            fh.write("sentinel\n")
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit) as cm:
                route.main(["--help"])
        self.assertEqual(cm.exception.code, 0)
        with open(self.out, encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "sentinel\n")

    def test_unknown_flag_writes_nothing(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                route.main(["--bogus"])
        self.assertFalse(os.path.exists(self.out))

    def test_output_carries_no_version(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(route.main([]), 0)
        with open(self.out, encoding="utf-8") as fh:
            text = fh.read()
        self.assertIn("### alpha — tools\n", text)
        self.assertNotIn("9.9.9", text)
        self.assertNotIn("_v", text)


if __name__ == "__main__":
    unittest.main()
