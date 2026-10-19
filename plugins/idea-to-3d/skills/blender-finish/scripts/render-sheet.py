#!/usr/bin/env python3
"""
Stage 4 headless Blender 5.2 preview sheet renderer (work/<slug>/preview/sheet.png).

Renders:
- Top row: Concept image (if provided) + Front, 3/4, Side, Back turnaround views in rest/idle pose
- Subsequent rows: One row per animation clip showing 4 views (front, 3/4, side, back) x 3 frames
  (start, mid, end), composited into a single labelled contact sheet PNG.

Run:
  "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b --factory-startup --python-exit-code 1 -P render-sheet.py -- --blend work/<slug>/blender/<slug>.blend --out work/<slug>/preview/sheet.png [--concept work/<slug>/images/front.png]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

import bpy
from mathutils import Vector


def parse_args() -> argparse.Namespace:
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Render Stage 4 Checkpoint C preview contact sheet")
    parser.add_argument("--blend", default="", help="Path to work/<slug>/blender/<slug>.blend")
    parser.add_argument("--glb", default="", help="Fallback path to work/<slug>/out/<slug>.glb")
    parser.add_argument("--out", required=True, help="Output PNG path (work/<slug>/preview/sheet.png)")
    parser.add_argument("--concept", default="", help="Optional concept/front image to include in header")
    parser.add_argument("--clips", default="", help="Optional comma-separated clip names")
    parser.add_argument("--tile-size", type=int, default=192, help="Render tile size in pixels (default: 192)")
    return parser.parse_args(argv)


def get_character_bounds() -> Tuple[Vector, Vector, float]:
    bpy.context.view_layer.update()
    meshes = [o for o in bpy.data.objects if o.type == "MESH"]
    if not meshes:
        return Vector((0, 0, 0)), Vector((0, 0, 1.7)), 1.7

    min_v = Vector((float("inf"), float("inf"), float("inf")))
    max_v = Vector((float("-inf"), float("-inf"), float("-inf")))
    for m in meshes:
        for corner in m.bound_box:
            w = m.matrix_world @ Vector(corner)
            min_v.x = min(min_v.x, w.x)
            min_v.y = min(min_v.y, w.y)
            min_v.z = min(min_v.z, w.z)
            max_v.x = max(max_v.x, w.x)
            max_v.y = max(max_v.y, w.y)
            max_v.z = max(max_v.z, w.z)
    dims = max_v - min_v
    return min_v, max_v, max(dims.x, dims.y, dims.z, 0.2)


def setup_lighting_and_camera(center: Vector, max_span: float, tile_size: int) -> bpy.types.Object:
    scene = bpy.context.scene
    avail_engines = {
        item.identifier for item in scene.render.bl_rna.properties["engine"].enum_items
    }
    if "BLENDER_EEVEE_NEXT" in avail_engines:
        scene.render.engine = "BLENDER_EEVEE_NEXT"
    elif "BLENDER_EEVEE" in avail_engines:
        scene.render.engine = "BLENDER_EEVEE"
    else:
        scene.render.engine = "BLENDER_WORKBENCH"

    if hasattr(scene, "eevee") and hasattr(scene.eevee, "taa_render_samples"):
        scene.eevee.taa_render_samples = 16

    scene.render.resolution_x = tile_size
    scene.render.resolution_y = tile_size
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"

    if scene.world is None:
        scene.world = bpy.data.worlds.new("PreviewWorld")
    if not scene.world.node_tree:
        scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (0.18, 0.19, 0.22, 1.0)
        bg_node.inputs[1].default_value = 1.0

    for obj in list(bpy.data.objects):
        if obj.type in {"LIGHT", "CAMERA"}:
            bpy.data.objects.remove(obj, do_unlink=True)

    light_specs = [
        ("KeyLight", "SUN", 3.2, (math.radians(50), 0.0, math.radians(-35))),
        ("FillLight", "SUN", 1.4, (math.radians(65), 0.0, math.radians(50))),
        ("RimLight", "SUN", 2.0, (math.radians(40), 0.0, math.radians(160))),
    ]
    for name, ltype, energy, rot in light_specs:
        ldata = bpy.data.lights.new(name=name, type=ltype)
        ldata.energy = energy
        lobj = bpy.data.objects.new(name=name, object_data=ldata)
        bpy.context.collection.objects.link(lobj)
        lobj.rotation_euler = rot

    target = bpy.data.objects.new("SheetCamTarget", None)
    bpy.context.collection.objects.link(target)
    target.location = center

    cam_data = bpy.data.cameras.new("SheetCam")
    cam_data.lens = 50.0
    cam_obj = bpy.data.objects.new("SheetCam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    scene.camera = cam_obj

    ttc = cam_obj.constraints.new(type="TRACK_TO")
    ttc.target = target
    ttc.track_axis = "TRACK_NEGATIVE_Z"
    ttc.up_axis = "UP_Y"

    return cam_obj


def composite_with_pil_or_blender(
    out_path: Path,
    tile_files: List[List[Path]],
    clip_names: List[str],
    tile_size: int,
    concept_path: str,
) -> Tuple[int, int]:
    helper_code = r"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

cfg = json.loads(sys.stdin.read())
out_path = cfg["out_path"]
tile_files = cfg["tile_files"]
clip_names = cfg["clip_names"]
tile = cfg["tile_size"]
concept_path = cfg["concept_path"]

font_path = r"C:\Windows\Fonts\segoeui.ttf"
title_font = ImageFont.truetype(font_path, 22) if os.path.exists(font_path) else ImageFont.load_default()
label_font = ImageFont.truetype(font_path, 15) if os.path.exists(font_path) else ImageFont.load_default()

num_rows = len(tile_files)
num_cols = len(tile_files[0]) if num_rows else 12
pad = 6
has_concept = bool(concept_path and os.path.exists(concept_path))
concept_col_w = (tile + pad) if has_concept else 0
label_w = 160
header_h = 54
width = concept_col_w + label_w + num_cols * (tile + pad) + pad
height = header_h + num_rows * (tile + pad) + pad

sheet = Image.new("RGBA", (width, height), (28, 30, 36, 255))
draw = ImageDraw.Draw(sheet)
draw.text(
    (16, 14),
    "Checkpoint C — Final Rigged & Animated Contact Sheet (Front | 3/4 | Side | Back x Start/Mid/End)",
    font=title_font,
    fill=(242, 245, 250, 255),
)

if has_concept:
    c_img = Image.open(concept_path).convert("RGBA").resize((tile, tile), Image.Resampling.LANCZOS)
    cy = header_h + pad
    sheet.alpha_composite(c_img, (pad, cy))
    draw.text((pad + 6, cy + 4), "Concept", font=label_font, fill=(30, 34, 42, 255))

view_labels = ["Front", "3/4", "Side", "Back"]
frame_labels = ["start", "mid", "end"]

for r_idx, row in enumerate(tile_files):
    y = header_h + r_idx * (tile + pad)
    cname = clip_names[r_idx] if r_idx < len(clip_names) else f"Clip {r_idx+1}"
    draw.text((concept_col_w + 16, y + tile // 2 - 12), f"Clip: {cname}", font=title_font, fill=(255, 255, 255, 255))
    for c_idx, tpath in enumerate(row):
        x = concept_col_w + label_w + c_idx * (tile + pad)
        t_img = Image.open(tpath).convert("RGBA").resize((tile, tile), Image.Resampling.LANCZOS)
        sheet.alpha_composite(t_img, (x, y))
        v_lbl = view_labels[(c_idx // 3) % 4]
        f_lbl = frame_labels[c_idx % 3]
        draw.text((x + 5, y + 4), f"{v_lbl} ({f_lbl})", font=label_font, fill=(220, 228, 240, 255))

os.makedirs(os.path.dirname(out_path), exist_ok=True)
sheet.convert("RGB").save(out_path, format="PNG")
print(json.dumps({"width": width, "height": height}))
"""
    payload = json.dumps(
        {
            "out_path": str(out_path),
            "tile_files": [[str(p) for p in r] for r in tile_files],
            "clip_names": clip_names,
            "tile_size": tile_size,
            "concept_path": concept_path,
        }
    )
    proc = subprocess.run(["python", "-c", helper_code], input=payload, text=True, capture_output=True)
    if proc.returncode == 0:
        info = json.loads(proc.stdout.strip().splitlines()[-1])
        return info["width"], info["height"]

    # Fallback: pure Blender bpy.data.images grid
    num_rows = max(len(tile_files), 1)
    num_cols = len(tile_files[0]) if tile_files else 12
    sheet_w = num_cols * tile_size
    sheet_h = num_rows * tile_size
    sheet_img = bpy.data.images.new(
        "ContactSheet", width=sheet_w, height=sheet_h, alpha=True, float_buffer=False
    )
    sheet_pixels = [0.11, 0.12, 0.14, 1.0] * (sheet_w * sheet_h)
    for r_idx, row_files in enumerate(tile_files):
        dest_row = (num_rows - 1) - r_idx
        y_offset = dest_row * tile_size
        for c_idx, tile_path in enumerate(row_files):
            x_offset = c_idx * tile_size
            t_img = bpy.data.images.load(str(tile_path))
            t_pixels = list(t_img.pixels)
            for ty in range(tile_size):
                s0 = ty * tile_size * 4
                d0 = ((y_offset + ty) * sheet_w + x_offset) * 4
                sheet_pixels[d0 : d0 + tile_size * 4] = t_pixels[s0 : s0 + tile_size * 4]
            bpy.data.images.remove(t_img)
    sheet_img.pixels = sheet_pixels
    sheet_img.filepath_raw = str(out_path)
    sheet_img.file_format = "PNG"
    sheet_img.save()
    bpy.data.images.remove(sheet_img)
    return sheet_w, sheet_h


def main() -> int:
    args = parse_args()
    out_path = Path(args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    if args.blend and Path(args.blend).exists():
        bpy.ops.wm.open_mainfile(filepath=str(Path(args.blend).resolve()))
    elif args.glb and Path(args.glb).exists():
        bpy.ops.wm.read_factory_settings(use_empty=True)
        bpy.ops.import_scene.gltf(filepath=str(Path(args.glb).resolve()))
    else:
        print(json.dumps({"error": "Either --blend or --glb must point to an existing file"}), file=sys.stderr)
        return 1

    armatures = [o for o in bpy.data.objects if o.type == "ARMATURE"]
    arm_obj = armatures[0] if armatures else None
    if arm_obj:
        arm_obj.animation_data_create()

    min_v, max_v, max_span = get_character_bounds()
    center = (min_v + max_v) * 0.5
    tile_size = args.tile_size
    cam_obj = setup_lighting_and_camera(center, max_span, tile_size)

    dist = max_span * 1.95
    cam_z = center.z + max_span * 0.1
    view_angles_deg = [0.0, 40.0, 90.0, 180.0]

    requested_clips = [c.strip() for c in args.clips.split(",") if c.strip()] if args.clips else []
    active_clips: List[Tuple[str, bpy.types.Action]] = []
    if requested_clips:
        for c in requested_clips:
            act = bpy.data.actions.get(c)
            if act is None:
                act = next((a for a in bpy.data.actions if a.name.lower() == c.lower()), None)
            if act is not None:
                active_clips.append((c, act))
    else:
        for act in bpy.data.actions:
            active_clips.append((act.name, act))

    tmpdir = Path(tempfile.mkdtemp(prefix="blender_sheet_"))
    tile_files: List[List[Path]] = []
    clip_names: List[str] = []

    try:
        num_rows = max(len(active_clips), 1)
        for r_idx in range(num_rows):
            row_files: List[Path] = []
            if r_idx < len(active_clips) and arm_obj is not None:
                clip_name, act = active_clips[r_idx]
                arm_obj.animation_data.action = act
                if hasattr(act, "slots") and act.slots:
                    arm_obj.animation_data.action_slot = act.slots[0]
                f_start, f_end = act.frame_range
                frames = [
                    int(round(f_start)),
                    int(round((f_start + f_end) * 0.5)),
                    int(round(f_end)),
                ]
            else:
                clip_name = "rest"
                frames = [0, 15, 30]
            clip_names.append(clip_name)

            for v_idx, angle_deg in enumerate(view_angles_deg):
                rad = math.radians(angle_deg)
                cam_obj.location = Vector(
                    (
                        center.x + dist * math.sin(rad),
                        center.y - dist * math.cos(rad),
                        cam_z,
                    )
                )
                for f_idx, frame_num in enumerate(frames):
                    bpy.context.scene.frame_set(frame_num)
                    bpy.context.view_layer.update()
                    tile_path = tmpdir / f"r{r_idx:02d}_v{v_idx}_f{f_idx}.png"
                    bpy.context.scene.render.filepath = str(tile_path)
                    bpy.ops.render.render(write_still=True)
                    row_files.append(tile_path)
            tile_files.append(row_files)

        sheet_w, sheet_h = composite_with_pil_or_blender(
            out_path=out_path,
            tile_files=tile_files,
            clip_names=clip_names,
            tile_size=tile_size,
            concept_path=args.concept,
        )
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    print(
        json.dumps(
            {
                "status": "ok",
                "output": str(out_path),
                "width": sheet_w,
                "height": sheet_h,
                "clips": clip_names,
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
