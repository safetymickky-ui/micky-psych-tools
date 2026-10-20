#!/usr/bin/env python3
"""
Checks an exported .glb file against all §6 requirements of the idea-to-3d handoff
without needing Blender:
- File size <= 8 MB (or max_bytes in pipeline.json)
- Triangle count <= triangle_budget in pipeline.json (default 40,000)
- Has a skin (skeleton joints)
- Expected animation clips exist, spelled exactly, no .001 suffixes, at least 'idle' + 1 clip
- Every animation channel targets only skin joints (never shape key weights or non-joint nodes)
- Every embedded image is image/webp or image/png
- No cameras or KHR_lights_punctual lights
- Model is standing on the ground (minimum Y ~ 0 in glTF +Y up) and height matches idea.md / pipeline.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import struct
import sys
from typing import Any

DEFAULT_MAX_TRIANGLES = 40_000
DEFAULT_MAX_BYTES = 8 * 1024 * 1024


def read_glb(path: str) -> tuple[dict[str, Any], bytes, int]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"GLB file not found: {path}")
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 20:
        raise ValueError(f"{path} is too small ({len(data)} bytes) to be a valid GLB")
    magic, version, total_len = struct.unpack_from("<4sII", data, 0)
    if magic != b"glTF":
        raise ValueError(f"{path} is not a GLB file (magic={magic!r})")
    json_len, json_type = struct.unpack_from("<I4s", data, 12)
    if json_type != b"JSON":
        raise ValueError(f"{path} first chunk is not JSON")
    gltf = json.loads(data[20 : 20 + json_len].decode("utf-8"))
    bin_chunk = b""
    offset = 20 + json_len
    if offset + 8 <= len(data):
        bin_len, bin_type = struct.unpack_from("<I4s", data, offset)
        if bin_type[:3] == b"BIN":
            bin_chunk = data[offset + 8 : offset + 8 + bin_len]
    return gltf, bin_chunk, len(data)


def mat4_identity() -> list[list[float]]:
    return [
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]


def mat4_mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    out = [[0.0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            out[i][j] = sum(a[i][k] * b[k][j] for k in range(4))
    return out


def mat4_from_node(node: dict[str, Any]) -> list[list[float]]:
    if "matrix" in node:
        m = node["matrix"]
        # glTF matrices are column-major
        return [
            [float(m[0]), float(m[4]), float(m[8]), float(m[12])],
            [float(m[1]), float(m[5]), float(m[9]), float(m[13])],
            [float(m[2]), float(m[6]), float(m[10]), float(m[14])],
            [float(m[3]), float(m[7]), float(m[11]), float(m[15])],
        ]
    tx, ty, tz = node.get("translation", [0.0, 0.0, 0.0])
    qx, qy, qz, qw = node.get("rotation", [0.0, 0.0, 0.0, 1.0])
    sx, sy, sz = node.get("scale", [1.0, 1.0, 1.0])

    x2, y2, z2 = qx + qx, qy + qy, qz + qz
    xx, xy, xz = qx * x2, qx * y2, qx * z2
    yy, yz, zz = qy * y2, qy * z2, qz * z2
    wx, wy, wz = qw * x2, qw * y2, qw * z2

    return [
        [(1.0 - (yy + zz)) * sx, (xy - wz) * sy, (xz + wy) * sz, float(tx)],
        [(xy + wz) * sx, (1.0 - (xx + zz)) * sy, (yz - wx) * sz, float(ty)],
        [(xz - wy) * sx, (yz + wx) * sy, (1.0 - (xx + yy)) * sz, float(tz)],
        [0.0, 0.0, 0.0, 1.0],
    ]


def transform_point(m: list[list[float]], p: tuple[float, float, float]) -> tuple[float, float, float]:
    x, y, z = p
    return (
        m[0][0] * x + m[0][1] * y + m[0][2] * z + m[0][3],
        m[1][0] * x + m[1][1] * y + m[1][2] * z + m[1][3],
        m[2][0] * x + m[2][1] * y + m[2][2] * z + m[2][3],
    )


def compute_scene_bounds(gltf: dict[str, Any]) -> tuple[tuple[float, float, float], tuple[float, float, float]] | None:
    nodes = gltf.get("nodes", [])
    meshes = gltf.get("meshes", [])
    accessors = gltf.get("accessors", [])
    if not nodes or not meshes or not accessors:
        return None

    parent_map: dict[int, int] = {}
    for idx, nd in enumerate(nodes):
        for ch in nd.get("children", []):
            parent_map[ch] = idx

    world_mats: dict[int, list[list[float]]] = {}

    def get_world_mat(n_idx: int) -> list[list[float]]:
        if n_idx in world_mats:
            return world_mats[n_idx]
        local = mat4_from_node(nodes[n_idx])
        if n_idx in parent_map:
            wm = mat4_mul(get_world_mat(parent_map[n_idx]), local)
        else:
            wm = local
        world_mats[n_idx] = wm
        return wm

    min_pt = [float("inf"), float("inf"), float("inf")]
    max_pt = [float("-inf"), float("-inf"), float("-inf")]
    found = False

    for n_idx, nd in enumerate(nodes):
        if "mesh" not in nd:
            continue
        mesh = meshes[nd["mesh"]]
        wm = get_world_mat(n_idx)
        for prim in mesh.get("primitives", []):
            pos_idx = prim.get("attributes", {}).get("POSITION")
            if pos_idx is None or pos_idx >= len(accessors):
                continue
            acc = accessors[pos_idx]
            amin = acc.get("min")
            amax = acc.get("max")
            if not amin or not amax or len(amin) < 3 or len(amax) < 3:
                continue
            for cx in (amin[0], amax[0]):
                for cy in (amin[1], amax[1]):
                    for cz in (amin[2], amax[2]):
                        wx, wy, wz = transform_point(wm, (float(cx), float(cy), float(cz)))
                        min_pt[0] = min(min_pt[0], wx)
                        min_pt[1] = min(min_pt[1], wy)
                        min_pt[2] = min(min_pt[2], wz)
                        max_pt[0] = max(max_pt[0], wx)
                        max_pt[1] = max(max_pt[1], wy)
                        max_pt[2] = max(max_pt[2], wz)
                        found = True

    if not found:
        return None
    return (min_pt[0], min_pt[1], min_pt[2]), (max_pt[0], max_pt[1], max_pt[2])


def parse_height_from_idea(idea_md_path: str) -> float | None:
    if not idea_md_path or not os.path.exists(idea_md_path):
        return None
    with open(idea_md_path, "r", encoding="utf-8") as f:
        text = f.read()
    m_meter = re.search(
        r"(?:height|tall|size)\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(?:m|meters?|metres?)\b",
        text,
        re.IGNORECASE,
    )
    if m_meter:
        return float(m_meter.group(1))
    m_cm = re.search(
        r"(?:height|tall|size)\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(?:cm|centimeters?|centimetres?)\b",
        text,
        re.IGNORECASE,
    )
    if m_cm:
        return float(m_cm.group(1)) / 100.0
    return None


def check_glb(
    glb_path: str,
    expected_clips: list[str] | None = None,
    target_height_m: float | None = None,
    triangle_budget: int = DEFAULT_MAX_TRIANGLES,
    max_bytes: int = DEFAULT_MAX_BYTES,
    allow_single_clip: bool = False,
) -> tuple[bool, list[str], dict[str, Any]]:
    gltf, _, size = read_glb(glb_path)
    problems: list[str] = []

    triangles = 0
    accessors = gltf.get("accessors", [])
    for mesh in gltf.get("meshes", []):
        names = (mesh.get("extras") or {}).get("targetNames", [])
        for prim in mesh.get("primitives", []):
            targets = prim.get("targets", [])
            if targets and names and len(targets) != len(names):
                problems.append(
                    f"mesh {mesh.get('name', '?')}: {len(names)} targetNames for {len(targets)} morph targets"
                )
            if prim.get("mode", 4) != 4:
                continue
            if "indices" in prim:
                triangles += accessors[prim["indices"]]["count"] // 3
            elif "POSITION" in prim.get("attributes", {}):
                triangles += accessors[prim["attributes"]["POSITION"]]["count"] // 3

    nodes = gltf.get("nodes", [])
    skins = gltf.get("skins", [])
    joint_ids = {j for skin in skins for j in skin.get("joints", [])}
    clips = {a.get("name", ""): a for a in gltf.get("animations", [])}

    if size > max_bytes:
        problems.append(f"file size {size / 1048576:.2f} MB exceeds {max_bytes / 1048576:.1f} MB limit")
    if triangles > triangle_budget:
        problems.append(f"{triangles} triangles exceeds budget of {triangle_budget}")
    if triangles == 0:
        problems.append("model contains 0 triangles")

    if not skins or not joint_ids:
        problems.append("no skin: model must be rigged with a skeleton skin")

    if gltf.get("cameras") or any("camera" in n for n in nodes):
        problems.append("file contains a camera")
    if "KHR_lights_punctual" in gltf.get("extensionsUsed", []):
        problems.append("file contains punctual lights (KHR_lights_punctual)")

    for img in gltf.get("images", []):
        mime = img.get("mimeType", "")
        if mime not in ("image/webp", "image/png"):
            problems.append(
                f"image {img.get('name', '?')} has mimeType '{mime or img.get('uri', '?')}', expected image/webp or image/png"
            )

    if not clips:
        problems.append("file has no animation clips")
    else:
        if "idle" not in clips:
            problems.append("missing required clip 'idle'")
        if not allow_single_clip and len(clips) < 2:
            problems.append("expected at least 'idle' and one more animation clip")

    if expected_clips:
        for req_clip in expected_clips:
            if req_clip not in clips:
                problems.append(f"missing expected clip '{req_clip}'")
        for actual_clip in clips:
            if actual_clip not in expected_clips:
                suffix_match = re.search(r"\.\d{3}$", actual_clip)
                problems.append(
                    f"unexpected clip '{actual_clip}'"
                    + (" (has .NNN duplicate suffix)" if suffix_match else "")
                )
    else:
        for actual_clip in clips:
            if not actual_clip or re.search(r"\.\d{3}$", actual_clip):
                problems.append(f"invalid or duplicate-suffixed clip name '{actual_clip}'")

    for name, anim in clips.items():
        channels = anim.get("channels", [])
        if not channels:
            problems.append(f"clip '{name}' has no animation channels")
        for ch in channels:
            target = ch.get("target", {})
            if target.get("path") == "weights":
                problems.append(f"clip '{name}' animates morph target weights (only skin joints allowed)")
            if target.get("node") not in joint_ids:
                problems.append(
                    f"clip '{name}' animates node {target.get('node')} which is not a skin joint"
                )

    bounds = compute_scene_bounds(gltf)
    min_y = None
    height = None
    if bounds is None:
        problems.append("could not compute mesh bounding box from POSITION accessors")
    else:
        bmin, bmax = bounds
        min_y = bmin[1]
        height = bmax[1] - bmin[1]
        tol_ground = max(0.03, (target_height_m or height or 1.0) * 0.05)
        if abs(min_y) > tol_ground:
            problems.append(
                f"model is not standing on the ground: minimum Y is {min_y:.4f} (expected ~0.0 within ±{tol_ground:.3f})"
            )
        if target_height_m is not None and target_height_m > 0:
            tol_h = max(0.03, target_height_m * 0.15)
            if abs(height - target_height_m) > tol_h:
                problems.append(
                    f"model height {height:.3f} m is far from target height {target_height_m:.3f} m (±{tol_h:.3f} m)"
                )

    summary = {
        "file": os.path.basename(glb_path),
        "bytes": size,
        "megabytes": round(size / 1048576, 3),
        "triangles": triangles,
        "bones": len(joint_ids),
        "clips": list(clips.keys()),
        "min_y": round(min_y, 4) if min_y is not None else None,
        "height_m": round(height, 4) if height is not None else None,
    }
    return len(problems) == 0, problems, summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a finished .glb against §6 rules")
    parser.add_argument("glb", help="Path to .glb file")
    parser.add_argument("--pipeline", default="", help="Optional path to work/<slug>/pipeline.json")
    parser.add_argument("--idea", default="", help="Optional path to work/<slug>/idea.md")
    parser.add_argument("--clips", default="", help="Comma-separated expected clip names")
    parser.add_argument("--height", type=float, default=None, help="Target height in meters")
    parser.add_argument("--max-triangles", type=int, default=None, help="Triangle budget")
    parser.add_argument("--max-bytes", type=int, default=None, help="Max file size in bytes")
    parser.add_argument(
        "--allow-single-clip",
        action="store_true",
        help="Allow a single clip (e.g. for §8.2 tracer bullet run)",
    )
    args = parser.parse_args(argv)

    expected_clips: list[str] | None = None
    target_height: float | None = args.height
    tri_budget = DEFAULT_MAX_TRIANGLES
    max_bytes = DEFAULT_MAX_BYTES

    # Auto-discover pipeline.json and idea.md if glb is in work/<slug>/out/<slug>.glb
    glb_abs = os.path.abspath(args.glb)
    parent_dir = os.path.dirname(glb_abs)
    slug_dir = os.path.dirname(parent_dir) if os.path.basename(parent_dir) in ("out", "meshy", "blender") else parent_dir

    pipeline_path = args.pipeline or os.path.join(slug_dir, "pipeline.json")
    idea_path = args.idea or os.path.join(slug_dir, "idea.md")

    if os.path.exists(pipeline_path):
        with open(pipeline_path, "r", encoding="utf-8") as f:
            pdata = json.load(f)
        if expected_clips is None and pdata.get("expected_clips"):
            expected_clips = list(pdata["expected_clips"])
        if target_height is None and pdata.get("target_height_m"):
            target_height = float(pdata["target_height_m"])
        if pdata.get("triangle_budget"):
            tri_budget = int(pdata["triangle_budget"])
        if pdata.get("max_bytes"):
            max_bytes = int(pdata["max_bytes"])

    if target_height is None and os.path.exists(idea_path):
        target_height = parse_height_from_idea(idea_path)

    if args.clips:
        expected_clips = [c.strip() for c in args.clips.split(",") if c.strip()]
    if args.max_triangles is not None:
        tri_budget = args.max_triangles
    if args.max_bytes is not None:
        max_bytes = args.max_bytes

    ok, problems, summary = check_glb(
        glb_path=glb_abs,
        expected_clips=expected_clips,
        target_height_m=target_height,
        triangle_budget=tri_budget,
        max_bytes=max_bytes,
        allow_single_clip=args.allow_single_clip,
    )

    print(
        f"{summary['file']}: {summary['megabytes']:.2f} MB, {summary['triangles']} triangles, "
        f"{summary['bones']} bones, min_y={summary['min_y']}, height={summary['height_m']}m, "
        f"clips={summary['clips']}"
    )
    if not ok:
        for p in problems:
            print(f"  FAIL: {p}")
        return 1
    print("  OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
