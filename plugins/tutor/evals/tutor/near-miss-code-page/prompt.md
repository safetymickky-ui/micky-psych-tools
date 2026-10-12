---
description: "Near-miss negative: code explained as an interactive page is code-explainer's job, even though the code is about softmax. The tutor must not fire."
tags: [tutor, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 8
---

Explain this code as an interactive page:

```python
def softmax(q, beta):
    z = np.exp(beta * q)
    return z / z.sum()
```
