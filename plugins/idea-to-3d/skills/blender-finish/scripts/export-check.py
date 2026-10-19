#!/usr/bin/env python3
"""
Stage 4 headless Blender 5.2 atomic glTF exporter & §6/§4.7 quality verifier.

Opens work/<slug>/blender/<slug>.blend, verifies materials/UVs/bone motion in Blender,
exports to work/<slug>/out/<slug>.tmp.glb with WebP textures and Action clips,
runs check-glb.py against all §6 requirements, and atomically replaces
work/<slug>/out/<slug>.glb only when every check passes.

Run:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup --python-exit-code 1 -P export-check.py -- --blend work/<slug>/blender/<slug>.blend --out work/<slug>/out/<slug>.glb
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else sys.argv[1:]
    parser = argparse.ArgumentParser(description="Atomically export .blend to .glb and verify all quality gates")
    parser.add_argument("--blend", default="", help="Path to input .blend file (work/<slug>/blender/<slug>.blend)")
    parser.add_argument("--out", "--glb", dest="out", required=True, help="Target .glb path (work/<slug>/out/<slug>.glb)")
    parser.add_argument("--pipeline", default="", help="Optional path to work/<slug>/pipeline.json")
    parser.add_argument("--idea", default="", help="Optional path to work/<slug>/idea.md")
    parser.add_argument("--clips", "--expected-clips", dest="clips", default="", help="Comma-separated expected clips")
    parser.add_argument("--height", type=float, default=None, help="Target character height in meters")
    parser.add_argument("--max-triangles", type=int, default=None, help="Maximum triangle budget")
    parser.add_argument("--max-bytes", type=int, default=None, help="Maximum GLB size in bytes")
    parser.add_argument("--allow-single-clip", action="store_true", help="Allow single idle clip (tracer bullet)")
    parser.add_argument("--report", default="", help="Optional path to write JSON verification report")
    return parser.parse_args(argv)


def load_check_glb_module():
    check_glb_path = Path(__file__).resolve().parent / "check-glb.py"
    spec = importlib.util.spec_from_file_location("check_glb", str(check_glb_path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {check_glb_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def inspect_and_export_in_blender(
    blend_path: str,
    tmp_glb_path: str,
    existing_glb_path: str,
    expected_clips: list[str] | None,
) -> dict[str, Any]:
    import bpy

    if blend_path and os.path.exists(blend_path):
        bpy.ops.wm.open_mainfile(filepath=os.path.abspath(blend_path))
    elif os.path.exists(existing_glb_path):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=os.path.abspath(existing_glb_path))
    else:
        raise FileNotFoundError(f"Neither --blend '{blend_path}' nor --out '{existing_glb_path}' exists")

    # Strip any cameras or lights prior to export
    for obj in list(bpy.data.objects):
        if obj.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(obj, do_unlink=True)

    errors: list[str] = []
    warnings: list[str] = []

    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    armatures = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    if not meshes:
        errors.append("No MESH objects in Blender scene")
    if not armatures:
        errors.append("No ARMATURE objects in Blender scene")

    # Verify UVs and non-black Principled BSDF materials
    material_summaries: list[dict[str, Any]] = []
    for m in meshes:
        uv_names = [uv.name for uv in m.data.uv_layers]
        if not uv_names:
            errors.append(f"Mesh '{m.name}' has no UVMap")
        if not m.data.materials:
            errors.append(f"Mesh '{m.name}' has no material assigned")
        for mat in m.data.materials:
            if not mat or not mat.node_tree:
                errors.append(f"Mesh '{m.name}' has invalid material")
                continue
            bsdf = next((n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if bsdf is None:
                errors.append(f"Material '{mat.name}' has no Principled BSDF shader node")
                continue
            base_in = bsdf.inputs.get("Base Color")
            mean_rgb = 0.0
            has_tex = False
            if base_in is not None:
                if base_in.is_linked:
                    for link in base_in.links:
                        if link.from_node.type == "TEX_IMAGE" and link.from_node.image is not None:
                            img = link.from_node.image
                            has_tex = True
                            px = list(img.pixels[: min(len(img.pixels), 4096)])
                            if px:
                                rgb_vals = [px[i] for i in range(len(px)) if (i % 4) != 3]
                                mean_rgb = sum(rgb_vals) / max(len(rgb_vals), 1)
                else:
                    col = list(base_in.default_value)[:3]
                    mean_rgb = sum(col) / 3.0
            if mean_rgb <= 0.02:
                errors.append(f"Material '{mat.name}' appears solid black (mean RGB={mean_rgb:.4f} <= 0.02)")
            material_summaries.append(
                {
                    "mesh": m.name,
                    "material": mat.name,
                    "has_texture": has_tex,
                    "mean_rgb": round(mean_rgb, 4),
                    "uv_layers": uv_names,
                }
            )

    # Verify actions and bone motion
    arm_obj = armatures[0] if armatures else None
    clip_summaries: dict[str, Any] = {}
    if arm_obj is not None:
        arm_obj.animation_data_create()
        clips_to_check = expected_clips if expected_clips else [a.name for a in bpy.data.actions]
        for cname in clips_to_check:
            act = bpy.data.actions.get(cname)
            if act is None:
                errors.append(f"Expected action '{cname}' not found in bpy.data.actions")
                continue
            f_start, f_end = act.frame_range
            if f_end <= f_start:
                errors.append(f"Action '{cname}' has degenerate frame_range ({f_start}, {f_end})")
                continue

            arm_obj.animation_data.action = act
            if hasattr(act, "slots") and act.slots:
                arm_obj.animation_data.action_slot = act.slots[0]

            sample_frames = [
                int(round(f_start)),
                int(round(f_start + (f_end - f_start) * 0.25)),
                int(round(f_start + (f_end - f_start) * 0.50)),
                int(round(f_start + (f_end - f_start) * 0.75)),
                int(round(f_end)),
            ]
            snaps: dict[str, list[tuple[Any, Any]]] = {pb.name: [] for pb in arm_obj.pose.bones}
            for f in sample_frames:
                bpy.context.scene.frame_set(f)
                bpy.context.view_layer.update()
                for pb in arm_obj.pose.bones:
                    mat_local = pb.matrix.copy()
                    snaps[pb.name].append((mat_local.to_translation(), mat_local.to_quaternion()))

            moved_bones = 0
            for bname, bsnaps in snaps.items():
                loc0, q0 = bsnaps[0]
                max_deg = 0.0
                max_disp = 0.0
                for loci, qi in bsnaps[1:]:
                    disp = (loci - loc0).length
                    dot = min(1.0, max(-1.0, abs(q0.dot(qi))))
                    deg = math.degrees(2.0 * math.acos(dot))
                    max_deg = max(max_deg, deg)
                    max_disp = max(max_disp, disp)
                if max_deg > 0.5 or max_disp > 0.002:
                    moved_bones += 1

            if moved_bones == 0:
                errors.append(f"Action '{cname}' does not move any pose bones across frames {f_start}..{f_end}")

            clip_summaries[cname] = {
                "frame_start": float(f_start),
                "frame_end": float(f_end),
                "moved_bones": moved_bones,
                "total_bones": len(arm_obj.pose.bones),
            }

        # Leave 'idle' active on the armature
        idle_act = bpy.data.actions.get("idle") or (bpy.data.actions[0] if bpy.data.actions else None)
        if idle_act is not None:
            arm_obj.animation_data.action = idle_act
            if hasattr(idle_act, "slots") and idle_act.slots:
                arm_obj.animation_data.action_slot = idle_act.slots[0]
        bpy.context.scene.frame_set(0)
        bpy.context.view_layer.update()

    # Export to tmp_glb_path if we loaded a .blend file (or if existing_glb_path doesn't exist yet)
    os.makedirs(os.path.dirname(os.path.abspath(tmp_glb_path)), exist_ok=True)
    if blend_path and os.path.exists(blend_path):
        bpy.ops.export_scene.gltf(
            filepath=os.path.abspath(tmp_glb_path),
            export_format="GLB",
            export_image_format="WEBP",
            export_cameras=False,
            export_lights=False,
            export_yup=True,
            export_skins=True,
            export_animations=True,
            export_animation_mode="ACTIONS",
            export_morph_animation=False,
        )
    else:
        # Inspecting an already exported GLB directly
        tmp_glb_path = os.path.abspath(existing_glb_path)

    return {
        "blender_ok": len(errors) == 0,
        "materials": material_summaries,
        "clips": clip_summaries,
        "errors": errors,
        "warnings": warnings,
        "inspected_glb": tmp_glb_path,
    }


def main() -> int:
    args = parse_args()
    out_glb = os.path.abspath(args.out)

    # Auto-infer --blend if not provided and work/<slug>/blender/<slug>.blend exists
    blend_path = os.path.abspath(args.blend) if args.blend else ""
    if not blend_path:
        parent_dir = os.path.dirname(out_glb)
        slug_dir = os.path.dirname(parent_dir) if os.path.basename(parent_dir) == "out" else parent_dir
        stem = os.path.splitext(os.path.basename(out_glb))[0]
        candidate_blend = os.path.join(slug_dir, "blender", f"{stem}.blend")
        if os.path.exists(candidate_blend):
            blend_path = candidate_blend

    in_blender = False
    try:
        import bpy  # noqa: F401

        in_blender = True
    except ImportError:
        in_blender = False

    if not in_blender:
        blender_exe = os.environ.get(
            "BLENDER_EXE", r"C:\Program Files\Blender Foundation\Blender 5.2\blender.exe"
        )
        cmd = [
            blender_exe,
            "-b",
            "--factory-startup",
            "--python-exit-code",
            "1",
            "-P",
            str(Path(__file__).resolve()),
            "--",
            "--out",
            out_glb,
        ]
        if blend_path:
            cmd.extend(["--blend", blend_path])
        if args.pipeline:
            cmd.extend(["--pipeline", os.path.abspath(args.pipeline)])
        if args.idea:
            cmd.extend(["--idea", os.path.abspath(args.idea)])
        if args.clips:
            cmd.extend(["--clips", args.clips])
        if args.height is not None:
            cmd.extend(["--height", str(args.height)])
        if args.max_triangles is not None:
            cmd.extend(["--max-triangles", str(args.max_triangles)])
        if args.max_bytes is not None:
            cmd.extend(["--max-bytes", str(args.max_bytes)])
        if args.allow_single_clip:
            cmd.append("--allow-single-clip")
        if args.report:
            cmd.extend(["--report", os.path.abspath(args.report)])
        proc = subprocess.run(cmd)
        return proc.returncode

    check_glb_mod = load_check_glb_module()

    # Resolve pipeline.json and idea.md parameters
    parent_dir = os.path.dirname(out_glb)
    slug_dir = (
        os.path.dirname(parent_dir)
        if os.path.basename(parent_dir) in ("out", "meshy", "blender")
        else parent_dir
    )
    pipeline_path = args.pipeline or os.path.join(slug_dir, "pipeline.json")
    idea_path = args.idea or os.path.join(slug_dir, "idea.md")

    expected_clips: list[str] | None = None
    target_height: float | None = args.height
    tri_budget = check_glb_mod.DEFAULT_MAX_TRIANGLES
    max_bytes = check_glb_mod.DEFAULT_MAX_BYTES

    if os.path.exists(pipeline_path):
        with open(pipeline_path, "r", encoding="utf-8") as f:
            pdata = json.load(f)
        if pdata.get("expected_clips"):
            expected_clips = list(pdata["expected_clips"])
        if target_height is None and pdata.get("target_height_m"):
            target_height = float(pdata["target_height_m"])
        if pdata.get("triangle_budget"):
            tri_budget = int(pdata["triangle_budget"])
        if pdata.get("max_bytes"):
            max_bytes = int(pdata["max_bytes"])

    if target_height is None and os.path.exists(idea_path):
        target_height = check_glb_mod.parse_height_from_idea(idea_path)

    if args.clips:
        expected_clips = [c.strip() for c in args.clips.split(",") if c.strip()]
    if args.max_triangles is not None:
        tri_budget = args.max_triangles
    if args.max_bytes is not None:
        max_bytes = args.max_bytes

    stem, _ = os.path.splitext(out_glb)
    tmp_glb = f"{stem}.tmp.glb" if (blend_path and os.path.exists(blend_path)) else out_glb

    blender_report = inspect_and_export_in_blender(
        blend_path=blend_path,
        tmp_glb_path=tmp_glb,
        existing_glb_path=out_glb,
        expected_clips=expected_clips,
    )

    glb_ok, glb_problems, glb_summary = check_glb_mod.check_glb(
        glb_path=blender_report["inspected_glb"],
        expected_clips=expected_clips,
        target_height_m=target_height,
        triangle_budget=tri_budget,
        max_bytes=max_bytes,
        allow_single_clip=args.allow_single_clip,
    )

    combined_errors = list(blender_report["errors"]) + list(glb_problems)
    all_ok = len(combined_errors) == 0

    if all_ok and tmp_glb != out_glb and os.path.exists(tmp_glb):
        os.makedirs(os.path.dirname(out_glb), exist_ok=True)
        os.replace(tmp_glb, out_glb)
        glb_summary["file"] = os.path.basename(out_glb)
    elif not all_ok and tmp_glb != out_glb and os.path.exists(tmp_glb):
        try:
            os.remove(tmp_glb)
        except OSError:
            pass

    final_report = {
        "ok": all_ok,
        "glb_path": out_glb,
        "summary": glb_summary,
        "blender_check": blender_report,
        "errors": combined_errors,
        "warnings": blender_report["warnings"],
    }

    if args.report:
        os.makedirs(os.path.dirname(os.path.abspath(args.report)), exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            json.dump(final_report, f, indent=2)

    print(
        f"{glb_summary['file']}: {glb_summary['megabytes']:.2f} MB, {glb_summary['triangles']} triangles, "
        f"{glb_summary['bones']} bones, min_y={glb_summary['min_y']}, height={glb_summary['height_m']}m, "
        f"clips={glb_summary['clips']}"
    )
    if not all_ok:
        for err in combined_errors:
            print(f"  FAIL: {err}")
        return 1
    print("  OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
