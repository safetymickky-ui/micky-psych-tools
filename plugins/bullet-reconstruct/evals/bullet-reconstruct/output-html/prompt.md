---
description: "Output contract on a text source (no figures, so no snips). The run must freeze units, pass the gate before building, and write one self-contained notes.html with the number kept and the citation markers gone. Needs -- --allow-tools \"Write,Edit,Bash(python3 *)\" and python3 with markdown installed."
tags: [bullet-reconstruct, output]
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, "Bash(python3 *)"]
max_turns: 40
timeout_seconds: 900
---

Reconstruct paper.txt into tight bullets and give me the HTML file, saved as notes.html.
