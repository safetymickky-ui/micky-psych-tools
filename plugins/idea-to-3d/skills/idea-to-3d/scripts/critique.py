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
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

SCRIPTS_DIR = Path(__file__).resolve().parent
REFERENCES_DIR = SCRIPTS_DIR.parent / "references"
SCHEMA_PATH = REFERENCES_DIR / "review.schema.json"
RUBRICS_DIR = REFERENCES_DIR / "rubrics"

sys.path.insert(0, str(SCRIPTS_DIR))
import pipeline_state  # noqa: E402

DEFAULT_MODEL = "gemini-4-argon-medium"
DEFAULT_TIMEOUT = 240
GATE_INPUTS = {
    "A1": ("idea.md", "preview/concepts.png"),
    "A2": ("idea.md", "images/chosen-concept.png", "images/front.png", "images/side.png", "images/back.png"),
    "B": ("idea.md", "images/front.png", "preview/tries.png"),
    "C": ("idea.md", "images/front.png", "preview/sheet.png", "out/quality_report.json"),
}
SEVERITIES = ("blocker", "major", "minor")
EXIT_OK, EXIT_USAGE, EXIT_UNAVAILABLE, EXIT_INVALID = 0, 1, 2, 3


class CriticUnavailable(Exception):
    """agy produced no usable answer: missing, failed, timed out, or not logged in."""


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
        lines += ["", "Your previous reply was rejected. Fix these problems:", *[f"- {e}" for e in errors]]
    return "\n".join(lines)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _int_in(value: Any, low: int, high: int) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and low <= value <= high


def validate_review(review: Any, gate: str) -> list[str]:
    """Return every problem with a critic review; an empty list means it is valid."""
    if not isinstance(review, dict):
        return ["review must be a JSON object"]
    errors = []
    if review.get("gate") != gate:
        errors.append(f'"gate" must be "{gate}"')
    verdict = review.get("verdict")
    if verdict not in ("PASS", "REVISE"):
        errors.append('"verdict" must be "PASS" or "REVISE"')
    scores = review.get("scores")
    if not isinstance(scores, list) or not scores:
        errors.append('"scores" must be a non-empty list')
    else:
        for i, score in enumerate(scores):
            if not (isinstance(score, dict) and _text(score.get("criterion")) and _int_in(score.get("score"), 1, 5)):
                errors.append(f"scores[{i}] needs a criterion and an integer score from 1 to 5")
    issues = review.get("issues")
    if not isinstance(issues, list):
        errors.append('"issues" must be a list')
        return errors
    for i, issue in enumerate(issues):
        if not isinstance(issue, dict):
            errors.append(f"issues[{i}] must be an object")
            continue
        for key in ("id", "criterion", "evidence", "fix"):
            if not _text(issue.get(key)):
                errors.append(f"issues[{i}].{key} must be non-empty text")
        if issue.get("severity") not in SEVERITIES:
            errors.append(f"issues[{i}].severity must be one of {', '.join(SEVERITIES)}")
        if not _int_in(issue.get("credits"), 0, 1000):
            errors.append(f"issues[{i}].credits must be an integer >= 0 (0 means a free fix)")
    serious = [x for x in issues if isinstance(x, dict) and x.get("severity") in ("blocker", "major")]
    if verdict == "PASS" and serious:
        errors.append("PASS is not allowed while a blocker or major issue is listed")
    if verdict == "REVISE" and not issues:
        errors.append("REVISE needs at least one issue")
    return errors


def last_json_object(text: str) -> Any:
    """The last top-level JSON object in free text, or None."""
    decoder = json.JSONDecoder()
    found, i = None, 0
    while i < len(text):
        if text[i] == "{":
            try:
                found, i = decoder.raw_decode(text, i)
                continue
            except json.JSONDecodeError:
                pass
        i += 1
    return found


def parse_agy_output(stdout: str) -> Any:
    try:
        envelope = json.loads(stdout.strip())
    except json.JSONDecodeError as exc:
        raise CriticUnavailable(f"agy printed non-JSON output: {exc}") from exc
    if not isinstance(envelope, dict) or envelope.get("status") != "SUCCESS":
        status = envelope.get("status") if isinstance(envelope, dict) else None
        raise CriticUnavailable(f"agy status {status!r}")
    structured = envelope.get("structured_output")
    if isinstance(structured, dict):
        return structured
    return last_json_object(str(envelope.get("response", "")))


def agy_command() -> list[str]:
    exe = os.environ.get("IDEA3D_AGY") or shutil.which("agy")
    if not exe:
        raise CriticUnavailable("agy not found on PATH (or set IDEA3D_AGY)")
    return [exe]


def call_agy(cmd_prefix: list[str], prompt: str, model: str, work_dir: Path, timeout: int) -> Any:
    argv = [
        *cmd_prefix, "-p", prompt, "--output-format", "json", "--mode", "plan",
        "--disable-slash-commands", "--model", model,
        "--json-schema", str(SCHEMA_PATH), "--add-dir", str(work_dir),
    ]
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, encoding="utf-8",
                              errors="replace", timeout=timeout)
    except OSError as exc:
        raise CriticUnavailable(f"cannot run agy: {exc}") from exc
    except subprocess.TimeoutExpired as exc:
        raise CriticUnavailable(f"agy timed out after {timeout}s") from exc
    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        raise CriticUnavailable(f"agy exited {proc.returncode}: {detail[0] if detail else 'no output'}")
    return parse_agy_output(proc.stdout)


def review_with_agy(cmd_prefix: list[str], gate: str, inputs: list[Path], model: str,
                    work_dir: Path, timeout: int) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    for _attempt in range(2):
        review = call_agy(cmd_prefix, build_prompt(gate, inputs, errors), model, work_dir, timeout)
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


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse exits 2 by default, which here would mean "critic unavailable".
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def parse_args(argv: list[str] | None) -> argparse.Namespace:
    p = _Parser(prog="critique.py", description="Independent critic for one idea-to-3d gate")
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
    return p.parse_args(argv)


def fail(code: int, message: str) -> int:
    print(f"critique.py: {message}", file=sys.stderr)
    return code


def main(argv: list[str] | None = None, cmd_prefix: list[str] | None = None) -> int:
    args = parse_args(argv)
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
        model = "claude-subagent" if args.critic == "claude-fallback" else args.model
    else:
        consent = state.get("critic")
        if consent is None:
            return fail(EXIT_USAGE, "Gemini consent not recorded: run pipeline_state.py set-critic <slug> gemini|claude")
        if consent == "claude":
            return fail(EXIT_UNAVAILABLE, "the user chose the Claude critic for this run")
        work_dir = Path(pipeline_state.get_work_dir(args.slug, args.work_root))
        try:
            inputs = gate_inputs(work_dir, args.gate)
            prefix = cmd_prefix if cmd_prefix is not None else agy_command()
            review, errors = review_with_agy(prefix, args.gate, inputs, args.model, work_dir, args.timeout)
        except UsageError as exc:
            return fail(EXIT_USAGE, str(exc))
        except CriticUnavailable as exc:
            return fail(EXIT_UNAVAILABLE, f"critic unavailable: {exc}")
        model = args.model

    if review is None:
        return fail(EXIT_INVALID, "invalid review:\n" + "\n".join(f"- {e}" for e in errors))
    path = write_review(args.slug, args.gate, round_no, review, args.critic, model, args.reason, args.work_root)
    print(path)
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
