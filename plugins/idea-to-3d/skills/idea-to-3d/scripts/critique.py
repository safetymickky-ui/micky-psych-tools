#!/usr/bin/env python3
"""
Independent critic for one idea-to-3d gate.

Sends the gate's files to Gemini through the Antigravity CLI (`agy`), validates the
review, writes work/<slug>/reviews/<gate>-r<round>.json and records it in pipeline.json.
A review written by the Claude fallback critic goes through the same validator with
--from-file.

    python critique.py <slug> <gate> [--round N] [--model ID] [--timeout 240] [--work-root .]
    python critique.py <slug> <gate> --from-file raw.json --critic claude-fallback --reason "..."

Exit codes: 0 review written (its path is printed) · 1 usage error · 2 critic
unavailable · 3 invalid review (twice from Gemini, or once from --from-file).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
REFERENCES_DIR = SCRIPTS_DIR.parent / "references"
SCHEMA_PATH = REFERENCES_DIR / "review.schema.json"
RUBRICS_DIR = REFERENCES_DIR / "rubrics"

sys.path.insert(0, str(SCRIPTS_DIR))
import pipeline_state  # noqa: E402
from agy_runner import AgyUnavailable, UsageParser, agy_command, run_agy  # noqa: E402

DEFAULT_MODEL = "gemini-4-argon-medium"
DEFAULT_TIMEOUT = 240
GATE_INPUTS = {
    "A1": ("idea.md", "preview/concepts.png"),
    "A2": ("idea.md", "images/chosen-concept.png", "images/front.png", "images/side.png", "images/back.png"),
    "B": ("idea.md", "images/front.png", "preview/tries.png"),
    "C": ("idea.md", "images/front.png", "preview/sheet.png", "out/quality_report.json"),
}
SEVERITIES = ("blocker", "major", "minor")
MAX_PROMPT_ERRORS = 20
EXIT_OK, EXIT_USAGE, EXIT_UNAVAILABLE, EXIT_INVALID = 0, 1, 2, 3


class UsageError(Exception):
    """The run cannot start: missing inputs."""


def gate_inputs(work_dir: Path, gate: str) -> list[Path]:
    paths = [work_dir / rel for rel in GATE_INPUTS[gate]]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise UsageError("missing gate inputs: " + ", ".join(missing))
    return paths


def build_prompt(gate: str, inputs: list[Path], errors: list[str] | None = None) -> str:
    rubric = (RUBRICS_DIR / f"{gate}.md").read_text(encoding="utf-8").strip()
    lines = [
        f"You are an independent art director reviewing Gate {gate} of a 3D character pipeline.",
        "You did not make this work. Judge only what the files show, against the brief and the rubric.",
        "",
        rubric,
        "",
        "## Files (read every one before judging; open each image and look at it)",
        *[f"- {path}" for path in inputs],
        "",
        f'Reply with only the JSON review object. "gate" must be "{gate}".',
    ]
    if errors:
        shown = [f"- {e}" for e in errors[:MAX_PROMPT_ERRORS]]
        if len(errors) > MAX_PROMPT_ERRORS:
            shown.append(f"- and {len(errors) - MAX_PROMPT_ERRORS} more")
        lines += ["", "Your previous reply was rejected. Fix these problems:", *shown]
    return "\n".join(lines)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _int_in(value: Any, low: int, high: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and low <= value <= high


def rubric_criteria(gate: str) -> set[str]:
    """The criterion ids a gate's rubric asks for: backticked ids opening bullets under `## Criteria`."""
    text = (RUBRICS_DIR / f"{gate}.md").read_text(encoding="utf-8")
    section = re.search(r"^## Criteria\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return set(re.findall(r"^- `([\w-]+)` —", section.group(1), re.M)) if section else set()


def validate_review(review: Any, gate: str) -> list[str]:
    """Return every problem with a critic review; an empty list means it is valid."""
    if not isinstance(review, dict):
        return ["review must be a JSON object"]
    errors = []
    allowed = rubric_criteria(gate)
    if review.get("gate") != gate:
        errors.append(f'"gate" must be "{gate}"')
    verdict = review.get("verdict")
    if verdict not in ("PASS", "REVISE"):
        errors.append('"verdict" must be "PASS" or "REVISE"')
    scores = review.get("scores")
    if not isinstance(scores, list) or not scores:
        errors.append('"scores" must be a non-empty list')
    else:
        scored: set[str] = set()
        for i, score in enumerate(scores):
            if not (isinstance(score, dict) and _text(score.get("criterion")) and _int_in(score.get("score"), 1, 5)):
                errors.append(f"scores[{i}] needs a criterion and an integer score from 1 to 5")
            if not (isinstance(score, dict) and _text(score.get("criterion"))):
                continue
            name = score["criterion"]
            if name not in allowed:
                errors.append(f'scores[{i}].criterion "{name}" is not a Gate {gate} criterion')
            elif name in scored:
                errors.append(f'criterion "{name}" is scored twice')
            scored.add(name)
        unscored = sorted(allowed - scored)
        if unscored:
            errors.append("criteria not scored: " + ", ".join(unscored))
    issues = review.get("issues")
    if not isinstance(issues, list):
        errors.append('"issues" must be a list')
        return errors
    seen_ids: set[str] = set()
    for i, issue in enumerate(issues):
        if not isinstance(issue, dict):
            errors.append(f"issues[{i}] must be an object")
            continue
        for key in ("id", "criterion", "evidence", "fix"):
            if not _text(issue.get(key)):
                errors.append(f"issues[{i}].{key} must be non-empty text")
        issue_id, criterion = issue.get("id"), issue.get("criterion")
        if _text(criterion) and criterion not in allowed:
            errors.append(f'issues[{i}].criterion "{criterion}" is not a Gate {gate} criterion')
        if _text(issue_id):
            if not re.fullmatch(rf"{gate}-\d+", issue_id):
                errors.append(f"issues[{i}].id must match {gate}-<number>, e.g. {gate}-1")
            if issue_id in seen_ids:
                errors.append(f'duplicate issue id "{issue_id}"')
            seen_ids.add(issue_id)
        if issue.get("severity") not in SEVERITIES:
            errors.append(f"issues[{i}].severity must be one of {', '.join(SEVERITIES)}")
        if not _int_in(issue.get("credits"), 0, 1000):
            errors.append(f"issues[{i}].credits must be an integer from 0 to 1000 (0 means a free fix)")
    serious = [x for x in issues if isinstance(x, dict) and x.get("severity") in ("blocker", "major")]
    if verdict == "PASS" and serious:
        errors.append("PASS is not allowed while a blocker or major issue is listed")
    if verdict == "REVISE" and not issues:
        errors.append("REVISE needs at least one issue")
    return errors


def last_review_object(text: str) -> Any:
    """The last top-level JSON object in free text that has a "verdict", or None."""
    decoder = json.JSONDecoder()
    found, i = None, 0
    while i < len(text):
        if text[i] == "{":
            try:
                obj, i = decoder.raw_decode(text, i)
            except json.JSONDecodeError:
                i += 1
                continue
            if isinstance(obj, dict) and "verdict" in obj:
                found = obj
            continue
        i += 1
    return found


def review_from_envelope(envelope: dict[str, Any]) -> Any:
    structured = envelope.get("structured_output")
    if isinstance(structured, dict):
        return structured
    return last_review_object(str(envelope.get("response", "")))


def call_agy(cmd_prefix: list[str], prompt: str, model: str, sandbox: Path, timeout: int) -> Any:
    args = [
        "-p", prompt, "--output-format", "json", "--mode", "plan",
        "--disable-slash-commands", "--model", model,
        "--json-schema", str(SCHEMA_PATH), "--add-dir", str(sandbox),
    ]
    return review_from_envelope(run_agy(cmd_prefix, args, sandbox, timeout))


def stage_inputs(work_dir: Path, gate: str) -> tuple[Path, list[Path]]:
    """Copy the gate's input files into a fresh temp dir, keeping relative paths, so the critic
    cannot see earlier reviews or pipeline.json. The caller removes the returned directory."""
    sources = gate_inputs(work_dir, gate)
    sandbox = Path(tempfile.mkdtemp(prefix="idea3d_critic_"))
    try:
        staged = []
        for rel, source in zip(GATE_INPUTS[gate], sources):
            dest = sandbox / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
            staged.append(dest)
    except BaseException:
        shutil.rmtree(sandbox, ignore_errors=True)
        raise
    return sandbox, staged


def review_with_agy(cmd_prefix: list[str], gate: str, inputs: list[Path], model: str,
                    sandbox: Path, timeout: int) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    for _attempt in range(2):
        review = call_agy(cmd_prefix, build_prompt(gate, inputs, errors), model, sandbox, timeout)
        errors = validate_review(review, gate)
        if not errors:
            return review, []
    return None, errors


def read_review_file(path: str, gate: str) -> tuple[dict | None, list[str]]:
    try:
        review = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"cannot read {path}: {exc}"]
    errors = validate_review(review, gate)
    return (None, errors) if errors else (review, [])


def write_review(slug: str, gate: str, round_no: int, review: dict, critic: str, model: str,
                 reason: str, work_root: str) -> Path:
    work_dir = Path(pipeline_state.get_work_dir(slug, work_root))
    out = work_dir / "reviews" / f"{gate}-r{round_no}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    record = {**review, "round": round_no, "critic": critic, "model": model, "reason": reason}
    tmp = out.with_name(f"{out.stem}.tmp.json")
    tmp.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, out)
    pipeline_state.record_review(
        slug, gate, round_no, critic=critic, model=model, verdict=review["verdict"],
        path=f"work/{pipeline_state.sanitize_slug(slug)}/reviews/{out.name}",
        open_issues=len(review["issues"]), reason=reason, work_root=work_root,
    )
    return out


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = UsageParser(prog="critique.py", description="Independent critic for one idea-to-3d gate")
    p.add_argument("slug")
    p.add_argument("gate", choices=tuple(GATE_INPUTS))
    p.add_argument("--round", dest="round_no", type=int, default=None,
                   help="review round (default: the next round for this gate)")
    p.add_argument("--model", default=os.environ.get("IDEA3D_CRITIC_MODEL") or DEFAULT_MODEL)
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="seconds per agy call")
    p.add_argument("--work-root", default=".")
    p.add_argument("--from-file", default=None, help="validate and record a review the Claude critic wrote")
    p.add_argument("--critic", choices=("gemini", "claude-fallback"), default="gemini")
    p.add_argument("--reason", default="", help="why the fallback critic ran")
    args = p.parse_args(argv)
    if args.timeout <= 0:
        p.error("--timeout must be a positive number of seconds")
    if bool(args.from_file) != (args.critic == "claude-fallback"):
        p.error("--from-file and --critic claude-fallback go together: use both or neither")
    return args


def fail(code: int, message: str) -> int:
    print(f"critique.py: {message}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None, cmd_prefix: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = parse_args(argv)
    try:
        return run(args, cmd_prefix)
    except Exception as exc:  # noqa: BLE001 - a traceback is no use to the orchestrator
        return fail(EXIT_USAGE, f"internal error: {exc}")


def run(args: argparse.Namespace, cmd_prefix: list[str] | None) -> int:
    try:
        state = pipeline_state.load_pipeline(args.slug, args.work_root)
    except (FileNotFoundError, ValueError) as exc:
        return fail(EXIT_USAGE, str(exc))
    round_no = args.round_no
    if round_no is None:
        round_no = pipeline_state.next_review_round(args.slug, args.gate, args.work_root)
    if round_no < 0:
        return fail(EXIT_USAGE, f"round cannot be negative: {round_no}")

    if args.from_file:
        review, errors = read_review_file(args.from_file, args.gate)
        model = "claude-subagent"
    else:
        consent = state.get("critic")
        if consent is None:
            return fail(EXIT_USAGE, "Gemini consent not recorded: run pipeline_state.py set-critic <slug> gemini|claude")
        if consent == "claude":
            return fail(EXIT_UNAVAILABLE, "the user chose the Claude critic for this run")
        if consent != "gemini":
            return fail(EXIT_USAGE, f"unknown critic choice {consent!r} in pipeline.json")
        work_dir = Path(pipeline_state.get_work_dir(args.slug, args.work_root))
        sandbox = None
        try:
            sandbox, inputs = stage_inputs(work_dir, args.gate)
            prefix = cmd_prefix if cmd_prefix is not None else agy_command()
            review, errors = review_with_agy(prefix, args.gate, inputs, args.model, sandbox, args.timeout)
        except UsageError as exc:
            return fail(EXIT_USAGE, str(exc))
        except AgyUnavailable as exc:
            return fail(EXIT_UNAVAILABLE, f"critic unavailable: {exc}")
        finally:
            if sandbox is not None:
                shutil.rmtree(sandbox, ignore_errors=True)
        model = args.model

    if review is None:
        return fail(EXIT_INVALID, "invalid review:\n" + "\n".join(f"- {e}" for e in errors))
    critic = "claude-fallback" if args.from_file else "gemini"
    path = write_review(args.slug, args.gate, round_no, review, critic, model, args.reason, args.work_root)
    print(path)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
