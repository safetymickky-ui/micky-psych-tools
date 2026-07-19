# Animation grammar — how a concept becomes motion

The rules every concept-animation build follows. SKILL.md decides *what* to animate; this
file decides *how*, so two animations from this plugin feel like siblings.

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
  once, at rest. It is the summary slide and the frame that gets exported as PNG.
- **Pacing:** total runtime 20–90 s. No meaningful transition faster than ~300 ms; at most
  two simultaneous motions unless simultaneity *is* the claim; a beat of stillness before
  the signature moment so the eye is parked where the "aha" happens.

## Technical contract

- **One HTML file.** Inline `<style>`, inline `<script>`, inline SVG. No external CSS, JS,
  fonts, images, or CDN — opens offline, identical everywhere. System font stack.
- **CSS keyframes / Web Animations API on SVG + a small vanilla-JS scene controller.** No
  libraries. One source of truth for scene state, so pause freezes everything coherently
  and Prev/Next lands on clean scene boundaries.
- **Controls, always visible:** Play/Pause, Restart, Prev/Next scene, current-scene
  indicator (e.g. `3 / 6`). Keyboard operable: Space toggles, arrows step. Buttons are real
  `<button>` elements with labels.
- **`prefers-reduced-motion: reduce` is mandatory:** animation disabled, scenes rendered as
  a stepped storyboard (Prev/Next through static frames, or all scenes stacked) that carries
  the full argument without motion.
- **Autoplay off by default** — the page loads on scene 1 at rest with a visible Play
  affordance.

## Accessibility

- Color is never the only signal — every color pairs with a label, shape, or icon; contrast
  meets WCAG AA in both the moving and the held states.
- Captions are real DOM text (selectable, screen-reader readable), never text baked into SVG
  paths or images.
- Informative SVGs carry `role="img"` and a `<title>`; decorative ones are hidden from the
  accessibility tree.
- Semantic structure: a real `<h1>` title, the caption region an `aria-live="polite"`
  element so scene changes are announced.

## Fidelity on screen

- Sourced numbers keep their units and qualifiers exactly as the source states them; a
  threshold line carries its value only if the value is sourced.
- Schematic curves, axes, and magnitudes are labelled **illustrative — not measured data**
  wherever they appear, clinical or not.
- Footer: source report title + counts (clinical lane) or *illustrative — established
  knowledge* (general lane); render date; for clinical content the line *teaching aid, not a
  substitute for clinical judgment or local protocol.*

## Verify

- Render in a headless browser; screenshot **each scene's hold + the final frame**.
- Look: nothing clipped or overlapping, captions legible, arrows and paths reading in the
  storyboard's direction, the final frame complete and labelled.
- Fix the HTML and re-render until it holds; export the final frame as the companion PNG.
- This pass changes how things sit on screen — never what they say.
