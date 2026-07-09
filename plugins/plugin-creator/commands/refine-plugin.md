---
description: Audit and refine an existing plugin or skill in the marketplace
argument-hint: [plugin or skill name to refine]
---

Invoke the `refine-plugin` skill to audit and refine an existing plugin or skill.

If `$ARGUMENTS` is non-empty, treat it as the target name and audit that plugin/skill.
If empty, list the marketplace's plugins/skills and ask which to refine.

Follow the skill's procedure exactly — select, guard, audit (two tiers), apply approved
fixes, bump via scripts/bump.py, then stop before committing.
