#!/usr/bin/env python3
"""
Tests for generate_image.py, the free image route through the Antigravity CLI.
No network: `agy` is replaced by tests/fake_agy.py, whose image modes write into a temp brain dir.
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
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from PIL import Image

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "skills" / "idea-to-3d" / "scripts"
FAKE_AGY = Path(__file__).resolve().parent / "fake_agy.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pipeline_state = load_module("pipeline_state_under_test_gi", SCRIPTS / "pipeline_state.py")
generate_image = load_module("generate_image_under_test", SCRIPTS / "generate_image.py")
agy_runner = load_module("agy_runner_under_test", SCRIPTS / "agy_runner.py")

PROMPT = "a small round teal robot with one big eye"


class TestAgyRunner(unittest.TestCase):
    def test_run_agy_returns_the_envelope_and_raises_when_unavailable(self) -> None:
        with mock.patch.dict(os.environ, {"FAKE_AGY_MODE": "image-none", "IDEA3D_AGY_BRAIN": tempfile.gettempdir()}):
            envelope = agy_runner.run_agy([sys.executable, str(FAKE_AGY)], ["-p", "x"], Path.cwd(), 30)
        self.assertEqual(envelope["status"], "SUCCESS")
        for mode in ("nonzero", "not-success"):
            with mock.patch.dict(os.environ, {"FAKE_AGY_MODE": mode}), self.assertRaises(agy_runner.AgyUnavailable):
                agy_runner.run_agy([sys.executable, str(FAKE_AGY)], ["-p", "x"], Path.cwd(), 30)
        with self.assertRaises(agy_runner.AgyUnavailable):
            agy_runner.run_agy(["no-such-agy-binary"], ["-p", "x"], Path.cwd(), 30)


class GenerateImageCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="test_genimg_"))
        self.root = str(self.tmp)
        pipeline_state.init_pipeline(slug="robot", idea="A teal robot", height_m=0.5, work_root=self.root)
        pipeline_state.set_critic("robot", "gemini", work_root=self.root)
        self.work = self.tmp / "work" / "robot"
        self.brain = self.tmp / "brain"
        self.log = self.tmp / "agy.log"
        self.env = mock.patch.dict(os.environ, {
            "IDEA3D_AGY_BRAIN": str(self.brain), "FAKE_AGY_LOG": str(self.log), "FAKE_AGY_MODE": "image",
        })
        self.env.start()
        self.wait = mock.patch.object(generate_image, "IMAGE_WAIT_SECONDS", 0)
        self.wait.start()
        self.printed = ""

    def tearDown(self) -> None:
        self.wait.stop()
        self.env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def generate(self, *extra: str, mode: str = "image", out: str = "images/concept-1.png",
                 prefix: list[str] | None = None) -> int:
        os.environ["FAKE_AGY_MODE"] = mode
        argv = ["robot", "--out", out, "--prompt", PROMPT, "--work-root", self.root, *extra]
        stdout = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(io.StringIO()):
            code = generate_image.main(argv, cmd_prefix=prefix or [sys.executable, str(FAKE_AGY)])
        self.printed = stdout.getvalue().strip()
        return code

    def calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def make_ref(self, directory: str, name: str) -> Path:
        path = self.tmp / directory / name
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGB", (8, 8), (10, 20, 30)).save(path)
        return path


class TestHappyPath(GenerateImageCase):
    def test_image_is_converted_to_png_at_the_output_and_its_path_printed(self) -> None:
        self.assertEqual(self.generate(), 0)
        out = self.work / "images" / "concept-1.png"
        with Image.open(out) as img:
            self.assertEqual((img.format, img.mode, img.size), ("PNG", "RGB", (64, 64)))
        self.assertEqual(Path(self.printed).resolve(), out.resolve())
        self.assertFalse(list((self.work / "images").glob("*.tmp*")))

    def test_output_parent_folders_are_created(self) -> None:
        self.assertEqual(self.generate(out="images/more/x.png"), 0)
        self.assertTrue((self.work / "images" / "more" / "x.png").is_file())

    def test_agy_is_called_in_default_mode_with_a_temp_add_dir(self) -> None:
        self.generate()
        argv = self.calls()[0]
        self.assertEqual(argv[argv.index("--output-format") + 1], "json")
        self.assertIn("--disable-slash-commands", argv)
        self.assertNotIn("--mode", argv)
        add_dir = Path(argv[argv.index("--add-dir") + 1])
        self.assertNotEqual(add_dir.resolve(), self.work.resolve())
        self.assertFalse(add_dir.exists(), "the temp dir is removed after the run")
        prompt = argv[argv.index("-p") + 1]
        self.assertIn("Use your image generation tool to generate exactly one image.", prompt)
        self.assertIn(PROMPT, prompt)
        self.assertIn("reply with only the absolute file path", prompt)
        self.assertNotIn("reference image", prompt)

    def test_response_path_missing_falls_back_to_the_newest_brain_image(self) -> None:
        self.assertEqual(self.generate(mode="image-late"), 0)
        with Image.open(self.work / "images" / "concept-1.png") as img:
            r, g, b = img.getpixel((5, 5))
            self.assertLess(r, 20)
            self.assertAlmostEqual(g, 128, delta=20)
            self.assertAlmostEqual(b, 128, delta=20)

    def test_a_response_path_outside_the_brain_conversation_is_ignored(self) -> None:
        self.assertEqual(self.generate(mode="image-outside"), 0)
        with Image.open(self.work / "images" / "concept-1.png") as img:
            r, g, b = img.getpixel((5, 5))
            self.assertLess(r, 60)
            self.assertGreater(g, 90)

    def test_a_response_path_outside_the_brain_conversation_alone_is_not_an_image(self) -> None:
        self.assertEqual(self.generate(mode="image-outside-only"), 2)
        self.assertFalse((self.work / "images" / "concept-1.png").exists())


class TestReferences(GenerateImageCase):
    def test_refs_are_copied_into_the_add_dir_and_listed_in_the_prompt(self) -> None:
        first = self.make_ref("a", "front.png")
        second = self.make_ref("b", "side.png")
        self.assertEqual(self.generate("--ref", str(first), "--ref", str(second)), 0)
        argv = self.calls()[0]
        add_dir = argv[argv.index("--add-dir") + 1]
        prompt = argv[argv.index("-p") + 1]
        self.assertIn("Pass each of these files to the image tool as a reference image", prompt)
        for name in ("front.png", "side.png"):
            self.assertIn(str(Path(add_dir) / name), prompt)
        self.assertNotIn(str(first), prompt)
        self.assertTrue(first.is_file() and second.is_file(), "the originals are untouched")

    def test_refs_with_the_same_basename_get_distinct_copies(self) -> None:
        first = self.make_ref("a", "front.png")
        second = self.make_ref("b", "front.png")
        self.assertEqual(self.generate("--ref", str(first), "--ref", str(second)), 0)
        argv = self.calls()[0]
        add_dir = argv[argv.index("--add-dir") + 1]
        prompt = argv[argv.index("-p") + 1]
        self.assertIn(str(Path(add_dir) / "front.png"), prompt)
        self.assertIn(str(Path(add_dir) / "front-2.png"), prompt)

    def test_missing_ref_or_more_than_five_is_a_usage_error(self) -> None:
        self.assertEqual(self.generate("--ref", str(self.tmp / "nope.png")), 1)
        refs = [str(self.make_ref("r", f"r{i}.png")) for i in range(6)]
        argv = [arg for ref in refs for arg in ("--ref", ref)]
        self.assertEqual(self.generate(*argv), 1)
        self.assertEqual(self.generate(*argv[:10]), 0)
        self.assertEqual(len(self.calls()), 1)


class TestAgyFailures(GenerateImageCase):
    def test_agy_failure_modes_exit_2(self) -> None:
        for mode in ("nonzero", "not-success"):
            self.assertEqual(self.generate(mode=mode), 2, mode)
        self.assertEqual(self.generate(prefix=[str(self.tmp / "no-such-agy.exe")]), 2)
        self.assertEqual(self.generate("--timeout", "1", mode="sleep"), 2)
        self.assertFalse((self.work / "images" / "concept-1.png").exists())

    def test_no_image_at_all_exits_2(self) -> None:
        self.assertEqual(self.generate(mode="image-none"), 2)
        self.assertFalse((self.work / "images" / "concept-1.png").exists())

    def test_an_unreadable_image_exits_2_and_leaves_no_output(self) -> None:
        conversation = self.brain / "conv-test"
        conversation.mkdir(parents=True)
        (conversation / "broken.jpg").write_bytes(b"not an image")
        self.assertEqual(self.generate(mode="image-none"), 2)
        self.assertEqual(list((self.work / "images").iterdir()), [])


class TestConsent(GenerateImageCase):
    def set_consent(self, value) -> None:
        state = pipeline_state.load_pipeline("robot", self.root)
        state["critic"] = value
        pipeline_state.save_pipeline("robot", state, self.root)

    def test_consent_gates_the_route_and_agy_is_never_called_without_it(self) -> None:
        for value, code in ((None, 1), ("claude", 2), ("gpt", 1)):
            self.set_consent(value)
            self.assertEqual(self.generate(), code, value)
        self.assertEqual(self.calls(), [])

    def test_missing_pipeline_is_a_usage_error(self) -> None:
        shutil.rmtree(self.work)
        self.assertEqual(self.generate(), 1)


class TestArguments(GenerateImageCase):
    def test_out_must_stay_inside_the_work_dir_and_be_a_png(self) -> None:
        absolute = str((self.tmp / "elsewhere.png").resolve())
        for bad in ("../x.png", "images/../../x.png", absolute, "images/concept.jpg", "images/concept"):
            self.assertEqual(self.generate(out=bad), 1, bad)
        self.assertEqual(self.calls(), [])
        self.assertFalse((self.tmp / "work" / "x.png").exists())

    def test_bad_arguments_exit_1_not_2(self) -> None:
        for extra in (["--timeout", "0"], ["--timeout", "-3"], ["--bogus"]):
            with self.assertRaises(SystemExit) as ctx, redirect_stderr(io.StringIO()):
                self.generate(*extra)
            self.assertEqual(ctx.exception.code, 1, extra)

    def test_unexpected_exception_is_an_internal_error_not_a_traceback(self) -> None:
        with mock.patch.object(generate_image, "find_image", side_effect=RuntimeError("boom")):
            self.assertEqual(self.generate(), 1)


if __name__ == "__main__":
    unittest.main()
