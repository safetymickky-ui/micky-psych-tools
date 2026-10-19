# DESIGN.md format

A condensed version of the Google Stitch spec
(<https://stitch.withgoogle.com/docs/design-md/specification/>, also printed by
`npx @google/design.md spec`), plus the extended sections the VoltAgent/awesome-design-md
files add. Tokens are the normative values. Prose explains how to apply them.

## Front matter (tokens)

The file starts with a line that is exactly `---`, YAML, then another exactly `---`.

```yaml
---
version: alpha
name: Acme-design-analysis
description: "One paragraph: canvas color, text color, the accent and where it may appear, type voice, card treatment, page rhythm."

colors:
  primary: "#5e6ad2"
  on-primary: "#ffffff"
  primary-hover: "#828fff"
  canvas: "#010102"
  surface-1: "#0f1011"
  hairline: "#23252a"
  ink: "#f7f8f8"
  ink-muted: "#8a8f98"
  error: "#e5484d"

typography:
  display-xl: { fontFamily: Inter, fontSize: 72px, fontWeight: 600, lineHeight: 1.05, letterSpacing: -2px }
  headline:   { fontFamily: Inter, fontSize: 28px, fontWeight: 600, lineHeight: 1.2,  letterSpacing: -0.5px }
  body:       { fontFamily: Inter, fontSize: 16px, fontWeight: 400, lineHeight: 1.5 }
  button:     { fontFamily: Inter, fontSize: 14px, fontWeight: 500, lineHeight: 1.2 }

rounded:
  sm: 6px
  md: 8px
  lg: 12px
  full: 9999px

spacing:
  xs: 8px
  md: 16px
  lg: 24px
  section: 96px

components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.on-primary}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: 8px 14px
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
---
```

Expand nested typography maps to block style in real files. The flow style above only
saves space here.

### Token types

| Type | Format | Example |
|---|---|---|
| Color | `#` + sRGB hex, quoted | `"#1A1C1E"` |
| Dimension | number + `px` / `em` / `rem` | `48px`, `-0.02em` |
| Token reference | `{group.name}` | `"{colors.primary}"` |
| Typography | `fontFamily`, `fontSize`, `fontWeight`, `lineHeight` (unitless preferred), `letterSpacing`, optional `fontFeature`, `fontVariation` | see above |

- References in `colors`, `rounded`, `spacing` must point at primitives. Only `components`
  may reference composites like `{typography.button}`.
- Component properties: `backgroundColor`, `textColor`, `typography`, `rounded`,
  `padding`, `size`, `height`, `width`. Others (for example `borderColor`) are accepted
  with a lint warning.
- Variants are separate entries: `button-primary-hover`, `button-primary-pressed`.
- Recommended names: colors `primary secondary tertiary neutral surface on-surface error`;
  typography `headline-display headline-lg headline-md body-lg body-md body-sm label-lg
  label-md label-sm`; rounded `none sm md lg xl full`. Custom names are valid.

## Body sections

All sections are `##`. An optional `#` title is not parsed. Omit a section that does not
apply, but keep the order. A duplicate section heading makes the file invalid.

| # | Section | What it holds |
|---|---|---|
| 1 | Overview | Personality, audience, mood, then a **Key Characteristics** bullet list. Fallback context when no rule applies. |
| 2 | Colors | Grouped `###` lists (Brand & Accent, Surface, Text, Semantic): **Name** (`{colors.x}`): hex + role. |
| 3 | Typography | `### Font Family` (with fallback stacks), `### Hierarchy` table (Token, Size, Weight, Line Height, Letter Spacing, Use), `### Principles`. |
| 4 | Layout | Spacing system, grid and container widths, whitespace philosophy. |
| 5 | Elevation & Depth | Shadow specs, or the flat alternative (tonal surface ladder, hairlines). |
| 6 | Shapes | Radius scale and where each step is used. |
| 7 | Components | `###` per component: anatomy, token refs, states. |
| 8 | Do's and Don'ts | `### Do` / `### Don't` guardrails. These steer generation hardest. |
| 9 | Responsive Behavior | Breakpoints, touch targets (44px min), collapsing strategy, image behavior. |
| 10 | Iteration Guide | Numbered rules for an agent editing UI with this file. Last rule: re-run lint. |
| 11 | Known Gaps | What could not be observed, proprietary fonts plus substitutes, provenance and credits. |

Sections 9–11 are extensions. Lint preserves unknown sections without error.

## Quality bar (from the reference collection)

- One accent, used scarcely. Say exactly where it may appear.
- Name colors by role (`ink`, `surface-2`, `hairline`), not by hue (`blue-500`).
- Every fill that carries text has an `on-*` partner that passes 4.5:1.
- Display tracking tightens as size grows. State the curve.
- Do's and Don'ts are concrete and checkable ("cards use `{rounded.lg}`, never pill"),
  not adjectives.
