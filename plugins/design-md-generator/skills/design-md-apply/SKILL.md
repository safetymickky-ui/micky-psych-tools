---
name: design-md-apply
description: Applies the active DESIGN.md (the project's own, else the personal default at ~/.claude/DESIGN.md) to any visual UI being built, turning its tokens into CSS variables or a Tailwind theme, building components from its specs, obeying its Do's and Don'ts, and checking the result for off-system colors before calling it done. Use whenever the user asks to "build a page", "make a landing page", "create a component", "make an artifact", "build a dashboard", "design the UI", "style this", "make it look good", "mock up a screen", "ทำหน้าเว็บ", "ออกแบบ UI", or writes any HTML/CSS, React, Vue, Svelte, Tailwind or Artifact markup, and whenever a session note says a DESIGN.md is active. Not for creating or extracting a DESIGN.md (design-md-generator), critiquing an existing interface (gridgeist), or Office .docx/.pptx/.xlsx files (clinical-minimal).
---

# design-md-apply

Makes every UI built here look like one system. A SessionStart hook in this plugin names
the active DESIGN.md at the start of each session; this skill turns that file into code.
If no hook note exists (the session moved folders, say), run the lookup in step 1 yourself.

## Procedure

1. **Locate the file.** The nearest `DESIGN.md` from the working folder upward wins, then
   `~/.claude/DESIGN.md`. If none exists, build normally and offer `/design-md` once in
   your reply. Do not block on it.
2. **Read it whole.** That means the YAML tokens plus Overview, Components, Do's and
   Don'ts, Responsive Behavior and Iteration Guide. The prose says where the accent may
   appear and which treatments are banned, and the tokens alone do not.
3. **Emit tokens once, at the top**, as the only place raw values appear:
   - Plain CSS and Artifacts: custom properties on `:root`, named after the tokens
     (`--color-primary`, `--radius-md`, `--space-lg`, `--font-body`). Put `dark-*`
     tokens under `@media (prefers-color-scheme: dark)` guarded by
     `:root:not([data-theme="light"])`, and again under `:root[data-theme="dark"]`.
   - Tailwind v4: an `@theme` block. Tailwind v3: `theme.extend`. Or generate either with
     `npx -p @google/design.md designmd export --format css-tailwind|json-tailwind <path>`.
   - Fonts: load the families the file names from Google Fonts. Use the file's fallback
     stack verbatim.
4. **Build from components.** Match each element to its `components:` entry (button,
   card, input, badge, table…) and its variants (hover, pressed, focused, disabled).
   Reference variables only. A value with no token is a gap: use the nearest token and
   name the gap in your reply. Never invent a hex.
5. **Check before done.**
   - Search the output for hex, rgb() and px values outside the token block. Anything
     found must be a token or must go.
   - Count accent uses against the file's own limit.
   - Confirm dark mode renders.
   - Check any text/fill pair you introduced against WCAG 4.5:1.

## Precedence

The user's explicit instructions come first, then the project DESIGN.md, then the personal
default, then any skill's generic styling defaults. For Artifacts, the artifact-design
contract still owns page structure, theming mechanics and the CDN allow-list; DESIGN.md
supplies the values inside that contract.

## Brand guard

A file named `*-design-analysis`, or copied unchanged from a real brand, is reference
material. Never publish an Artifact or site that passes as that company: no its name, logo
or wordmark. Remixed, renamed systems are fine.

## Not for

Creating, extracting or editing the DESIGN.md itself (design-md-generator / `/design-md`).
Reviewing or redesigning an existing interface (gridgeist). Office documents
(clinical-minimal). Backend or non-visual code.
