# Baseline measurements

One dated section per wave exit (spec S12, I17). `baseline measure` rewrites only its own dated section.

## W0 — 2026-09-24

Written by `python3 scripts/rewrite_gate.py baseline measure --wave W0 --write` (micky-psych-tools). Tokens = chars / 4 unless the source is `plugin details`. MANUAL cells need an interactive session; the owner fills them in.

| Surface | Value | Source |
|---|---|---|
| micky CLAUDE.md | 14,466 B / 208 lines / ~3,590 tok | wc -c; tokens = chars / 4 |
| learn-hub CLAUDE.md | 269,154 B / 3,135 lines / ~66,790 tok | /home/user/learn-hub/CLAUDE.md |
| micky MEMORY.md | 108,765 B / 1,154 lines / ~26,863 tok | wc -c |
| ROUTING.md | 20,057 B / 168 lines / ~4,888 tok | wc -c |
| micky authored listing entries | 29 entries (17 skills, 12 commands, 0 agents) / 17,358 description chars | description + when_to_use, plugins/*/{skills,commands,agents} |
| learn-hub project-skill listing (loads in cloud) | 11 entries / 8,726 description chars | .claude/skills/*/SKILL.md |
| micky always-on (plugin details sum) | ~6,579 tok over 14 plugins | claude --plugin-dir <p> plugin details <p>, isolated CLAUDE_CONFIG_DIR |
| claude.ai-synced listing | 22 entries / 15,360 description chars | /root/.claude/skills/synced |
| Total paid before work, multi-repo cloud (estimate) | ~108,153 tok | learn-hub CLAUDE.md 66,790 + micky CLAUDE.md 3,590 + MEMORY.md 26,863 + ROUTING.md 4,888 + learn-hub listing 2,182 + synced listing 3,840 |
| micky descriptions over 1,024 chars | none | hard cap |
| micky descriptions at 1,000-1,024 chars | 8: comprehensive-review (1020), concept-animation (1022), decision-interview (1013), firecrawl (1009), intent-lock (1020), plan-critique (1012), pubmed-research-note (1007), empty-vault (1003) |  |
| micky descriptions over 600 chars (soft cap) | 17 of 29 |  |
| /doctor listing cost and overflow | MANUAL — owner records after a real session | checklist row f |
| /skill-doctor | MANUAL — owner records after a real session | Windows, W5 |

Per plugin (`plugin details`):

| Plugin | always-on | on-invoke per component |
|---|---|---|
| clinical-infographic | ~411 | clinical-infographic ~3,900, infographic ~260 |
| code-explainer | ~368 | code-explainer ~3,000, explain-code ~290 |
| comprehensive-review | ~440 | comprehensive-review ~160, comprehensive-review ~4,000 |
| concept-animation | ~442 | animate ~280, concept-animation ~3,200 |
| decision-interview | ~388 | decision-interview ~2,500, resolve-decisions ~110 |
| firecrawl | ~368 | firecrawl ~6,200 |
| gridgeist | ~280 | gridgeist ~1,500 |
| intent-lock | ~655 | intent-lock ~8,100, misread-capture ~1,300 |
| ml-concept-lab | ~468 | ml-concept-lab ~4,900, visualize ~420 |
| plan-critique | ~442 | critique-plan ~190, plan-critique ~3,400 |
| plugin-creator | ~721 | new-plugin ~150, plugin-creator ~1,500, refine-plugin ~150, refine-plugin ~1,300, route ~420 |
| psych-paper-digest | ~391 | digest ~210, psych-paper-digest ~3,000 |
| pubmed-research-note | ~432 | pubmed-research-note ~6,400 |
| vault-keeper | ~773 | empty-vault ~210, empty-vault ~2,100, vault-keeper ~2,500 |

Named skills (body = SKILL.md after frontmatter; references = every file under `references/`):

| Skill | body lines | body tok | references tok |
|---|---|---|---|
| intent-lock | 246 | ~6,193 | ~1,274 |
| pubmed-research-note | 305 | ~4,693 | ~8,527 |
| firecrawl | 368 | ~4,215 | ~0 |
| ml-concept-lab | 226 | ~3,534 | ~7,306 |
