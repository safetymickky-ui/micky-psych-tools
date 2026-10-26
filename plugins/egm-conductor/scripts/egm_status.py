#!/usr/bin/env python3
"""Report EGM install health and pipeline progress for one project as JSON.

Used by the egm-conductor skills to locate the installed `egm@egm` plugin
(never guessing a cache version) and to infer which EGM phase comes next.

Usage: python egm_status.py [--project DIR]
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

MIN_CLAUDE = (2, 1, 271)  # omitClaudeMd support, required for Goldfish isolation
PLUGIN_KEY = "egm@egm"
STATE_FILE = Path(".egm-conductor") / "state.json"
REPORT_NAMES = [
    "zoom_out_report.md",
    "comprehension_report.md",
    "critic_report.md",
    "intermediate_zoom_out_report.md",
    "implementation_readiness_report.md",
    "consolidated_review_report.md",
    "goldfish_review_report.md",
]
PHASES = ["preflight", "bootstrap", "brainstorm", "draft", "review",
          "human_gate", "implement", "drift"]


def claude_home() -> Path:
    return Path.home() / ".claude"


def find_egm() -> dict:
    registry = claude_home() / "plugins" / "installed_plugins.json"
    info = {"installed": False, "enabled": None, "root": None, "version": None}
    if registry.exists():
        data = json.loads(registry.read_text(encoding="utf-8"))
        entries = data.get("plugins", data).get(PLUGIN_KEY) or []
        if entries:
            entry = entries[0]
            root = Path(entry["installPath"])
            info.update(installed=root.exists(), root=str(root),
                        version=entry.get("version"))
    settings = claude_home() / "settings.json"
    if settings.exists():
        enabled = json.loads(settings.read_text(encoding="utf-8")).get("enabledPlugins", {})
        info["enabled"] = enabled.get(PLUGIN_KEY)
    if info["root"]:
        skills = Path(info["root"]) / "skills"
        info["skills"] = sorted(p.parent.name for p in skills.glob("*/SKILL.md"))
    return info


def claude_version() -> dict:
    try:
        out = subprocess.run(["claude", "--version"], capture_output=True,
                             text=True, timeout=30, shell=False).stdout
    except (OSError, subprocess.TimeoutExpired):
        return {"version": None, "ok": False}
    match = re.search(r"(\d+)\.(\d+)\.(\d+)", out)
    if not match:
        return {"version": None, "ok": False}
    version = tuple(int(x) for x in match.groups())
    return {"version": ".".join(map(str, version)), "ok": version >= MIN_CLAUDE}


def artifact_dir(project: Path) -> Path:
    """Honour an `EGM artifact directory: <path>` line, as EGM itself does."""
    for name in ("CLAUDE.md", "AGENTS.md"):
        f = project / name
        if f.exists():
            m = re.search(r"^EGM artifact directory:\s*(.+)$",
                          f.read_text(encoding="utf-8", errors="ignore"), re.M)
            if m:
                return (project / m.group(1).strip()).resolve()
    return project


def rel(path: Path, project: Path) -> str:
    try:
        return str(path.relative_to(project))
    except ValueError:
        return str(path)


def scan_project(project: Path) -> dict:
    art = artifact_dir(project)
    design_dir = project / "docs" / "designs"
    designs = sorted(p for p in design_dir.glob("*.md")
                     if p.name not in ("SITEMAP.md", "README.md")) if design_dir.exists() else []
    found = {
        "git_repo": (project / ".git").exists(),
        "artifact_dir": rel(art, project),
        "concepts_brief": next((rel(p, project) for p in
                                (art / "concepts_brief.md", project / "scratch" / "concepts_brief.md")
                                if p.exists()), None),
        "design_draft": rel(art / "design_draft.md", project) if (art / "design_draft.md").exists() else None,
        "design_docs": [rel(p, project) for p in designs],
        "review_reports": [n for n in REPORT_NAMES if (art / n).exists()],
        "drift_reports": sorted(p.name for p in art.glob("*_DRIFT_REPORT.md")),
        "has_root_readme": (project / "README.md").exists(),
    }
    return found


def load_state(project: Path) -> dict | None:
    f = project / STATE_FILE
    if not f.exists():
        return None
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"error": f"{STATE_FILE} is not valid JSON"}


def suggest_phase(egm: dict, cli: dict, found: dict, state: dict | None) -> str:
    if not (egm["installed"] and egm["enabled"] is not False and cli["ok"]):
        return "preflight"
    if state and state.get("phase") in PHASES and not state.get("error"):
        return state["phase"]
    if found["review_reports"]:
        return "review"
    if found["design_docs"] and not found["design_draft"]:
        return "review"
    if found["design_draft"] or found["concepts_brief"]:
        return "draft"
    return "brainstorm"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", default=".")
    project = Path(parser.parse_args().project).resolve()

    egm = find_egm()
    cli = claude_version()
    found = scan_project(project)
    state = load_state(project)
    print(json.dumps({
        "project": str(project),
        "egm": egm,
        "claude_cli": cli,
        "artifacts": found,
        "state": state,
        "suggested_phase": suggest_phase(egm, cli, found, state),
    }, indent=2))


if __name__ == "__main__":
    main()
