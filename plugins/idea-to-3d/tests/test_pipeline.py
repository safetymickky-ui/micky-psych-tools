#!/usr/bin/env python3
"""
Automated Unit, Integration, and Headless Blender 5.2 End-to-End Test Suite
for the `idea-to-3d` plugin (0 Meshy credits spent).
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
BLENDER_EXE = os.environ.get(
    "BLENDER_EXE", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pipeline_state = load_module(
    "pipeline_state", REPO_ROOT / "skills" / "idea-to-3d" / "scripts" / "pipeline_state.py"
)
check_glb_mod = load_module(
    "check_glb", REPO_ROOT / "skills" / "blender-finish" / "scripts" / "check-glb.py"
)
make_concept_sheet_mod = load_module(
    "make_concept_sheet", REPO_ROOT / "skills" / "concept-art" / "scripts" / "make-concept-sheet.py"
)


class TestPipelineStateUnit(unittest.TestCase):
    """Unit tests for pipeline_state.py and make-concept-sheet.py CLI parsing."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="test_state_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_init_and_stage_transitions(self) -> None:
        data = pipeline_state.init_pipeline(
            slug="cute-owl",
            idea="A whimsical stylized owl",
            height_m=1.65,
            is_humanoid=False,
            clips=["idle", "wave"],
            work_root=str(self.tmpdir),
        )
        self.assertEqual(data["slug"], "cute-owl")
        self.assertEqual(data["stage"], "concept-art")
        self.assertFalse(data["is_humanoid"])
        self.assertTrue((self.tmpdir / "work" / "cute-owl" / "images").is_dir())
        self.assertTrue((self.tmpdir / "work" / "cute-owl" / "out").is_dir())

        data = pipeline_state.set_stage("cute-owl", "image-to-3d", work_root=str(self.tmpdir))
        self.assertEqual(data["stage"], "image-to-3d")

        data = pipeline_state.record_checkpoint(
            "cute-owl", "A", True, choice="concept-1", notes="Looks great", work_root=str(self.tmpdir)
        )
        self.assertTrue(data["checkpoints"]["A"]["approved"])
        self.assertEqual(data["chosen_concept"], "concept-1")

        # Verify atomic CLI set-stage + --checkpoint
        rc = pipeline_state.main(
            [
                "set-stage",
                "cute-owl",
                "blender-finish",
                "--checkpoint",
                "B",
                "--approved",
                "true",
                "--choice",
                "2",
                "--work-root",
                str(self.tmpdir),
            ]
        )
        self.assertEqual(rc, 0)
        loaded = pipeline_state.load_pipeline("cute-owl", str(self.tmpdir))
        self.assertEqual(loaded["stage"], "blender-finish")
        self.assertTrue(loaded["checkpoints"]["B"]["approved"])
        self.assertEqual(loaded["chosen_try"], 2)

        # Verify make-concept-sheet.py accepts both path=Label and Label=path
        sample_img = str(REPO_ROOT / "assets" / "logo.png")
        self.assertEqual(
            make_concept_sheet_mod._parse_item_spec(f"{sample_img}=Concept 1"),
            (sample_img, "Concept 1"),
        )
        self.assertEqual(
            make_concept_sheet_mod._parse_item_spec(f"Concept 1={sample_img}"),
            (sample_img, "Concept 1"),
        )


    def test_task_recording_and_validation(self) -> None:
        pipeline_state.init_pipeline(
            slug="desk-robot",
            idea="Spherical desk robot",
            height_m=0.35,
            work_root=str(self.tmpdir),
        )
        entry = pipeline_state.record_task(
            slug="desk-robot",
            step_key="try-1",
            task_id="task-123",
            tool="meshy_multi_image_to_3d",
            task_type="multi-image-to-3d",
            credits=30,
            status="SUCCEEDED",
            work_root=str(self.tmpdir),
        )
        self.assertEqual(entry["task_id"], "task-123")
        self.assertEqual(entry["credits"], 30)

        fetched = pipeline_state.get_task("desk-robot", "try-1", work_root=str(self.tmpdir))
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched["task_id"], "task-123")

        # Negative credits must raise ValueError
        with self.assertRaises(ValueError):
            pipeline_state.record_task(
                slug="desk-robot",
                step_key="rig",
                task_id="task-789",
                tool="meshy_rig",
                task_type="rigging",
                credits=-5,
                work_root=str(self.tmpdir),
            )

    def test_invalid_inputs_rejected(self) -> None:
        for bad_slug in ["", "---", "!!!"]:
            with self.assertRaises(ValueError):
                pipeline_state.init_pipeline(bad_slug, "bad slug test", work_root=str(self.tmpdir))

        with self.assertRaises(ValueError):
            pipeline_state.init_pipeline("valid-slug", "", work_root=str(self.tmpdir))

        with self.assertRaises(ValueError):
            pipeline_state.init_pipeline("valid-slug", "idea", height_m=-1.0, work_root=str(self.tmpdir))


class TestCheckGlbUnit(unittest.TestCase):
    """Unit tests for check-glb.py binary parser and §6 validator."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="test_glb_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _build_minimal_glb(self, gltf_dict: dict, bin_size: int = 1024) -> Path:
        json_bytes = json.dumps(gltf_dict).encode("utf-8")
        pad = (4 - (len(json_bytes) % 4)) % 4
        json_bytes += b" " * pad
        bin_bytes = b"\x00" * bin_size

        total_len = 12 + 8 + len(json_bytes) + 8 + len(bin_bytes)
        glb_path = self.tmpdir / "sample.glb"
        with glb_path.open("wb") as f:
            f.write(struct.pack("<III", 0x46546C67, 2, total_len))
            f.write(struct.pack("<II", len(json_bytes), 0x4E4F534A))
            f.write(json_bytes)
            f.write(struct.pack("<II", len(bin_bytes), 0x004E4942))
            f.write(bin_bytes)
        return glb_path

    def test_valid_glb_passes(self) -> None:
        gltf_dict = {
            "asset": {"version": "2.0"},
            "nodes": [
                {"name": "RootJoint"},
                {"name": "BodyMesh", "mesh": 0, "skin": 0},
            ],
            "meshes": [
                {
                    "name": "Body",
                    "primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "mode": 4}],
                }
            ],
            "accessors": [
                {"count": 300, "min": [-0.3, 0.0, -0.2], "max": [0.3, 1.7, 0.2]},
                {"count": 600},
            ],
            "skins": [{"joints": [0]}],
            "animations": [
                {"name": "idle", "channels": [{"target": {"node": 0, "path": "rotation"}}], "samplers": [{}]},
                {"name": "wave", "channels": [{"target": {"node": 0, "path": "rotation"}}], "samplers": [{}]},
            ],
            "materials": [{"name": "Mat"}],
            "textures": [{"source": 0}],
            "images": [{"name": "Tex", "mimeType": "image/webp"}],
        }
        glb_path = self._build_minimal_glb(gltf_dict, bin_size=2048)
        ok, problems, summary = check_glb_mod.check_glb(
            str(glb_path),
            expected_clips=["idle", "wave"],
            target_height_m=1.7,
        )
        self.assertTrue(ok, f"Expected valid GLB to pass, got problems: {problems}")
        self.assertEqual(summary["clips"], ["idle", "wave"])

    def _idle_only_glb(self) -> Path:
        gltf_dict = {
            "asset": {"version": "2.0"},
            "nodes": [{"name": "RootJoint"}, {"name": "BodyMesh", "mesh": 0, "skin": 0}],
            "meshes": [{"name": "Body", "primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "mode": 4}]}],
            "accessors": [
                {"count": 300, "min": [-0.1, 0.0, -0.1], "max": [0.1, 0.4, 0.1]},
                {"count": 600},
            ],
            "skins": [{"joints": [0]}],
            "animations": [
                {"name": "idle", "channels": [{"target": {"node": 0, "path": "rotation"}}], "samplers": [{}]},
            ],
        }
        return self._build_minimal_glb(gltf_dict, bin_size=2048)

    def test_single_idle_clip_passes_when_idle_is_the_only_expected_clip(self) -> None:
        glb_path = self._idle_only_glb()
        ok, problems, _ = check_glb_mod.check_glb(str(glb_path), expected_clips=["idle"], target_height_m=0.4)
        self.assertTrue(ok, problems)

        # Humanoid behaviour unchanged: a lone idle still fails without an idle-only expectation.
        for expected in (None, ["idle", "walk", "wave"]):
            ok, problems, _ = check_glb_mod.check_glb(str(glb_path), expected_clips=expected, target_height_m=0.4)
            self.assertFalse(ok)
            self.assertIn("expected at least 'idle' and one more animation clip", problems)

    def test_cli_reads_idle_only_expected_clips_from_pipeline_json(self) -> None:
        out_dir = self.tmpdir / "out"
        out_dir.mkdir()
        glb_path = self._idle_only_glb().replace(out_dir / "lantern.glb")
        pipeline = {"expected_clips": ["idle"], "target_height_m": 0.4}
        (self.tmpdir / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_glb_mod.main([str(glb_path)]), 0)
            pipeline["expected_clips"] = ["idle", "wave"]
            (self.tmpdir / "pipeline.json").write_text(json.dumps(pipeline), encoding="utf-8")
            self.assertEqual(check_glb_mod.main([str(glb_path)]), 1)

    def test_invalid_magic_or_missing_skin_fails(self) -> None:
        bad_path = self.tmpdir / "bad.glb"
        bad_path.write_bytes(b"NOT_A_GLB_FILE_HEADER_1234567890")
        with self.assertRaises(ValueError):
            check_glb_mod.read_glb(str(bad_path))

        # Missing skin and animations
        gltf_no_skin = {
            "asset": {"version": "2.0"},
            "nodes": [{"name": "Root", "mesh": 0}],
            "meshes": [{"name": "Body", "primitives": [{"attributes": {"POSITION": 0}}]}],
            "accessors": [{"count": 300, "min": [-0.3, 0.0, -0.2], "max": [0.3, 1.7, 0.2]}],
        }
        no_skin_path = self._build_minimal_glb(gltf_no_skin, bin_size=512)
        ok, problems, _ = check_glb_mod.check_glb(str(no_skin_path), expected_clips=["idle", "wave"])
        self.assertFalse(ok)
        self.assertGreaterEqual(len(problems), 2)


class TestBlenderEndToEndPipeline(unittest.TestCase):
    """End-to-End headless Blender 5.2 tests covering Stage 1, Stage 2, and Stage 4 scripts."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp(prefix="test_blender_e2e_"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_full_headless_blender_pipeline_and_multi_glb_merge(self) -> None:
        self.assertTrue(
            Path(BLENDER_EXE).exists(), f"Blender 5.2 executable not found at {BLENDER_EXE}"
        )

        # Initialize pipeline state for test-bot
        pipeline_state.init_pipeline(
            slug="test-bot",
            idea="Spherical floating lab assistant robot",
            height_m=1.7,
            is_humanoid=False,
            clips=["idle", "wave"],
            work_root=str(self.tmpdir),
        )

        # 1. Stage 1 concept sheet test (make-concept-sheet.py via system python)
        images_dir = self.tmpdir / "work" / "test-bot" / "images"
        logo_png = REPO_ROOT / "assets" / "logo.png"
        for view in ["front", "side", "back"]:
            shutil.copy2(logo_png, images_dir / f"{view}.png")

        concept_sheet = self.tmpdir / "work" / "test-bot" / "preview" / "concepts.png"
        make_sheet_script = REPO_ROOT / "skills" / "concept-art" / "scripts" / "make-concept-sheet.py"
        proc_sheet = subprocess.run(
            [
                sys.executable,
                str(make_sheet_script),
                "--normalize",
                "--out",
                str(concept_sheet),
                "--title",
                "test-bot: Turnaround Sheet",
                f"{images_dir / 'front.png'}=Front",
                f"{images_dir / 'side.png'}=Side",
                f"{images_dir / 'back.png'}=Back",
            ],
            capture_output=True,
            text=True,
            timeout=60,
        )
        self.assertEqual(proc_sheet.returncode, 0, f"make-concept-sheet failed: {proc_sheet.stderr}")
        self.assertTrue(concept_sheet.exists())
        self.assertGreater(concept_sheet.stat().st_size, 5000)

        # 2. Stage 4 scripted robot + procedural rig build (import-merge.py)
        blend_out = self.tmpdir / "work" / "test-bot" / "blender" / "test-bot.blend"
        glb_out = self.tmpdir / "work" / "test-bot" / "out" / "test-bot.glb"
        import_merge_script = REPO_ROOT / "skills" / "blender-finish" / "scripts" / "import-merge.py"

        proc_merge = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(import_merge_script),
                "--",
                "--out",
                str(blend_out),
                "--scripted-robot",
                "--clips",
                "idle,wave",
                "--height",
                "1.7",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        self.assertEqual(proc_merge.returncode, 0, f"import-merge failed: {proc_merge.stderr}")
        self.assertTrue(blend_out.exists())

        # 3. Stage 4 atomic export & quality gate verification (export-check.py)
        report_json = self.tmpdir / "work" / "test-bot" / "out" / "quality_report.json"
        export_check_script = REPO_ROOT / "skills" / "blender-finish" / "scripts" / "export-check.py"
        proc_check = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(export_check_script),
                "--",
                "--blend",
                str(blend_out),
                "--out",
                str(glb_out),
                "--report",
                str(report_json),
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        self.assertEqual(
            proc_check.returncode,
            0,
            f"export-check failed:\nstdout={proc_check.stdout}\nstderr={proc_check.stderr}",
        )
        self.assertTrue(glb_out.exists(), "Expected atomic export to produce test-bot.glb")
        report_data = json.loads(report_json.read_text(encoding="utf-8"))
        self.assertTrue(report_data["ok"], f"Quality gates failed: {report_data['errors']}")

        # 4. Stage 2 4-view turnaround comparison render (render-meshy.py)
        stage2_preview = self.tmpdir / "work" / "test-bot" / "preview" / "tries.png"
        render_meshy_script = REPO_ROOT / "skills" / "image-to-3d" / "scripts" / "render-meshy.py"
        proc_s2 = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(render_meshy_script),
                "--",
                str(stage2_preview),
                str(images_dir / "front.png"),
                f"{glb_out}=Try 1 (Scripted Robot)",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        self.assertEqual(proc_s2.returncode, 0, f"render-meshy failed: {proc_s2.stderr}")
        self.assertTrue(stage2_preview.exists())
        self.assertGreater(stage2_preview.stat().st_size, 5000)

        # 5. Stage 4 contact sheet render (render-sheet.py)
        final_preview = self.tmpdir / "work" / "test-bot" / "preview" / "sheet.png"
        render_sheet_script = REPO_ROOT / "skills" / "blender-finish" / "scripts" / "render-sheet.py"
        proc_s4 = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(render_sheet_script),
                "--",
                "--blend",
                str(blend_out),
                "--out",
                str(final_preview),
                "--concept",
                str(images_dir / "front.png"),
                "--tile-size",
                "96",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        self.assertEqual(proc_s4.returncode, 0, f"render-sheet failed: {proc_s4.stderr}")
        self.assertTrue(final_preview.exists())
        self.assertGreater(final_preview.stat().st_size, 10000)

        # 6. Test merging separate clip GLBs (simulating Meshy Stage 3 outputs)
        merged_blend = self.tmpdir / "work" / "test-merged" / "blender" / "test-merged.blend"
        merged_glb = self.tmpdir / "work" / "test-merged" / "out" / "test-merged.glb"
        proc_multi = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(import_merge_script),
                "--",
                "--out",
                str(merged_blend),
                "--rigged",
                str(glb_out),
                "--clip",
                f"idle={glb_out}",
                "--clip",
                f"wave={glb_out}",
                "--height",
                "1.7",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        self.assertEqual(proc_multi.returncode, 0, f"Multi-GLB merge failed: {proc_multi.stderr}")
        self.assertTrue(merged_blend.exists())

        proc_multi_check = subprocess.run(
            [
                BLENDER_EXE,
                "-b",
                "--factory-startup",
                "--python-exit-code",
                "1",
                "-P",
                str(export_check_script),
                "--",
                "--blend",
                str(merged_blend),
                "--out",
                str(merged_glb),
                "--clips",
                "idle,wave",
                "--height",
                "1.7",
            ],
            capture_output=True,
            text=True,
            timeout=90,
        )
        self.assertEqual(
            proc_multi_check.returncode,
            0,
            f"Multi-GLB export-check failed:\nstdout={proc_multi_check.stdout}\nstderr={proc_multi_check.stderr}",
        )
        self.assertTrue(merged_glb.exists())


if __name__ == "__main__":
    unittest.main()
