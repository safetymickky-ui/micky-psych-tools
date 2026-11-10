"""Tests for skills/session-recap/scripts/build_recap.py.

    python3 -m unittest discover -s plugins/session-recap/tests
"""
import copy
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "skills", "session-recap", "scripts")
sys.path.insert(0, SCRIPTS)
import build_recap as br  # noqa: E402

with open(os.path.join(HERE, "fixtures", "recap.json"), encoding="utf-8") as _fh:
    GOOD = json.load(_fh)
with open(br.TEMPLATE, encoding="utf-8") as _fh:
    TEMPLATE = _fh.read()


def recap(**changes):
    data = copy.deepcopy(GOOD)
    data.update(changes)
    return data


def errors_of(data):
    return br.check(data)[0]


class CheckTests(unittest.TestCase):
    def assert_error(self, data, fragment):
        errors = errors_of(data)
        self.assertTrue(any(fragment in e for e in errors), f"no error holding {fragment!r} in {errors}")

    def test_fixture_is_clean(self):
        errors, warnings = br.check(GOOD)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_not_an_object(self):
        self.assertEqual(errors_of([]), ["the recap is not a JSON object"])

    def test_title_word_count(self):
        self.assert_error(recap(title="Recap"), "two to four words")
        self.assert_error(recap(title="A very long recap title here"), "two to four words")

    def test_title_is_a_name_not_a_caption(self):
        self.assert_error(recap(title="Upload client: recap"), "not a caption")

    def test_date_and_lang(self):
        self.assert_error(recap(date="10 Nov 2026"), "YYYY-MM-DD")
        self.assert_error(recap(lang="fr"), "lang")

    def test_outcome_required_and_capped(self):
        self.assert_error(recap(outcome=" "), "outcome: required")
        self.assert_error(recap(outcome="x" * 401), "cap 400")

    def test_open_key_is_required(self):
        data = recap()
        del data["open"]
        self.assert_error(data, "open: the key is required")

    def test_empty_open_with_unfinished_work_warns(self):
        errors, warnings = br.check(recap(open=[]))
        self.assertEqual(errors, [])
        self.assertTrue(any("not finished" in w for w in warnings))

    def test_open_vocabulary(self):
        data = recap()
        data["open"][0]["kind"] = "later"
        self.assert_error(data, "open[0].kind")

    def test_done_needs_an_item(self):
        self.assert_error(recap(done=[]), "done: at least one item")

    def test_status_vocabulary(self):
        data = recap()
        data["done"][0]["status"] = "complete"
        self.assert_error(data, "done[0].status")

    def test_verified_needs_a_passed_check(self):
        data = recap()
        data["done"][0]["check"] = ""
        self.assert_error(data, "name the check that passed")
        data["done"][0]["check"] = "c9"
        self.assert_error(data, "no check has the id 'c9'")
        data["done"][0]["check"] = "c2"
        self.assert_error(data, "so the item is not verified")

    def test_failed_item_cannot_be_verified(self):
        data = recap()
        data["done"][3]["verified"] = "yes"
        data["done"][3]["check"] = "c1"
        self.assert_error(data, "a failed item cannot be verified")

    def test_not_applicable_only_for_answers(self):
        data = recap()
        data["done"][0]["verified"] = "n/a"
        self.assert_error(data, "n/a is only for type answer")

    def test_unfinished_item_needs_detail(self):
        data = recap()
        data["done"][3]["detail"] = ""
        self.assert_error(data, "required when the status is failed")

    def test_change_needs_evidence(self):
        data = recap()
        data["done"][0]["evidence"] = []
        self.assert_error(data, "needs at least one piece of evidence")

    def test_answer_needs_no_evidence(self):
        self.assertEqual(GOOD["done"][2]["evidence"], [])
        self.assertEqual(errors_of(GOOD), [])

    def test_evidence_url_must_be_http(self):
        data = recap()
        data["done"][0]["evidence"][0]["url"] = "javascript:alert(1)"
        self.assert_error(data, "must start with http")

    def test_check_ids_are_unique(self):
        data = recap()
        data["checks"][1]["id"] = "c1"
        self.assert_error(data, "used twice")

    def test_commit_sha(self):
        data = recap()
        data["changes"]["commits"][0]["sha"] = "latest"
        self.assert_error(data, "7 to 40 hex")

    def test_file_cap(self):
        data = recap()
        data["changes"]["files"] = [{"path": f"f{i}.py", "change": "added"} for i in range(41)]
        self.assert_error(data, "cap 40")

    def test_pr_url_and_state(self):
        data = recap()
        data["changes"]["prs"][0]["url"] = "github.com/x"
        data["changes"]["prs"][0]["state"] = "pending"
        self.assert_error(data, "changes.prs[0].url")
        self.assert_error(data, "changes.prs[0].state")

    def test_asked_needs_a_request(self):
        self.assert_error(recap(asked=[]), "asked: at least one request")

    def test_secrets_fail_the_build(self):
        samples = [
            "the key sk-" + "a1B2" * 8,
            "ghp_" + "A1b2" * 9,
            "AKIA" + "ABCD1234EFGH5678",
            "-----BEGIN RSA PRIVATE KEY-----",
            "password = hunter2hunter2",
            "API_KEY: abcd1234efgh",
        ]
        for text in samples:
            data = recap()
            data["done"][0]["detail"] = text
            self.assert_error(data, "never its value")

    def test_plain_words_are_not_secrets(self):
        data = recap()
        data["done"][0]["detail"] = "The token is read from the environment; the password field was renamed."
        self.assertEqual(errors_of(data), [])

    def test_praise_and_email_warn(self):
        data = recap(outcome="The retry was successfully added. Ask sam@example.com.")
        errors, warnings = br.check(data)
        self.assertEqual(errors, [])
        self.assertTrue(any("praise" in w for w in warnings))
        self.assertTrue(any("email" in w for w in warnings))

    def test_praise_in_the_users_own_request_is_kept(self):
        data = recap()
        data["asked"][0]["text"] = "Make it robust please"
        self.assertEqual(br.check(data)[1], [])


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.page = br.render(GOOD, TEMPLATE)

    def test_no_placeholder_is_left(self):
        self.assertNotIn("{{", self.page)

    def test_title_and_meta(self):
        self.assertTrue(self.page.startswith("<title>Upload client recap</title>"))
        self.assertIn('<meta name="session-recap" content="recap-page">', self.page)

    def test_open_comes_before_done(self):
        self.assertLess(self.page.index('id="h-open"'), self.page.index('id="h-done"'))
        self.assertLess(self.page.index('id="h-done"'), self.page.index('id="h-asked"'))

    def test_statuses_are_words(self):
        for word in ("Done", "Partly done", "Failed", "Your decision", "Risk", "Not run"):
            self.assertIn(f">{word}</span>", self.page)

    def test_inline_code(self):
        self.assertIn("<code>client.py</code>", self.page)

    def test_verified_line_names_the_check(self):
        self.assertIn("Verified by <code>pytest tests/unit -q</code>", self.page)
        self.assertIn("Not verified by a check", self.page)

    def test_summary_mark_and_gaps(self):
        self.assertIn("From a compacted part of the session", self.page)
        self.assertIn("compacted summary", self.page)
        self.assertIn("CI result was not read", self.page)

    def test_tally(self):
        self.assertIn("2 requests · 3 done · 2 not finished · 3 open", self.page)

    def test_empty_sections_are_left_out(self):
        self.assertNotIn(">Artifacts</h3>", self.page)
        data = recap(decisions=[], checks=[], changes={})
        data["done"][0]["verified"] = "no"
        data["done"][0].pop("check")
        page = br.render(data, TEMPLATE)
        for key in ("h-decisions", "h-checks", "h-changes"):
            self.assertNotIn(key, page)

    def test_nothing_open_is_stated(self):
        data = recap(open=[], done=[GOOD["done"][0]])
        self.assertEqual(br.check(data), ([], []))
        self.assertIn("Nothing is left open.", br.render(data, TEMPLATE))

    def test_html_is_escaped(self):
        data = recap()
        data["asked"][0]["text"] = '<script>alert("x")</script>'
        data["done"][0]["what"] = "Fixed `a<b` & more"
        page = br.render(data, TEMPLATE)
        self.assertNotIn("<script>alert", page)
        self.assertIn("&lt;script&gt;", page)
        self.assertIn("<code>a&lt;b</code> &amp; more", page)

    def test_no_table_in_the_page(self):
        self.assertNotIn("<table", self.page)

    def test_thai_labels(self):
        page = br.render(recap(lang="th"), TEMPLATE)
        self.assertIn("ยังค้างอยู่", page)
        self.assertIn("สิ่งที่ทำ", page)
        self.assertIn('lang="th"', page)

    def test_focus_line(self):
        page = br.render(recap(focus="the retry work"), TEMPLATE)
        self.assertIn("This page covers only: the retry work.", page)


class CliTests(unittest.TestCase):
    def run_cli(self, data, *extra):
        with tempfile.TemporaryDirectory() as tmp:
            src = os.path.join(tmp, "recap.json")
            out = os.path.join(tmp, "recap.html")
            with open(src, "w", encoding="utf-8") as fh:
                json.dump(data, fh)
            buf = io.StringIO()
            with redirect_stdout(buf):
                code = br.main([src, *(extra or ("-o", out))])
            written = None
            if os.path.exists(out):
                with open(out, encoding="utf-8") as fh:
                    written = fh.read()
        return code, json.loads(buf.getvalue()), written

    def test_builds_a_page(self):
        code, report, written = self.run_cli(GOOD)
        self.assertEqual(code, 0)
        self.assertTrue(report["ok"])
        self.assertIn("Upload client recap", written)

    def test_writes_nothing_on_error(self):
        code, report, written = self.run_cli(recap(done=[]))
        self.assertEqual(code, 1)
        self.assertFalse(report["ok"])
        self.assertIsNone(written)

    def test_check_only(self):
        code, report, written = self.run_cli(GOOD, "--check")
        self.assertEqual(code, 0)
        self.assertIsNone(report["out"])
        self.assertIsNone(written)

    def test_unreadable_input(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = br.main(["/nonexistent/recap.json", "--check"])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
