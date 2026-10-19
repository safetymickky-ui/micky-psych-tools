"""SessionStart hook: announce the active DESIGN.md so every UI build uses it.

Lookup order: the nearest DESIGN.md from the session's cwd up to the filesystem root,
then the personal default at ~/.claude/DESIGN.md. Prints nothing when neither exists.
"""
import json
import sys
from pathlib import Path


def find_design_md(cwd: Path) -> tuple[Path, str] | None:
    for folder in (cwd, *cwd.parents):
        candidate = folder / "DESIGN.md"
        if candidate.is_file():
            return candidate, "project"
    default = Path.home() / ".claude" / "DESIGN.md"
    if default.is_file():
        return default, "personal default"
    return None


def front_matter_name(path: Path) -> str:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return ""
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:40]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        payload = {}
    found = find_design_md(Path(payload.get("cwd") or Path.cwd()))
    if not found:
        return
    path, scope = found
    name = front_matter_name(path) or "unnamed"
    context = (
        f"DESIGN.md active ({scope}): {path} — system '{name}'. Before writing any visual UI "
        "(web pages, HTML/CSS, React/Vue/Svelte components, Tailwind themes, Artifacts, "
        "dashboards, charts, mockups), load the design-md-apply skill and build from these "
        "tokens and rules. The user's explicit instructions override it; Office files follow "
        "clinical-minimal instead."
    )
    print(json.dumps({
        "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}
    }))


if __name__ == "__main__":
    main()
