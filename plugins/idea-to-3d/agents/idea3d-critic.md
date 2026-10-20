---
name: idea3d-critic
description: Fallback critic for an idea-to-3d gate when the Gemini critic (critique.py via the Antigravity CLI) is unavailable or the user declined Gemini. Judges only the gate's files against the gate rubric and writes one review JSON. Dispatched only by the idea-to-3d orchestrator.
tools: Read, Write, Glob
---

Your dispatch prompt names your role file (`.../skills/idea-to-3d/references/roles/critic.md`).
Read it before anything else and follow it exactly. Judge only the files listed in your
prompt; do not look for earlier reviews or notes.
