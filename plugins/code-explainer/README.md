# code-explainer

Turns **given code** into one self-contained, interactive HTML page: the original source on
the **left** in an editor styled as VS Code (Dark Modern, line numbers, syntax highlighting),
the explanation on the **right**, and the two wired to each other so the reader never has to
hold a line number in their head.

Opens offline in any browser. No CDN, no build step, no runtime highlighter.

## What's on the page

```
┌───────────────────────────────────────────────────────────────┐
│ ● ● ●   retry.js — code-explainer                             │
├────┬──────────────────────────────────┬───────────────────────┤
│ a  │  retry.js  ×                     │  EXPLANATION          │
│ c  ├──────────────────────────────────┤  ┌─────────────────┐  │
│ t  │  src › retry.js › withRetry      │  │ 1 · lines 1-4   │  │
│ i  ├──────────────────────────────────┤  └─────────────────┘  │
│ v  │  1  export async function …      │  ┌─────────────────┐  │
│ i  │ ▶2      const { retries = 3 } …  │  │ 2 · lines 6-11  │  │
│ t  │  3      …                        │  └─────────────────┘  │
│ y  ├──────────────────────────────────┤                       │
│    │ FLOW │ STATE                     │                       │
│    │  ┌──┐ → ◇ → ┌──┐  ⟲              │                       │
├────┴──────────────────────────────────┴───────────────────────┤
│ ⎇ main    Ln 2, Col 1    JavaScript    Step 2 / 8             │
└───────────────────────────────────────────────────────────────┘
```

Three interactive modes, all wired to **one shared `data-range` id space** — so every way of
navigating the code points at the same thing:

| Mode | What it does |
| --- | --- |
| **Linked highlighting** | Hover or click a line → its explanation card lights up. Hover or click a card → its lines light up. Both directions, keyboard operable. |
| **Step-through walkthrough** | A debug-session player (Restart · Prev · Play · Next) that walks the code **in execution order** — which is often not source order, and that divergence is usually the point. |
| **Flow diagram** | Hand-authored inline SVG in the bottom panel — control flow, call graph, data flow, state, or containment, whichever the code's shape asks for. Every node is clickable and jumps the walkthrough. |

Plus an optional **STATE** tab: a variable trace for algorithmic code, left out entirely for
config and glue.

## The accuracy contract

A page this polished is believed, so every failure mode is the same one: something on screen
that the code does not actually do.

- **The code is reproduced byte for byte** — whitespace, blank lines, comments. Never
  reformatted, renamed, re-indented, or quietly fixed on the way in.
- **Explains the code, not the intent.** Behaviour that depends on a caller or on unread
  library semantics is written as such.
- **Defects are named, never smoothed.** A swallowed exception is not "handles errors".
- **No invented runtime values** — a non-deterministic delay is written `0 … ceiling`, not
  `137 ms`.
- **`&`, `<`, `>` are escaped before tokenising**, or `List<int>` silently disappears.

It is not a code review and not a refactor. If a defect surfaces, it gets named in its card
and the fix is offered as separate work.

## Gating and output

- **Scope gate is conditional.** A clear snippet is explained immediately. `intent-lock` runs
  first only when the ask has more than one reading — a whole directory, several concerns, or
  a bare "explain this".
- **Vault is opt-in.** The file lands in the working directory. Ask to keep it and it is
  handed to `vault-keeper` as an asset; this plugin never resolves a vault path itself.

## Use it

```
/explain-code src/auth/session.ts
/explain-code withRetry
/explain-code            # explains the code in the conversation above
```

Or just ask: "explain this code", "walk me through this function", "annotate this",
"อธิบายโค้ดนี้".

## What's inside

```
skills/code-explainer/
  SKILL.md
  references/vscode-shell.md            # chrome, exact Dark+ palette, closed token set
  references/explanation-contract.md    # the three modes, fidelity, a11y, verification
  references/explainer-template.html    # working skeleton — steps with zero edits
examples/
  async-retry-with-backoff.html         # worked example + preview PNG
commands/explain-code.md
```

## Install

```
/plugin marketplace add <owner>/micky-psych-tools
/plugin install code-explainer@micky-psych-tools
```

Local development:

```
/plugin marketplace add .
/plugin install code-explainer@micky-psych-tools
```
