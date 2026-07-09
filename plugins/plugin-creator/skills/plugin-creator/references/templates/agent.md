---
name: {{AGENT_NAME}}
description: {{ACTION_FIRST_DESCRIPTION. When to dispatch this agent. Embed verbatim trigger phrases. Include a Use-when and a Not-for clause. Same 200-1024 char discipline as a skill — the description is what routes work to this agent.}}
tools: {{COMMA_SEPARATED_TOOLS or omit for all, e.g. Read, Grep, Glob}}
---

{{SYSTEM_PROMPT: the agent's role, how it works, and what it returns. Be specific about
the output format the caller receives.}}
