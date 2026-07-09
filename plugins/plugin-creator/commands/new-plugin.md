---
description: Scaffold a new plugin into the micky-psych-tools marketplace
argument-hint: [optional one-line plugin idea]
---

Invoke the `plugin-creator` skill to scaffold a new plugin into this marketplace.

If `$ARGUMENTS` is non-empty, treat it as the seed idea: pre-fill the checklist's
purpose slot from it and only ask for the slots it doesn't already answer.
If empty, start the elicitation checklist cold.

Follow the skill's procedure exactly — elicit, guard, scaffold, register, validate,
then stop before committing.
