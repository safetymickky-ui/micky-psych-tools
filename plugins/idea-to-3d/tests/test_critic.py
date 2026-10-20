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


if __name__ == "__main__":
    unittest.main()
