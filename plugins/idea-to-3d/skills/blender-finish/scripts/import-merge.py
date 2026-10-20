# Stage 4 headless Blender assembly script:
# Mode 1 (Meshy rigged + animated clips):
#   Imports the rigged GLB (or the multi-clip GLB from one meshy_animate action_ids call, whose
#   clips --bundle-clips names in file order) and each separate clip GLB, moves every action
#   onto the single armature named for the clip (idle, walk, wave, ...), removes duplicate meshes/armatures
#   and stray actions, welds UV-seam doubles, decimates if above budget, scales to real-world
#   height from idea.md/pipeline.json, grounds at the origin (Z=0 in Blender, Y=0 in glTF)
#   facing -Y (+Z in glTF), and saves work/<slug>/blender/<slug>.blend.
# Mode 2 (Unrigged mesh --procedural-rig):
#   Imports an unrigged mesh GLB, cleans/scales/grounds it, builds a simple hierarchical
#   armature (Root, Spine, Chest, Head, Arm.L, Arm.R), weights the mesh automatically with
#   guaranteed fallback weights, keys seamless 'idle' (breathing loop) plus requested clips,
#   and saves work/<slug>/blender/<slug>.blend.
# Mode 3 (Pure scripted robot build --scripted-robot):
#   Builds a polished hovering/standing spherical robot assistant with articulated arms and
#   antenna, procedural emissive/pearl materials, armature, and clips.
#
# Run:
#   "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --factory-startup --python-exit-code 1 -P import-merge.py -- --out <slug.blend> [--rigged <rigged.glb> [--bundle-clips idle,wave]] [--clip walk=<walk.glb> ...] [--mesh <mesh.glb> --procedural-rig] [--scripted-robot] [--height 1.7] [--max-triangles 40000] [--clips idle,wave]
import argparse
import json
import math
import os
import struct
import sys

import bmesh
import bpy
from mathutils import Matrix, Quaternion, Vector


def parse_args():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    parser = argparse.ArgumentParser(description="Import, merge clips, clean up, or rig in headless Blender")
    parser.add_argument("--out", required=True, help="Output .blend file path")
    parser.add_argument("--rigged", default="", help="Path to rigged base .glb")
    parser.add_argument(
        "--bundle-clips",
        default="",
        help="Comma-separated clip names for the --rigged GLB's animations, in file order (the meshy_animate action_ids order)",
    )
    parser.add_argument(
        "--clip",
        action="append",
        default=[],
        help="Clip mapping name=path.glb (may be specified multiple times)",
    )
    parser.add_argument("--mesh", default="", help="Path to unrigged mesh .glb (with --procedural-rig)")
    parser.add_argument("--procedural-rig", action="store_true", help="Build simple armature & clips in Blender")
    parser.add_argument("--scripted-robot", action="store_true", help="Build procedural robot mesh + rig in Blender")
    parser.add_argument("--height", type=float, default=1.7, help="Target real-world height in meters")
    parser.add_argument("--max-triangles", type=int, default=40_000, help="Maximum triangle budget")
    parser.add_argument("--clips", default="idle,wave", help="Comma-separated clips to generate for procedural rig")
    return parser.parse_args(argv)


def iter_action_fcurves(act):
    """Yield all F-Curves in a Blender Action (supports both legacy action.fcurves and Blender 5.0+ layered actions)."""
    if hasattr(act, "fcurves") and act.fcurves:
        for fc in act.fcurves:
            yield fc
    if hasattr(act, "layers"):
        for layer in act.layers:
            for strip in getattr(layer, "strips", []):
                if hasattr(strip, "channelbags"):
                    for bag in strip.channelbags:
                        for fc in getattr(bag, "fcurves", []):
                            yield fc
                elif hasattr(strip, "fcurves"):
                    for fc in strip.fcurves:
                        yield fc


def remove_action_fcurve(act, fc) -> None:
    if hasattr(act, "fcurves") and fc in list(act.fcurves):
        act.fcurves.remove(fc)
        return
    if hasattr(act, "layers"):
        for layer in act.layers:
            for strip in getattr(layer, "strips", []):
                for bag in getattr(strip, "channelbags", []):
                    if fc in list(getattr(bag, "fcurves", [])):
                        bag.fcurves.remove(fc)
                        return


def reset_pose(arm) -> None:
    if arm.animation_data:
        arm.animation_data.action = None
    for pb in arm.pose.bones:
        pb.location = (0.0, 0.0, 0.0)
        pb.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
        pb.rotation_euler = (0.0, 0.0, 0.0)
        pb.scale = (1.0, 1.0, 1.0)


def weld_and_budget_meshes(meshes: list, max_triangles: int) -> None:
    """Merge doubled vertices along UV seams and decimate if total triangles exceed budget."""
    for obj in meshes:
        if obj.type != "MESH":
            continue
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts[:], dist=1e-5)
        bm.to_mesh(obj.data)
        bm.free()
        obj.data.update()

    total_tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in meshes if o.type == "MESH")
    if total_tris > max_triangles:
        target_ratio = (max_triangles * 0.92) / total_tris
        for obj in meshes:
            if obj.type != "MESH" or len(obj.data.polygons) < 100:
                continue
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            mod = obj.modifiers.new("BudgetDecimate", "DECIMATE")
            mod.ratio = max(0.05, min(target_ratio, 1.0))
            bpy.ops.object.modifier_apply(modifier=mod.name)
            obj.select_set(False)


def normalize_rigged_transform(arm, meshes: list, target_height: float, actions: list) -> None:
    """Scale and ground the armature and meshes so the model stands at (0,0,0) at target_height
    with identity world matrices on both armature and meshes, scaling bone location F-curves to match."""
    reset_pose(arm)
    bpy.context.view_layer.update()

    # Temporarily unparent meshes while preserving world matrix so parent transforms don't double-apply
    arm_world = arm.matrix_world.copy()
    for obj in meshes:
        mesh_world = obj.matrix_world.copy()
        obj.parent = None
        obj.matrix_world = Matrix.Identity(4)
        obj.data.transform(mesh_world)
        obj.data.update()

    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for eb in arm.data.edit_bones:
        eb.transform(arm_world)
    bpy.ops.object.mode_set(mode="OBJECT")
    arm.parent = None
    arm.matrix_world = Matrix.Identity(4)
    bpy.context.view_layer.update()

    # Measure rest-pose world bounds of all meshes
    verts_world = [v.co.copy() for o in meshes for v in o.data.vertices]
    if not verts_world:
        raise RuntimeError("No vertices found in meshes")
    lo = Vector((min(v[i] for v in verts_world) for i in range(3)))
    hi = Vector((max(v[i] for v in verts_world) for i in range(3)))
    raw_h = max(hi.z - lo.z, 1e-4)
    scale_factor = target_height / raw_h

    mid_x = (lo.x + hi.x) * 0.5
    mid_y = (lo.y + hi.y) * 0.5
    min_z = lo.z

    # Transform: translate bottom-center to origin, then scale by scale_factor
    xform = Matrix.Scale(scale_factor, 4) @ Matrix.Translation((-mid_x, -mid_y, -min_z))

    for obj in meshes:
        obj.data.transform(xform)
        obj.data.update()

    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for eb in arm.data.edit_bones:
        eb.transform(xform)
    bpy.ops.object.mode_set(mode="OBJECT")

    # Re-parent meshes to armature with identity parent inverse
    for obj in meshes:
        obj.parent = arm
        obj.matrix_parent_inverse = Matrix.Identity(4)
        arm_mod = next((m for m in obj.modifiers if m.type == "ARMATURE"), None)
        if arm_mod is None:
            arm_mod = obj.modifiers.new("Armature", "ARMATURE")
        arm_mod.object = arm

    # Scale pose bone location F-Curves by scale_factor so animations match the new size
    arm_scale = arm_world.to_scale()
    avg_arm_scale = (abs(arm_scale.x) + abs(arm_scale.y) + abs(arm_scale.z)) / 3.0
    loc_mult = scale_factor * avg_arm_scale

    for act in actions:
        for fc in list(iter_action_fcurves(act)):
            dp = fc.data_path or ""
            # Strip any non-pose-bone channels (e.g. object transforms or shape keys)
            if not dp.startswith("pose.bones["):
                remove_action_fcurve(act, fc)
                continue
            if dp.endswith(".location"):
                for kp in fc.keyframe_points:
                    kp.co.y *= loc_mult
                    kp.handle_left.y *= loc_mult
                    kp.handle_right.y *= loc_mult
                fc.update()

    reset_pose(arm)
    bpy.context.view_layer.update()


def extract_actions_from_import(before_objs: set, before_acts: set):
    new_objs = [o for o in bpy.data.objects if o not in before_objs]
    new_acts = [a for a in bpy.data.actions if a not in before_acts]
    for o in new_objs:
        if o.animation_data and o.animation_data.action and o.animation_data.action not in new_acts:
            new_acts.append(o.animation_data.action)
    return new_objs, new_acts


def glb_animation_names(path: str) -> list[str]:
    """Read the glTF animation names, in file order, from a .glb's JSON chunk."""
    with open(path, "rb") as f:
        data = f.read()
    if len(data) < 20 or data[:4] != b"glTF":
        raise ValueError(f"Not a GLB file: {path}")
    chunk_len = struct.unpack_from("<I", data, 12)[0]
    gltf = json.loads(data[20 : 20 + chunk_len].decode("utf-8"))
    return [a.get("name", "") for a in gltf.get("animations", [])]


def name_bundle_clips(rigged_path: str, base_acts: list, clip_names: list[str]) -> dict:
    """Map each animation of a multi-clip GLB to its clip name, in file order."""
    anim_names = glb_animation_names(rigged_path)
    if len(anim_names) != len(clip_names):
        raise RuntimeError(
            f"--bundle-clips names {len(clip_names)} clips but {rigged_path} has "
            f"{len(anim_names)} animations: {anim_names}"
        )
    if len(set(clip_names)) != len(clip_names):
        raise ValueError(f"--bundle-clips has duplicate names: {clip_names}")
    # Blender 5.2 names each imported action exactly after its glTF animation.
    by_name = {a.name: a for a in base_acts}
    missing = [n for n in anim_names if n not in by_name]
    if missing:
        raise RuntimeError(
            f"No imported action for animations {missing} in {rigged_path}; actions: {sorted(by_name)}"
        )
    picked = [by_name[n] for n in anim_names]
    # Rename in two passes so swapped names (idle <-> wave) never collide into ".001".
    for i, act in enumerate(picked):
        act.name = f"__bundle_clip_{i}"
    clips = {}
    for clip_name, act in zip(clip_names, picked):
        act.name = clip_name
        act.use_fake_user = True
        clips[clip_name] = act
    return clips


def assign_action_to_armature(arm, act) -> None:
    arm.animation_data_create()
    arm.animation_data.action = act
    if hasattr(act, "slots") and act.slots:
        arm.animation_data.action_slot = act.slots[0]


def strip_bone_custom_shapes_and_helpers(objs: list) -> list:
    """Clear glTF bone custom_shape widgets (e.g. Icosphere) and return only real character meshes."""
    custom_shapes = set()
    for o in objs:
        if o.type == "ARMATURE":
            for pb in o.pose.bones:
                if pb.custom_shape is not None:
                    custom_shapes.add(pb.custom_shape)
                    pb.custom_shape = None
    real_meshes = [
        o
        for o in objs
        if o.type == "MESH"
        and o not in custom_shapes
        and not o.name.startswith("Icosphere")
    ]
    return real_meshes


def run_meshy_merge(args) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if not os.path.exists(args.rigged):
        raise FileNotFoundError(f"Rigged GLB not found: {args.rigged}")

    before_objs = set(bpy.data.objects)
    before_acts = set(bpy.data.actions)
    bpy.ops.import_scene.gltf(filepath=os.path.abspath(args.rigged))
    base_objs, base_acts = extract_actions_from_import(before_objs, before_acts)

    arms = [o for o in base_objs if o.type == "ARMATURE"]
    meshes = strip_bone_custom_shapes_and_helpers(base_objs)
    if not arms or not meshes:
        raise RuntimeError(f"Expected armature and mesh in {args.rigged}, found {len(arms)} armatures, {len(meshes)} meshes")

    main_arm = arms[0]
    main_arm.name = "Armature"

    for o in list(base_objs):
        if o not in [main_arm] + meshes:
            bpy.data.objects.remove(o, do_unlink=True)

    bundle_names = [c.strip() for c in args.bundle_clips.split(",") if c.strip()]
    wanted_clips: dict[str, bpy.types.Action] = (
        name_bundle_clips(args.rigged, base_acts, bundle_names) if bundle_names else {}
    )

    # Import each separate clip GLB and transfer its action onto main_arm;
    # a clip name already in the bundle replaces that bundle clip.
    for clip_spec in args.clip:
        if "=" not in clip_spec:
            raise ValueError(f"Invalid --clip spec '{clip_spec}', expected name=path.glb")
        clip_name, clip_path = clip_spec.split("=", 1)
        clip_name = clip_name.strip()
        clip_path = os.path.abspath(clip_path.strip())
        if not os.path.exists(clip_path):
            raise FileNotFoundError(f"Clip GLB not found: {clip_path}")

        b_objs = set(bpy.data.objects)
        b_acts = set(bpy.data.actions)
        bpy.ops.import_scene.gltf(filepath=clip_path)
        imp_objs, imp_acts = extract_actions_from_import(b_objs, b_acts)
        strip_bone_custom_shapes_and_helpers(imp_objs)

        if not imp_acts:
            raise RuntimeError(f"No animation action found in {clip_path}")
        chosen_act = imp_acts[0]

        for extra_act in imp_acts[1:]:
            bpy.data.actions.remove(extra_act)
        for obj in list(imp_objs):
            bpy.data.objects.remove(obj, do_unlink=True)

        # Remove any orphaned helper meshes left in bpy.data.objects
        for obj in list(bpy.data.objects):
            if obj not in [main_arm] + meshes:
                bpy.data.objects.remove(obj, do_unlink=True)

        # If an action already has clip_name, rename or remove it first
        existing = bpy.data.actions.get(clip_name)
        if existing and existing != chosen_act:
            bpy.data.actions.remove(existing)
        chosen_act.name = clip_name
        chosen_act.use_fake_user = True
        wanted_clips[clip_name] = chosen_act

    # If no external --clip was given and base_acts has actions, rename first to 'idle'
    if not wanted_clips and base_acts:
        act = base_acts[0]
        act.name = "idle"
        act.use_fake_user = True
        wanted_clips["idle"] = act

    # Remove all stray actions not in wanted_clips
    for act in list(bpy.data.actions):
        if act not in wanted_clips.values():
            bpy.data.actions.remove(act)

    weld_and_budget_meshes(meshes, args.max_triangles)
    normalize_rigged_transform(main_arm, meshes, args.height, list(wanted_clips.values()))

    # Ensure each action is bound to main_arm at least once so Blender 5.2 action slots match main_arm
    for act in wanted_clips.values():
        assign_action_to_armature(main_arm, act)
    reset_pose(main_arm)


def key_pose_clip(arm, name: str, frames: int, step: int, pose_fn) -> bpy.types.Action:
    old = bpy.data.actions.get(name)
    if old:
        bpy.data.actions.remove(old)
    act = bpy.data.actions.new(name)
    act.use_fake_user = True
    arm.animation_data_create()
    arm.animation_data.action = act
    if hasattr(act, "slots") and act.slots:
        arm.animation_data.action_slot = act.slots[0]

    X, Y, Z = Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    for frame in range(0, frames + 1, step):
        t = frame / frames
        bones_pose = pose_fn(t, X, Y, Z)
        for bname, p in bones_pose.items():
            if bname not in arm.pose.bones:
                continue
            pb = arm.pose.bones[bname]
            rest = arm.data.bones[bname].matrix_local.to_3x3()
            back = rest.inverted()
            if "rot" in p:
                q = Quaternion()
                for axis, deg in p["rot"]:
                    q = Quaternion(axis, math.radians(deg)) @ q
                pb.rotation_quaternion = (back @ q.to_matrix() @ rest).to_quaternion()
                pb.keyframe_insert("rotation_quaternion", frame=frame)
            if "loc" in p:
                pb.location = back @ Vector(p["loc"])
                pb.keyframe_insert("location", frame=frame)
            if "scale" in p:
                pb.scale = (p["scale"],) * 3
                pb.keyframe_insert("scale", frame=frame)

    act.frame_range = (0, frames)
    reset_pose(arm)
    return act


def build_procedural_rig_and_clips(meshes: list, target_height: float, clip_names: list[str]):
    # Merge meshes into a single clean mesh if multiple parts exist
    bpy.ops.object.select_all(action="DESELECT")
    for o in meshes:
        w = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = w
        o.data.transform(w)
        o.matrix_world = Matrix.Identity(4)

    if len(meshes) > 1:
        for o in meshes:
            o.select_set(True)
        bpy.context.view_layer.objects.active = meshes[0]
        bpy.ops.object.join()
        meshes = [bpy.context.view_layer.objects.active]

    mesh_obj = meshes[0]
    mesh_obj.name = "Body"

    verts = [v.co.copy() for v in mesh_obj.data.vertices]
    lo = Vector((min(v[i] for v in verts) for i in range(3)))
    hi = Vector((max(v[i] for v in verts) for i in range(3)))
    raw_h = max(hi.z - lo.z, 1e-4)
    scale_f = target_height / raw_h
    mid_x = (lo.x + hi.x) * 0.5
    mid_y = (lo.y + hi.y) * 0.5
    min_z = lo.z

    xform = Matrix.Scale(scale_f, 4) @ Matrix.Translation((-mid_x, -mid_y, -min_z))
    mesh_obj.data.transform(xform)
    mesh_obj.data.update()

    verts2 = [v.co.copy() for v in mesh_obj.data.vertices]
    lo2 = Vector((min(v[i] for v in verts2) for i in range(3)))
    hi2 = Vector((max(v[i] for v in verts2) for i in range(3)))
    width_x = max(hi2.x - lo2.x, target_height * 0.3)
    H = target_height

    arm_data = bpy.data.armatures.new("Armature")
    arm = bpy.data.objects.new("Armature", arm_data)
    bpy.context.collection.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    ebones = arm_data.edit_bones

    def add_bone(name, head, tail, parent=None):
        b = ebones.new(name)
        b.head = Vector(head)
        b.tail = Vector(tail)
        if parent:
            b.parent = ebones[parent]
        b.use_connect = False
        return b

    add_bone("Root", (0, 0, 0), (0, 0, 0.15 * H))
    add_bone("Spine", (0, 0, 0.15 * H), (0, 0, 0.45 * H), "Root")
    add_bone("Chest", (0, 0, 0.45 * H), (0, 0, 0.72 * H), "Spine")
    add_bone("Head", (0, 0, 0.72 * H), (0, 0, 0.96 * H), "Chest")
    add_bone("Arm.L", (0.37 * width_x, 0, 0.50 * H), (0.48 * width_x, 0, 0.22 * H), "Chest")
    add_bone("Arm.R", (-0.37 * width_x, 0, 0.50 * H), (-0.48 * width_x, 0, 0.22 * H), "Chest")
    bpy.ops.object.mode_set(mode="OBJECT")

    # Assign smooth height & lateral weights deterministically so non-humanoid meshes never tear
    mesh_obj.vertex_groups.clear()
    bone_names = ("Root", "Spine", "Chest", "Head", "Arm.L", "Arm.R")
    vgroups = {bn: mesh_obj.vertex_groups.new(name=bn) for bn in bone_names}
    centers = {
        "Spine": 0.28 * H,
        "Chest": 0.55 * H,
        "Head": 0.85 * H,
    }
    for v in mesh_obj.data.vertices:
        z = v.co.z
        x = v.co.x
        if abs(x) > 0.37 * width_x and 0.10 * H <= z <= 0.54 * H:
            arm_tag = "Arm.L" if x > 0 else "Arm.R"
            raw_t = min(1.0, (abs(x) - 0.37 * width_x) / max(0.09 * width_x, 1e-4))
            # Smoothstep falloff to prevent any crease on the shell
            arm_w = raw_t * raw_t * (3.0 - 2.0 * raw_t) * 0.85
            vgroups[arm_tag].add([v.index], arm_w, "REPLACE")
            vgroups["Chest"].add([v.index], 1.0 - arm_w, "REPLACE")
        else:
            raw_w = {
                bn: max(0.05, 1.0 - abs(z - cz) / (0.65 * H))
                for bn, cz in centers.items()
            }
            tot = sum(raw_w.values())
            for bn, w in raw_w.items():
                vgroups[bn].add([v.index], w / tot, "REPLACE")

    mesh_obj.parent = arm
    mod = mesh_obj.modifiers.new("Armature", "ARMATURE")
    mod.object = arm

    # Remove any old actions
    for act in list(bpy.data.actions):
        bpy.data.actions.remove(act)

    bpy.context.scene.render.fps = 30
    s = lambda t, n=1, phase=0.0: math.sin(2 * math.pi * n * t + phase)

    if "idle" not in clip_names:
        clip_names = ["idle"] + clip_names

    for cname in clip_names:
        if cname == "idle":
            key_pose_clip(
                arm,
                "idle",
                120,
                4,
                lambda t, X, Y, Z: {
                    "Spine": {"loc": (0, 0, 0.025 * H * s(t, 2))},
                    "Chest": {"rot": [(X, 2.5 * s(t, 2, -0.4)), (Z, 4.0 * s(t, 1))]},
                    "Head": {"rot": [(Z, 3.0 * s(t, 1)), (Y, 2.0 * s(t, 1, 1.2))]},
                    "Arm.L": {"rot": [(X, 6.0 * s(t, 2))]},
                    "Arm.R": {"rot": [(X, -6.0 * s(t, 2))]},
                },
            )
        elif cname == "wave":
            key_pose_clip(
                arm,
                "wave",
                72,
                4,
                lambda t, X, Y, Z: {
                    "Spine": {
                        "loc": (0, 0, 0.035 * H * math.sin(math.pi * t)),
                        "rot": [(Y, -6.0 * math.sin(math.pi * t)), (Z, 8.0 * s(t, 1) * math.sin(math.pi * t))],
                    },
                    "Chest": {"rot": [(Y, -5.0 * math.sin(math.pi * t)), (X, -4.0 * math.sin(math.pi * t))]},
                    "Head": {"rot": [(Y, -4.0 * math.sin(math.pi * t)), (Z, 6.0 * s(t, 2) * math.sin(math.pi * t))]},
                    "Arm.R": {
                        "rot": [
                            (X, -24.0 * math.sin(math.pi * t)),
                            (Y, 16.0 * math.sin(math.pi * t) + 10.0 * s(t, 3) * math.sin(math.pi * t)),
                        ]
                    },
                    "Arm.L": {"rot": [(X, 8.0 * math.sin(math.pi * t))]},
                },
            )
        elif cname in ("walk", "run"):
            freq = 2 if cname == "run" else 1
            key_pose_clip(
                arm,
                cname,
                60,
                3,
                lambda t, X, Y, Z, f=freq: {
                    "Spine": {"loc": (0, 0, 0.03 * H * abs(s(t, f * 2))), "rot": [(Z, 6.0 * s(t, f))]},
                    "Chest": {"rot": [(X, 5.0 + 3.0 * s(t, f * 2))]},
                    "Head": {"rot": [(Z, -4.0 * s(t, f))]},
                    "Arm.L": {"rot": [(X, 18.0 * s(t, f))]},
                    "Arm.R": {"rot": [(X, -18.0 * s(t, f))]},
                },
            )
        else:
            # Generic expressive action (bounce / cheer / nod / spin)
            key_pose_clip(
                arm,
                cname,
                60,
                3,
                lambda t, X, Y, Z: {
                    "Spine": {
                        "loc": (0, 0, 0.08 * H * math.sin(math.pi * t) * abs(s(t, 2))),
                        "rot": [(Z, 14.0 * s(t, 1) * math.sin(math.pi * t))],
                    },
                    "Chest": {"rot": [(X, -7.0 * math.sin(math.pi * t)), (Y, 5.0 * s(t, 2) * math.sin(math.pi * t))]},
                    "Head": {"rot": [(Z, 6.0 * s(t, 1) * math.sin(math.pi * t)), (X, -5.0 * math.sin(math.pi * t))]},
                    "Arm.L": {"rot": [(X, -22.0 * math.sin(math.pi * t)), (Y, -12.0 * math.sin(math.pi * t))]},
                    "Arm.R": {"rot": [(X, -22.0 * math.sin(math.pi * t)), (Y, 12.0 * math.sin(math.pi * t))]},
                },
            )


def build_scripted_robot_mesh() -> list:
    """Create a clean textured spherical robot character mesh in Blender for --scripted-robot."""
    bpy.ops.wm.read_factory_settings(use_empty=True)
    # Create a 256x256 palette texture image so the GLB has a valid WebP texture map
    img = bpy.data.images.new("RobotPalette", 256, 256, alpha=False)
    px = []
    for y in range(256):
        for x in range(256):
            if y < 128 and x < 128:
                px.extend((0.95, 0.96, 0.98, 1.0))  # Pearl shell
            elif y < 128:
                px.extend((0.26, 0.52, 0.96, 1.0))  # Gemini blue accent
            elif x < 128:
                px.extend((0.03, 0.04, 0.07, 1.0))  # Dark visor screen
            else:
                px.extend((0.35, 0.92, 1.0, 1.0))  # Cyan glow eyes
    img.pixels = px
    img.pack()

    mat = bpy.data.materials.new("RobotMaterial")
    if not mat.node_tree:
        mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = next(n for n in nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Roughness"].default_value = 0.28
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = img
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(bm, u_segments=32, v_segments=24, radius=0.42)
    for v in bm.verts:
        v.co.z += 0.50

    # Add two stubby side arms and a top antenna
    for side in (-1.0, 1.0):
        ret = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=12, radius=0.11)
        for v in ret["verts"]:
            v.co.x = v.co.x * 0.8 + side * 0.48
            v.co.z = v.co.z * 1.4 + 0.46

    ret_ant = bmesh.ops.create_uvsphere(bm, u_segments=14, v_segments=10, radius=0.07)
    for v in ret_ant["verts"]:
        v.co.z += 0.98

    me = bpy.data.meshes.new("RobotBody")
    bm.to_mesh(me)
    bm.free()
    me.materials.append(mat)
    for p in me.polygons:
        p.use_smooth = True

    uv_layer = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        c = poly.center
        if c.z > 0.90 or (c.y < -0.35 and 0.42 <= c.z <= 0.58 and abs(c.x) < 0.22):
            u, v_coord = (0.75, 0.75) if abs(c.x) > 0.06 or c.z > 0.90 else (0.25, 0.75)
        elif abs(c.x) > 0.36:
            u, v_coord = (0.75, 0.25)
        else:
            u, v_coord = (0.25, 0.25)
        for li in poly.loop_indices:
            uv_layer.data[li].uv = (u, v_coord)

    obj = bpy.data.objects.new("RobotBody", me)
    bpy.context.collection.objects.link(obj)
    return [obj]


def main() -> None:
    args = parse_args()
    clip_list = [c.strip() for c in args.clips.split(",") if c.strip()]

    if args.scripted_robot:
        meshes = build_scripted_robot_mesh()
        weld_and_budget_meshes(meshes, args.max_triangles)
        build_procedural_rig_and_clips(meshes, args.height, clip_list)
    elif args.procedural_rig:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        if not args.mesh or not os.path.exists(args.mesh):
            raise FileNotFoundError(f"Mesh GLB not found for --procedural-rig: {args.mesh}")
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.abspath(args.mesh))
        imp = [o for o in bpy.data.objects if o not in before]
        meshes = [o for o in imp if o.type == "MESH"]
        if not meshes:
            raise RuntimeError(f"No mesh objects in {args.mesh}")
        for o in imp:
            if o not in meshes:
                bpy.data.objects.remove(o, do_unlink=True)
        weld_and_budget_meshes(meshes, args.max_triangles)
        build_procedural_rig_and_clips(meshes, args.height, clip_list)
    else:
        run_meshy_merge(args)

    # Remove any cameras or lights before saving .blend
    for o in list(bpy.data.objects):
        if o.type in ("CAMERA", "LIGHT"):
            bpy.data.objects.remove(o, do_unlink=True)

    out_blend = os.path.abspath(args.out)
    os.makedirs(os.path.dirname(out_blend), exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=out_blend)
    print(f"Wrote {out_blend}")


if __name__ == "__main__":
    main()
