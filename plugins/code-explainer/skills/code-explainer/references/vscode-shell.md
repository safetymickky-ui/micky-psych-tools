# The VS Code shell — design system

The left pane must read as **VS Code**, not as "a dark code block". Recognition is the
point: the reader trusts the annotation because the code sits where they read code every
day. Every value below is fixed — do not improvise a palette, and do not swap in a
different editor's look.

Theme is **Dark Modern / Dark+ only**. No light mode, no `prefers-color-scheme` switch —
committing to one iconic theme is what makes it recognisable. (`prefers-reduced-motion`
IS honoured; see `explanation-contract.md`.)

## Layout skeleton

```
┌───────────────────────────────────────────────────────────────┐
│ title bar        ● ● ●   retry.js — code-explainer            │
├────┬──────────────────────────────────┬───────────────────────┤
│ a  │ tab bar   ⟨ retry.js  ×⟩         │  EXPLANATION          │
│ c  ├──────────────────────────────────┤  ┌─────────────────┐  │
│ t  │ breadcrumb  src › retry.js › …   │  │ 1 · lines 1-4   │  │
│ i  ├──────────────────────────────────┤  │ …               │  │
│ v  │  1  export async function …      │  └─────────────────┘  │
│ i  │  2      …                  [mini]│  ┌─────────────────┐  │
│ t  │ ▶3      …                  [map ]│  │ 2 · lines 6-11  │  │
│ y  │  4      …                        │  │ …               │  │
│    ├──────────────────────────────────┤  └─────────────────┘  │
│    │ panel  FLOW │ STATE              │                       │
│    │  ┌──┐   ┌──┐   ┌──┐              │                       │
│    │  └──┘ → └──┘ → └──┘              │                       │
├────┴──────────────────────────────────┴───────────────────────┤
│ status bar  ⎇ main   Ln 3, Col 1   JavaScript   Step 2 / 8    │
└───────────────────────────────────────────────────────────────┘
```

CSS grid, `100svh`, panes scroll internally — the page itself never scrolls (see the fit
rule in `explanation-contract.md`).

## Colour tokens — chrome

Declare these as CSS custom properties on `:root` and use them by name. Values are VS
Code's own Dark Modern defaults, with **one deliberate exception**: the status bar keeps
the classic Dark+ `#007acc` blue rather than Dark Modern's `#181818`, because it is the
single most recognisable pixel in the editor and recognition is the whole point.

| Part | Property | Value |
| --- | --- | --- |
| editor background | `--vsc-editor-bg` | `#1f1f1f` |
| editor foreground | `--vsc-editor-fg` | `#cccccc` |
| title bar | `--vsc-titlebar-bg` | `#181818` |
| activity bar | `--vsc-activitybar-bg` | `#181818` |
| activity bar icon | `--vsc-activitybar-fg` | `#868686` (active `#d7d7d7`) |
| side/explanation panel | `--vsc-sidebar-bg` | `#181818` |
| tab bar strip | `--vsc-tabbar-bg` | `#181818` |
| active tab | `--vsc-tab-active-bg` | `#1f1f1f` (top border `#0078d4`) |
| inactive tab | `--vsc-tab-inactive-bg` | `#181818`, fg `#9d9d9d` |
| breadcrumb fg | `--vsc-breadcrumb-fg` | `#a9a9a9` |
| borders / separators | `--vsc-border` | `#2b2b2b` |
| line number | `--vsc-linenr` | `#6e7681` (active line `#cccccc`) |
| current-line highlight | `--vsc-line-highlight` | `#282828` |
| selection | `--vsc-selection` | `#264f78` |
| status bar | `--vsc-statusbar-bg` | `#007acc`, fg `#ffffff` |
| badge / accent | `--vsc-accent` | `#0078d4` |
| focus ring | `--vsc-focus` | `#0078d4` |
| scrollbar slider | `--vsc-scrollbar` | `#79797966` |
| debug current line | `--vsc-stackframe` | `rgba(255, 255, 0, 0.18)` |
| breakpoint dot | `--vsc-breakpoint` | `#e51400` |

The `#007acc` status bar is the single most recognisable pixel in VS Code. Keep it.

## Colour tokens — syntax

A **closed set** of token classes. The skill emits pre-tokenised markup; there is no
runtime highlighter (see `explanation-contract.md`). Map every language onto these:

| Class | Meaning | Colour |
| --- | --- | --- |
| `.t-com` | comment | `#6a9955` |
| `.t-str` | string, template literal, char | `#ce9178` |
| `.t-num` | number, boolean-ish literal value | `#b5cea8` |
| `.t-key` | control keyword — `if else for while return await yield import from try catch throw` | `#c586c0` |
| `.t-dec` | declaration/storage keyword — `def class const let var function async export public static` | `#569cd6` |
| `.t-fn` | function or method name at definition and call site; decorators | `#dcdcaa` |
| `.t-typ` | class, type, interface, enum, namespace, module | `#4ec9b0` |
| `.t-var` | identifier, parameter, property, field | `#9cdcfe` |
| `.t-con` | language constant — `True False None null undefined self this` | `#569cd6` |
| `.t-op` | operator and punctuation | `#d4d4d4` |
| `.t-rgx` | regular expression body | `#d16969` |
| `.t-esc` | escape sequence inside a string | `#d7ba7d` |
| `.t-inv` | deliberately invalid / error-marked token | `#f44747` |

Unclassified text inherits `--vsc-editor-fg`. Never invent a fourteenth class, and never
colour a token to make a point the code does not make.

**Contrast:** the syntax tokens above all clear WCAG AA on `#1f1f1f` — the darkest,
`.t-com` `#6a9955`, measures ≈ 4.9:1 and `.t-key` `#c586c0` ≈ 5.9:1. The one value that
does **not** is the inactive line number, `#6e7681` ≈ 3.6:1, which is exactly why line
numbers are `aria-hidden` decoration and every range is also named in text on its card.
Everything in the **explanation rail, status bar, panel labels, and controls** must clear
**4.5:1** — those are not fidelity-bound, so if a chrome value fights legibility, adjust
the chrome, never the token colours. Measure rather than assume if you deviate at all.

## Typography

```css
--font-code: ui-monospace, "Cascadia Code", "Cascadia Mono", Consolas,
             "SF Mono", Menlo, "DejaVu Sans Mono", monospace;
--font-ui:   system-ui, "Segoe UI", -apple-system, "Helvetica Neue", sans-serif;
```

No `@font-face`, no Google Fonts, no CDN — the file must open offline. Code 13px /
line-height 20px (VS Code's default ratio); UI chrome 12–13px; explanation body 14–15px
in `--font-ui` (the rail is prose — do not set it in mono).

## Chrome parts — what each must do

- **Title bar** — the filename and the plugin name. Three window dots are fine as pure
  decoration; give the group `aria-hidden="true"`.
- **Activity bar** — a narrow icon strip, inline SVG only (Explorer, Search, Source
  Control, Run & Debug, Extensions). It is **decoration**: `aria-hidden="true"`, no
  `<button>`, no hover affordance implying a click. Never render a control that does
  nothing.
- **Tab bar** — one active tab: language file-icon glyph, filename, a dirty/close dot.
  Multiple tabs only if you are genuinely explaining multiple files, and then they must
  actually switch.
- **Breadcrumb** — the real path through the code (`file › Class › method`), driven by
  the current step when stepping. For a snippet with no enclosing scope, show just the
  filename — never fake a path, and never delete the element (the row is part of the
  editor's grid).
- **Gutter** — right-aligned line numbers; the current step's first line gets the active
  colour plus a `▶` execution arrow; every annotated range start carries a
  breakpoint-style dot in `--vsc-breakpoint`. Line numbers are `user-select: none` and
  `aria-hidden` (they are visual; the explanation cards name the ranges in text).
- **Minimap** — optional, and only for code over ~40 lines. Render it as a CSS/SVG
  abstraction of line lengths, not real text. Cheap and convincing; drop it entirely
  rather than faking it badly.
- **Panel** — bottom dock, VS Code's terminal-panel idiom, uppercase 11px tab labels
  (`FLOW`, and `STATE` when a trace exists). Real tabs: they switch, they are `<button>`s
  with `role="tab"`, and they are keyboard operable.
- **Status bar** — `#007acc`, left: branch/language glyphs; right: `Ln n, Col 1`,
  language name, and the live `Step n / N`. The step counter here is the reader's
  position indicator — keep it in sync.
- **Debug toolbar** — the walkthrough is styled as a **debug session**: a floating pill
  toolbar at the top-centre of the editor pane (`#181818`, 1px `--vsc-border`, 6px
  radius, soft shadow) with Restart · Prev · Play/Pause · Next. Real buttons, real
  labels, real focus rings.

## Fidelity guardrails

- Never render a VS Code affordance that does not work. Decorative chrome is
  `aria-hidden` and visually inert; anything that looks clickable must be clickable.
- Do not add editor features the artefact does not have — no fake IntelliSense popup, no
  fake squiggle under working code, no fake git decorations in the gutter.
- `.t-inv` and a red squiggle are allowed **only** where the explanation names a real
  defect in the code being explained.
