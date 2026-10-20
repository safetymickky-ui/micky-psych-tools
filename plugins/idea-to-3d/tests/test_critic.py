#!/usr/bin/env python3
"""
Tests for the idea-to-3d critic loop core: pipeline_state reviews and consent,
review validation, and critique.py. No network: `agy` is replaced by tests/fake_agy.py.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "skills" / "idea-to-3d" / "scripts"
REFERENCES = PLUGIN_ROOT / "skills" / "idea-to-3d" / "references"
FAKE_AGY = Path(__file__).resolve().parent / "fake_agy.py"
PNG_BYTES = b"\x89PNG\r\n\x1a\n"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pipeline_state = load_module("pipeline_state_under_test", SCRIPTS / "pipeline_state.py")
critique = load_module("critique_under_test", SCRIPTS / "critique.py")


class TempPipelineCase(unittest.TestCase):
    """A fresh work root with an initialised fox-knight pipeline."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="test_critic_"))
        self.root = str(self.tmp)
        pipeline_state.init_pipeline(
            slug="fox-knight", idea="A fox knight with a lantern", height_m=1.2, work_root=self.root
        )
        self.work = self.tmp / "work" / "fox-knight"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestPipelineReviews(TempPipelineCase):
    def test_init_creates_reviews_dir_and_no_critic_choice(self) -> None:
        state = pipeline_state.load_pipeline("fox-knight", self.root)
        self.assertEqual(state["reviews"], [])
        self.assertIsNone(state["critic"])
        self.assertTrue((self.work / "reviews").is_dir())

    def test_set_critic_records_choice_and_rejects_unknown(self) -> None:
        state = pipeline_state.set_critic("fox-knight", "claude", work_root=self.root)
        self.assertEqual(state["critic"], "claude")
        with self.assertRaises(ValueError):
            pipeline_state.set_critic("fox-knight", "gpt", work_root=self.root)

    def test_record_review_appends_and_history_filters_by_gate(self) -> None:
        pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict="REVISE",
                                     path="work/fox-knight/reviews/B-r0.json", open_issues=2, work_root=self.root)
        pipeline_state.record_review("fox-knight", "C", 0, critic="gemini", model="m", verdict="PASS",
                                     path="work/fox-knight/reviews/C-r0.json", open_issues=0, work_root=self.root)
        self.assertEqual(len(pipeline_state.review_history("fox-knight", work_root=self.root)), 2)
        only_b = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([(r["gate"], r["verdict"], r["open_issues"]) for r in only_b], [("B", "REVISE", 2)])

    def test_record_review_same_round_replaces_and_next_round_counts(self) -> None:
        self.assertEqual(pipeline_state.next_review_round("fox-knight", "B", self.root), 0)
        pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict="REVISE",
                                     path="p", open_issues=1, work_root=self.root)
        pipeline_state.record_review("fox-knight", "B", 1, critic="gemini", model="m", verdict="REVISE",
                                     path="p", open_issues=1, work_root=self.root)
        pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict="PASS",
                                     path="p", open_issues=0, work_root=self.root)
        history = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([(r["round"], r["verdict"]) for r in history], [(0, "PASS"), (1, "REVISE")])
        self.assertEqual(pipeline_state.next_review_round("fox-knight", "B", self.root), 2)

    def test_record_review_rejects_bad_gate_and_negative_round(self) -> None:
        with self.assertRaises(ValueError):
            pipeline_state.record_review("fox-knight", "D", 0, critic="gemini", model="m", verdict="PASS",
                                         path="p", open_issues=0, work_root=self.root)
        with self.assertRaises(ValueError):
            pipeline_state.record_review("fox-knight", "B", -1, critic="gemini", model="m", verdict="PASS",
                                         path="p", open_issues=0, work_root=self.root)
        self.assertEqual(pipeline_state.review_history("fox-knight", work_root=self.root), [])
        with self.assertRaises(ValueError):
            pipeline_state.next_review_round("fox-knight", "D", self.root)
        with self.assertRaises(ValueError):
            pipeline_state.review_history("fox-knight", "D", work_root=self.root)

    def test_v1_pipeline_without_review_keys_still_works_and_init_backfills(self) -> None:
        state = pipeline_state.load_pipeline("fox-knight", self.root)
        state.pop("reviews")
        state.pop("critic")
        pipeline_state.save_pipeline("fox-knight", state, self.root)
        self.assertEqual(pipeline_state.review_history("fox-knight", work_root=self.root), [])
        self.assertEqual(pipeline_state.next_review_round("fox-knight", "B", self.root), 0)
        pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict="PASS",
                                     path="p", open_issues=0, work_root=self.root)
        self.assertEqual(pipeline_state.set_critic("fox-knight", "gemini", work_root=self.root)["critic"], "gemini")

        state = pipeline_state.load_pipeline("fox-knight", self.root)
        state.pop("reviews")
        state.pop("critic")
        pipeline_state.save_pipeline("fox-knight", state, self.root)
        resumed = pipeline_state.init_pipeline(
            slug="fox-knight", idea="A fox knight with a lantern", height_m=1.2, work_root=self.root
        )
        self.assertEqual(resumed["reviews"], [])
        self.assertIsNone(resumed["critic"])

    def test_cli_set_critic_and_review_history(self) -> None:
        self.assertEqual(pipeline_state.main(["set-critic", "fox-knight", "gemini", "--work-root", self.root]), 0)
        self.assertEqual(pipeline_state.load_pipeline("fox-knight", self.root)["critic"], "gemini")
        pipeline_state.record_review("fox-knight", "A1", 0, critic="gemini", model="m", verdict="PASS",
                                     path="p", open_issues=0, work_root=self.root)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = pipeline_state.main(["review-history", "fox-knight", "--gate", "A1", "--work-root", self.root])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out.getvalue())[0]["gate"], "A1")


class TestReferenceFiles(unittest.TestCase):
    def test_schema_is_valid_json_with_expected_shape(self) -> None:
        schema = json.loads((REFERENCES / "review.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["required"]), {"gate", "verdict", "scores", "issues"})
        self.assertEqual(schema["properties"]["gate"]["enum"], list(pipeline_state.VALID_GATES))
        issue = schema["properties"]["issues"]["items"]
        self.assertEqual(set(issue["required"]), {"id", "severity", "criterion", "evidence", "fix", "credits"})
        self.assertEqual(issue["properties"]["severity"]["enum"], ["blocker", "major", "minor"])

    def test_every_gate_has_a_rubric_with_criteria_severity_and_fixes(self) -> None:
        for gate in pipeline_state.VALID_GATES:
            text = (REFERENCES / "rubrics" / f"{gate}.md").read_text(encoding="utf-8")
            for heading in ("## Criteria", "## Severity", "## Fixes and their credits"):
                self.assertIn(heading, text, f"{gate}.md lacks {heading}")


def valid_review(gate: str = "B", verdict: str = "REVISE") -> dict:
    issues = [] if verdict == "PASS" else [{
        "id": f"{gate}-1", "severity": "major", "criterion": "geometry",
        "evidence": "Try 2, side: left hand fused to the hip",
        "fix": "new try with pose_mode a-pose", "credits": 30,
    }]
    return {"gate": gate, "verdict": verdict,
            "scores": [{"criterion": "geometry", "score": 2}], "issues": issues}


class TestValidateReview(unittest.TestCase):
    def test_valid_revise_and_pass_are_accepted(self) -> None:
        self.assertEqual(critique.validate_review(valid_review(), "B"), [])
        self.assertEqual(critique.validate_review(valid_review(verdict="PASS"), "B"), [])

    def test_pass_with_major_issue_is_rejected(self) -> None:
        review = valid_review()
        review["verdict"] = "PASS"
        self.assertTrue(any("PASS is not allowed" in e for e in critique.validate_review(review, "B")))

    def test_revise_without_issues_is_rejected(self) -> None:
        review = valid_review(verdict="PASS")
        review["verdict"] = "REVISE"
        self.assertTrue(any("REVISE needs" in e for e in critique.validate_review(review, "B")))

    def test_bad_score_credits_gate_and_type_are_rejected(self) -> None:
        review = valid_review()
        review["scores"][0]["score"] = True
        review["issues"][0]["credits"] = -5
        errors = critique.validate_review(review, "C")
        self.assertTrue(any("scores[0]" in e for e in errors))
        self.assertTrue(any("credits" in e for e in errors))
        self.assertTrue(any('"gate" must be "C"' in e for e in errors))
        self.assertEqual(critique.validate_review(["not", "an", "object"], "B"), ["review must be a JSON object"])

    def test_gate_lists_match_pipeline_state(self) -> None:
        self.assertEqual(tuple(critique.GATE_INPUTS), pipeline_state.VALID_GATES)


class TestAgyParsing(unittest.TestCase):
    def test_last_json_object_returns_the_outer_object(self) -> None:
        text = 'I will read it.\n{"a": {"b": 1}} trailing'
        self.assertEqual(critique.last_json_object(text), {"a": {"b": 1}})
        self.assertIsNone(critique.last_json_object("no json here"))

    def test_parse_prefers_structured_output_then_response(self) -> None:
        body = valid_review()
        both = json.dumps({"status": "SUCCESS", "response": "x", "structured_output": body})
        self.assertEqual(critique.parse_agy_output(both), body)
        only_text = json.dumps({"status": "SUCCESS", "response": "Reading.\n" + json.dumps(body)})
        self.assertEqual(critique.parse_agy_output(only_text), body)

    def test_parse_raises_on_failure_status_or_garbage(self) -> None:
        with self.assertRaises(critique.CriticUnavailable):
            critique.parse_agy_output(json.dumps({"status": "ERROR"}))
        with self.assertRaises(critique.CriticUnavailable):
            critique.parse_agy_output("Loaded cached credentials. Error")

    def test_agy_command_uses_env_then_path(self) -> None:
        with mock.patch.dict(os.environ, {"IDEA3D_AGY": r"C:\tools\agy.exe"}):
            self.assertEqual(critique.agy_command(), [r"C:\tools\agy.exe"])
        with mock.patch.dict(os.environ, {"IDEA3D_AGY": ""}), \
                mock.patch.object(critique.shutil, "which", return_value=None):
            with self.assertRaises(critique.CriticUnavailable):
                critique.agy_command()


class TestCritiqueRun(TempPipelineCase):
    def setUp(self) -> None:
        super().setUp()
        pipeline_state.set_critic("fox-knight", "gemini", work_root=self.root)
        (self.work / "idea.md").write_text("# Fox knight\nHeight: 1.2 m\n", encoding="utf-8")
        (self.work / "images" / "front.png").write_bytes(PNG_BYTES)
        (self.work / "preview" / "tries.png").write_bytes(PNG_BYTES)
        self.log = self.tmp / "agy.log"
        self.env = mock.patch.dict(os.environ, {"FAKE_AGY_LOG": str(self.log), "IDEA3D_CRITIC_MODEL": ""})
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        super().tearDown()

    def run_critic(self, mode: str, *extra: str, prefix: list[str] | None = None) -> int:
        os.environ["FAKE_AGY_MODE"] = mode
        argv = ["fox-knight", "B", "--work-root", self.root, *extra]
        with redirect_stdout(io.StringIO()):
            return critique.main(argv, cmd_prefix=prefix or [sys.executable, str(FAKE_AGY)])

    def calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_valid_review_is_written_and_recorded(self) -> None:
        self.assertEqual(self.run_critic("ok"), 0)
        saved = json.loads((self.work / "reviews" / "B-r0.json").read_text(encoding="utf-8"))
        self.assertEqual((saved["round"], saved["critic"], saved["model"]), (0, "gemini", "gemini-4-argon-medium"))
        history = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([(h["verdict"], h["open_issues"]) for h in history], [("REVISE", 1)])

    def test_agy_is_called_read_only_with_schema_and_work_dir(self) -> None:
        self.run_critic("ok")
        argv = self.calls()[0]
        for flag, value in (("--mode", "plan"), ("--output-format", "json"),
                            ("--model", "gemini-4-argon-medium"), ("--add-dir", str(self.work))):
            self.assertEqual(argv[argv.index(flag) + 1], value)
        self.assertIn("--disable-slash-commands", argv)
        self.assertTrue(argv[argv.index("--json-schema") + 1].endswith("review.schema.json"))
        prompt = argv[argv.index("-p") + 1]
        self.assertIn(str(self.work / "preview" / "tries.png"), prompt)
        self.assertIn("Gate B", prompt)

    def test_round_defaults_to_the_next_round(self) -> None:
        self.run_critic("ok")
        self.assertEqual(self.run_critic("pass"), 0)
        self.assertTrue((self.work / "reviews" / "B-r1.json").is_file())

    def test_response_text_is_used_when_structured_output_is_missing(self) -> None:
        self.assertEqual(self.run_critic("response-only"), 0)

    def test_invalid_review_is_retried_once_with_the_errors(self) -> None:
        self.assertEqual(self.run_critic("bad-then-ok"), 0)
        calls = self.calls()
        self.assertEqual(len(calls), 2)
        self.assertIn("rejected", calls[1][calls[1].index("-p") + 1])

    def test_invalid_twice_exits_3_and_writes_nothing(self) -> None:
        self.assertEqual(self.run_critic("bad"), 3)
        self.assertFalse((self.work / "reviews" / "B-r0.json").exists())

    def test_unavailable_critic_exits_2(self) -> None:
        self.assertEqual(self.run_critic("nonzero"), 2)
        self.assertEqual(self.run_critic("not-success"), 2)
        self.assertEqual(self.run_critic("sleep", "--timeout", "1"), 2)
        self.assertEqual(self.run_critic("ok", prefix=[str(self.tmp / "no-such-agy.exe")]), 2)

    def test_missing_input_or_consent_is_a_usage_error(self) -> None:
        (self.work / "preview" / "tries.png").unlink()
        self.assertEqual(self.run_critic("ok"), 1)
        (self.work / "preview" / "tries.png").write_bytes(PNG_BYTES)
        state = pipeline_state.load_pipeline("fox-knight", self.root)
        state["critic"] = None
        pipeline_state.save_pipeline("fox-knight", state, self.root)
        self.assertEqual(self.run_critic("ok"), 1)
        self.assertEqual(self.calls(), [])

    def test_claude_choice_skips_gemini_with_exit_2(self) -> None:
        pipeline_state.set_critic("fox-knight", "claude", work_root=self.root)
        self.assertEqual(self.run_critic("ok"), 2)
        self.assertEqual(self.calls(), [])

    def test_from_file_records_a_claude_fallback_review(self) -> None:
        raw = self.tmp / "raw.json"
        raw.write_text(json.dumps(valid_review(verdict="PASS")), encoding="utf-8")
        rc = self.run_critic("ok", "--from-file", str(raw), "--critic", "claude-fallback", "--reason", "exit 2: timeout")
        self.assertEqual(rc, 0)
        saved = json.loads((self.work / "reviews" / "B-r0.json").read_text(encoding="utf-8"))
        self.assertEqual((saved["critic"], saved["reason"]), ("claude-fallback", "exit 2: timeout"))
        self.assertEqual(self.calls(), [])

    def test_from_file_with_an_invalid_review_exits_3(self) -> None:
        raw = self.tmp / "raw.json"
        raw.write_text('{"gate": "B", "verdict": "PASS"}', encoding="utf-8")
        self.assertEqual(self.run_critic("ok", "--from-file", str(raw), "--critic", "claude-fallback"), 3)

    def test_bad_arguments_exit_1_not_2(self) -> None:
        with self.assertRaises(SystemExit) as ctx, mock.patch("sys.stderr", io.StringIO()):
            critique.main(["fox-knight", "Z", "--work-root", self.root])
        self.assertEqual(ctx.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
