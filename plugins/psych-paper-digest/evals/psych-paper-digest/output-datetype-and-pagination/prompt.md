---
description: "W0 smoke seed (S04-W0-1). Mined from skills/psych-paper-digest/evals/evals.json id 8 (registry-readout-section), prompt verbatim; section 4.2 folds id 8 into this case. Seeds today's behaviour only: the PubMed call is windowed (date_from and date_to), the registry is swept, and the digest carries its header count line and the Act / Read / Registry watch / Suppressed sections. The datetype=edat and retstart graders of section 4.1 assert the H46/H47 fix and are added when that fix lands, not here (today's sweep-recipes.md passes neither). scaffold.sh writes a one-domain watchlist last swept 7 days ago; the engines answer from this case's mocks. The digest file needs the Write grant (-- --allow-tools Write)."
tags: [psych-paper-digest, output, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 30
timeout_seconds: 900
---

Sweep my watchlist.
