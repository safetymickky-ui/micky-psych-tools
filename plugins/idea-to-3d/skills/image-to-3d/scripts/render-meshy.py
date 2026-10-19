# Renders Meshy image-to-3D tries side-by-side in front, three-quarter, side, and close-up face/upper
# views, all centered and normalized to the same height, then composites them with the concept image
# into work/<slug>/preview/tries.png for Checkpoint B.
# Run:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P render-meshy.py -- <out_sheet.png> <concept.png> <try1.glb>[=Label] [<try2.glb>[=Label] ...]
import math
import os
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
if len(args) < 3:
    raise SystemExit(
        "Usage: blender -b --factory-startup --python-exit-code 1 -P render-meshy.py -- <out_sheet.png> <concept.png> <try1.glb>[=Label] ..."
    )

OUT_SHEET = os.path.abspath(args[0])
CONCEPT_PATH = os.path.abspath(args[1]) if args[1] and args[1] != "none" else ""
TRY_SPECS = args[2:]

RENDER_DIR = os.path.join(os.path.dirname(OUT_SHEET), "tries_views")
VIEWS = {
    "front": (0, 2.3, 0.0),
    "three-quarter": (35, 2.3, 0.0),
    "side": (90, 2.3, 0.0),
    "face": (0, 0.78, 0.52),
}
RENDER_SIZE = 1024


def setup_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    engines = [e.identifier for e in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items]
    scene.render.engine = next(
        e for e in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE", "BLENDER_WORKBENCH") if e in engines
    )
    views = [
        i.identifier
        for i in bpy.types.ColorManagedViewSettings.bl_rna.properties["view_transform"].enum_items
    ]
    scene.view_settings.view_transform = (
        "Khronos PBR Neutral" if "Khronos PBR Neutral" in views else "Standard"
    )
    scene.render.resolution_x = scene.render.resolution_y = RENDER_SIZE
    scene.render.film_transparent = True

    world = bpy.data.worlds.new("World")
    if not world.node_tree:
        world.use_nodes = True
    bg = next((n for n in world.node_tree.nodes if n.type == "BACKGROUND"), None)
    if bg:
        bg.inputs["Color"].default_value = (0.45, 0.47, 0.52, 1.0)
        bg.inputs["Strength"].default_value = 0.7
    scene.world = world

    cam = bpy.data.objects.new("Camera", bpy.data.cameras.new("Camera"))
    scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    cam.data.ortho_scale = 2.3
    cam.location = (0, -10, 0)
    cam.rotation_euler = (math.radians(90), 0, 0)
    scene.camera = cam

    for name, energy, rot in (
        ("Key", 3.0, (50, 0, -30)),
        ("Fill", 1.2, (60, 0, 40)),
        ("Rim", 1.5, (-40, 0, 180)),
    ):
        light = bpy.data.objects.new(name, bpy.data.lights.new(name, "SUN"))
        light.data.energy = energy
        light.rotation_euler = tuple(math.radians(a) for a in rot)
        scene.collection.objects.link(light)
    return scene


def load_model(path: str):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    parts = [o for o in bpy.data.objects if o not in before]
    bpy.context.view_layer.update()
    meshes = [o for o in parts if o.type == "MESH"]
    if not meshes:
        raise RuntimeError(f"No mesh objects found in {path}")
    corners = [o.matrix_world @ Vector(c) for o in meshes for c in o.bound_box]
    lo = Vector((min(c[i] for c in corners) for i in range(3)))
    hi = Vector((max(c[i] for c in corners) for i in range(3)))
    span_z = max(hi.z - lo.z, 1e-4)

    pivot = bpy.data.objects.new("Pivot", None)
    bpy.context.scene.collection.objects.link(pivot)
    mid = (lo + hi) / 2
    for o in parts:
        if o.parent is None:
            o.location -= mid
            o.parent = pivot
    pivot.scale = (2.0 / span_z,) * 3
    face_count = sum(len(o.data.polygons) for o in meshes)
    print(f"{os.path.basename(path)}: {face_count} faces, raw size {tuple(round(x, 3) for x in (hi - lo))}")
    return pivot, parts, face_count


def build_sheet(rows_meta: list[tuple[str, str, int]]) -> None:
    import json
    import subprocess

    helper_code = r"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

cfg = json.loads(sys.stdin.read())
OUT_SHEET = cfg["out_sheet"]
CONCEPT_PATH = cfg["concept_path"]
RENDER_DIR = cfg["render_dir"]
VIEWS = cfg["views"]
rows_meta = cfg["rows_meta"]

font_path = r"C:\Windows\Fonts\segoeui.ttf"
title_font = ImageFont.truetype(font_path, 26) if os.path.exists(font_path) else ImageFont.load_default()
label_font = ImageFont.truetype(font_path, 20) if os.path.exists(font_path) else ImageFont.load_default()

tile = 340
pad = 16
label_w = 260
has_concept = bool(CONCEPT_PATH and os.path.exists(CONCEPT_PATH))
cols = len(VIEWS) + (1 if has_concept else 0)
header_h = 56
width = label_w + cols * (tile + pad) + pad
height = header_h + len(rows_meta) * (tile + pad) + pad

sheet = Image.new("RGBA", (width, height), (42, 44, 48, 255))
draw = ImageDraw.Draw(sheet)
draw.text(
    (20, 14),
    "Checkpoint B — Meshy Tries Comparison (Front | 3/4 | Side | Close-Up)",
    font=title_font,
    fill=(245, 247, 250, 255),
)

concept_tile = None
if has_concept:
    concept_tile = (
        Image.open(CONCEPT_PATH)
        .convert("RGBA")
        .resize((tile, tile), Image.Resampling.LANCZOS)
    )

for r_idx, (stem, label, faces) in enumerate(rows_meta):
    y = header_h + r_idx * (tile + pad)
    draw.text((20, y + tile // 2 - 28), label, font=label_font, fill=(255, 255, 255, 255))
    draw.text(
        (20, y + tile // 2 + 4),
        f"{faces:,} faces",
        font=label_font,
        fill=(180, 190, 205, 255),
    )
    col_offset = 0
    if concept_tile is not None:
        x = label_w + col_offset * (tile + pad)
        sheet.alpha_composite(concept_tile, (x, y))
        draw.text((x + 8, y + 8), "Concept", font=label_font, fill=(255, 255, 255, 255))
        col_offset += 1

    for view_name in ("front", "three-quarter", "side", "face"):
        x = label_w + col_offset * (tile + pad)
        vpath = os.path.join(RENDER_DIR, f"{stem}-{view_name}.png")
        vimg = (
            Image.open(vpath)
            .convert("RGBA")
            .resize((tile, tile), Image.Resampling.LANCZOS)
        )
        bg = Image.new("RGBA", (tile, tile), (64, 67, 74, 255))
        bg.alpha_composite(vimg)
        sheet.alpha_composite(bg, (x, y))
        draw.text((x + 8, y + 8), view_name, font=label_font, fill=(230, 235, 242, 255))
        col_offset += 1

os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
sheet.convert("RGB").save(OUT_SHEET, format="PNG")
print(f"Wrote {OUT_SHEET} ({sheet.width}x{sheet.height})")
"""
    payload = json.dumps(
        {
            "out_sheet": OUT_SHEET,
            "concept_path": CONCEPT_PATH,
            "render_dir": RENDER_DIR,
            "views": list(VIEWS.keys()),
            "rows_meta": rows_meta,
        }
    )
    proc = subprocess.run(["python", "-c", helper_code], input=payload, text=True, capture_output=True)
    if proc.returncode == 0:
        print(proc.stdout.strip())
        return

    # Fallback to bpy.data.images if system python PIL is unavailable
    tile = RENDER_SIZE
    cols = len(VIEWS)
    rows = max(len(rows_meta), 1)
    sheet_w = cols * tile
    sheet_h = rows * tile
    sheet_img = bpy.data.images.new("TriesSheet", width=sheet_w, height=sheet_h, alpha=True)
    pixels = [0.16, 0.17, 0.19, 1.0] * (sheet_w * sheet_h)
    view_names = ("front", "three-quarter", "side", "face")
    for r_idx, (stem, _label, _faces) in enumerate(rows_meta):
        dst_row = (rows - 1) - r_idx
        y_off = dst_row * tile
        for c_idx, vname in enumerate(view_names):
            x_off = c_idx * tile
            vpath = os.path.join(RENDER_DIR, f"{stem}-{vname}.png")
            t_img = bpy.data.images.load(vpath)
            t_px = list(t_img.pixels)
            for ty in range(tile):
                s0 = ty * tile * 4
                d0 = ((y_off + ty) * sheet_w + x_off) * 4
                pixels[d0 : d0 + tile * 4] = t_px[s0 : s0 + tile * 4]
            bpy.data.images.remove(t_img)
    os.makedirs(os.path.dirname(OUT_SHEET), exist_ok=True)
    sheet_img.pixels = pixels
    sheet_img.filepath_raw = OUT_SHEET
    sheet_img.file_format = "PNG"
    sheet_img.save()
    bpy.data.images.remove(sheet_img)
    print(f"Wrote {OUT_SHEET} ({sheet_w}x{sheet_h})")



scene = setup_scene()
os.makedirs(RENDER_DIR, exist_ok=True)
rows_info: list[tuple[str, str, int]] = []

for spec in TRY_SPECS:
    if "=" in spec:
        glb_path, label = spec.split("=", 1)
    else:
        glb_path = spec
        label = os.path.splitext(os.path.basename(spec))[0]
    glb_path = os.path.abspath(glb_path)
    stem = os.path.splitext(os.path.basename(glb_path))[0]
    pivot, parts, face_count = load_model(glb_path)
    for view, (turn, ortho_w, z_pos) in VIEWS.items():
        pivot.rotation_euler.z = math.radians(turn)
        scene.camera.data.ortho_scale = ortho_w
        scene.camera.location.z = z_pos
        bpy.context.view_layer.update()
        scene.render.filepath = os.path.join(RENDER_DIR, f"{stem}-{view}.png")
        bpy.ops.render.render(write_still=True)
    for o in parts + [pivot]:
        bpy.data.objects.remove(o, do_unlink=True)
    rows_info.append((stem, label, face_count))

build_sheet(rows_info)
