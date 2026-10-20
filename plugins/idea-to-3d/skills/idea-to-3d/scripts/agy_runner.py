#!/usr/bin/env python3
"""
Shared runner for the Antigravity CLI (`agy`): locate it, run one non-interactive call,
tree-kill it on timeout, and return the parsed JSON envelope. Used by critique.py (review)
and generate_image.py (free image route). Stdlib only.
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

EXIT_USAGE = 1


class AgyUnavailable(Exception):
    """agy produced no usable answer: missing, failed, timed out, or not logged in."""


class UsageParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        # argparse exits 2 by default, which in these scripts means "route unavailable".
        self.print_usage(sys.stderr)
        self.exit(EXIT_USAGE, f"{self.prog}: error: {message}\n")


def agy_command() -> list[str]:
    exe = os.environ.get("IDEA3D_AGY") or shutil.which("agy")
    if not exe:
        raise AgyUnavailable("agy not found on PATH (or set IDEA3D_AGY)")
    return [exe]


def kill_tree(proc: subprocess.Popen) -> None:
    """Kill agy and any children; children holding the pipes would otherwise block communicate()."""
    if os.name == "nt":
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)], capture_output=True)
    else:
        proc.kill()


def parse_envelope(stdout: str) -> dict[str, Any]:
    try:
        envelope = json.loads(stdout.strip())
    except json.JSONDecodeError as exc:
        raise AgyUnavailable(f"agy printed non-JSON output: {exc}") from exc
    if not isinstance(envelope, dict) or envelope.get("status") != "SUCCESS":
        status = envelope.get("status") if isinstance(envelope, dict) else None
        raise AgyUnavailable(f"agy status {status!r}")
    return envelope


def run_agy(cmd_prefix: list[str], args: list[str], cwd: Path, timeout: int) -> dict[str, Any]:
    """Run `[*cmd_prefix, *args]` in cwd and return the SUCCESS envelope; raise AgyUnavailable otherwise."""
    try:
        proc = subprocess.Popen([*cmd_prefix, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, encoding="utf-8", errors="replace", cwd=cwd)
    except OSError as exc:
        raise AgyUnavailable(f"cannot run agy: {exc}") from exc
    try:
        stdout, stderr = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        kill_tree(proc)
        try:
            proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            pass
        raise AgyUnavailable(f"agy timed out after {timeout}s") from exc
    if proc.returncode != 0:
        detail = (stderr or stdout or "").strip().splitlines()
        raise AgyUnavailable(f"agy exited {proc.returncode}: {detail[0] if detail else 'no output'}")
    return parse_envelope(stdout)
