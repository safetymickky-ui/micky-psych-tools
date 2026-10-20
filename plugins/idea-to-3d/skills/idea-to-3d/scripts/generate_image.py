#!/usr/bin/env python3
"""
Free image generation through the Antigravity CLI (`agy`).

Asks agy to generate one image (optionally from reference images), finds the file agy wrote in
its conversation folder, and saves it as a PNG under work/<slug>/.

    python generate_image.py <slug> --out images/concept-1.png --prompt "<text>"
           [--ref <path> ...] [--timeout 300] [--work-root .]

Needs the user's Google consent recorded in pipeline.json (`set-critic <slug> gemini`): the
prompt and reference images are sent to Google.

Exit codes: 0 image written (its absolute path is printed) · 1 usage or internal error ·
2 route unavailable (the caller falls back to the paid image route).
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))
import pipeline_state  # noqa: E402
from agy_runner import AgyUnavailable, UsageParser, agy_command, run_agy  # noqa: E402

DEFAULT_TIMEOUT = 300
IMAGE_WAIT_SECONDS = 60  # the file can appear slightly after agy's reply
MAX_REFS = 5
IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")
DEFAULT_BRAIN = Path.home() / ".gemini" / "antigravity-cli" / "brain"
EXIT_OK, EXIT_USAGE, EXIT_UNAVAILABLE = 0, 1, 2


class UsageError(Exception):
    """The run cannot start: bad arguments or missing consent."""


class RouteUnavailable(Exception):
    """agy cannot supply an image; the caller should use the paid route."""


def brain_conversation_dir(conversation_id: Any) -> Path | None:
    """agy keeps each conversation's generated files in <brain>/<conversation_id>/."""
    if not isinstance(conversation_id, str) or not conversation_id or Path(conversation_id).name != conversation_id:
        return None
    brain = Path(os.environ.get("IDEA3D_AGY_BRAIN") or DEFAULT_BRAIN)
    return brain / conversation_id


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_SUFFIXES and path.is_file()


def inside(path: Path, folder: Path) -> bool:
    try:
        path.resolve().relative_to(folder.resolve())
    except (OSError, ValueError):
        return False
    return True


def find_image(conversation_dir: Path | None, response: str) -> Path | None:
    """The image path named on the last matching line of the reply, else the newest image in the folder."""
    if conversation_dir is None:
        return None
    for line in reversed(response.splitlines()):
        text = line.strip().strip("`'\"")
        if text and os.path.isabs(text) and is_image(Path(text)):
            if inside(Path(text), conversation_dir):
                return Path(text)
            break
    if not conversation_dir.is_dir():
        return None
    images = [p for p in conversation_dir.iterdir() if is_image(p)]
    return max(images, key=lambda p: p.stat().st_mtime) if images else None


def wait_for_image(conversation_dir: Path | None, response: str) -> Path | None:
    deadline = time.monotonic() + IMAGE_WAIT_SECONDS
    while True:
        found = find_image(conversation_dir, response)
        if found or time.monotonic() >= deadline:
            return found
        time.sleep(1)


def copy_refs(refs: list[Path], folder: Path) -> list[Path]:
    """Copy reference images into the folder agy may read, keeping basenames unique."""
    copies = []
    for ref in refs:
        dest = folder / ref.name
        n = 2
        while dest.exists():
            dest = folder / f"{ref.stem}-{n}{ref.suffix}"
            n += 1
        shutil.copy2(ref, dest)
        copies.append(dest)
    return copies


def build_prompt(text: str, copies: list[Path]) -> str:
    lines = [f"Use your image generation tool to generate exactly one image. {text}"]
    if copies:
        lines += ["Pass each of these files to the image tool as a reference image:",
                  *[f"- {path}" for path in copies]]
    lines.append("Generate one image only. Then reply with only the absolute file path of the generated image file.")
    return "\n".join(lines)


def save_png(source: Path, out: Path) -> None:
    """Convert to RGB PNG and replace the output atomically; a file Pillow cannot read is unavailable."""
    from PIL import Image

    tmp = out.with_name(f"{out.stem}.tmp.png")
    try:
        with Image.open(source) as img:
            rgb = img.convert("RGB")
        out.parent.mkdir(parents=True, exist_ok=True)
        rgb.save(tmp, "PNG")
        os.replace(tmp, out)
    except (OSError, ValueError) as exc:
        tmp.unlink(missing_ok=True)
        raise RouteUnavailable(f"agy returned a file that is not a readable image: {exc}") from exc


def resolve_out(work_dir: Path, out: str) -> Path:
    if Path(out).is_absolute() or Path(out).anchor:
        raise UsageError(f"--out must be relative to work/<slug>/, not absolute: {out}")
    target = work_dir / out
    if not inside(target, work_dir):
        raise UsageError(f"--out must stay inside {work_dir}: {out}")
    if target.suffix.lower() != ".png":
        raise UsageError(f"--out must end in .png: {out}")
    return target


def resolve_refs(refs: list[str]) -> list[Path]:
    if len(refs) > MAX_REFS:
        raise UsageError(f"at most {MAX_REFS} --ref images, got {len(refs)}")
    paths = [Path(ref) for ref in refs]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise UsageError("reference image not found: " + ", ".join(missing))
    return paths


def check_consent(state: dict[str, Any]) -> None:
    consent = state.get("critic")
    if consent is None:
        raise UsageError("Google consent not recorded: run pipeline_state.py set-critic <slug> gemini|claude")
    if consent == "claude":
        raise RouteUnavailable("the user declined Google; use the paid image route")
    if consent != "gemini":
        raise UsageError(f"unknown critic choice {consent!r} in pipeline.json")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = UsageParser(prog="generate_image.py", description="Generate one image for free through agy")
    p.add_argument("slug")
    p.add_argument("--out", required=True, help="output PNG, relative to work/<slug>/ (e.g. images/concept-1.png)")
    p.add_argument("--prompt", required=True)
    p.add_argument("--ref", action="append", default=[], help="reference image (repeatable, at most 5)")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds for the agy call")
    p.add_argument("--work-root", default=".")
    args = p.parse_args(argv)
    if args.timeout <= 0:
        p.error("--timeout must be a positive number of seconds")
    return args


def fail(code: int, message: str) -> int:
    print(f"generate_image.py: {message}", file=sys.stderr)
    return code


def generate(args: argparse.Namespace, cmd_prefix: list[str] | None) -> Path:
    try:
        state = pipeline_state.load_pipeline(args.slug, args.work_root)
    except (FileNotFoundError, ValueError) as exc:
        raise UsageError(str(exc)) from exc
    check_consent(state)
    work_dir = Path(pipeline_state.get_work_dir(args.slug, args.work_root))
    out = resolve_out(work_dir, args.out)
    refs = resolve_refs(args.ref)

    folder = Path(tempfile.mkdtemp(prefix="idea3d_image_"))
    try:
        prompt = build_prompt(args.prompt, copy_refs(refs, folder))
        prefix = cmd_prefix if cmd_prefix is not None else agy_command()
        envelope = run_agy(prefix, ["-p", prompt, "--output-format", "json", "--disable-slash-commands",
                                    "--add-dir", str(folder)], folder, args.timeout)
        conversation = brain_conversation_dir(envelope.get("conversation_id"))
        source = wait_for_image(conversation, str(envelope.get("response", "")))
        if source is None:
            raise RouteUnavailable("agy returned no image")
        save_png(source, out)
    finally:
        shutil.rmtree(folder, ignore_errors=True)
    return out


def main(argv: list[str] | None = None, cmd_prefix: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args(argv)
    try:
        out = generate(args, cmd_prefix)
    except UsageError as exc:
        return fail(EXIT_USAGE, str(exc))
    except (RouteUnavailable, AgyUnavailable) as exc:
        return fail(EXIT_UNAVAILABLE, f"image route unavailable: {exc}")
    except Exception as exc:  # noqa: BLE001 - a traceback is no use to the orchestrator
        return fail(EXIT_USAGE, f"internal error: {exc}")
    print(out)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
