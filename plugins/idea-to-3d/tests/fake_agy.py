#!/usr/bin/env python3
"""
Stand-in for the Antigravity CLI (`agy`) in tests. Behaviour comes from FAKE_AGY_MODE:
ok | pass | response-only | bad | bad-then-ok | nonzero | not-success | sleep | hang-child
for the critic, and for image generation (IDEA3D_AGY_BRAIN required):
image | image-late | image-delayed | image-other-conv | image-none | image-outside | image-outside-only.
When FAKE_AGY_LOG is set, each call appends its argv to it as one JSON line.
"""
import json
import os
import re
import subprocess
import sys
import time

CRITERIA = ("geometry", "artifacts", "texture", "symmetry", "rig-readiness")


def review(gate: str, verdict: str) -> dict:
    issues = [] if verdict == "PASS" else [{
        "id": f"{gate}-1", "severity": "major", "criterion": "geometry",
        "evidence": "Try 2, side: left hand fused to the hip",
        "fix": "new try with pose_mode a-pose", "credits": 30,
    }]
    return {"gate": gate, "verdict": verdict,
            "scores": [{"criterion": c, "score": 2} for c in CRITERIA], "issues": issues}


def write_jpeg(path: str, colour: tuple[int, int, int]) -> str:
    from PIL import Image

    os.makedirs(os.path.dirname(path), exist_ok=True)
    Image.new("RGB", (64, 64), colour).save(path, "JPEG")
    return path


def image_mode(mode: str, calls: int) -> int:
    """Image generation: the brain image is teal, a file outside the brain dir is red."""
    conversation = "conv-test"
    brain_image = os.path.join(os.environ["IDEA3D_AGY_BRAIN"], conversation, f"fake_{calls}.jpg")
    reply = ""
    if mode == "image-delayed":
        # The file appears ~1 s after this process exits, as agy's does after its reply.
        code = "; ".join((
            "import os, sys, time", "from PIL import Image", "time.sleep(1)",
            "os.makedirs(os.path.dirname(sys.argv[1]), exist_ok=True)",
            "Image.new('RGB', (64, 64), (0, 128, 128)).save(sys.argv[1] + '.part', 'JPEG')",
            "os.replace(sys.argv[1] + '.part', sys.argv[1])",
        ))
        subprocess.Popen([sys.executable, "-c", code, brain_image], stdin=subprocess.DEVNULL,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, close_fds=True)
    if mode == "image-other-conv":
        reply = write_jpeg(os.path.join(os.environ["IDEA3D_AGY_BRAIN"], "other-conv", "x.jpg"), (0, 128, 128)) + "\n"
    if mode in ("image", "image-late", "image-outside"):
        write_jpeg(brain_image, (0, 128, 128))
    if mode == "image":
        reply = f"Generating the image now...\n{brain_image}\n"
    elif mode == "image-late":
        reply = "The image is ready in the conversation folder."
    elif mode in ("image-outside", "image-outside-only"):
        reply = write_jpeg(os.path.join(os.getcwd(), "outside.jpg"), (255, 0, 0)) + "\n"
    print(json.dumps({"conversation_id": conversation, "status": "SUCCESS", "response": reply}))
    return 0


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
    if mode.startswith("image"):
        return image_mode(mode, calls)
    match = re.search(r'"gate" must be "(\w+)"', prompt)
    gate = match.group(1) if match else "?"

    if mode == "nonzero":
        print("Error authenticating: not logged in", file=sys.stderr)
        return 1
    if mode == "not-success":
        print(json.dumps({"status": "ERROR", "response": ""}))
        return 0
    if mode == "sleep":
        time.sleep(5)
        return 0
    if mode == "hang-child":
        # A child that inherits stdout keeps the pipe open after the parent is killed.
        subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
        time.sleep(30)
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
