# Animation grammar — how a concept becomes motion

The rules for **watch mode** in concept-lab (a scene-by-scene animation with no parameter
controls). SKILL.md decides *what* to animate; this file decides *how* it moves. Page layout,
palette, touch targets and the footer come from [build-contract.md](build-contract.md).

## The semantic motion vocabulary

Every motion is a claim. Pick from this table; if a motion's claim cannot be named, cut it.

| Motion                    | The claim it makes                                  |
| ------------------------- | --------------------------------------------------- |
| Fade/slide in             | This element enters the story now                   |
| Movement along a path     | Transport, flow, signal travelling                  |
| Morph / scale / color shift | State change, transformation, activation          |
| Pulse / glow              | Activity, firing, ongoing signal                    |
| Accumulation (count/fill) | A quantity building up                              |
| Split / merge             | Differentiation / combination                       |
| Motions in sequence       | Order, causality — A then B *because* A             |
| Motions in parallel       | Independence, simultaneity                          |
| Loop                      | A cycle, feedback                                   |
| Dim / fade out            | Leaves the story, inhibited, depleted               |

Two corollaries: **sequence is the strongest claim** — never sequence two events the concept
holds simultaneous, and never parallelize a causal chain; and **an eased curve is not
data** — easing is style, position and order are semantics.

## Scene architecture

- **3–8 scenes, one idea each.** A scene is *build* (elements enter) → *action* (the motion
  that makes the scene's claim) → *hold* (nothing moves; the caption is readable).
- **Caption per scene:** one sentence, on screen for at least twice its reading time, placed
  in a fixed caption region — never overlapping the action.
- **The final scene composes the full labelled diagram** — everything important on screen at
  once, at rest. It is the summary slide.
- **Pacing:** total runtime 20–90 s. No meaningful transition faster than ~300 ms; at most
  two simultaneous motions unless simultaneity *is* the claim; a beat of stillness before
  the signature moment so the eye is parked where the "aha" happens.

## Technical contract

- **Page:** the five-part page of the build contract. The main view (`.view`) is one inline SVG
  with a ≈4:3 `viewBox` and `preserveAspectRatio="xMidYMid meet"`. The caption is the status
  line (`#status`, `aria-live`). There are no presets and no parameter controls.
- **Player:** `Play/Pause` (`id="play"`), `Prev` (`id="prev"`), `Next` (`id="next"`),
  `Restart` (`id="restart"`), and a scene indicator (`3 / 6`). Real buttons, 44 px, keyboard
  operable (Space toggles, arrows step).
- **One scene controller.** CSS keyframes or the Web Animations API on SVG, driven by one
  vanilla-JS scene state (`data-scene` on the wrapper), so pause freezes everything coherently
  and Prev/Next land on clean scene boundaries. No libraries.
- **Autoplay off.** The page loads on scene 1 at rest.
- **`prefers-reduced-motion: reduce`:** animation off; each scene renders as a static frame
  that Prev/Next step through, carrying the full argument without motion.
- **Hooks for `verify.mjs`:** `window.__lab = { mode: 'watch', scenes: <count>, checks() }`.
  `checks()` asserts at least: every scene has a caption; the final scene shows every labelled
  element; in the clinical lane, every number on screen is in the `SOURCED` list.

## Accessibility

- Color is never the only signal — every color pairs with a label, shape, or icon; contrast
  meets WCAG AA in both the moving and the held states.
- Captions are real DOM text (selectable, screen-reader readable), never text baked into SVG
  paths or images.
- Informative SVGs carry `role="img"` and a `<title>`; decorative ones are hidden from the
  accessibility tree.
- Semantic structure: a real `<h1>` title; the caption is the `aria-live="polite"` status
  line, so scene changes are announced.

## Fidelity on screen

- Sourced numbers keep their units and qualifiers exactly as the source states them; a
  threshold line carries its value only if the value is sourced.
- Schematic curves, axes, and magnitudes are labelled **illustrative — not measured data**
  wherever they appear, clinical or not.
- Footer: as in the build contract, starting "Animation, illustrative." (general lane) or
  "Animation from: {report title, date}." (clinical lane).

## Verify

`scripts/verify.mjs` walks every scene at phone and desktop size, with motion on and reduced,
and saves one screenshot per scene hold. Then look at them: nothing clipped or overlapping,
captions legible, arrows and paths reading in the storyboard's direction, the final frame
complete and labelled. This pass changes how things sit on screen, never what they say.
