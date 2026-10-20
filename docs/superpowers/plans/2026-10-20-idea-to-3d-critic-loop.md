# idea-to-3d v2 Critic Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Port the `idea-to-3d` Antigravity plugin into the micky-psych-tools marketplace as a Claude Code plugin and give every stage a maker → independent Gemini critic → reviser loop, then backport the same shared core to the Antigravity repo.

**Architecture:** A shared, platform-neutral core (`critique.py`, review schema, four gate rubrics, three role briefs, the loop protocol, the extended `pipeline_state.py`, tests) lives in `plugins/idea-to-3d/` and is copied byte-for-byte into the Antigravity repo by `sync-core.ps1`. `critique.py` sends a gate's files to Gemini through the Antigravity CLI (`agy -p --mode plan --json-schema`), validates the review and logs it in `pipeline.json`; a Claude critic agent is the fallback. Each platform's orchestrator `SKILL.md` maps the roles onto its own tools inside one marked `platform` block.

**Tech Stack:** Python 3.10+ stdlib (`unittest`, `subprocess`, `argparse`), Pillow (already used by v1), Antigravity CLI `agy` (model `gemini-4-argon-medium`), Meshy MCP (user-scope `meshy`), Blender 5.2 headless, PowerShell 5.1 for the sync script.

**Spec:** `docs/superpowers/specs/2026-10-20-idea-to-3d-critic-loop-design.md`

**Repos and branches:**
- Marketplace: `C:\Users\User\micky-psych-tools`, branch `feat/idea-to-3d-critic-loop` (already created; spec committed as `a741306`). Tasks 1–9 and 12.
- Antigravity: `C:\Users\User\Desktop\repo\idea-to-3d`. Tasks 10–11 on a new branch `feat/critic-loop`.
- Never commit `work/` in either repo. Never hand-edit a marketplace plugin version (use `scripts/bump.py`).

---

## File map

Marketplace `plugins/idea-to-3d/` (new):

| Path | Responsibility | Core? |
|---|---|---|
| `.claude-plugin/plugin.json` | manifest | no |
| `README.md`, `CHANGELOG.md`, `LICENSE` | docs | no |
| `core-files.txt` | list of shared-core paths the Antigravity repo pulls | no |
| `assets/logo.png` | test fixture image (v1 tests use it) | no |
| `agents/idea3d-maker.md`, `idea3d-reviser.md`, `idea3d-critic.md` | thin Claude Code wrappers around the role files | no |
| `skills/{idea-to-3d,concept-art,image-to-3d,rig-animate,blender-finish}/` | v1 skills, adapted for Claude Code | no |
| `skills/idea-to-3d/references/rules.md` | v1 rules, adapted (was `rules/idea-to-3d.md`) | no |
| `skills/idea-to-3d/references/loop.md` | gate protocol | **yes** |
| `skills/idea-to-3d/references/review.schema.json` | review JSON schema (also passed to `agy --json-schema`) | **yes** |
| `skills/idea-to-3d/references/rubrics/{A1,A2,B,C}.md` | per-gate criteria, severity, fix catalogue with credits | **yes** |
| `skills/idea-to-3d/references/roles/{maker,reviser,critic}.md` | role briefs | **yes** |
| `skills/idea-to-3d/scripts/critique.py` | Gemini critic + validator + review writer | **yes** |
| `skills/idea-to-3d/scripts/pipeline_state.py` | v1 state manager + reviews log + critic consent | **yes** |
| `tests/test_critic.py`, `tests/fake_agy.py` | core tests, fake `agy` | **yes** |
| `tests/test_pipeline.py` | v1 tests minus the Antigravity-only hook tests | no |

Marketplace repo-level (modified): `.claude-plugin/marketplace.json`, `CLAUDE.md`, `MEMORY.md`, `ROUTING.md` (generated).

Antigravity repo (modified/new): core files above (synced), `scripts/sync-core.ps1`, `tests/test_core_parity.py`, `skills/idea-to-3d/SKILL.md`, four stage `SKILL.md` gate notes, `rules/idea-to-3d.md`, `plugin.json`, `README.md`.

---

### Task 1: Port v1 into the marketplace

**Files:**
- Create: everything under `plugins/idea-to-3d/` listed as "no" in the file map except `agents/`, `core-files.txt` (later tasks)
- Modify: `.claude-plugin/marketplace.json`
- Delete: stray ignored `plugins/idea-to-3d/skills/blender-finish/scripts/__pycache__/`

- [ ] **Step 1: Confirm nothing tracked will be lost, then copy v1**

Run (Bash, from `C:\Users\User\micky-psych-tools`):

```bash
SRC=/c/Users/User/Desktop/repo/idea-to-3d
DST=plugins/idea-to-3d
test "$(git ls-files "$DST" | wc -l)" -eq 0 && echo "nothing tracked under $DST"
rm -rf "$DST"
mkdir -p "$DST/.claude-plugin" "$DST/tests" "$DST/assets" "$DST/skills"
cp -r "$SRC/skills/." "$DST/skills/"
mkdir -p "$DST/skills/idea-to-3d/references"
cp "$SRC/rules/idea-to-3d.md" "$DST/skills/idea-to-3d/references/rules.md"
cp "$SRC/assets/logo.png" "$DST/assets/"
cp "$SRC/tests/test_pipeline.py" "$DST/tests/"
cp plugins/bullet-reconstruct/LICENSE "$DST/LICENSE"
find "$DST" -name __pycache__ -type d -prune -exec rm -rf {} +
find "$DST" -type f | sort
```

Expected: `nothing tracked under plugins/idea-to-3d`, then a list with 5 `SKILL.md`, 8 scripts, `rules.md`, `logo.png`, `test_pipeline.py`, `LICENSE`. If the first line does not print, stop and inspect `git ls-files plugins/idea-to-3d`.

- [ ] **Step 2: Adapt the copied files for Claude Code**

Write this one-off script to the session scratchpad as `port_v1.py` (not committed) and run it from the marketplace root with `python port_v1.py`:

```python
"""One-off: adapt the Antigravity v1 copy in plugins/idea-to-3d for Claude Code."""
import re
import sys
from pathlib import Path

P = Path("plugins/idea-to-3d")
SKILLS = ["idea-to-3d", "concept-art", "image-to-3d", "rig-animate", "blender-finish"]
ROOT_LINE = ("`<plugin_root>` is this plugin's directory: two levels above this skill's base "
             "directory. Use it as an absolute path in every command.\n")


def read(path):
    return path.read_text(encoding="utf-8")


def write(path, text):
    path.write_text(text, encoding="utf-8", newline="\n")


def sub_once(text, old, new, where):
    n = text.count(old)
    if n != 1:
        sys.exit(f"{where}: expected 1 match for {old[:70]!r}, found {n}")
    return text.replace(old, new)


def tool_names(text):
    text = text.replace("`ask_question`", "`AskUserQuestion`").replace("ask_question", "AskUserQuestion")
    return text.replace("`view_file`", "`Read`").replace("view_file", "Read")


for skill in SKILLS:
    path = P / "skills" / skill / "SKILL.md"
    text = tool_names(read(path))
    h1 = re.search(r"^# .+\n", text, re.M)
    text = text[: h1.end()] + "\n" + ROOT_LINE + text[h1.end():]
    write(path, text)

NEW_STEP2 = """1. **Image route (Claude Code): Meshy `nano-banana-pro`, 9 credits per image.** The credits must be approved first (the orchestrator asks; run on its own, ask with `AskUserQuestion`). Call `meshy_text_to_image` once per concept with `ai_model: "nano-banana-pro"`, `aspect_ratio: "1:1"` and a prompt built from `idea.md`, and record each `task_id` with `pipeline_state.py record-task <slug> concept-<n> ...` the moment it is created.
2. Poll each task with `meshy_get_task_status` (`wait: true`, `timeout_seconds: 150`) and download it with `meshy_download_model` (`save_to: "work/<slug>/images/concept-<n>.png"`). If the file is a JPEG, convert it to PNG with Pillow before building the sheet.
"""
ca = P / "skills/concept-art/SKILL.md"
t = read(ca)
start = t.index("1. **Primary path (Antigravity")
end = t.index("3. Build the comparison sheet")
t = t[:start] + NEW_STEP2 + t[end:]
t = sub_once(t, "via Nano Banana `image-generator`: **0 Meshy credits**",
             "via `meshy_image_to_image` (`nano-banana-pro`): **27 credits** (3 × 9)", "concept-art")
t = sub_once(t, "pass that file path in `ImagePaths` (or `reference_file_paths` in `meshy_image_to_image`)",
             "pass that file path in `reference_file_paths` of `meshy_image_to_image` (`ai_model: \"nano-banana-pro\"`, "
             "`aspect_ratio: \"1:1\"`, 9 credits per view; download each result with `meshy_download_model` and `save_to`)",
             "concept-art")
t = sub_once(t, "(`ImageName`: `<slug>_front`)", "(saved as `work/<slug>/images/front.png`)", "concept-art")
t = sub_once(t, "(`ImageName`: `<slug>_side`) and `back.png` (`ImageName`: `<slug>_back`)",
             "(saved as `images/side.png`) and `back.png` (saved as `images/back.png`)", "concept-art")
t = sub_once(t, "in `ImagePaths`.", "in `reference_file_paths`.", "concept-art")
write(ca, t)

rules = P / "skills/idea-to-3d/references/rules.md"
t = tool_names(read(rules))
t = re.sub(r"\A---\n.*?\n---\n\n?", "", t, flags=re.S)
t = sub_once(t, "inform the user that the image will be uploaded to Meshy and get an explicit **yes**",
             "inform the user that images and the brief go to Meshy (`meshy.ai`) and, for review, to Gemini "
             "(Google, through the Antigravity CLI), and get an explicit **yes**", "rules")
t, n = re.subn(r"^- \*\*Updating the installed plugin on Windows:\*\*.*\n", "", t, flags=re.M)
if n != 1:
    sys.exit(f"rules: expected 1 Antigravity sync bullet, found {n}")
t = t.rstrip("\n") + """

## 6. Critic loop

- Every gate (A1, A2, B, C) follows [loop.md](loop.md): critic, then reviser, then paid fixes only after a yes, then the critic again; it ends on PASS or after 2 revise rounds.
- The critic sees only files. Never pass it the maker's or reviser's messages, and never judge a gate yourself.
- Record the Gemini answer with `pipeline_state.py set-critic <slug> gemini|claude` before the first gate; `critique.py` refuses to run until it is recorded.
"""
write(rules, t)

tests = P / "tests/test_pipeline.py"
t = read(tests)
start = t.index("class TestSaveImageHookIntegration")
end = t.index("class TestBlenderEndToEndPipeline")
write(tests, t[:start] + t[end:])
print("port_v1: ok")
```

Expected output: `port_v1: ok`. Any `expected 1 match` exit means the v1 text drifted: open the file, find the passage, and adjust that one `sub_once` string.

- [ ] **Step 3: Check no Antigravity-only names remain outside the orchestrator**

Run:

```bash
grep -rnE "image-generator|generate_image|send_message|ImagePaths|ImageName|ask_question|view_file|save-image" plugins/idea-to-3d --include=*.md | grep -v "skills/idea-to-3d/SKILL.md"
```

Expected: no output. (The orchestrator `skills/idea-to-3d/SKILL.md` is rewritten in Task 8.)

- [ ] **Step 4: Write the manifest, CHANGELOG and a minimal README**

`plugins/idea-to-3d/.claude-plugin/plugin.json`:

```json
{
  "name": "idea-to-3d",
  "version": "1.0.0",
  "description": "Turns a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) with a preview sheet: concept art and image-to-3D, remesh, rigging and clips on Meshy, finishing in headless Blender 5.2, across three user checkpoints.",
  "author": {
    "name": "Thanawat Suharit (Micky)"
  },
  "license": "MIT",
  "keywords": [
    "3d",
    "meshy",
    "blender",
    "glb",
    "rigging",
    "animation",
    "concept-art"
  ]
}
```

`plugins/idea-to-3d/CHANGELOG.md`:

```markdown
# Changelog

## 1.0.0 — 2026-10-20

Ported into micky-psych-tools from the Antigravity plugin (`Desktop/repo/idea-to-3d` v1.0.0).
Claude Code adaptations applied in place: `AskUserQuestion` for every checkpoint, `Read` on
preview PNGs, Meshy `nano-banana-pro` as the image route (9 credits per image), the
pipeline rules moved to `skills/idea-to-3d/references/rules.md`, and the Antigravity-only
`save-image` hook and its tests left out. Uses the user-scope `meshy` MCP server.
```

`plugins/idea-to-3d/README.md`:

```markdown
# idea-to-3d

Turns a one-line character or prop idea into a textured, rigged, animated `.glb` and a
preview sheet: concept art and image-to-3D on Meshy, remesh/rig/clips on Meshy, finishing
in headless Blender 5.2, with three user checkpoints. Ported from the Antigravity plugin
at `Desktop/repo/idea-to-3d`.

Requires Windows, Blender 5.2, Python with Pillow, and the user-scope `meshy` MCP server.
```

- [ ] **Step 5: Add the catalog entry**

Run:

```bash
python3 - <<'EOF'
import json
p = ".claude-plugin/marketplace.json"
d = json.load(open(p, encoding="utf-8"))
assert not any(e["name"] == "idea-to-3d" for e in d["plugins"])
d["plugins"].append({
    "name": "idea-to-3d",
    "source": "./plugins/idea-to-3d",
    "description": "Turns a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) with a preview sheet. Concept art and image-to-3D, remesh, rigging and clips run on Meshy (credits spent only after explicit approval); headless Blender 5.2 cleans up, merges clips, validates and renders the sheet. Three user checkpoints. Ported from the Antigravity plugin. Needs Windows, Blender 5.2 and the user-scope meshy MCP server.",
    "category": "design",
    "keywords": ["3d", "meshy", "blender", "glb", "rigging", "animation", "concept-art"],
})
with open(p, "w", encoding="utf-8", newline="\n") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write("\n")
EOF
git diff --stat .claude-plugin/marketplace.json
```

Expected: only additions (about 16 `+` lines). If any other line changed, run `git checkout .claude-plugin/marketplace.json` and add the entry by hand at the end of the `plugins` array instead.

- [ ] **Step 6: Run the v1 unit tests and health**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_pipeline.py" -k Unit -v
bash scripts/health.sh --fast
```

Expected: all `TestPipelineStateUnit` and `TestCheckGlbUnit` tests `ok`; `health: OK`. A trigger-lock warning about unlocked phrases is fine (warning, not error).

- [ ] **Step 7: Commit**

```bash
git add plugins/idea-to-3d .claude-plugin/marketplace.json
git commit -m "feat(idea-to-3d): port the Antigravity plugin v1.0.0 into the marketplace

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 2: Reviews log and critic consent in `pipeline_state.py`

**Files:**
- Modify: `plugins/idea-to-3d/skills/idea-to-3d/scripts/pipeline_state.py`
- Create: `plugins/idea-to-3d/tests/test_critic.py` (pipeline part; later tasks append)

- [ ] **Step 1: Write the failing tests**

Create `plugins/idea-to-3d/tests/test_critic.py`:

```python
#!/usr/bin/env python3
"""
Tests for the idea-to-3d critic loop core: pipeline_state reviews and consent,
review validation, and critique.py. No network: `agy` is replaced by tests/fake_agy.py.
"""
from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = PLUGIN_ROOT / "skills" / "idea-to-3d" / "scripts"
REFERENCES = PLUGIN_ROOT / "skills" / "idea-to-3d" / "references"
FAKE_AGY = Path(__file__).resolve().parent / "fake_agy.py"
PNG_BYTES = b"\x89PNG\r\n\x1a\n"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {name} from {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pipeline_state = load_module("pipeline_state_under_test", SCRIPTS / "pipeline_state.py")


class TempPipelineCase(unittest.TestCase):
    """A fresh work root with an initialised fox-knight pipeline."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="test_critic_"))
        self.root = str(self.tmp)
        pipeline_state.init_pipeline(
            slug="fox-knight", idea="A fox knight with a lantern", height_m=1.2, work_root=self.root
        )
        self.work = self.tmp / "work" / "fox-knight"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestPipelineReviews(TempPipelineCase):
    def test_init_creates_reviews_dir_and_no_critic_choice(self) -> None:
        state = pipeline_state.load_pipeline("fox-knight", self.root)
        self.assertEqual(state["reviews"], [])
        self.assertIsNone(state["critic"])
        self.assertTrue((self.work / "reviews").is_dir())

    def test_set_critic_records_choice_and_rejects_unknown(self) -> None:
        state = pipeline_state.set_critic("fox-knight", "claude", work_root=self.root)
        self.assertEqual(state["critic"], "claude")
        with self.assertRaises(ValueError):
            pipeline_state.set_critic("fox-knight", "gpt", work_root=self.root)

    def test_record_review_appends_and_history_filters_by_gate(self) -> None:
        pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict="REVISE",
                                     path="work/fox-knight/reviews/B-r0.json", open_issues=2, work_root=self.root)
        pipeline_state.record_review("fox-knight", "C", 0, critic="gemini", model="m", verdict="PASS",
                                     path="work/fox-knight/reviews/C-r0.json", open_issues=0, work_root=self.root)
        self.assertEqual(len(pipeline_state.review_history("fox-knight", work_root=self.root)), 2)
        only_b = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([(r["gate"], r["verdict"], r["open_issues"]) for r in only_b], [("B", "REVISE", 2)])

    def test_record_review_same_round_replaces_and_next_round_counts(self) -> None:
        self.assertEqual(pipeline_state.next_review_round("fox-knight", "B", self.root), 0)
        for verdict in ("REVISE", "PASS"):
            pipeline_state.record_review("fox-knight", "B", 0, critic="gemini", model="m", verdict=verdict,
                                         path="p", open_issues=0, work_root=self.root)
        history = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([r["verdict"] for r in history], ["PASS"])
        self.assertEqual(pipeline_state.next_review_round("fox-knight", "B", self.root), 1)

    def test_record_review_rejects_bad_gate_and_negative_round(self) -> None:
        with self.assertRaises(ValueError):
            pipeline_state.record_review("fox-knight", "D", 0, critic="gemini", model="m", verdict="PASS",
                                         path="p", open_issues=0, work_root=self.root)
        with self.assertRaises(ValueError):
            pipeline_state.record_review("fox-knight", "B", -1, critic="gemini", model="m", verdict="PASS",
                                         path="p", open_issues=0, work_root=self.root)

    def test_cli_set_critic_and_review_history(self) -> None:
        self.assertEqual(pipeline_state.main(["set-critic", "fox-knight", "gemini", "--work-root", self.root]), 0)
        pipeline_state.record_review("fox-knight", "A1", 0, critic="gemini", model="m", verdict="PASS",
                                     path="p", open_issues=0, work_root=self.root)
        out = io.StringIO()
        with redirect_stdout(out):
            rc = pipeline_state.main(["review-history", "fox-knight", "--gate", "A1", "--work-root", self.root])
        self.assertEqual(rc, 0)
        self.assertEqual(json.loads(out.getvalue())[0]["gate"], "A1")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run them to verify they fail**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v`
Expected: FAIL/ERROR — `KeyError: 'reviews'`, `AttributeError: ... has no attribute 'set_critic'` / `'record_review'`.

- [ ] **Step 3: Implement in `pipeline_state.py`**

Edit the constants block (after `VALID_CHECKPOINTS`):

```python
VALID_STAGES = ("concept-art", "image-to-3d", "rig-animate", "blender-finish", "done")
VALID_CHECKPOINTS = ("A", "B", "C")
VALID_GATES = ("A1", "A2", "B", "C")
VALID_CRITICS = ("gemini", "claude")
SUBDIRS = ("images", "meshy", "blender", "out", "preview", "reviews")
```

In `init_pipeline`, add two keys to the new `state` dict, directly after `"chosen_try": None,`:

```python
        "critic": None,
        "reviews": [],
```

Add these functions after `set_stage`:

```python
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
    state["reviews"] = reviews
    save_pipeline(slug, state, work_root)
    return entry


def review_history(slug: str, gate: str | None = None, work_root: str = ".") -> list[dict[str, Any]]:
    state = load_pipeline(slug, work_root)
    return [r for r in state.get("reviews", []) if gate is None or r["gate"] == gate]


def next_review_round(slug: str, gate: str, work_root: str = ".") -> int:
    rounds = [r["round"] for r in review_history(slug, gate, work_root)]
    return max(rounds) + 1 if rounds else 0
```

In `main`, add two subparsers after the `set-stage` parser:

```python
    p_critic = sub.add_parser("set-critic", help="Record the Gemini review answer (gemini or claude)")
    p_critic.add_argument("slug")
    p_critic.add_argument("critic", choices=VALID_CRITICS)
    p_critic.add_argument("--work-root", default=".")

    p_hist = sub.add_parser("review-history", help="List critic reviews, optionally for one gate")
    p_hist.add_argument("slug")
    p_hist.add_argument("--gate", choices=VALID_GATES, default=None)
    p_hist.add_argument("--work-root", default=".")
```

and two handlers before the final `return 1`:

```python
    if args.cmd == "set-critic":
        state = set_critic(args.slug, args.critic, args.work_root)
        print(f"Critic set to {state['critic']}")
        return 0

    if args.cmd == "review-history":
        print(json.dumps(review_history(args.slug, args.gate, args.work_root), indent=2))
        return 0
```

- [ ] **Step 4: Run the tests to verify they pass, and the v1 tests still pass**

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_pipeline.py" -k Unit -q
```

Expected: 6 tests OK; v1 unit tests OK.

- [ ] **Step 5: Commit**

```bash
git add plugins/idea-to-3d/skills/idea-to-3d/scripts/pipeline_state.py plugins/idea-to-3d/tests/test_critic.py
git commit -m "feat(idea-to-3d): log critic reviews and the Gemini consent in pipeline.json

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 3: Review schema and gate rubrics

**Files:**
- Create: `plugins/idea-to-3d/skills/idea-to-3d/references/review.schema.json`
- Create: `plugins/idea-to-3d/skills/idea-to-3d/references/rubrics/A1.md`, `A2.md`, `B.md`, `C.md`
- Test: `plugins/idea-to-3d/tests/test_critic.py` (append)

- [ ] **Step 1: Append the failing tests**

Append to `test_critic.py`, above the `if __name__ == "__main__":` line:

```python
class TestReferenceFiles(unittest.TestCase):
    def test_schema_is_valid_json_with_expected_shape(self) -> None:
        schema = json.loads((REFERENCES / "review.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["required"]), {"gate", "verdict", "scores", "issues"})
        self.assertEqual(schema["properties"]["gate"]["enum"], list(pipeline_state.VALID_GATES))
        issue = schema["properties"]["issues"]["items"]
        self.assertEqual(set(issue["required"]), {"id", "severity", "criterion", "evidence", "fix", "credits"})
        self.assertEqual(issue["properties"]["severity"]["enum"], ["blocker", "major", "minor"])

    def test_every_gate_has_a_rubric_with_criteria_severity_and_fixes(self) -> None:
        for gate in pipeline_state.VALID_GATES:
            text = (REFERENCES / "rubrics" / f"{gate}.md").read_text(encoding="utf-8")
            for heading in ("## Criteria", "## Severity", "## Fixes and their credits"):
                self.assertIn(heading, text, f"{gate}.md lacks {heading}")
```

- [ ] **Step 2: Run to verify they fail**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -k Reference -v`
Expected: ERROR `FileNotFoundError ... review.schema.json`.

- [ ] **Step 3: Write `review.schema.json`**

Kept to plain types and enums so Gemini structured output accepts it; `critique.py` enforces the rest.

```json
{
  "type": "object",
  "required": ["gate", "verdict", "scores", "issues"],
  "properties": {
    "gate": { "type": "string", "enum": ["A1", "A2", "B", "C"] },
    "verdict": { "type": "string", "enum": ["PASS", "REVISE"] },
    "scores": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["criterion", "score"],
        "properties": {
          "criterion": { "type": "string" },
          "score": { "type": "integer", "minimum": 1, "maximum": 5 }
        }
      }
    },
    "issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "severity", "criterion", "evidence", "fix", "credits"],
        "properties": {
          "id": { "type": "string" },
          "severity": { "type": "string", "enum": ["blocker", "major", "minor"] },
          "criterion": { "type": "string" },
          "evidence": { "type": "string" },
          "fix": { "type": "string" },
          "credits": { "type": "integer", "minimum": 0 }
        }
      }
    }
  }
}
```

- [ ] **Step 4: Write the four rubrics**

`references/rubrics/A1.md`:

````markdown
# Gate A1 — concept candidates

Inputs: `idea.md` (the brief) and `preview/concepts.png` (3–4 labelled candidates side by side).

The user will pick one candidate. Rate the gate by its **best** candidate; problems that only
affect weaker candidates are `minor`. Name the candidate in every `evidence` ("Concept 2: …").

## Criteria

Give one score (1–5) for each:

- `brief-fidelity` — silhouette, proportions, hex palette, materials and mood match `idea.md`.
- `meshy-readiness` — one subject, full body uncropped with margin, plain light background, soft light, no cast shadows, low perspective; humanoids in an A- or T-pose with arms clear of the torso and fingers apart.
- `buildability` — survives a ~40k-triangle mesh: no thin floating parts, loose hair strands, fur, smoke or transparent elements Meshy cannot model.
- `variety` — the candidates differ enough that the pick means something.

## Severity

- `blocker` — no candidate is usable (all off-brief, or all fail meshy-readiness).
- `major` — the best candidate breaks a criterion a viewer would notice (fused arms, cropped feet, wrong palette, a prop merged into the body).
- `minor` — polish, small palette drift, weak variety, problems limited to weaker candidates.

## Fixes and their credits

Use these numbers in `credits` (Meshy list prices):

- Rewrite the brief or the image prompt in `idea.md`: 0 — only useful together with a regeneration, so pair it with the next fix.
- Regenerate one concept with `meshy_text_to_image` (`nano-banana-pro`): 9 per image. Say what the new prompt must change.
- Offer a scripted Blender build instead (round, hard-surface, symmetric subjects): 0.

Write `fix` as a concrete change ("regenerate Concept 3 with arms 20° away from the torso"), never "improve quality".
````

`references/rubrics/A2.md`:

````markdown
# Gate A2 — turnaround views for Meshy

Inputs: `idea.md`, `images/front.png`, `images/side.png`, `images/back.png`.

These three images go to `meshy_multi_image_to_3d` next, which costs 15–30 credits per try.
Judge them as Meshy input: anything Meshy would misread becomes a bad mesh.

## Criteria

Give one score (1–5) for each:

- `one-view-each` — each image holds exactly one view (no grids, no extra figures, no text).
- `consistency` — side and back show the same character as the front: proportions, palette, costume, props, height in frame.
- `orthographic` — front is straight on, side is a 90° profile, back is 180°; low perspective distortion.
- `meshy-readiness` — full body centred with margin, plain light grey background, soft even light, no cast shadows; humanoids in the same A- or T-pose in all three.

## Severity

- `blocker` — an image is unusable (wrong view, multi-panel, a different character).
- `major` — a mismatch Meshy will bake in (a prop missing in one view, pose differs, cropped limb, heavy shadow).
- `minor` — small colour or lighting drift, tight margins.

## Fixes and their credits

- Crop, pad, recentre, or flatten the background with Pillow: 0.
- Regenerate one view with `meshy_image_to_image` (`nano-banana-pro`, `reference_file_paths` = chosen concept + `front.png`): 9 per image. Say which view and what must change.

Write `evidence` as "<view>: <what you see>".
````

`references/rubrics/B.md`:

````markdown
# Gate B — Meshy image-to-3D tries

Inputs: `idea.md`, `images/front.png` (the approved front view), `preview/tries.png` (each try
rendered front, three-quarter, side and a face close-up, labelled "Try 1", "Try 2").

Judge each try against the front view and the brief. Rate the gate by its **best** try:
issues on the weaker try are `minor` unless no try is usable.

## Criteria

Give one score (1–5) for each:

- `geometry` — silhouette and proportions match the front view from every angle; nothing missing or extra.
- `artifacts` — no holes, melted or smeared face or hands, fused limbs or fingers, floating fragments, spikes, paper-thin parts.
- `texture` — colours match the brief's hex palette; no smeared, mirrored or misplaced texture.
- `symmetry` — left and right match where the design is symmetric.
- `rig-readiness` — humanoids: clear A- or T-pose, limbs separated from the body, hands open; non-humanoids: parts that must move are separate enough to bend.

## Severity

- `blocker` — no try can go on to rigging (both have a melted face, fused arms, or large holes).
- `major` — the best try has a defect a viewer notices at full-body size.
- `minor` — close-up flaws, small colour drift, defects only on the weaker try.

## Fixes and their credits

- Pick the other try: 0 — say which and why.
- Clean or recrop the input images before a re-run: 0, but it only helps together with a new try.
- New try with `meshy_multi_image_to_3d`, `meshy-7.1`, 4K texture: 30. Name the setting or input to change (for example `pose_mode: "a-pose"`, a regenerated side view).
- New tracer try with `meshy-6-lite`: 15.

Write `evidence` as "Try N, <view>: <what you see>". One issue per defect.
````

`references/rubrics/C.md`:

````markdown
# Gate C — rig, clips and Blender finish

Inputs: `idea.md`, `images/front.png`, `preview/sheet.png` (concept column, then 4 views ×
start/mid/end frames for each clip), `out/quality_report.json` (the `check-glb.py` result).

## Criteria

Give one score (1–5) for each:

- `checks` — every check in `quality_report.json` passes (scale, triangles, size, clips, materials).
- `deformation` — in every clip frame: no tearing, candy-wrapper twists, collapsed shoulders or hips, limbs passing through the body.
- `clip-readability` — each clip reads as its name (idle breathes, walk steps, wave waves) from the front and three-quarter views.
- `placement` — the model stands on the ground, faces front, and its height matches `idea.md`.
- `texture-seams` — no visible seams, stretched UVs or missing texture regions.

## Severity

- `blocker` — any failed check in `quality_report.json`, or a clip that tears the mesh.
- `major` — visible deformation or a clip that does not read as its name.
- `minor` — small seams, slight foot sliding, subtle interpenetration.

## Fixes and their credits

- Re-run `import-merge.py` with different options, then `export-check.py` and `render-sheet.py`: 0. Name the option: `--height <m>`, `--max-triangles <n>`, `--clips <list>`, `--procedural-rig` (non-humanoids, or when the Meshy rig tears), `--scripted-robot`.
- Re-rig with `meshy_rig`: 5.
- Re-animate one clip with `meshy_animate`: 3 per action. Name the action.
- A fix that needs a code change to a plugin script: credits 0 and start `fix` with "needs plugin change:" — the reviser cannot apply it and it stays open at the checkpoint.

Write `evidence` as "<clip>, <view>, <frame>: <what you see>" or "quality_report: <check>".
````

- [ ] **Step 5: Run to verify the tests pass**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v`
Expected: 8 tests OK.

- [ ] **Step 6: Commit**

```bash
git add plugins/idea-to-3d/skills/idea-to-3d/references plugins/idea-to-3d/tests/test_critic.py
git commit -m "feat(idea-to-3d): add the review schema and the four gate rubrics

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 4: `critique.py` and the fake `agy`

**Files:**
- Create: `plugins/idea-to-3d/skills/idea-to-3d/scripts/critique.py`
- Create: `plugins/idea-to-3d/tests/fake_agy.py`
- Test: `plugins/idea-to-3d/tests/test_critic.py` (append)

- [ ] **Step 1: Write the fake `agy`**

`plugins/idea-to-3d/tests/fake_agy.py`:

```python
#!/usr/bin/env python3
"""
Stand-in for the Antigravity CLI (`agy`) in tests. Behaviour comes from FAKE_AGY_MODE:
ok | pass | response-only | bad | bad-then-ok | nonzero | not-success | sleep.
When FAKE_AGY_LOG is set, each call appends its argv to it as one JSON line.
"""
import json
import os
import re
import sys
import time


def review(gate: str, verdict: str) -> dict:
    issues = [] if verdict == "PASS" else [{
        "id": f"{gate}-1", "severity": "major", "criterion": "geometry",
        "evidence": "Try 2, side: left hand fused to the hip",
        "fix": "new try with pose_mode a-pose", "credits": 30,
    }]
    return {"gate": gate, "verdict": verdict,
            "scores": [{"criterion": "geometry", "score": 2}], "issues": issues}


def main() -> int:
    argv = sys.argv[1:]
    prompt = argv[argv.index("-p") + 1]
    mode = os.environ.get("FAKE_AGY_MODE", "ok")
    calls = 1
    log = os.environ.get("FAKE_AGY_LOG")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(json.dumps(argv) + "\n")
        with open(log, encoding="utf-8") as f:
            calls = sum(1 for _ in f)
    match = re.search(r'"gate" must be "(\w+)"', prompt)
    gate = match.group(1) if match else "B"

    if mode == "nonzero":
        print("Error authenticating: not logged in", file=sys.stderr)
        return 1
    if mode == "not-success":
        print(json.dumps({"status": "ERROR", "response": ""}))
        return 0
    if mode == "sleep":
        time.sleep(5)
        return 0
    if mode == "bad" or (mode == "bad-then-ok" and calls == 1):
        print(json.dumps({"status": "SUCCESS", "response": "looks fine",
                          "structured_output": {"gate": gate, "verdict": "PASS"}}))
        return 0
    body = review(gate, "PASS" if mode == "pass" else "REVISE")
    if mode == "response-only":
        print(json.dumps({"status": "SUCCESS", "response": "I will read the files.\n" + json.dumps(body)}))
        return 0
    print(json.dumps({"status": "SUCCESS", "response": json.dumps(body), "structured_output": body}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 2: Append the failing tests**

Append to `test_critic.py`, above `if __name__ == "__main__":`. Also add `critique = load_module("critique_under_test", SCRIPTS / "critique.py")` directly below the existing `pipeline_state = load_module(...)` line at the top of the file.

```python
def valid_review(gate: str = "B", verdict: str = "REVISE") -> dict:
    issues = [] if verdict == "PASS" else [{
        "id": f"{gate}-1", "severity": "major", "criterion": "geometry",
        "evidence": "Try 2, side: left hand fused to the hip",
        "fix": "new try with pose_mode a-pose", "credits": 30,
    }]
    return {"gate": gate, "verdict": verdict,
            "scores": [{"criterion": "geometry", "score": 2}], "issues": issues}


class TestValidateReview(unittest.TestCase):
    def test_valid_revise_and_pass_are_accepted(self) -> None:
        self.assertEqual(critique.validate_review(valid_review(), "B"), [])
        self.assertEqual(critique.validate_review(valid_review(verdict="PASS"), "B"), [])

    def test_pass_with_major_issue_is_rejected(self) -> None:
        review = valid_review()
        review["verdict"] = "PASS"
        self.assertTrue(any("PASS is not allowed" in e for e in critique.validate_review(review, "B")))

    def test_revise_without_issues_is_rejected(self) -> None:
        review = valid_review(verdict="PASS")
        review["verdict"] = "REVISE"
        self.assertTrue(any("REVISE needs" in e for e in critique.validate_review(review, "B")))

    def test_bad_score_credits_gate_and_type_are_rejected(self) -> None:
        review = valid_review()
        review["scores"][0]["score"] = True
        review["issues"][0]["credits"] = -5
        errors = critique.validate_review(review, "C")
        self.assertTrue(any("scores[0]" in e for e in errors))
        self.assertTrue(any("credits" in e for e in errors))
        self.assertTrue(any('"gate" must be "C"' in e for e in errors))
        self.assertEqual(critique.validate_review(["not", "an", "object"], "B"), ["review must be a JSON object"])

    def test_gate_lists_match_pipeline_state(self) -> None:
        self.assertEqual(tuple(critique.GATE_INPUTS), pipeline_state.VALID_GATES)


class TestAgyParsing(unittest.TestCase):
    def test_last_json_object_returns_the_outer_object(self) -> None:
        text = 'I will read it.\n{"a": {"b": 1}} trailing'
        self.assertEqual(critique.last_json_object(text), {"a": {"b": 1}})
        self.assertIsNone(critique.last_json_object("no json here"))

    def test_parse_prefers_structured_output_then_response(self) -> None:
        body = valid_review()
        both = json.dumps({"status": "SUCCESS", "response": "x", "structured_output": body})
        self.assertEqual(critique.parse_agy_output(both), body)
        only_text = json.dumps({"status": "SUCCESS", "response": "Reading.\n" + json.dumps(body)})
        self.assertEqual(critique.parse_agy_output(only_text), body)

    def test_parse_raises_on_failure_status_or_garbage(self) -> None:
        with self.assertRaises(critique.CriticUnavailable):
            critique.parse_agy_output(json.dumps({"status": "ERROR"}))
        with self.assertRaises(critique.CriticUnavailable):
            critique.parse_agy_output("Loaded cached credentials. Error")

    def test_agy_command_uses_env_then_path(self) -> None:
        with mock.patch.dict(os.environ, {"IDEA3D_AGY": r"C:\tools\agy.exe"}):
            self.assertEqual(critique.agy_command(), [r"C:\tools\agy.exe"])
        with mock.patch.dict(os.environ, {"IDEA3D_AGY": ""}), \
                mock.patch.object(critique.shutil, "which", return_value=None):
            with self.assertRaises(critique.CriticUnavailable):
                critique.agy_command()


class TestCritiqueRun(TempPipelineCase):
    def setUp(self) -> None:
        super().setUp()
        pipeline_state.set_critic("fox-knight", "gemini", work_root=self.root)
        (self.work / "idea.md").write_text("# Fox knight\nHeight: 1.2 m\n", encoding="utf-8")
        (self.work / "images" / "front.png").write_bytes(PNG_BYTES)
        (self.work / "preview" / "tries.png").write_bytes(PNG_BYTES)
        self.log = self.tmp / "agy.log"
        self.env = mock.patch.dict(os.environ, {"FAKE_AGY_LOG": str(self.log), "IDEA3D_CRITIC_MODEL": ""})
        self.env.start()

    def tearDown(self) -> None:
        self.env.stop()
        super().tearDown()

    def run_critic(self, mode: str, *extra: str, prefix: list[str] | None = None) -> int:
        os.environ["FAKE_AGY_MODE"] = mode
        argv = ["fox-knight", "B", "--work-root", self.root, *extra]
        with redirect_stdout(io.StringIO()):
            return critique.main(argv, cmd_prefix=prefix or [sys.executable, str(FAKE_AGY)])

    def calls(self) -> list[list[str]]:
        if not self.log.exists():
            return []
        return [json.loads(line) for line in self.log.read_text(encoding="utf-8").splitlines()]

    def test_valid_review_is_written_and_recorded(self) -> None:
        self.assertEqual(self.run_critic("ok"), 0)
        saved = json.loads((self.work / "reviews" / "B-r0.json").read_text(encoding="utf-8"))
        self.assertEqual((saved["round"], saved["critic"], saved["model"]), (0, "gemini", "gemini-4-argon-medium"))
        history = pipeline_state.review_history("fox-knight", "B", work_root=self.root)
        self.assertEqual([(h["verdict"], h["open_issues"]) for h in history], [("REVISE", 1)])

    def test_agy_is_called_read_only_with_schema_and_work_dir(self) -> None:
        self.run_critic("ok")
        argv = self.calls()[0]
        for flag, value in (("--mode", "plan"), ("--output-format", "json"),
                            ("--model", "gemini-4-argon-medium"), ("--add-dir", str(self.work))):
            self.assertEqual(argv[argv.index(flag) + 1], value)
        self.assertIn("--disable-slash-commands", argv)
        self.assertTrue(argv[argv.index("--json-schema") + 1].endswith("review.schema.json"))
        prompt = argv[argv.index("-p") + 1]
        self.assertIn(str(self.work / "preview" / "tries.png"), prompt)
        self.assertIn("Gate B", prompt)

    def test_round_defaults_to_the_next_round(self) -> None:
        self.run_critic("ok")
        self.assertEqual(self.run_critic("pass"), 0)
        self.assertTrue((self.work / "reviews" / "B-r1.json").is_file())

    def test_response_text_is_used_when_structured_output_is_missing(self) -> None:
        self.assertEqual(self.run_critic("response-only"), 0)

    def test_invalid_review_is_retried_once_with_the_errors(self) -> None:
        self.assertEqual(self.run_critic("bad-then-ok"), 0)
        calls = self.calls()
        self.assertEqual(len(calls), 2)
        self.assertIn("rejected", calls[1][calls[1].index("-p") + 1])

    def test_invalid_twice_exits_3_and_writes_nothing(self) -> None:
        self.assertEqual(self.run_critic("bad"), 3)
        self.assertFalse((self.work / "reviews" / "B-r0.json").exists())

    def test_unavailable_critic_exits_2(self) -> None:
        self.assertEqual(self.run_critic("nonzero"), 2)
        self.assertEqual(self.run_critic("not-success"), 2)
        self.assertEqual(self.run_critic("sleep", "--timeout", "1"), 2)
        self.assertEqual(self.run_critic("ok", prefix=[str(self.tmp / "no-such-agy.exe")]), 2)

    def test_missing_input_or_consent_is_a_usage_error(self) -> None:
        (self.work / "preview" / "tries.png").unlink()
        self.assertEqual(self.run_critic("ok"), 1)
        (self.work / "preview" / "tries.png").write_bytes(PNG_BYTES)
        state = pipeline_state.load_pipeline("fox-knight", self.root)
        state["critic"] = None
        pipeline_state.save_pipeline("fox-knight", state, self.root)
        self.assertEqual(self.run_critic("ok"), 1)
        self.assertEqual(self.calls(), [])

    def test_claude_choice_skips_gemini_with_exit_2(self) -> None:
        pipeline_state.set_critic("fox-knight", "claude", work_root=self.root)
        self.assertEqual(self.run_critic("ok"), 2)
        self.assertEqual(self.calls(), [])

    def test_from_file_records_a_claude_fallback_review(self) -> None:
        raw = self.tmp / "raw.json"
        raw.write_text(json.dumps(valid_review(verdict="PASS")), encoding="utf-8")
        rc = self.run_critic("ok", "--from-file", str(raw), "--critic", "claude-fallback", "--reason", "exit 2: timeout")
        self.assertEqual(rc, 0)
        saved = json.loads((self.work / "reviews" / "B-r0.json").read_text(encoding="utf-8"))
        self.assertEqual((saved["critic"], saved["reason"]), ("claude-fallback", "exit 2: timeout"))
        self.assertEqual(self.calls(), [])

    def test_from_file_with_an_invalid_review_exits_3(self) -> None:
        raw = self.tmp / "raw.json"
        raw.write_text('{"gate": "B", "verdict": "PASS"}', encoding="utf-8")
        self.assertEqual(self.run_critic("ok", "--from-file", str(raw), "--critic", "claude-fallback"), 3)

    def test_bad_arguments_exit_1_not_2(self) -> None:
        with self.assertRaises(SystemExit) as ctx, mock.patch("sys.stderr", io.StringIO()):
            critique.main(["fox-knight", "Z", "--work-root", self.root])
        self.assertEqual(ctx.exception.code, 1)
```

- [ ] **Step 3: Run to verify they fail**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v`
Expected: ERROR at import — `FileNotFoundError` / `No such file ... critique.py`.

- [ ] **Step 4: Write `critique.py`**

`plugins/idea-to-3d/skills/idea-to-3d/scripts/critique.py`:

```python
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
    "A2": ("idea.md", "images/front.png", "images/side.png", "images/back.png"),
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
```

- [ ] **Step 5: Run to verify the tests pass**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v`
Expected: all tests OK (about 30). The timeout test takes ~1 s.

- [ ] **Step 6: Live smoke test against the real `agy` (free; uses the Antigravity quota)**

This proves `agy` accepts `review.schema.json` and reads PNGs. Save as `smoke_critic.py` in the session scratchpad and run it from the marketplace root with `python smoke_critic.py` (Bash `timeout: 600000`):

```python
"""Live check: one gate-B review of two synthetic images through the real agy CLI."""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

SCRIPTS = Path("plugins/idea-to-3d/skills/idea-to-3d/scripts").resolve()
root = Path(tempfile.mkdtemp(prefix="critic_smoke_"))
run = lambda *a: subprocess.run([sys.executable, *a], check=True)
run(str(SCRIPTS / "pipeline_state.py"), "init", "red-ball", "--idea", "A red rubber ball",
    "--height", "0.3", "--non-humanoid", "--work-root", str(root))
run(str(SCRIPTS / "pipeline_state.py"), "set-critic", "red-ball", "gemini", "--work-root", str(root))
work = root / "work" / "red-ball"
(work / "idea.md").write_text("# Red ball\nA glossy red (#D92020) rubber ball. Height: 0.3 m\n", encoding="utf-8")
front = Image.new("RGB", (512, 512), (216, 216, 220))
ImageDraw.Draw(front).ellipse((96, 96, 416, 416), fill=(217, 32, 32))
front.save(work / "images" / "front.png")
tries = Image.new("RGB", (1024, 512), (216, 216, 220))
d = ImageDraw.Draw(tries)
d.ellipse((96, 96, 416, 416), fill=(217, 32, 32))
d.ellipse((608, 96, 928, 416), fill=(40, 90, 220))
d.text((200, 460), "Try 1", fill=(0, 0, 0))
d.text((712, 460), "Try 2", fill=(0, 0, 0))
tries.save(work / "preview" / "tries.png")
proc = subprocess.run([sys.executable, str(SCRIPTS / "critique.py"), "red-ball", "B", "--work-root", str(root)],
                      capture_output=True, text=True)
print("exit", proc.returncode)
print(proc.stdout or proc.stderr)
if proc.returncode == 0:
    print(Path(proc.stdout.strip()).read_text(encoding="utf-8"))
```

Expected: `exit 0`, a review path, and a review whose issues mention Try 2 being blue rather than red. If `exit 2` with a schema complaint from `agy` in stderr, remove `minimum`/`maximum` from `review.schema.json` (the validator still enforces them), rerun the unit tests, then rerun this smoke test. Record the outcome (exit code, duration, verdict) in the Task 4 commit message body.

- [ ] **Step 7: Commit**

```bash
git add plugins/idea-to-3d/skills/idea-to-3d/scripts/critique.py plugins/idea-to-3d/tests
git commit -m "feat(idea-to-3d): add critique.py, the Gemini critic run through agy

Live smoke on a synthetic gate-B pair: <exit code, seconds, verdict>.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

(Replace the `<...>` line with the smoke-test result before committing.)

---

### Task 5: Loop protocol and role briefs

**Files:**
- Create: `plugins/idea-to-3d/skills/idea-to-3d/references/loop.md`
- Create: `plugins/idea-to-3d/skills/idea-to-3d/references/roles/maker.md`, `reviser.md`, `critic.md`
- Test: `plugins/idea-to-3d/tests/test_critic.py` (append)

- [ ] **Step 1: Append the failing test**

Above `if __name__ == "__main__":`:

```python
class TestCoreIsPlatformNeutral(unittest.TestCase):
    PLATFORM_TOOLS = ("AskUserQuestion", "ask_question", "view_file", "image-generator", "send_message")

    def test_loop_and_roles_exist_and_name_no_platform_tool(self) -> None:
        files = [REFERENCES / "loop.md"] + [REFERENCES / "roles" / f"{r}.md" for r in ("maker", "reviser", "critic")]
        files += sorted((REFERENCES / "rubrics").glob("*.md"))
        for path in files:
            text = path.read_text(encoding="utf-8")
            for tool in self.PLATFORM_TOOLS:
                self.assertNotIn(tool, text, f"{path.name} names {tool}")
```

- [ ] **Step 2: Run to verify it fails**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -k Neutral -v`
Expected: ERROR `FileNotFoundError ... loop.md`.

- [ ] **Step 3: Write `references/loop.md`**

````markdown
# Critic loop protocol

Every stage's output is judged by an independent critic and revised before the user sees
it. This file is shared by the Claude Code and Antigravity copies of the plugin, so it never
names a platform tool: "ask the user" means the platform's question tool, "dispatch" means
its subagent tool, as mapped in the orchestrator's Platform section.

## Gates

| Gate | Runs | Critic inputs (under `work/<slug>/`) |
|---|---|---|
| A1 | after the concept candidates, before Checkpoint A | `idea.md`, `preview/concepts.png` |
| A2 | after the turnarounds, before Stage 2 spends credits | `idea.md`, `images/front.png`, `images/side.png`, `images/back.png` |
| B | after the Meshy tries, before Checkpoint B | `idea.md`, `images/front.png`, `preview/tries.png` |
| C | after the Blender finish, before Checkpoint C (also judges Stage 3's rig and clips) | `idea.md`, `images/front.png`, `preview/sheet.png`, `out/quality_report.json` |

Rubrics: `references/rubrics/<gate>.md`. Schema: `references/review.schema.json`.

## Before the first gate

Record the user's answer to the Gemini question (asked together with the first Meshy
consent): `pipeline_state.py set-critic <slug> gemini` or `... claude`. `critique.py`
refuses to run until it is recorded.

## Steps at each gate

Round `r` starts at 0.

1. **Critique.** Run `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>`. It can take several minutes; allow up to 10. It prints the review path.
   - exit 0: read the review.
   - exit 2 or 3: dispatch the critic role (`roles/critic.md`) with the gate, the rubric path, the input files and the output path `work/<slug>/reviews/<gate>-r<r>.raw.json`. Then run `critique.py <slug> <gate> --from-file <raw path> --critic claude-fallback --reason "exit <code>: <first stderr line>"`. If that also fails, go to the checkpoint and say the gate is unreviewed.
   - exit 1: an input is missing or consent is not recorded. Fix that and rerun.
2. **PASS** → go to the checkpoint.
3. **REVISE and r < 2** → dispatch the reviser (`roles/reviser.md`) with the review path.
   - If the reviser returns `paid_requests`, ask the user once for all of them: one option per request (tool, model, credits, issue it fixes, recommended first: the one fixing the most severe issue) plus "Skip paid fixes". For each approved request, dispatch the maker with that request as its budget.
   - If nothing changed a gate input (no free fix applied, no paid fix approved), stop and go to the checkpoint — critiquing unchanged files again wastes a round.
   - Otherwise set r = r + 1 and go back to step 1.
4. **REVISE and r = 2** → go to the checkpoint with the open issues.

## At the checkpoint

Show one short gate summary next to the usual checkpoint content:

```
Gate B: r0 gemini REVISE (1 blocker, 1 major) → fixed B-2 free; new try approved (30 cr)
        r1 gemini PASS. Open issues: none. Fix credits spent: 30.
```

List every open issue with severity, evidence and the suggested fix with its credits.

## Rules

- **Independence.** The critic receives files only — never the maker's or reviser's messages, never `pipeline.json` notes. The orchestrator never judges a gate itself.
- **Credits.** `credits` in a review are Meshy list prices. If the platform has a cheaper route for the same fix (a free image generator), use it; the fix then needs no approval. Every other credit-spending fix needs the user's yes in this run, and the maker may spend only what was approved.
- **Idempotency.** Paid fixes follow the pipeline rules: read `pipeline.json` before any Meshy create call and record every `task_id` the moment it exists.
- **Resume.** `pipeline_state.py review-history <slug>` shows the last gate and round; continue from there.
````

- [ ] **Step 4: Write the three role briefs**

`references/roles/maker.md`:

````markdown
# Role: maker

You run one stage of the idea-to-3d pipeline and nothing else. You never ask the user
anything and you never judge your own output.

## Your dispatch prompt gives you

- `slug`, `work_root`, `plugin_root`
- `stage_skill`: path to the stage `SKILL.md` to follow (concept-art, image-to-3d, rig-animate or blender-finish) and which of its steps to run
- `budget`: the credit-spending calls the user approved, each with tool, model, settings and credits — or "none"
- for a paid fix: the approved request (issue id, tool, model, settings, credits)

## Rules

1. Read `<plugin_root>/skills/idea-to-3d/references/rules.md` and the stage skill first.
2. Run only the steps named in your prompt. Stop before the stage's checkpoint step: the orchestrator runs the gate and the checkpoint.
3. Skip any "ask the user" step in the stage skill — the orchestrator already asked. If the approval you need is not in your `budget`, stop and report what is missing.
4. Spend only your `budget`. Before every Meshy create call, check `pipeline_state.py get-task <slug> <step_key>`; if the task exists, poll it instead. Record every new `task_id` with `record-task` the moment it is created.
5. Do not read `work/<slug>/reviews/`. A paid fix tells you exactly what to change.

## Final message

Only this JSON:

```json
{"stage": "<stage>", "artifacts": ["work/<slug>/..."], "credits_spent": 0,
 "tasks": ["<step_key>"], "notes": "<anything the orchestrator must know>"}
```
````

`references/roles/reviser.md`:

````markdown
# Role: reviser

You fix what the critic found, using free means only. You never spend Meshy credits and
never ask the user.

## Your dispatch prompt gives you

- `slug`, `work_root`, `plugin_root`, `gate`, `round`
- `review`: path to `work/<slug>/reviews/<gate>-r<round>.json`
- `rubric`: path to `references/rubrics/<gate>.md` (its "Fixes and their credits" list is your toolbox)
- `stage_skill`: path to the stage `SKILL.md` (for the preview command)

## Rules

1. Read the review, the rubric, `references/rules.md`, and the stage skill.
2. Before changing any file, copy it to `work/<slug>/reviews/backup-<gate>-r<round>/` (keep its relative path).
3. For each issue with `credits: 0`: apply the fix with free means only — edit `idea.md` or a prompt, clean or crop images with Pillow, rerun headless Blender scripts with different options, or note that the other try should be picked. A fix starting "needs plugin change:" is out of reach: put it under `declined`.
4. For each issue with `credits > 0`: do not fix it. Write a paid request with the exact tool, model, settings and credits. If a free fix solves the same issue, apply that instead and say so.
5. If a fix fails (a script exits non-zero), restore the backed-up files, and list it under `failed` with the first error line.
6. After your fixes, regenerate the gate's preview with the stage skill's command (A1 `make-concept-sheet.py`, A2 the turnaround sheet, B `render-meshy.py`, C `export-check.py` then `render-sheet.py`) so the critic sees the change.
7. Never edit plugin files, never touch `pipeline.json` tasks, never call a Meshy tool that costs credits.

## Final message

Only this JSON:

```json
{"gate": "B", "round": 0,
 "applied": [{"issue": "B-2", "change": "<what you did>", "files": ["work/<slug>/..."]}],
 "paid_requests": [{"issue": "B-1", "tool": "meshy_multi_image_to_3d", "model": "meshy-7.1",
                    "settings": {"pose_mode": "a-pose"}, "credits": 30, "why": "<what it fixes>"}],
 "declined": [{"issue": "C-3", "reason": "needs plugin change"}],
 "failed": [{"issue": "C-1", "error": "<first error line>"}],
 "inputs_changed": true}
```

`inputs_changed` is true only if a file the critic reads for this gate changed.
````

`references/roles/critic.md`:

````markdown
# Role: critic (fallback)

You stand in for the Gemini critic when `critique.py` cannot reach it. You judge files
only. You did not make this work and owe it nothing.

## Your dispatch prompt gives you

- `gate`, `rubric` (path), `inputs` (absolute paths), `out` (where to write your review)

## Rules

1. Read the rubric and every input file; open each image and look at it closely.
2. Do not read `work/<slug>/reviews/`, `pipeline.json`, or any message from the maker or reviser. Do not look for earlier reviews.
3. Write exactly one JSON object to `out`, matching `references/review.schema.json`:
   `gate`, `verdict` (`PASS`/`REVISE`), `scores` (one `{criterion, score 1–5}` per rubric criterion), `issues` (each with `id`, `severity`, `criterion`, `evidence`, `fix`, `credits`).
4. PASS is not allowed while any blocker or major issue is listed. REVISE needs at least one issue. `credits` is 0 for a free fix, else the rubric's price.
5. Evidence names the image and what is visible in it. Fixes are concrete changes.

## Final message

Only the path you wrote.
````

- [ ] **Step 5: Run the test to verify it passes**

Run: `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v`
Expected: all tests OK.

- [ ] **Step 6: Commit**

```bash
git add plugins/idea-to-3d/skills/idea-to-3d/references plugins/idea-to-3d/tests/test_critic.py
git commit -m "feat(idea-to-3d): add the critic loop protocol and the maker, reviser, critic briefs

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 6: Claude Code agent wrappers

**Files:**
- Create: `plugins/idea-to-3d/agents/idea3d-maker.md`, `idea3d-reviser.md`, `idea3d-critic.md`

- [ ] **Step 1: Write the three agents**

`agents/idea3d-maker.md` (no `tools` line: it inherits all tools, including the `meshy` MCP server):

```markdown
---
name: idea3d-maker
description: Runs one idea-to-3d stage (concept art, image-to-3D, rig and animate, or Blender finish) inside a Meshy credit budget the user already approved, and returns the artifact paths as JSON. Dispatched only by the idea-to-3d orchestrator; never asks the user and never judges its own output.
---

Your dispatch prompt names your role file (`.../skills/idea-to-3d/references/roles/maker.md`).
Read it before anything else and follow it exactly; it overrides any habit of yours.
Everything you need (slug, work root, plugin root, stage skill, budget) is in the dispatch
prompt. If any of it is missing, reply with the JSON the role file defines and put what is
missing in `notes`.
```

`agents/idea3d-reviser.md` (no Meshy tools, so it cannot spend credits):

```markdown
---
name: idea3d-reviser
description: Applies the free fixes from an idea-to-3d critic review (brief and prompt edits, Pillow image cleanup, headless Blender re-runs), re-renders the gate preview, and returns paid fixes as requests for the user to approve. Dispatched only by the idea-to-3d orchestrator; it has no Meshy tools and never spends credits.
tools: Bash, Read, Write, Edit, Glob, Grep
---

Your dispatch prompt names your role file (`.../skills/idea-to-3d/references/roles/reviser.md`).
Read it before anything else and follow it exactly. Back up every file before you change
it, and reply only with the JSON the role file defines.
```

`agents/idea3d-critic.md`:

```markdown
---
name: idea3d-critic
description: Fallback critic for an idea-to-3d gate when the Gemini critic (critique.py via the Antigravity CLI) is unavailable or the user declined Gemini. Judges only the gate's files against the gate rubric and writes one review JSON. Dispatched only by the idea-to-3d orchestrator.
tools: Read, Write, Glob
---

Your dispatch prompt names your role file (`.../skills/idea-to-3d/references/roles/critic.md`).
Read it before anything else and follow it exactly. Judge only the files listed in your
prompt; do not look for earlier reviews or notes.
```

- [ ] **Step 2: Validate**

Run: `bash scripts/health.sh --fast`
Expected: `health: OK` (validate.py checks each agent has a description ≤ 1024 chars).

- [ ] **Step 3: Commit**

```bash
git add plugins/idea-to-3d/agents
git commit -m "feat(idea-to-3d): add the maker, reviser and critic agents

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 7: Gate notes in the four stage skills

**Files:**
- Modify: `plugins/idea-to-3d/skills/{concept-art,image-to-3d,rig-animate,blender-finish}/SKILL.md`

- [ ] **Step 1: Insert the notes**

Save as `gate_notes.py` in the scratchpad (Task 11 reuses it on the Antigravity repo) and run `python gate_notes.py plugins/idea-to-3d`:

```python
"""Insert the critic-loop gate note into the four idea-to-3d stage skills. Usage: gate_notes.py <plugin dir>"""
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
LOOP = "`../idea-to-3d/references/loop.md`"
NOTES = {
    "concept-art": (r"^## Step 3: Checkpoint A",
                    f"> **Critic loop:** under the orchestrator, gate A1 ({LOOP}) runs before this checkpoint "
                    "and gate A2 runs after Step 4. A maker subagent stops here and hands back to the orchestrator.\n\n"),
    "image-to-3d": (r"^## Step 4: Checkpoint B",
                    f"> **Critic loop:** under the orchestrator, gate B ({LOOP}) runs before this checkpoint, "
                    "and Step 1's consent and credit question was already asked at Checkpoint A. "
                    "A maker subagent stops here.\n\n"),
    "blender-finish": (r"^### Step 4: Inspection Gate & Checkpoint C",
                       f"> **Critic loop:** under the orchestrator, gate C ({LOOP}) runs before this checkpoint; "
                       "it also judges Stage 3's rig and clips. A maker subagent stops here.\n\n"),
}
for skill, (heading, note) in NOTES.items():
    path = root / "skills" / skill / "SKILL.md"
    text = path.read_text(encoding="utf-8")
    if "**Critic loop:**" in text:
        continue
    m = re.search(heading, text, re.M)
    if not m:
        sys.exit(f"{skill}: heading {heading!r} not found")
    path.write_text(text[: m.start()] + note + text[m.start():], encoding="utf-8", newline="\n")

rig = root / "skills" / "rig-animate" / "SKILL.md"
text = rig.read_text(encoding="utf-8")
if "**Critic loop:**" not in text:
    text = text.rstrip("\n") + (f"\n\n> **Critic loop:** Stage 3 has no gate of its own. Its rig and clips are judged "
                                f"at gate C ({LOOP}) once Blender renders them; re-rig and re-animate fixes come back "
                                "from there as paid requests.\n")
    rig.write_text(text, encoding="utf-8", newline="\n")
print("gate notes: ok")
```

Expected: `gate notes: ok`; `grep -c "Critic loop" plugins/idea-to-3d/skills/*/SKILL.md` shows 1 for each of the four stage skills.

- [ ] **Step 2: Commit**

```bash
bash scripts/health.sh --fast
git add plugins/idea-to-3d/skills
git commit -m "docs(idea-to-3d): point each stage skill at its critic gate

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 8: Orchestrator `SKILL.md` with the loop wired in

**Files:**
- Modify (full rewrite): `plugins/idea-to-3d/skills/idea-to-3d/SKILL.md`

Everything platform-specific sits between `<!-- platform:begin -->` and `<!-- platform:end -->`; Task 11 swaps only that block for Antigravity.

- [ ] **Step 1: Replace the file with this content**

`````markdown
---
name: idea-to-3d
description: Turns a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) plus a preview sheet (/idea-to-3d). Use when the user wants a 3D character, prop, mascot or figure made from an idea or a concept image, says "make this a 3D model", "idea to 3D", "rig and animate it", or resumes a work/<slug> pipeline. Runs concept art, image-to-3D, remesh/rig/animation on Meshy and headless Blender finishing across three user checkpoints; before each one an independent Gemini critic (Antigravity CLI, Claude fallback) reviews the stage and a reviser fixes it. Spends Meshy credits only after explicit approval. Not for 3D-printing prep or hand-editing an open Blender scene.
---

# Idea to 3D Orchestrator (`/idea-to-3d`)

Turns a one-line idea into an animated `.glb` (`work/<slug>/out/<slug>.glb`) and a preview
sheet (`work/<slug>/preview/sheet.png`). Every stage's output is judged by an independent
critic and revised before the user sees it.

```text
idea → Stage 1 concepts ─ gate A1 ─ [Checkpoint A] ─ turnarounds ─ gate A2
     → Stage 2 image-to-3D ─ gate B ─ [Checkpoint B]
     → Stage 3 remesh, rig, clips → Stage 4 Blender finish ─ gate C ─ [Checkpoint C]

gate = critique.py (Gemini) → reviser (free fixes) → paid fixes only after a yes
       → critique again; ends on PASS or after 2 revise rounds
```

Before starting, read [references/rules.md](references/rules.md) (credits, idempotency,
consent, Blender discipline — binding at every stage) and
[references/loop.md](references/loop.md) (the gate protocol).

<!-- platform:begin -->
## Platform: Claude Code

- `<plugin_root>` is this plugin's directory: two levels above this skill's base directory. Use absolute paths in every command.
- **Ask the user** = `AskUserQuestion`, recommended option first with a label ending in "(Recommended)". Only you (the main thread) ask; subagents cannot.
- **Look at a PNG** = `Read` on the file.
- **Image route** (concepts, turnarounds, image fixes): Meshy `nano-banana-pro` at 9 credits per image — `meshy_text_to_image` for concepts, `meshy_image_to_image` with `reference_file_paths` for turnarounds and fixes. A turnaround set is 3 images = 27 credits. Every image costs credits, so every image fix is a paid request.
- **Roles:**

| Role | Run it as | Credits |
|---|---|---|
| maker | `Agent` with `subagent_type: "idea-to-3d:idea3d-maker"`; the prompt gives the role file `<plugin_root>/skills/idea-to-3d/references/roles/maker.md`, slug, work root, plugin root, the stage `SKILL.md` path and steps, and the approved budget | approved budget only |
| critic | `Bash`: `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>` with `timeout: 600000` | none |
| critic fallback | `Agent` with `subagent_type: "idea-to-3d:idea3d-critic"`; the prompt gives `references/roles/critic.md`, gate, rubric, inputs, out path | none |
| reviser | `Agent` with `subagent_type: "idea-to-3d:idea3d-reviser"`; the prompt gives `references/roles/reviser.md`, gate, round, review path, rubric, stage skill | none (it has no Meshy tools) |

- Never judge a gate yourself: the critic is the script or the critic agent.
<!-- platform:end -->

## Workspace & State (`work/<slug>/pipeline.json`)

```text
work/<slug>/
├── pipeline.json     idea, slug, stage, Meshy task ids with settings & credits, chosen try,
│                     checkpoint answers, critic consent, review log, file paths
├── idea.md           the idea expanded into a brief (look, hex colours, pose, height, style)
├── images/           concept-1.png..concept-4.png; chosen copied to front.png, plus side.png & back.png
├── meshy/            <slug>-try-<n>.glb, chosen as <slug>-meshy.glb, <slug>-remesh.glb, rigged & clip GLBs
├── blender/          <slug>.blend
├── out/              <slug>.glb, quality_report.json
├── preview/          concepts.png, turnaround.png, tries.png, sheet.png
└── reviews/          <gate>-r<n>.json critic reviews, reviser backups
```

Manage state with `pipeline_state.py`:

```powershell
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" init <slug> --idea "<idea>" --height <meters> [--non-humanoid] --clips "idle,walk,wave"
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" show <slug>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" get-task <slug> <step_key>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-task <slug> <step_key> --task-id <id> --tool <tool> --task-type <type> --credits <n> --status <status>
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" record-checkpoint <slug> <A|B|C> --approved true --choice "<choice>"
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" set-critic <slug> gemini|claude
python "<plugin_root>/skills/idea-to-3d/scripts/pipeline_state.py" review-history <slug> [--gate A1|A2|B|C]
```

## Execution Protocol

### 0. Start or resume

- Derive `<slug>` (lowercase kebab-case, e.g. `fox-knight`).
- If `work/<slug>/pipeline.json` exists, run `show` and `review-history` and resume from the current stage, any unapproved checkpoint, any in-progress Meshy `task_id`, or the last gate round.
- Otherwise run `init` and write `work/<slug>/idea.md` yourself (concept-art Step 1).

### 1. Stage 1 — concepts, gate A1, Checkpoint A, turnarounds, gate A2

1. Ask the user, in one question, to approve concept generation and the outside services. Say that the images and brief go to Meshy (`meshy.ai`) and, for review, to Gemini (Google, through the Antigravity CLI). Give the cost from the Platform image route. Options:
   - (Recommended) 3 concepts, review by Gemini.
   - 4 concepts, review by Gemini.
   - 3 concepts, review by the Claude critic only (nothing goes to Gemini).
   Record the answer with `set-critic <slug> gemini` or `set-critic <slug> claude`.
2. Dispatch the maker for concept-art Step 2 with the approved budget. It writes `images/concept-<n>.png` and `preview/concepts.png`.
3. Run gate A1 ([loop.md](references/loop.md)).
4. **Checkpoint A** — look at `preview/concepts.png`, then ask in one question: which concept (recommended first, with the reason and the gate A1 summary), together with what continuing costs — the turnarounds (Platform image route) and Stage 2 (`2 × meshy-7.1` 4K = 60 credits, or `1 × meshy-6-lite` = 15). Offer the scripted Blender build when `idea.md` flags it. Record with `record-checkpoint <slug> A`, and copy the chosen concept to `images/front.png`.
5. Dispatch the maker for concept-art Step 4 (turnarounds) with the approved budget.
6. Run gate A2. Its paid fixes (regenerating a view) are asked as in loop.md.

### 2. Stage 2 — image-to-3D, gate B, Checkpoint B

1. Dispatch the maker for image-to-3d Steps 2–3 with the Stage 2 budget approved at Checkpoint A. It writes the tries and `preview/tries.png`.
2. Run gate B.
3. **Checkpoint B** — look at `preview/tries.png`, then ask in one question: which try (recommended first, with the gate B summary), together with the Stage 3 cost (`meshy_remesh` 5 + `meshy_rig` 5 + `meshy_animate` 3 per action, or remesh only, 5, for non-humanoids). Record with `record-checkpoint <slug> B` and copy the chosen try to `meshy/<slug>-meshy.glb`.

### 3. Stage 3 — remesh, rig, clips

Dispatch the maker for rig-animate with the Stage 3 budget. No gate here: the rig and clips
are judged at gate C once Blender renders them.

### 4. Stage 4 — Blender finish, gate C, Checkpoint C

1. Dispatch the maker for blender-finish Steps 1–3 (free). `export-check.py` must be run with `--report "work/<slug>/out/quality_report.json"`.
2. Run gate C. Re-rig (5) and re-animate (3 per action) fixes come back as paid requests.
3. **Checkpoint C** — look at `preview/sheet.png`, then ask: approve, or request changes. Show the `check-glb.py` result and the gate C summary. Record with `record-checkpoint <slug> C`.

## Guardrails

- Every credit-spending call needs the user's yes in this run, with tool, model and credits named.
- Never re-create a Meshy task recorded in `pipeline.json`; poll it.
- The critic never sees the maker's or reviser's messages.
- Stop at every checkpoint until the user answers.
`````

- [ ] **Step 2: Check the description and validate**

Run:

```bash
python3 -c "import re;t=open('plugins/idea-to-3d/skills/idea-to-3d/SKILL.md',encoding='utf-8').read();d=re.search(r'^description: (.*)$',t,re.M).group(1);print(len(d))"
grep -nE "ask_question|view_file|image-generator|send_message" plugins/idea-to-3d/skills/idea-to-3d/SKILL.md
bash scripts/health.sh --fast
```

Expected: a number below 1024 (≈ 690); no grep output; `health: OK`.

- [ ] **Step 3: Commit**

```bash
git add plugins/idea-to-3d/skills/idea-to-3d/SKILL.md
git commit -m "feat(idea-to-3d): wire the maker, critic and reviser loop into the orchestrator

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 9: Release 2.0.0 in the marketplace

**Files:**
- Modify: `plugins/idea-to-3d/.claude-plugin/plugin.json` (via `bump.py` + description), `CHANGELOG.md`, `README.md`
- Create: `plugins/idea-to-3d/core-files.txt`
- Modify: `.claude-plugin/marketplace.json` (description), `CLAUDE.md`, `MEMORY.md`, `ROUTING.md`

- [ ] **Step 1: Write `core-files.txt`**

```text
# Shared critic-loop core. Owned by micky-psych-tools/plugins/idea-to-3d (source of truth).
# The Antigravity repo pulls these with scripts/sync-core.ps1; never edit them there.
skills/idea-to-3d/references/loop.md
skills/idea-to-3d/references/review.schema.json
skills/idea-to-3d/references/roles/maker.md
skills/idea-to-3d/references/roles/reviser.md
skills/idea-to-3d/references/roles/critic.md
skills/idea-to-3d/references/rubrics/A1.md
skills/idea-to-3d/references/rubrics/A2.md
skills/idea-to-3d/references/rubrics/B.md
skills/idea-to-3d/references/rubrics/C.md
skills/idea-to-3d/scripts/critique.py
skills/idea-to-3d/scripts/pipeline_state.py
tests/test_critic.py
tests/fake_agy.py
```

- [ ] **Step 2: Bump to 2.0.0**

Run: `python3 scripts/bump.py idea-to-3d major` (dry run; expect `1.0.0 -> 2.0.0`), then `python3 scripts/bump.py idea-to-3d major --write`.
Expected: plugin.json version `2.0.0`, a new `## 2.0.0 — 2026-10-20` heading in CHANGELOG.md, validation OK.

- [ ] **Step 3: Fill the CHANGELOG entry and update descriptions**

Under the new `## 2.0.0 — 2026-10-20` heading in `CHANGELOG.md`, add:

```markdown
Every stage is now checked before the user sees it: maker → independent critic → reviser.

- **Gates A1, A2, B, C.** A1 judges the concept set, A2 the turnarounds (before Stage 2
  spends credits), B the Meshy tries, C the rig, clips and Blender finish together.
  Rubrics with criteria, severity and a free/paid fix catalogue live in
  `skills/idea-to-3d/references/rubrics/`.
- **Gemini critic.** `scripts/critique.py` sends a gate's files to Gemini
  (`gemini-4-argon-medium`) through the Antigravity CLI (`agy -p --mode plan
  --json-schema`), validates the review and logs it in `pipeline.json`. Gemini CLI's
  personal login is retired (`IneligibleTierError`), so it is not used.
- **Fallback.** On exit 2/3 the `idea3d-critic` Claude agent reviews the same files; its
  review goes through the same validator (`--from-file`).
- **Reviser.** The `idea3d-reviser` agent applies free fixes and returns credit-spending
  fixes as requests; it has no Meshy tools. Paid fixes run only after a yes.
- **Stop rule.** PASS, or 2 revise rounds, then the checkpoint lists any open issues.
- **Consent.** The first question now covers Meshy and Gemini; `set-critic` records the
  answer and `critique.py` refuses to run without it.
- Shared core listed in `core-files.txt`; the Antigravity repo pulls it with
  `scripts/sync-core.ps1`.
```

Set the `description` in `plugin.json` and in the `idea-to-3d` entry of `.claude-plugin/marketplace.json` to:

```text
Turns a one-line character or prop idea into a textured, rigged, animated 3D model (.glb) with a preview sheet: concepts, image-to-3D, rigging and clips on Meshy, finishing in headless Blender 5.2. Before each checkpoint an independent Gemini critic (Antigravity CLI, Claude fallback) reviews the stage and a reviser applies free fixes; fixes that spend credits run only after approval. Five skills, three agents. Needs Windows, Blender 5.2, agy and the user-scope meshy MCP.
```

(475 chars; the catalog cap is 500.)

- [ ] **Step 4: Replace `README.md`**

`````markdown
# idea-to-3d

Turns a one-line character or prop idea into a textured, rigged, animated `.glb` and a
preview sheet. Every stage is reviewed by an independent critic and revised before you see it.

```text
idea → concepts ─ A1 ─ [Checkpoint A] ─ turnarounds ─ A2 → Meshy tries ─ B ─ [Checkpoint B]
     → remesh, rig, clips → Blender finish ─ C ─ [Checkpoint C]
```

## The critic loop

| Role | What it does | Spends credits |
|---|---|---|
| maker (`idea3d-maker` agent) | runs a stage skill | only what you approved |
| critic (`critique.py` → Gemini via `agy`) | judges the gate's files against a rubric, returns PASS/REVISE + issues | no |
| critic fallback (`idea3d-critic` agent) | same job when Gemini is unavailable or declined | no |
| reviser (`idea3d-reviser` agent) | applies free fixes, asks for paid ones | no (no Meshy tools) |

The loop ends on PASS or after 2 revise rounds; the checkpoint shows any open issues.
Rubrics: `skills/idea-to-3d/references/rubrics/`. Protocol: `skills/idea-to-3d/references/loop.md`.

## Requirements

- Windows, Python 3.10+ with Pillow, Blender 5.2 at `C:\Program Files\Blender Foundation\Blender 5.2\blender.exe`.
- The Meshy MCP server registered at user scope as `meshy` (`MESHY_API_KEY` in `HKCU\Environment`, never in files).
- The Antigravity CLI `agy`, logged in, for the Gemini critic. Without it the Claude critic runs.

## Use

Ask for a 3D model of an idea ("make a fox knight with a lantern as a rigged 3D model") or
run the `idea-to-3d` skill. Work goes to `work/<slug>/` in the current folder.

## Tests

```bash
python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -v
python -m unittest discover -s plugins/idea-to-3d/tests -p "test_pipeline.py" -k Unit -v
```

## Antigravity copy

`C:\Users\User\Desktop\repo\idea-to-3d` is the same pipeline for Antigravity. It pulls the
files listed in `core-files.txt` from here with `scripts/sync-core.ps1`; this copy is the
source of truth.
`````

- [ ] **Step 5: Update `CLAUDE.md`, `MEMORY.md`, `ROUTING.md`**

In `CLAUDE.md`, under `## Plugins`, after the `design-md-generator` bullet, add:

```markdown
- **idea-to-3d** — one-line idea → textured, rigged, animated `.glb` + preview sheet: concept
  art, image-to-3D, remesh/rig/clips on Meshy (user-scope `meshy` MCP), finishing in headless
  Blender 5.2, three user checkpoints. Each stage passes a maker → critic → reviser loop first:
  an independent Gemini critic (`critique.py` via the Antigravity CLI `agy`; the
  `idea3d-critic` Claude agent as fallback) at gates A1/A2/B/C, free fixes applied by the
  `idea3d-reviser` agent (no Meshy tools), credit-spending fixes only on approval, PASS or 2
  revise rounds. Five skills + three agents, no commands. Shares its critic core
  (`core-files.txt`) with the Antigravity repo `Desktop/repo/idea-to-3d`, which pulls it via
  `scripts/sync-core.ps1` — this copy is the source of truth.
```

In `MEMORY.md`: add `| idea-to-3d            | 2.0.0   |` as a row of the versions table directly below the `design-md-generator` row; add a milestone under `## Recent milestones` in the same format as its neighbours: "2026-10-20 — idea-to-3d 2.0.0: ported from the Antigravity plugin with a maker → Gemini critic → reviser loop at gates A1/A2/B/C. Gemini CLI personal OAuth is retired (`IneligibleTierError`); the critic runs through `agy` with `gemini-4-argon-medium`."; and under `## Open threads`: "idea-to-3d: once the plugin is installed, remove the user-scope copies (`~/.claude/skills/{idea-to-3d,concept-art,image-to-3d,rig-animate,blender-finish}` and `~/.claude/rules/idea-to-3d.md`) — the skill names collide; needs the user's OK. First live acceptance run still pending."

Then run: `python3 scripts/route.py`

- [ ] **Step 6: Full health and tests**

Run:

```bash
bash scripts/health.sh
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s plugins/idea-to-3d/tests -p "test_critic.py" -q
```

Expected: `health: OK`; critic tests OK.

- [ ] **Step 7: Commit**

```bash
git add plugins/idea-to-3d .claude-plugin/marketplace.json CLAUDE.md MEMORY.md ROUTING.md
git commit -m "feat(idea-to-3d): release 2.0.0 with the Gemini critic loop

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 10: Antigravity — sync script and parity test

**Files (in `C:\Users\User\Desktop\repo\idea-to-3d`):**
- Create: `scripts/sync-core.ps1`, `tests/test_core_parity.py`
- Synced in: every path in the marketplace `core-files.txt`

- [ ] **Step 1: Branch**

```bash
git -C /c/Users/User/Desktop/repo/idea-to-3d status --short
git -C /c/Users/User/Desktop/repo/idea-to-3d switch -c feat/critic-loop
```

Expected: empty status, then `Switched to a new branch 'feat/critic-loop'`. If status is not empty, stop and ask the user.

- [ ] **Step 2: Write the failing parity test**

`tests/test_core_parity.py`:

```python
#!/usr/bin/env python3
"""The shared critic-loop core must match the marketplace copy (the source of truth)."""
from __future__ import annotations

import hashlib
import os
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = Path(os.environ.get(
    "IDEA3D_MARKETPLACE", r"C:\Users\User\micky-psych-tools\plugins\idea-to-3d"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


@unittest.skipUnless((MARKETPLACE / "core-files.txt").is_file(), "marketplace copy not present")
class TestCoreParity(unittest.TestCase):
    def test_core_files_match_the_marketplace_copy(self) -> None:
        lines = (MARKETPLACE / "core-files.txt").read_text(encoding="utf-8").splitlines()
        core = [line.strip() for line in lines if line.strip() and not line.startswith("#")]
        self.assertTrue(core)
        for rel in core:
            with self.subTest(rel=rel):
                local = REPO_ROOT / rel
                self.assertTrue(local.is_file(), f"{rel} missing: run scripts/sync-core.ps1")
                self.assertEqual(digest(local), digest(MARKETPLACE / rel),
                                 f"{rel} differs from the marketplace copy: run scripts/sync-core.ps1")


if __name__ == "__main__":
    unittest.main()
```

Run: `cd /c/Users/User/Desktop/repo/idea-to-3d && PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_core_parity -v`
Expected: FAIL — `skills/idea-to-3d/references/loop.md missing: run scripts/sync-core.ps1` (and a mismatch for `pipeline_state.py`).

- [ ] **Step 3: Write `scripts/sync-core.ps1`**

```powershell
# Copies the shared critic-loop core from the micky-psych-tools marketplace plugin (the
# source of truth) into this repo. The file list is the marketplace's core-files.txt.
# Never edit core files here; change them in the marketplace and sync.
param(
    [string]$Source = (Join-Path $env:USERPROFILE "micky-psych-tools\plugins\idea-to-3d")
)
$ErrorActionPreference = 'Stop'

$repo = Split-Path -Parent $PSScriptRoot
$list = Join-Path $Source "core-files.txt"
if (-not (Test-Path -LiteralPath $list)) {
    throw "core-files.txt not found under $Source"
}

$files = Get-Content -LiteralPath $list | Where-Object { $_.Trim() -and -not $_.StartsWith('#') }
foreach ($rel in $files) {
    $from = Join-Path $Source $rel
    $to = Join-Path $repo $rel
    if (-not (Test-Path -LiteralPath $from)) {
        throw "Core file missing in the marketplace copy: $rel"
    }
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $to) | Out-Null
    Copy-Item -LiteralPath $from -Destination $to -Force
    Write-Host "synced $rel"
}
Write-Host "Core synced: $($files.Count) files from $Source"
```

- [ ] **Step 4: Sync and verify**

Run (PowerShell):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\User\Desktop\repo\idea-to-3d\scripts\sync-core.ps1"
```

Expected: 13 `synced ...` lines and `Core synced: 13 files ...`.

Then (Bash):

```bash
cd /c/Users/User/Desktop/repo/idea-to-3d
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_core_parity tests.test_critic -v
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_pipeline -k Unit -q
```

Expected: parity OK, all critic tests OK, v1 unit tests OK (the new `reviews` subdir does not affect them).

- [ ] **Step 5: Commit (in the Antigravity repo)**

```bash
cd /c/Users/User/Desktop/repo/idea-to-3d
git add scripts/sync-core.ps1 tests/test_core_parity.py tests/test_critic.py tests/fake_agy.py skills/idea-to-3d
git status --short   # must not list work/ or meshy_output/
git commit -m "feat: pull the shared critic-loop core from the marketplace plugin

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

---

### Task 11: Antigravity — orchestrator, gate notes, rules, 2.0.0

**Files (in `C:\Users\User\Desktop\repo\idea-to-3d`):**
- Modify (replace): `skills/idea-to-3d/SKILL.md`
- Modify: four stage `SKILL.md` (gate notes), `rules/idea-to-3d.md`, `plugin.json`, `README.md`

- [ ] **Step 1: Build the Antigravity orchestrator from the marketplace one**

Save as `ag_orchestrator.py` in the scratchpad and run `python ag_orchestrator.py`:

```python
"""Build the Antigravity orchestrator SKILL.md: marketplace copy with the platform block swapped."""
import re
import sys
from pathlib import Path

SRC = Path(r"C:\Users\User\micky-psych-tools\plugins\idea-to-3d\skills\idea-to-3d\SKILL.md")
DST = Path(r"C:\Users\User\Desktop\repo\idea-to-3d\skills\idea-to-3d\SKILL.md")

AG_BLOCK = """<!-- platform:begin -->
## Platform: Antigravity

- `<plugin_root>` is the installed plugin directory (`%USERPROFILE%\\.gemini\\config\\plugins\\idea-to-3d`). Use absolute paths in every command.
- **Ask the user** = the `ask_question` tool, recommended option first with "(Recommended)". Only you ask; subagents cannot.
- **Look at a PNG** = `view_file`.
- **Image route** (concepts, turnarounds, image fixes): the `image-generator` subagent (`generate_image`), 0 Meshy credits. The `save-image.ps1` hook writes `work/<slug>/images/*.png` (`ImageName` `<slug>_concept_<n>`, `<slug>_front`, `<slug>_side`, `<slug>_back`). Reuse the same image-generator conversation with `send_message` and the chosen concept in `ImagePaths` so side and back views match the front. Image fixes are therefore free and need no approval. If the image-generator is unavailable, fall back to Meshy `nano-banana-pro` at 9 credits per image after approval.
- **Roles:** dispatch a fresh subagent per role, briefed with the role file plus the inputs it lists:

| Role | Run it as | Credits |
|---|---|---|
| maker | subagent briefed with `<plugin_root>/skills/idea-to-3d/references/roles/maker.md`, slug, work root, plugin root, the stage `SKILL.md` path and steps, and the approved budget | approved budget only |
| critic | shell command: `python "<plugin_root>/skills/idea-to-3d/scripts/critique.py" <slug> <gate> --work-root <root>` (allow up to 10 minutes) | none |
| critic fallback | fresh subagent briefed with `references/roles/critic.md`, gate, rubric, inputs, out path | none |
| reviser | subagent briefed with `references/roles/reviser.md`, gate, round, review path, rubric, stage skill; it must not call any Meshy tool that costs credits | none |

- Never judge a gate yourself. If no fresh subagent can be dispatched for the fallback critic, record the gate as unreviewed and say so at the checkpoint.
<!-- platform:end -->"""

text = SRC.read_text(encoding="utf-8")
new, n = re.subn(r"<!-- platform:begin -->.*?<!-- platform:end -->", lambda _m: AG_BLOCK, text, flags=re.S)
if n != 1:
    sys.exit(f"expected one platform block, found {n}")
DST.write_text(new, encoding="utf-8", newline="\n")
print("antigravity orchestrator: ok")
```

Expected: `antigravity orchestrator: ok`. Then check: `grep -c "AskUserQuestion\|subagent_type" /c/Users/User/Desktop/repo/idea-to-3d/skills/idea-to-3d/SKILL.md` prints `0`.

- [ ] **Step 2: Gate notes in the Antigravity stage skills**

Run the Task 7 script against this repo: `python gate_notes.py /c/Users/User/Desktop/repo/idea-to-3d`
Expected: `gate notes: ok`.

- [ ] **Step 3: Rules, manifest, README**

In `rules/idea-to-3d.md`:
- Replace `inform the user that the image will be uploaded to Meshy and get an explicit **yes**` with `inform the user that images and the brief go to Meshy (`meshy.ai`) and, for review, to Gemini (Google, through the Antigravity CLI), and get an explicit **yes**`.
- Append:

```markdown

## 6. Critic loop

- Every gate (A1, A2, B, C) follows `skills/idea-to-3d/references/loop.md`: critic, then reviser, then paid fixes only after a yes, then the critic again; it ends on PASS or after 2 revise rounds.
- The critic sees only files. Never pass it the maker's or reviser's messages, and never judge a gate yourself.
- Record the Gemini answer with `pipeline_state.py set-critic <slug> gemini|claude` before the first gate; `critique.py` refuses to run until it is recorded.
- The shared core files listed in the marketplace's `core-files.txt` are synced with `scripts/sync-core.ps1`; never edit them in this repo.
```

In `plugin.json` set `"version": "2.0.0"` (this repo has no bump script).

In `README.md`, append:

```markdown

## Critic loop (v2.0.0)

Every stage is reviewed by an independent critic and revised before you see it.

| Role | What it does | Spends credits |
|---|---|---|
| maker (subagent, `roles/maker.md`) | runs a stage skill | only what you approved |
| critic (`critique.py` → Gemini via `agy`) | judges the gate's files against a rubric, returns PASS/REVISE + issues | no |
| critic fallback (subagent, `roles/critic.md`) | same job when Gemini is unavailable or declined | no |
| reviser (subagent, `roles/reviser.md`) | applies free fixes, asks for paid ones | no |

Gates: A1 concepts, A2 turnarounds, B Meshy tries, C rig + clips + Blender finish. The loop
ends on PASS or after 2 revise rounds; the checkpoint shows any open issues. Requires the
Antigravity CLI `agy`, logged in (`gemini-4-argon-medium`).

The core files (`skills/idea-to-3d/references/`, `critique.py`, `pipeline_state.py`,
`tests/test_critic.py`, `tests/fake_agy.py`) come from `micky-psych-tools/plugins/idea-to-3d`;
change them there and run `scripts/sync-core.ps1`.
```

- [ ] **Step 4: Tests, install, commit**

```bash
cd /c/Users/User/Desktop/repo/idea-to-3d
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_core_parity tests.test_critic -q
PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.test_pipeline -k Unit -q
git add -A skills rules plugin.json README.md
git status --short   # must not list work/ or meshy_output/
git commit -m "feat: add the maker, Gemini critic, reviser loop (v2.0.0)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
```

Expected: all tests OK. Then install into the live Antigravity plugin directory (this updates the user's installed copy; it was the documented v1 route):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "C:\Users\User\Desktop\repo\idea-to-3d\scripts\sync-plugin.ps1"
```

Expected: `Successfully synced and validated idea-to-3d at ...`.

---

### Task 12: Acceptance (user-gated, spends credits)

Not automatic. Ask the user before starting, naming the cost.

- [ ] **Step 1: Claude Code dry check (free)** — in a fresh Claude Code session with the marketplace plugin installed, run the orchestrator on `a red rubber ball` up to the first question only, and confirm it: lists both consent targets (Meshy and Gemini), offers the Claude-only option, and does not call any Meshy tool before the answer.
- [ ] **Step 2: Tracer run (≈ 27 + 15 + 5 credits in Claude Code)** — with the user's yes: 3 concepts, gate A1, pick, turnarounds, gate A2, one `meshy-6-lite` try, gate B, remesh-only non-humanoid, Blender finish, gate C. Pass criteria: a review file for every gate in `work/<slug>/reviews/`, every review in `review-history`, no Meshy task created twice, every paid fix preceded by a question, `out/<slug>.glb` passing `check-glb.py`.
- [ ] **Step 3: Antigravity tracer** — same idea in Antigravity (images free there), same pass criteria.
- [ ] **Step 4: Record** — add the outcomes to `MEMORY.md` (marketplace) and `LESSONS_LEARNED.md` (Antigravity); close the "first live acceptance run" open thread.
