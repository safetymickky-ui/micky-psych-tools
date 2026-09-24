"""Tests for scripts/delivery_log.py (S11-W0-1).

Run: PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_delivery_log.py' -v
Fixtures are inline strings or tempfile dirs: no network, no wall clock, no real `claude`.
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

import delivery_log as dl

TEMPLATE = """# Delivery log

One row per change to how plugins and VM tooling reach an environment, newest last.
To roll back row N: set the same variable in the same environment to row N's `previous`
value, then append a row whose reason is `rollback of #N`.

Format owner: spec S11 (interface I16). Check: `python3 scripts/delivery_log.py check`
(scripts/health.sh runs it). Setup script text: `docs/rewrite/cloud-setup.sh`.

## Environments

| id | configured at | network access |
|---|---|---|
| `cloud:<id>` | claude.ai/code, cloud environment menu in the session title bar, environment `<name>`, Edit | `<level>` |
| `windows:<host>` | user environment variables on `<host>` (`$env:COMPUTERNAME`), set with PowerShell | n/a |

## W0 mechanism checklist

| check | question | answer | evidence | date | fallback taken |
|---|---|---|---|---|---|
| a | Does a new platform-started multi-repo session load `gridgeist@inline`? | pending | | | |
| b | Do a probe plugin's SessionStart and PreToolUse(Bash) hooks fire in that session? | pending | | | |
| c | Does a many-to-one `renames` map validate on a scratch copy of the real catalog? | pending | | | |
| d | Is `claude plugin eval` enabled on the account, with an http MCP mock answering? | pending | | | |
| e | Do learn-hub `.claude/skills` load, and does a `.claude/rules` file with `paths:` load, in a multi-repo session? | pending | | | |
| f | Does `/doctor` report the listing cost, without overflow, in a multi-repo session? | pending | | | |
| g | Windows: CLI at least 2.1.280, micky source type, learn-hub-local state, and does the variable load a canary? | pending | | | |
| h | Does the setup script run before the repos are cloned? | pending | | | |

## Log

| # | date | environment | variable | previous | new | reason | evidence | rollback |
|---|---|---|---|---|---|---|---|---|
"""

SETUP_OK = "#!/bin/bash\nSETUP_VERSION=1\necho hi\nexit 0\n"


def named(template=TEMPLATE):
    """The template with real environment ids."""
    return (template.replace("`cloud:<id>`", "`cloud:main`").replace("`windows:<host>`", "`windows:PC1`")
            .replace("`<name>`", "`main`").replace("`<level>`", "`full`").replace("on `<host>`", "on `PC1`"))


def row(n, env, var, prev, new, reason="W0 step 4", evidence="https://example.invalid/s", rollback="set (unset)",
        date="2026-09-24"):
    return f"| {n} | {date} | {env} | {var} | `{prev}` | `{new}` | {reason} | {evidence} | {rollback} |\n"


def answered(text, answer="yes"):
    for key in "abcdefgh":
        text = text.replace(f"| {key} | ", f"| {key} |X| ", 1)
    out = []
    for line in text.split("\n"):
        if "|X| " in line:
            cells = line.split("|X| ", 1)
            q, rest = cells[1].split(" | pending |", 1)
            line = f"{cells[0]}| {q} | {answer} | url | 2026-09-24 | {'none' if answer == 'no' else ''} |"
        out.append(line)
    return "\n".join(out)


class Base(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.dir = self._tmp.name
        self.setup = self.write("setup.sh", SETUP_OK)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, name, text):
        path = os.path.join(self.dir, name)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        return path

    def check(self, text, strict=False, setup=None):
        return dl.check(text, setup or self.setup, strict=strict)

    def rules(self, res, kind="errors"):
        return [x["rule"] for x in res[kind]]

    def messages(self, res, rule):
        return " ".join(x["message"] for x in res["errors"] if x["rule"] == rule)

    def plugin(self, root, name):
        os.makedirs(os.path.join(root, ".claude-plugin"), exist_ok=True)
        with open(os.path.join(root, ".claude-plugin", "plugin.json"), "w", encoding="utf-8") as fh:
            json.dump({"name": name, "version": "0.0.1"}, fh)


class CheckTests(Base):
    def test_template_passes_with_pending_warnings(self):
        res = self.check(TEMPLATE)
        self.assertTrue(res["ok"], res["errors"])
        self.assertEqual(self.rules(res, "warnings").count("DL14"), 8)
        self.assertEqual(self.rules(res, "warnings").count("DL4"), 2)
        strict = self.check(TEMPLATE, strict=True)
        self.assertFalse(strict["ok"])
        self.assertEqual(self.rules(strict).count("DL14"), 8)

    def test_tilde_segment_rejected(self):
        res = self.check(named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "~/plugins"))
        self.assertIn("DL8", self.rules(res))
        self.assertIn("/root", self.messages(res, "DL8"))

    def test_relative_segment_rejected(self):
        res = self.check(named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "plugins/x"))
        self.assertIn("no error line", self.messages(res, "DL8"))

    def test_cloud_value_with_semicolon_rejected(self):
        res = self.check(named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "/a/plugins;/b/plugins"))
        self.assertIn("DL8", self.rules(res))

    def test_windows_value_separators(self):
        bad = self.check(named() + row(1, "windows:PC1", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)",
                                       r"C:\a\plugins:C:\b\plugins"))
        self.assertIn("DL8", self.rules(bad))
        good = self.check(named() + row(1, "windows:PC1", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)",
                                        r"C:\Users\User\Desktop\My skill\micky-psych-tools\plugins;"
                                        r"C:\Users\User\Desktop\Learn\plugins"))
        self.assertNotIn("DL8", self.rules(good))

    def test_duplicate_segment_rejected(self):
        res = self.check(named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "/a/p:/a/p"))
        self.assertIn("listed twice", self.messages(res, "DL8"))

    def test_chain_break_rejected(self):
        text = named() + row(1, "cloud:main", "LEARN_HUB_DIR", "(unset)", "/home/user/learn-hub") \
            + row(2, "cloud:main", "LEARN_HUB_DIR", "/other", "/home/user/lh")
        self.assertIn("DL7", self.rules(self.check(text)))

    def test_secret_values_rejected(self):
        res = self.check(named() + row(1, "cloud:main", "FIRECRAWL_API_KEY", "(unset)", "fc-abcdef1234567890"))
        self.assertIn("DL10", self.rules(res))
        res = self.check(named() + row(1, "cloud:main", "LEARN_HUB_DIR", "(unset)", "/x",
                                       evidence="service_role key shown"))
        self.assertIn("DL10", self.rules(res))

    def test_unknown_environment_and_variable(self):
        res = self.check(named() + row(1, "cloud:other", "SOME_VAR", "(unset)", "1"))
        self.assertIn("DL4", self.rules(res))
        self.assertIn("DL5", self.rules(res))

    def test_reason_evidence_rollback_required(self):
        res = self.check(named() + row(1, "cloud:main", "LEARN_HUB_DIR", "(unset)", "/x",
                                       reason="because", evidence="", rollback=""))
        for rule in ("DL11", "DL12", "DL13"):
            self.assertIn(rule, self.rules(res))

    def test_checklist_no_needs_fallback(self):
        text = named().replace("| c | Does a many-to-one `renames` map validate on a scratch copy of the real "
                               "catalog? | pending | | | |",
                               "| c | Does a many-to-one `renames` map validate on a scratch copy of the real "
                               "catalog? | no | exit 1 | 2026-09-24 | |")
        res = self.check(text)
        self.assertIn("DL14", self.rules(res))
        self.assertIn("fallback", self.messages(res, "DL14"))

    def test_static_listed_once(self):
        a, b = os.path.join(self.dir, "a"), os.path.join(self.dir, "b")
        self.plugin(os.path.join(a, "dup"), "dup")
        self.plugin(os.path.join(b, "dup"), "dup")
        env = "windows:PC1" if os.name == "nt" else "cloud:main"
        sep = ";" if os.name == "nt" else ":"
        res = self.check(named() + row(1, env, "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", f"{a}{sep}{b}"))
        self.assertIn("DL15", self.rules(res))

    def test_setup_version_must_match_log(self):
        text = named() + row(1, "cloud:main", "setup-script", "(none)", "setup_version=2", rollback="empty the field")
        self.assertIn("DL17", self.rules(self.check(text)))

    def test_setup_repo_paths_rejected(self):
        setup = self.write("s2.sh", "#!/bin/bash\nSETUP_VERSION=1\nls /home/user/learn-hub\nexit 0\n")
        self.assertIn("DL18", self.rules(self.check(TEMPLATE, setup=setup)))

    def test_setup_last_line_exit_0(self):
        setup = self.write("s3.sh", "#!/bin/bash\nSETUP_VERSION=1\necho done\n")
        self.assertIn("DL18", self.rules(self.check(TEMPLATE, setup=setup)))

    def test_probe_remnants_fail_strict(self):
        text = answered(named()) + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)",
                                       "/home/user/micky-psych-tools/plugins/gridgeist:/opt/w0-probe/hookprobe")
        setup = self.write("s4.sh", "#!/bin/bash\nSETUP_VERSION=1\n# w0-probe block\nexit 0\n")
        res = self.check(text, strict=True, setup=setup)
        self.assertEqual(self.rules(res).count("DL19"), 2)
        self.assertNotIn("DL19", self.rules(self.check(text, strict=False, setup=setup)))


class LiveTests(Base):
    def test_live_duplicates(self):
        entries = [{"id": "intent-lock@inline", "enabled": True, "installPath": "/x/a/intent-lock"},
                   {"id": "intent-lock@inline", "enabled": True, "installPath": "/x/b/intent-lock"}]
        res = dl.live(entries, {"CLAUDE_CODE_PLUGIN_DIRS": "/x/a:/x/b"}, synced_dir=self.dir)
        self.assertIn("L2", [e["rule"] for e in res["errors"]])
        self.assertEqual(res["duplicates"], ["intent-lock"])
        self.assertIn("/x/b/intent-lock", " ".join(e["message"] for e in res["errors"]))

    def test_live_path_not_found(self):
        entries = [{"id": "inline[1]", "enabled": False, "errors": ["Path not found: /root/x (commands)"]}]
        res = dl.live(entries, {}, synced_dir=self.dir)
        self.assertIn("L1", [e["rule"] for e in res["errors"]])

    def test_live_expect_reports_disabled(self):
        entries = [{"id": "firecrawl@inline", "enabled": False, "installPath": "/p/firecrawl"}]
        res = dl.live(entries, {"CLAUDE_CODE_PLUGIN_DIRS": "/p/firecrawl"}, expect="firecrawl", synced_dir=self.dir)
        self.assertIn("present but disabled", " ".join(e["message"] for e in res["errors"] if e["rule"] == "L5"))
        self.assertEqual(res["disabled"], ["firecrawl@inline"])

    def test_live_project_skill_collision(self):
        proj = os.path.join(self.dir, "proj")
        os.makedirs(os.path.join(proj, ".claude", "skills", "concept-animation"))
        plug = os.path.join(self.dir, "plugins", "concept-animation")
        os.makedirs(os.path.join(plug, "skills", "concept-animation"))
        self.write(os.path.join("plugins", "concept-animation", "skills", "concept-animation", "SKILL.md"), "x")
        entries = [{"id": "concept-animation@inline", "enabled": True, "installPath": plug}]
        res = dl.live(entries, {"CLAUDE_CODE_PLUGIN_DIRS": plug}, project_roots=[proj], synced_dir=self.dir)
        self.assertIn("L6", [e["rule"] for e in res["errors"]])

    def test_live_installpath_outside_dirs_and_env_mismatch(self):
        entries = [{"id": "gridgeist@inline", "enabled": True, "installPath": "/elsewhere/gridgeist"}]
        text = named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "/p/gridgeist")
        res = dl.live(entries, {"CLAUDE_CODE_PLUGIN_DIRS": "/q/gridgeist"}, log_text=text, env="cloud:main",
                      synced_dir=self.dir)
        self.assertIn("L4", [e["rule"] for e in res["errors"]])
        self.assertIn("L3", [w["rule"] for w in res["warnings"]])


class CliTests(Base):
    def test_current_prints_latest_value(self):
        log = self.write("log.md", named() + row(1, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "(unset)", "/a/p")
                         + row(2, "cloud:main", "CLAUDE_CODE_PLUGIN_DIRS", "/a/p", "/b/p"))
        out = io.StringIO()
        self.assertEqual(dl.main(["current", "--env", "cloud:main", "--log", log], out=out), 0)
        self.assertEqual(out.getvalue(), "/b/p\n")
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(dl.main(["current", "--env", "cloud:none", "--log", log], out=io.StringIO()), 1)

    def test_help_has_no_side_effects(self):
        empty = os.path.join(self.dir, "empty")
        os.makedirs(empty)
        script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "delivery_log.py")
        res = subprocess.run([sys.executable, script, "--help"], cwd=empty, capture_output=True, text=True,
                             env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        self.assertEqual(res.returncode, 0)
        self.assertIn("check", res.stdout)
        self.assertEqual(os.listdir(empty), [])

    def test_live_from_file_and_bad_json(self):
        good = self.write("list.json", json.dumps([{"id": "gridgeist@inline", "enabled": True,
                                                     "installPath": "/p/gridgeist"}]))
        bad = self.write("bad.json", "{}")
        out = io.StringIO()
        code = dl.main(["live", "--from", good], environ={"CLAUDE_CODE_PLUGIN_DIRS": "/p/gridgeist"}, out=out)
        self.assertEqual(code, 0, out.getvalue())
        self.assertEqual(json.loads(out.getvalue())["loaded"], ["gridgeist"])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(dl.main(["live", "--from", bad], environ={}, out=io.StringIO()), 3)

    def test_check_unreadable_log_exits_2(self):
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(dl.main(["check", "--log", os.path.join(self.dir, "none.md")], out=io.StringIO()), 2)


if __name__ == "__main__":
    unittest.main()
