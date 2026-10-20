#!/usr/bin/env python3
"""
Deterministic state manager for work/<slug>/pipeline.json.
Ensures atomic writes, idempotent Meshy task tracking (preventing duplicate credit charges),
and resumable checkpoint persistence across conversations.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from typing import Any

VALID_STAGES = ("concept-art", "image-to-3d", "rig-animate", "blender-finish", "done")
VALID_CHECKPOINTS = ("A", "B", "C")
VALID_GATES = ("A1", "A2", "B", "C")
VALID_CRITICS = ("gemini", "claude")
SUBDIRS = ("images", "meshy", "blender", "out", "preview", "reviews")
DEFAULT_TRIANGLE_BUDGET = 40_000
DEFAULT_MAX_BYTES = 8 * 1024 * 1024


def sanitize_slug(raw: str) -> str:
    """Convert an arbitrary string or slug into a safe lowercase kebab-case slug."""
    if not raw or not isinstance(raw, str):
        raise ValueError("Slug must be a non-empty string")
    cleaned = re.sub(r"[^a-z0-9]+", "-", raw.strip().lower()).strip("-")
    if not cleaned:
        raise ValueError(f"Slug '{raw}' contains no alphanumeric characters")
    return cleaned[:64].strip("-")


def parse_height_from_idea_md(idea_md_path: str) -> float | None:
    """Extract target real-world height in meters from idea.md if present."""
    if not os.path.exists(idea_md_path):
        return None
    with open(idea_md_path, "r", encoding="utf-8") as f:
        text = f.read()
    # Look for patterns like "height: 1.65 m", "Height: 0.15m", "15 cm tall"
    m_meter = re.search(
        r"(?:height|tall|size)\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(?:m|meters?|metres?)\b",
        text,
        re.IGNORECASE,
    )
    if m_meter:
        val = float(m_meter.group(1))
        if 0.02 <= val <= 20.0:
            return val
    m_cm = re.search(
        r"(?:height|tall|size)\s*[:=-]?\s*(\d+(?:\.\d+)?)\s*(?:cm|centimeters?|centimetres?)\b",
        text,
        re.IGNORECASE,
    )
    if m_cm:
        val = float(m_cm.group(1)) / 100.0
        if 0.02 <= val <= 20.0:
            return val
    return None


def get_work_dir(slug: str, work_root: str = ".") -> str:
    safe_slug = sanitize_slug(slug)
    return os.path.abspath(os.path.join(work_root, "work", safe_slug))


def get_pipeline_path(slug: str, work_root: str = ".") -> str:
    return os.path.join(get_work_dir(slug, work_root), "pipeline.json")


def utc_now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def save_pipeline(slug: str, data: dict[str, Any], work_root: str = ".") -> str:
    work_dir = get_work_dir(slug, work_root)
    os.makedirs(work_dir, exist_ok=True)
    for sub in SUBDIRS:
        os.makedirs(os.path.join(work_dir, sub), exist_ok=True)
    path = os.path.join(work_dir, "pipeline.json")
    tmp_path = os.path.join(work_dir, "pipeline.tmp.json")
    data["updated_at"] = utc_now_iso()
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    os.replace(tmp_path, path)
    return path


def load_pipeline(slug: str, work_root: str = ".") -> dict[str, Any]:
    path = get_pipeline_path(slug, work_root)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Pipeline state not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "slug" not in data:
        raise ValueError(f"Invalid pipeline state in {path}")
    return data


def init_pipeline(
    slug: str,
    idea: str,
    height_m: float = 1.7,
    is_humanoid: bool = True,
    clips: list[str] | None = None,
    triangle_budget: int = DEFAULT_TRIANGLE_BUDGET,
    max_bytes: int = DEFAULT_MAX_BYTES,
    work_root: str = ".",
) -> dict[str, Any]:
    safe_slug = sanitize_slug(slug)
    if not idea or not idea.strip():
        raise ValueError("Idea description cannot be empty")
    if height_m <= 0 or height_m > 50:
        raise ValueError(f"Invalid target height_m: {height_m}")
    if triangle_budget < 100 or triangle_budget > 500_000:
        raise ValueError(f"Invalid triangle_budget: {triangle_budget}")
    if max_bytes < 10_000:
        raise ValueError(f"Invalid max_bytes: {max_bytes}")

    # A procedural wave bends rigid props out of shape, so a non-humanoid expects idle only.
    expected_clips = clips if clips else (["idle", "walk", "wave"] if is_humanoid else ["idle"])
    if "idle" not in expected_clips:
        expected_clips = ["idle"] + expected_clips

    path = get_pipeline_path(safe_slug, work_root)
    if os.path.exists(path):
        state = load_pipeline(safe_slug, work_root)
        state["idea"] = idea.strip()
        state["target_height_m"] = height_m
        state["is_humanoid"] = is_humanoid
        state["expected_clips"] = expected_clips
        state["triangle_budget"] = triangle_budget
        state["max_bytes"] = max_bytes
        state.setdefault("critic", None)
        state.setdefault("reviews", [])
        save_pipeline(safe_slug, state, work_root)
        return state

    rel_base = f"work/{safe_slug}"
    state = {
        "idea": idea.strip(),
        "slug": safe_slug,
        "stage": "concept-art",
        "is_humanoid": bool(is_humanoid),
        "target_height_m": float(height_m),
        "triangle_budget": int(triangle_budget),
        "max_bytes": int(max_bytes),
        "expected_clips": expected_clips,
        "tasks": {},
        "chosen_concept": None,
        "chosen_try": None,
        "critic": None,
        "reviews": [],
        "checkpoints": {
            "A": {"approved": False, "choice": None, "notes": "", "timestamp": None},
            "B": {"approved": False, "choice": None, "notes": "", "timestamp": None},
            "C": {"approved": False, "choice": None, "notes": "", "timestamp": None},
        },
        "files": {
            "idea_md": f"{rel_base}/idea.md",
            "front_png": f"{rel_base}/images/front.png",
            "side_png": f"{rel_base}/images/side.png",
            "back_png": f"{rel_base}/images/back.png",
            "meshy_glb": f"{rel_base}/meshy/{safe_slug}-meshy.glb",
            "remeshed_glb": f"{rel_base}/meshy/{safe_slug}-remesh.glb",
            "rigged_glb": f"{rel_base}/meshy/{safe_slug}-rigged.glb",
            "blend": f"{rel_base}/blender/{safe_slug}.blend",
            "out_glb": f"{rel_base}/out/{safe_slug}.glb",
            "tries_png": f"{rel_base}/preview/tries.png",
            "sheet_png": f"{rel_base}/preview/sheet.png",
        },
        "created_at": utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    save_pipeline(safe_slug, state, work_root)
    return state


def record_task(
    slug: str,
    step_key: str,
    task_id: str | None = None,
    tool: str | None = None,
    task_type: str | None = None,
    credits: int | None = None,
    status: str | None = None,
    settings: dict[str, Any] | None = None,
    output_path: str | None = None,
    work_root: str = ".",
) -> dict[str, Any]:
    """Record a new task or update a recorded one; a field left as None keeps its stored value."""
    if not step_key or not step_key.strip():
        raise ValueError("step_key cannot be empty")
    if credits is not None and credits < 0:
        raise ValueError(f"credits cannot be negative: {credits}")

    state = load_pipeline(slug, work_root)
    existing = state.setdefault("tasks", {}).get(step_key, {})

    def pick(value: Any, key: str, default: Any = None) -> Any:
        return value if value is not None else existing.get(key, default)

    entry = {
        "task_id": (pick(task_id, "task_id") or "").strip(),
        "tool": (pick(tool, "tool") or "").strip(),
        "task_type": (pick(task_type, "task_type") or "").strip(),
        "credits": int(pick(credits, "credits", 0)),
        "status": pick(status, "status", "PENDING").strip(),
        "settings": pick(settings, "settings", {}),
        "output_path": pick(output_path, "output_path"),
        "recorded_at": existing.get("recorded_at") or utc_now_iso(),
        "updated_at": utc_now_iso(),
    }
    for key in ("task_id", "tool", "task_type"):
        if not entry[key]:
            raise ValueError(f"{key} is required when recording a new task")
    state["tasks"][step_key] = entry
    save_pipeline(slug, state, work_root)
    return entry


def get_task(slug: str, step_key: str, work_root: str = ".") -> dict[str, Any] | None:
    state = load_pipeline(slug, work_root)
    return state.get("tasks", {}).get(step_key)


def record_checkpoint(
    slug: str,
    checkpoint: str,
    approved: bool,
    choice: str | None = None,
    notes: str = "",
    work_root: str = ".",
) -> dict[str, Any]:
    cp = checkpoint.strip().upper()
    if cp not in VALID_CHECKPOINTS:
        raise ValueError(f"Invalid checkpoint '{checkpoint}'. Must be one of {VALID_CHECKPOINTS}")

    state = load_pipeline(slug, work_root)
    state.setdefault("checkpoints", {})[cp] = {
        "approved": bool(approved),
        "choice": choice,
        "notes": notes,
        "timestamp": utc_now_iso(),
    }
    if cp == "A" and approved:
        if choice:
            state["chosen_concept"] = choice
        state["stage"] = "image-to-3d"
    elif cp == "B" and approved:
        if choice is not None:
            try:
                state["chosen_try"] = int(choice)
            except ValueError:
                state["chosen_try"] = choice
        state["stage"] = "rig-animate"
    elif cp == "C" and approved:
        state["stage"] = "done"

    save_pipeline(slug, state, work_root)
    return state


def set_stage(slug: str, stage: str, work_root: str = ".") -> dict[str, Any]:
    if stage not in VALID_STAGES:
        raise ValueError(f"Invalid stage '{stage}'. Must be one of {VALID_STAGES}")
    state = load_pipeline(slug, work_root)
    state["stage"] = stage
    save_pipeline(slug, state, work_root)
    return state


def set_critic(slug: str, critic: str, work_root: str = ".") -> dict[str, Any]:
    """Store the user's answer to the Gemini review question (gemini or claude)."""
    if critic not in VALID_CRITICS:
        raise ValueError(f"Invalid critic '{critic}'. Must be one of {VALID_CRITICS}")
    state = load_pipeline(slug, work_root)
    state["critic"] = critic
    save_pipeline(slug, state, work_root)
    return state


def record_review(
    slug: str,
    gate: str,
    round_no: int,
    critic: str,
    model: str,
    verdict: str,
    path: str,
    open_issues: int,
    reason: str = "",
    work_root: str = ".",
) -> dict[str, Any]:
    """Log one critic review; a second review for the same gate and round replaces the first."""
    if gate not in VALID_GATES:
        raise ValueError(f"Invalid gate '{gate}'. Must be one of {VALID_GATES}")
    if round_no < 0:
        raise ValueError(f"round cannot be negative: {round_no}")
    state = load_pipeline(slug, work_root)
    reviews = [
        r for r in state.get("reviews", []) if not (r["gate"] == gate and r["round"] == round_no)
    ]
    entry = {
        "gate": gate,
        "round": int(round_no),
        "critic": critic,
        "model": model,
        "verdict": verdict,
        "open_issues": int(open_issues),
        "path": path,
        "reason": reason,
        "recorded_at": utc_now_iso(),
    }
    reviews.append(entry)
    state["reviews"] = sorted(reviews, key=lambda r: (r["gate"], r["round"]))
    save_pipeline(slug, state, work_root)
    return entry


def review_history(slug: str, gate: str | None = None, work_root: str = ".") -> list[dict[str, Any]]:
    if gate is not None and gate not in VALID_GATES:
        raise ValueError(f"Invalid gate '{gate}'. Must be one of {VALID_GATES}")
    state = load_pipeline(slug, work_root)
    return [r for r in state.get("reviews", []) if gate is None or r["gate"] == gate]


def next_review_round(slug: str, gate: str, work_root: str = ".") -> int:
    if gate not in VALID_GATES:
        raise ValueError(f"Invalid gate '{gate}'. Must be one of {VALID_GATES}")
    rounds = [r["round"] for r in review_history(slug, gate, work_root)]
    return max(rounds) + 1 if rounds else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage work/<slug>/pipeline.json state")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="Initialize or update pipeline.json")
    p_init.add_argument("slug", help="Idea slug (kebab-case)")
    p_init.add_argument("--idea", required=True, help="One-line idea description")
    p_init.add_argument("--height", type=float, default=1.7, help="Target height in meters")
    p_init.add_argument("--non-humanoid", action="store_true", help="Mark character as non-humanoid (default clips: idle only)")
    p_init.add_argument("--clips", default="", help="Comma-separated expected animation clips")
    p_init.add_argument("--triangle-budget", type=int, default=DEFAULT_TRIANGLE_BUDGET)
    p_init.add_argument("--work-root", default=".")

    p_show = sub.add_parser("show", help="Display current pipeline.json")
    p_show.add_argument("slug")
    p_show.add_argument("--work-root", default=".")

    p_get = sub.add_parser("get-task", help="Look up a recorded Meshy task by step key")
    p_get.add_argument("slug")
    p_get.add_argument("step_key")
    p_get.add_argument("--work-root", default=".")

    p_rec = sub.add_parser(
        "record-task",
        help="Record or update a Meshy task; on an update, omitted options keep their stored values",
    )
    p_rec.add_argument("slug")
    p_rec.add_argument("step_key")
    p_rec.add_argument("--task-id", default=None, help="Required for a new task")
    p_rec.add_argument("--tool", default=None, help="Required for a new task")
    p_rec.add_argument("--task-type", default=None, help="Required for a new task")
    p_rec.add_argument("--credits", type=int, default=None, help="Default 0 for a new task")
    p_rec.add_argument("--status", default=None, help="Default PENDING for a new task")
    p_rec.add_argument("--settings", default=None, help="JSON object")
    p_rec.add_argument("--output", default=None)
    p_rec.add_argument("--work-root", default=".")

    p_cp = sub.add_parser("record-checkpoint", help="Record checkpoint A, B, or C decision")
    p_cp.add_argument("slug")
    p_cp.add_argument("checkpoint", choices=VALID_CHECKPOINTS)
    p_cp.add_argument("--approved", choices=("true", "false"), required=True)
    p_cp.add_argument("--choice", default=None)
    p_cp.add_argument("--notes", default="")
    p_cp.add_argument("--work-root", default=".")

    p_stage = sub.add_parser("set-stage", help="Set current pipeline stage (and optionally record checkpoint)")
    p_stage.add_argument("slug")
    p_stage.add_argument("stage", choices=VALID_STAGES)
    p_stage.add_argument("--checkpoint", choices=VALID_CHECKPOINTS, default=None)
    p_stage.add_argument("--approved", choices=("true", "false"), default="true")
    p_stage.add_argument("--choice", default=None)
    p_stage.add_argument("--notes", default="")
    p_stage.add_argument("--work-root", default=".")

    p_critic = sub.add_parser("set-critic", help="Record the Gemini review answer (gemini or claude)")
    p_critic.add_argument("slug")
    p_critic.add_argument("critic", choices=VALID_CRITICS)
    p_critic.add_argument("--work-root", default=".")

    p_hist = sub.add_parser("review-history", help="List critic reviews, optionally for one gate")
    p_hist.add_argument("slug")
    p_hist.add_argument("--gate", choices=VALID_GATES, default=None)
    p_hist.add_argument("--work-root", default=".")

    args = parser.parse_args(argv)

    if args.cmd == "init":
        clips = [c.strip() for c in args.clips.split(",") if c.strip()] if args.clips else None
        state = init_pipeline(
            slug=args.slug,
            idea=args.idea,
            height_m=args.height,
            is_humanoid=not args.non_humanoid,
            clips=clips,
            triangle_budget=args.triangle_budget,
            work_root=args.work_root,
        )
        print(json.dumps(state, indent=2))
        return 0

    if args.cmd == "show":
        state = load_pipeline(args.slug, args.work_root)
        print(json.dumps(state, indent=2))
        return 0

    if args.cmd == "get-task":
        task = get_task(args.slug, args.step_key, args.work_root)
        if task is None:
            print("NOT_FOUND")
            return 1
        print(json.dumps(task, indent=2))
        return 0

    if args.cmd == "record-task":
        settings = json.loads(args.settings) if args.settings else None
        entry = record_task(
            slug=args.slug,
            step_key=args.step_key,
            task_id=args.task_id,
            tool=args.tool,
            task_type=args.task_type,
            credits=args.credits,
            status=args.status,
            settings=settings,
            output_path=args.output,
            work_root=args.work_root,
        )
        print(json.dumps(entry, indent=2))
        return 0

    if args.cmd == "record-checkpoint":
        state = record_checkpoint(
            slug=args.slug,
            checkpoint=args.checkpoint,
            approved=(args.approved == "true"),
            choice=args.choice,
            notes=args.notes,
            work_root=args.work_root,
        )
        print(json.dumps(state["checkpoints"][args.checkpoint], indent=2))
        return 0

    if args.cmd == "set-stage":
        if args.checkpoint:
            record_checkpoint(
                slug=args.slug,
                checkpoint=args.checkpoint,
                approved=(args.approved == "true"),
                choice=args.choice,
                notes=args.notes,
                work_root=args.work_root,
            )
        state = set_stage(args.slug, args.stage, args.work_root)
        print(f"Stage set to {state['stage']}")
        return 0

    if args.cmd == "set-critic":
        state = set_critic(args.slug, args.critic, args.work_root)
        print(f"Critic set to {state['critic']}")
        return 0

    if args.cmd == "review-history":
        print(json.dumps(review_history(args.slug, args.gate, args.work_root), indent=2))
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
