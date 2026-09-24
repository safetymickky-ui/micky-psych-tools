# Spec S05: visuals family shell, concept-animation (sole owner) and ml-concept-lab

| Field | Value |
|---|---|
| Repos | micky-psych-tools (`/home/user/micky-psych-tools`) and learn-hub (`/home/user/learn-hub`) |
| Units (today → target) | `plugins/concept-animation`(+`/animate`) → `plugins/visuals/skills/concept-animation`+dmi alias `visuals:animate`. `plugins/ml-concept-lab`(+`/visualize`) → `plugins/visuals/skills/ml-concept-lab`+dmi alias `visuals:visualize`. learn-hub `.claude/skills/concept-animation` (the copy) → absorbed then deleted (atomic swap, W2). New family files: `references/html-artifact-contract.md`, `references/render-verify.md`, `scripts/check-html.mjs`(+tests, fallback port), parity fixture. |
| Waves | W1 (copy YAML fix, H43); W2 (layout port+5-frame verify both skills; `check-html.mjs`+parity fixture; filing via sink; atomic swap deletes copy); W3 (move into `visuals`; shared contract stated once; ML size trim) |
| Owner decisions assumed | OD1-a, OD2-a, OD3-a, OD4-a, OD5-a, OD9-a, OD10-a, OD13-a, OD14-a |
| Defects closed | 27 of 27 assigned (HIGH: H38, H39, H40, H41, H43) |
| Interfaces owned | I07 |
| Interfaces consumed | I01(S01), I08(S16), I09(S15), I11(S07), I16(S11), I17(S12), I20(S08), I23(S10) |
| Depends on specs | S01, S06, S07, S08, S10, S11, S12, S15, S16, S19 |

## 1. Current state (measured 2026-09-24)

Repo heads: micky `e4ae3d8`, learn-hub `7ce31aa`. Tokens=chars/4. Probes this session (read-only): P1 learn-hub audits on the 4 examples; P2 5-frame Playwright render of today's CA/ML/copy examples; P3 Chromium launch variants; P4 same render with the W2 contract simulated; P5 ML explorable drive; P6 `node --test` glob behavior; P7 §2.7 static rules on the 4 examples+2 known-bad fixtures.

### 1.1 Files

| Path | L/B/Tok | Role |
|---|---|---|
| micky `concept-animation/skills/concept-animation/SKILL.md` | 168/10,541/2,599(body 2,325) | the skill |
| micky `.../references/animation-grammar.md` | 96/6,060/1,505 | motion vocab+doc/layout+verify |
| micky `concept-animation/examples/tms-electromagnetic-induction.html`(+`.final.png`) | 456/26,532/6,600 | worked example; unlinked from SKILL.md |
| micky `concept-animation/.claude-plugin/plugin.json`,`commands/animate.md` | 17+18 lines | v0.1.1; `/animate` wrapper |
| micky `ml-concept-lab/skills/ml-concept-lab/SKILL.md` | 241/15,381/3,800(body 3,533) | the skill |
| micky `.../references/build-contract.md` | 245/13,248/3,286 | contract+48-line JS verify recipe(:195-242); no `## Contents` |
| micky `.../references/concept-patterns.md` | 234/16,461/4,020 | 8 families+anti-patterns; no `## Contents` |
| micky `ml-concept-lab/examples/learning-rate-and-conditioning.html`(+README,`.preview.png`) | 710/33,051/8,227 | worked explorable |
| micky `ml-concept-lab/.claude-plugin/plugin.json`,`commands/visualize.md` | 17+24 lines | v0.1.0; `/visualize` wrapper |
| learn-hub `.claude/skills/concept-animation/SKILL.md` | 207/13,515/3,345(body 3,084) | the copy; YAML invalid |
| learn-hub `.../references/animation-grammar.md` | 132/9,124/2,264 | copy's grammar (newer layout) |
| learn-hub `.../examples/tms-electromagnetic-induction.html` | 492/28,624/7,120 | copy's example |
| learn-hub consumed: `scripts/lib/animation-responsive.mjs`+`.test.mjs`, `infographic-responsive.mjs`, `src/lib/animation-layout.ts`, `scripts/animations/pk-plasma/verify.mjs` | ~780 lines total | source of the audits/floor guard/5-frame verify ported into I07/§2.5 |

Micky CA/ML have no README, CHANGELOG, LICENSE, `scripts/` or `evals/`.

### 1.2 Descriptions

| Unit | Chars/Bytes | YAML | Use-when/Not-for at | Quoted / slash triggers |
|---|---|---|---|---|
| micky CA (SKILL.md:3-15) | 1,022/1,074 | yes | 252/850 | "animate this concept","create an animation","make an animation of X","animated explainer","show it moving","ทำแอนิเมชัน","ภาพเคลื่อนไหว"; unquoted `/animate` |
| micky ML (SKILL.md:3-15) | 997/1,039 | yes | 311/815 | "visualize this concept","interactive visualization","make an interactive demo","explorable","let me play with the parameters","show me how X works","animate this algorithm","ทำภาพอธิบายแบบโต้ตอบ"; unquoted `/visualize` |
| copy CA (SKILL.md:3) | 1,000/1,006 | **no** — `yaml.safe_load` "mapping values are not allowed here" | 436/869 | same core CA phrases + "/animate","add an animation to the hub" |

### 1.3 Defects

Every id, prefixes `concept-animation-`,`ml-concept-lab-`,`concept-animation (learn-hub copy)-` (defect-index.txt:223-241,252-259), appears once. `ca-N`/`ml-N`/`copy-N` shorthand below.

| Id | Sev | H# | Evidence | Problem → fix | Wave |
|---|---|---|---|---|---|
| concept-animation-1 | H | H38 | grammar:46,48 `.wrap{height:100dvh}`+`min-height:0` stage. P2: stage 87-401px, clipped all 5 frames | Collapses on phones → S05-W2-3: I07-C port | W2 |
| concept-animation-2 | H | H39 | SKILL.md:110-115 "1366×768…no scroll" | 1 viewport can't fail on collapse → S05-W2-1, S05-W2-3: 5-frame check | W2 |
| concept-animation-3 | M | — | SKILL.md:111 `calc(100svh-6rem)`; `animation-viewer.tsx:343` differs | Stale geometry → S05-W2-3: deleted, formula in I07-G | W2 |
| concept-animation-4 | M | — | example:1 no `<!DOCTYPE`, 0 `color-scheme`; P2 `BackCompat` | Quirks mode → S05-W2-3: full document(I07-B) | W2 |
| concept-animation-5 | M | — | description 1,022 chars | Hard-cap → S05-W2-3: 627 W2; S05-W3-2: 600 W3 | W2/W3 |
| concept-animation-6 | M | — | SKILL.md:6 "algorithms"; ML:9-10 overlaps | No boundary → S05-W2-3: Not-for/Handoffs name each other | W2 |
| concept-animation-7 | M | — | SKILL.md:122-126 "→`vault/assets/`"; empty-vault:55-56 removed w/topic | Filed assets dead-end → S05-W2-3: sink(I09/I11) | W2 |
| concept-animation-8 | L | — | SKILL.md:104-106; no `scripts/` | Checks as prose → S05-W2-1, S05-W2-3: `check-html.mjs --shots` | W2 |
| concept-animation-9 | L | — | 0 hits `grep examples SKILL.md` | Example orphaned → S05-W2-3: Step 3 links it | W2 |
| concept-animation-10 | L | — | only SKILL.md+references/ | No evals → S05-W2-5: 4 cases | W2 |
| ml-concept-lab-1 | H | H40 | build-contract:140,141 same as ca-1. P2: stage 0px, 4 frames | Same collapse → S05-W2-4: I07-C port | W2 |
| ml-concept-lab-2 | H | H41 | build-contract:195-202 bare `import{chromium}`,1 viewport; `ERR_MODULE_NOT_FOUND`(global-only) | Recipe can't run → S05-W2-4: resolves via `npm root -g`; recipe deleted | W2 |
| ml-concept-lab-3 | M | — | build-contract:103 "rel err<1e-5" vs example:333-346 absolute-diff impl | Contract drifted → S05-W2-4: abs diff+floor(H-10) | W2 |
| ml-concept-lab-4 | M | — | SKILL.md:15 clinical→CI;:196-198 clinical→CA | Routing self-contradicts → S05-W2-4: all clinical→CA | W2 |
| ml-concept-lab-5 | M | — | SKILL.md:76-77 path unresolvable from skill dir | S05-W2-4: → `${CLAUDE_PLUGIN_ROOT}/examples/…` | W2 |
| ml-concept-lab-6 | M | — | body 3,533 tok; JS recipe in fence; 10,839 tok full load | Over-long → S05-W2-4: script(W2); S05-W3-3: ≤5,000(W3) | W2/W3 |
| ml-concept-lab-7 | L | — | SKILL.md:9-10 2 CA-overlapping phrases | Over-broad → S05-W2-4: removed | W2 |
| ml-concept-lab-8 | L | — | example doctype-less | Quirks mode → S05-W2-4: full document | W2 |
| ml-concept-lab-9 | L | — | no evals/CHANGELOG/README | S05-W2-5: → 4 cases; S05-W2-6: +files | W2 |
| concept-animation (learn-hub copy)-1 | H | H43 | copy SKILL.md:3 unquoted `description:` w/": " → ScannerError | Strict loaders get empty metadata → S05-W1-1: folded `>-` | W1 |
| concept-animation (learn-hub copy)-2 | M | — | copy grammar:58 `min()` overridden. P2: 116px at 844×390 | Collapses landscape → S05-W2-3: `max()` port; S05-W2-8: copy deleted | W2 |
| concept-animation (learn-hub copy)-3 | M | — | copy SKILL.md:129 omits 844×390 | S05-W2-3: → 5-frame check; S05-W2-8: copy deleted | W2 |
| concept-animation (learn-hub copy)-4 | M | — | copy example doctype-less, violates own grammar | S05-W2-3: → micky example rebuilt; S05-W2-8: copy deleted | W2 |
| concept-animation (learn-hub copy)-5 | M | — | copy SKILL.md:171 "`npm run sync`→apply" | Names dry SQL emitter → S05-W2-8: not ported (deleted with the copy; owned by S16/S13) | W2 |
| concept-animation (learn-hub copy)-6 | L | — | copy SKILL.md:94 stale builder path | S05-W2-8: → corrected handover(H-6), copy deleted | W2 |
| concept-animation (learn-hub copy)-7 | L | — | copy sidecar/SQL verify duplicates `ingest-animation` | S05-W2-8: → deleted, owned by `ingest-visual`(S16) | W2 |
| concept-animation (learn-hub copy)-8 | L | — | copy triggers = micky CA's, different destinations | S05-W2-8, S11-W2-3: atomic swap (branch push + merge) | W2 |

No deferrals; no ratchet entry kept past W3.

### 1.4 Other findings

Shared tail (verify/output/handoffs/close/failure) = 41% CA / 35% ML body → W3 moves into `html-artifact-contract.md`. The layout fix existed only in the learn-hub copy → one ported grammar(I07-C); ground truth lives entirely in learn-hub scripts, ported by `check-html.mjs`. NEW-1(P3): Playwright with `PUPPETEER_EXECUTABLE_PATH` crashes; its own Chromium works → resolution order §2.5. NEW-3: the copy's example differs from `vault/tms-principles/…html` only at line 156 (vault has the fixed floor). NEW-6(P6): a quoted test glob is required, Node 22 fails on a bare dir. NEW-7: `auditAnimationLayout` misses copy-2's landscape defect — only render check I07-G catches it. NEW-9/10/11(P4/P5): both examples' non-layout logic is sound; the W2 contract renders clean at all 5 frames. NEW-12: refs need `## Contents`.

## 2. Target state

### 2.1 Location and tree

**After W2** (plugins stay at today's names): `CA` gets `plugin.json`(v0.2.0)+README/CHANGELOG/LICENSE; `commands/animate.md`(pointer only, deleted W3); rebuilt `examples/tms-electromagnetic-induction.html`(+`.final.png`); `scripts/check-html.mjs`+`.test.mjs`+`fixtures/{bad-animation.html,bad-infographic.html,parity.json}`(canonical, I07); `skills/concept-animation/SKILL.md`+`references/animation-grammar.md`; 4 eval cases. `ML` mirrors it (v0.2.0, README/CHANGELOG/LICENSE, rebuilt example, byte-identical `check-html.mjs`, `skills/ml-concept-lab/SKILL.md`+`references/{build-contract,concept-patterns}.md`, 4 eval cases). Plus `plugins/clinical-infographic/scripts/check-html.mjs`(byte-identical copy, S06 uses it). learn-hub `.claude/skills/concept-animation/` DELETED on a branch by S05-W2-8, merged by S11-W2-3 (CX-30).

**After W3** (S10's skeleton moves both plugins unchanged into `plugins/visuals/`; S05 edits content): `V=plugins/visuals` gets `.claude-plugin/plugin.json`(S10 creates; S05-W3-4 sets fields), README/CHANGELOG/LICENSE, `references/{html-artifact-contract,render-verify}.md`(I07, stated once), `scripts/check-html.mjs`+`.test.mjs`+`fixtures/`(single copy), both examples(+S06's), `skills/{concept-animation,ml-concept-lab,animate(dmi),visualize(dmi)}/`+S06's 4 skills, `evals/{concept-animation,ml-concept-lab}/`. Removed in W3: `plugins/concept-animation/`, `plugins/ml-concept-lab/`, both `commands/` files, the 2 non-canonical `check-html.mjs` copies after `cmp` confirms identity.

### 2.2 Frontmatter

One description per skill, used at W2 and W3: sibling names unprefixed at W2, `visuals:…` at W3. Parsed with `yaml.safe_load` this session. `→` below = "W2 name → W3 name"; the shipped file names only the wave's own form.

**`concept-animation`** (627 chars W2/600 W3, Use-when 193, Not-for 363, no I/you/your, no angle brackets):
```yaml
---
name: concept-animation
description: >-
  Builds a watch-only HTML animation that explains one concept scene by scene, clinical
  mechanisms included: a self-contained file with captions, player controls and a
  reduced-motion storyboard. Use when the user says "animate this concept", "create an
  animation", "make an animation of X", "animated explainer", "show it moving",
  "ทำแอนิเมชัน" or "ภาพเคลื่อนไหว". Not for an explorable the learner drives (use
  ml-concept-lab:ml-concept-lab → visuals:ml-concept-lab), a static one-page sheet (use
  clinical-infographic:clinical-infographic → visuals:clinical-infographic), a walkthrough
  of given code (use code-explainer:code-explainer → visuals:code-explainer), or a chart
  of the user's own data (use dataviz).
argument-hint: "[concept, or path/title of a sourced report]"
allowed-tools:
  - "Bash(node ${CLAUDE_PLUGIN_ROOT}/scripts/check-html.mjs *)"
  - "Bash(npm --prefix * run -s audit:visual *)"
metadata:
  profile: cc
---
```

**`ml-concept-lab`** (602 chars W2/585 W3, Use-when 217, Not-for 398):
```yaml
---
name: ml-concept-lab
description: >-
  Builds an interactive explorable of a machine-learning, AI or computer-science concept
  such as gradient descent or attention: one self-contained HTML file where the real
  algorithm runs live and the learner drives it. Use when the user says "visualize this
  concept", "interactive visualization", "make an interactive demo", "explorable", "let me
  play with the parameters" or "ทำภาพอธิบายแบบโต้ตอบ". Not for a watch-only animation or
  any clinical concept (use concept-animation:concept-animation → visuals:concept-animation),
  charting the user's data (use dataviz) or a walkthrough of given code (use
  code-explainer:code-explainer → visuals:code-explainer).
argument-hint: "[ML/AI/CS concept, e.g. gradient descent, self-attention, Dijkstra]"
allowed-tools:
  - "Bash(node ${CLAUDE_PLUGIN_ROOT}/scripts/check-html.mjs *)"
  - "Bash(npm --prefix * run -s audit:visual *)"
metadata:
  profile: cc
---
```

**W3 alias skills** (dmi; S10's skeleton creates them from the I20 template — §2.7 ASSUMES-4 tracks who writes it): `skills/animate/SKILL.md` (89-char description, 1-line body):
```markdown
---
name: animate
description: "Typed shortcut: /animate runs visuals:concept-animation with the given concept or source."
disable-model-invocation: true
argument-hint: "[concept, or path/title of a sourced report]"
metadata:
  profile: cc
---

Invoke `visuals:concept-animation` with: $ARGUMENTS
```
`skills/visualize/SKILL.md` (91-char description): same shape, `visuals:ml-concept-lab`, `argument-hint: "[ML/AI/CS concept, e.g. gradient descent, self-attention, Dijkstra]"`.

**Learn-hub copy, W1** (H43): only SKILL.md:3 changes — `description: Author a self-contained …` becomes `description: >-` followed by the identical 1,000-char text, indented, folded. `yaml.safe_load` returns the same string. Body (203 lines) unchanged.

Kept trigger phrases: all 7 CA, 5 of ML's 8 (drops "show me how X works","animate this algorithm" — ml-7). Full list §6.

### 2.3 Body outline

Actions: keep|cut(reason)|move→file|script→name|new. Targets: CA SKILL.md ≤185/≤2,900 tok(today 152/2,325); CA grammar ≤150/≤2,400; ML SKILL.md ≤240/≤3,600(today 225/3,533); ML build-contract ≤215/≤2,800.

**CA SKILL.md**: title/rules/refs keep + R27 + "Step3.5 pass before Step4". Step0: new(H-2), adds `topic_hint`. Step1: keep, widened+OPTIONAL fallback(H-3). Step2: keep. Step3: rewrite — full document, self-contained, I07-C layout, I07-E hooks, captions, reduced motion, a11y, footer; start from the example. Step3.5: script→`check-html.mjs`(H-5), cuts ca-2/ca-3. Step4: rewrite — write+surface+file(H-7,I09). Handoffs: rewrite per §2.6. Close/Gotchas(new,H-8)/Failure: keep+`Assumed:`+verdict; 7 conditions kept, 3 replaced.

**CA grammar**: keep title/motion vocab/scenes; replace layout/doc rules with I07-B/I07-C(cuts stale geometry, 1366×768 check); keep controls+I07-E,reduced motion,a11y,fidelity; cut verify→SKILL.md Step3.5; add `## Contents`.

**ML SKILL.md**: title/rules keep + R27 + Step-3.5-before-4. Refs: rewrite — read `concept-patterns.md`'s `## Contents` then match; read `build-contract.md`; example path via `${CLAUDE_PLUGIN_ROOT}`(ml-5,R13,R49). Step0: new(H-2). Steps1-2: keep. Step3: keep + full document + drive hooks. Step3.5: script→`--kind explorable`(H-5 variant). Step4: rewrite as CA, `kind:explorable`. Handoffs: rewrite — CA(watch-only+clinical, fixes ml-4); code-explainer; dataviz; gridgeist; firecrawl/vault-keeper(OPT). Close/Gotchas(new,H-9)/Failure: same edits as CA.

**ML build-contract**: keep title+anatomy/engine/determinism/numbers+`## Contents`; gradient row replaced by H-10; keep perf; replace explorable layout with I07-C variant; keep palette/a11y/footer; replace the JS recipe with a ≤10-line list of what `check-html.mjs` drives. `concept-patterns.md`: add `## Contents` only.

**Learn-hub copy→destinations**: description phrases→CA description+`ingest-visual`(S16); Step0/1/topic→CA; Step3/builder/phone rules→CA/grammar(W2)→`html-artifact-contract.md`+I07-C(W3, H-6 to S16); viewport verify+frame formula→`check-html.mjs`+`render-verify.md`; sidecar/sync/SQL verify→cut(`ingest-visual` owns filing); example→superseded by the vault-file rebuild.

**W3 trims** (CA body ≤130/≤2,000, grammar ≤70/≤1,100; ML mandatory load ≤5,000 tok, arch §9): Step-3 rows point at `html-artifact-contract.md`; Step-3.5 keeps a 4-line command+pass rule, rest→`render-verify.md`; Step-4/Close collapse into the contract's `§Output`. References keep motion-vocab/anatomy/engine/self-check/palette/footer; document+layout move out.

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `.../animation-grammar.md` | motion vocab, scenes, hooks, fidelity(W3);+doc/layout(W2) | "Before Step 2, read …" | W2 ≤150/≤2,400; W3 ≤70/≤1,100 |
| `.../build-contract.md` | anatomy, engine, determinism, numbers, self-check, perf, palette, footer | "Before Step 3, read …" | W2 ≤215/≤2,800; W3 ≤1,700 |
| `.../concept-patterns.md` | 8 families | "Before Step 1, read `## Contents`, then match" | unchanged |
| `references/html-artifact-contract.md`(W3, family) | I07-A…F+output+failure | "Before Step 3, read …" | ≤150/≤1,400 |
| `references/render-verify.md`(W3, family) | I07-G tool order/frames/thresholds/exit codes | "If Step 3.5 not pass, read …" | ≤90/≤900 |
| examples (both) | reference build/lab | named at reference load/Step 3 | unchanged |

### 2.5 Scripts

**`check-html.mjs`**(I07). W2 at `concept-animation/scripts/`, byte-identical at `ml-concept-lab/scripts/`+`clinical-infographic/scripts/`(S06). W3: single copy at `visuals/scripts/`. ESM, Node ≥18, no npm deps; Playwright optional, loaded at run time.

CLI:
```
node check-html.mjs <file.html> [--kind infographic|animation|explorable|code-explainer]
                    [--own] [--static-only] [--shots <dir>] [--learn-hub <dir>] [--json]
node check-html.mjs --parity [--root <micky-dir>] [--learn-hub <dir>] [--json]
node check-html.mjs --help
```
`--kind` picks the rule set(I07-A), inferred if omitted; skills always pass it. `--learn-hub` default `$LEARN_HUB_DIR`, valid only if a real learn-hub checkout. Default **delegates** to `npm --prefix <dir> run -s audit:visual -- <abs file> --json --kind <kind>` when valid (`"tool":"audit:visual"`); on failure, `delegation_error`+own checks. `--kind code-explainer` is **never delegated** — I08's `audit:visual` rejects it (exit 2); `check-html.mjs` always runs its own port for that kind (CX-10). `--own` skips delegation. `--static-only` skips render/drive. `--shots <dir>` writes PNGs regardless of delegation. `--root` default `$MICKY_TOOLS_DIR`. `--help` exits 0.

Own checks: (1) static(I07-H, no browser); (2) render(anim/explorable): per `VIEWPORTS`, context `appFrame(vw,vh)`, load+measure(I07-G); animation walks scenes via `#nextBtn`, keeps worst; plus a reduced-motion pass for page-errors; (3) drive: animation completes the walk+`#restartBtn`; explorable exercises every `[data-preset]`/range/`#play`/`#reset`/`#step`/`[data-check]`, scans for non-finite tokens.

Browser resolution: Playwright via `createRequire`(falls back to `npm root -g`) → its bundled Chromium → `PUPPETEER_EXECUTABLE_PATH` if set(NEW-1 order) → no render, reason stated. 10s/action, ≤180s/file.

Stdout, one JSON object: `tool,schema,file,kind,verdict,delegated,render{ran,browser,reason},issues[{code,method,where,detail,fix}],frames[{viewport,frame,stage_min_px,controls_max_bottom_px,limit_px,clipped,overlaps,scroll_width_px}],drive{ran,scenes,restart_ok,checks_failing},shots`; delegation adds `raw` instead of `frames`/`drive`.

`verdict`: `fail` on any issue; `pass` when every check the kind needs ran; `incomplete` if render/drive couldn't run — including when delegating and `audit:visual`'s own response carries a non-empty `skipped` array (a producer must never file an unrendered file as `pass`, CX-10). Exit: 0 pass, 1 fail, 2 usage error, 3 incomplete/`--parity` env missing.

`--parity`(I07-J): reads `fixtures/parity.json`, resolves rows by basename(0/≥2 matches→exit 2), runs own+`audit:visual` per row, prints `agree`+per-row `missing_codes`. Exit 0 all agree, 1 disagree, 3 env missing.

Pure exports (tested browser-free): `RULES,VIEWPORTS,inferKind,staticIssues,appFrame,foldLimit,overlapPairs,parseIndicator,verdictOf,loadParityManifest,resolveByBasename`. Ported verbatim, commented at source (learn-hub `7ce31aa`), from the 4 files cited in §1.1.

**`check-html.test.mjs`** (`node:test`; no network/browser/wall-clock). Run via the quoted glob(NEW-6), never a bare dir. Groups: help/usage; bad fixtures (exact codes); static rules (pass+fail per rule); layout (the 8 `auditAnimationLayout` cases ported from `animation-responsive.test.mjs:81-169`); geometry (`appFrame`, fold limits, overlap sort, indicator parse, kind inference); copies+parity (byte-equal canonical; manifest valid, static verdict=`expected`).

### 2.6 Handoffs

Exact sentences. W2 names given; W3 substitutes `intent-lock:intent-lock`→`alignment:intent-lock`, `comprehensive-review:comprehensive-review`→`evidence:comprehensive-review`, `pubmed-research-note:pubmed-research-note`→`evidence:pubmed-research-note`, sibling names→`visuals:…`. `vault-keeper:vault-keeper` unchanged.

**H-2 Step 0** (both; I01 verbatim): "Run `intent-lock:intent-lock` (OPTIONAL). If it is not available in this session — or it needs an interactive picker and none exists here (subagent, headless, scheduled run) — do not stall: take the broadest reading that fits the request and open the output with one line `Assumed: <reading> — say if wrong.`" CA settles aha/audience/depth/scope/topic; ML settles misconception/audience/depth/scope. Opt-outs: "just animate it"(CA), "just build it"(ML).

**H-3 CA Step 1**: "Query `vault-keeper:vault-keeper` (OPTIONAL) for a matching review or decision report. If it is not available, ask the user to point at a sourced report file. In a headless run, use the general lane only and name the clinical facts left out."

**H-5 Step 3.5** (CA; ML uses `--kind explorable`/"preview"):
> Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/check-html.mjs <file> --kind animation --shots <shots-dir>`. It uses `npm run audit:visual` when `$LEARN_HUB_DIR` is valid, its own port otherwise; the JSON `tool` field says which ran. Proceed to Step 4 only on `verdict:"pass"`. On `fail`, fix each issue's `fix` text and re-run. On `incomplete`(exit 3), say the render checks did not run and why, deliver with that statement. Then open the shots: each scene's hold and the final frame, storyboard order, nothing clipped, captions legible. Keep the final-frame PNG.

**H-6 Handover to S16** (pk-plasma-animation; replaces copy SKILL.md:92-99, copy-6):
> An animation with a real simulator or state machine is built, not hand-written. Keep the engine and state as pure, import-free modules (shared `scripts/animations/pk-plasma/`, drug data `scripts/animations/<drug>-plasma/`), test with vitest, inline with `node scripts/animations/pk-plasma/build.mjs <drug>-plasma` (methylphenidate: `npm run anim:mph`). Two phone rules: a mobile grid override uses `minmax(0,1fr)`, never a bare `1fr`; the stage is never `position:sticky` over the controls.

The two phone rules also enter I07-C.

**H-7 Step 4 filing** (I11 visual filing sentence, owner S07 §2.7, adopted verbatim per CX-8): "Run `vault-keeper:vault-keeper` (OPTIONAL). If it is not available in this session — or the sink cannot resolve a destination and this is a non-interactive run — do not stall: file via `vault-keeper` when present; if absent, write `<slug>.html` and `<slug>.meta.json` to `$LEARN_HUB_DIR/research-notes/visuals/` when its marker validates, otherwise to cwd, and say where." As a separate sentence: "Filing never publishes: the user files it into the Learn hub with `ingest-visual` ('file <asset>')."

`.meta.json`(I09): `{kind:"animation",title:"<h1>",description:"<concept+aha>",topic_hint:"<id/phrase/null>",source_report:"<basename or established-knowledge>",producer:"concept-animation",created:"<YYYY-MM-DD>",audit:{tool,verdict:"pass|incomplete"}}`. ML writes `kind:"explorable"`,`producer:"ml-concept-lab"`. W3: `producer` gains `visuals:` prefix.

**H-8 CA Gotchas**(4): fixed `height:100dvh` pushes overflow into children — filed animations collapsed on phones; use `min-height:100dvh`. A proportional floor needs an absolute one under it — bare `min(38dvh,280px)` gives 116px landscape; use `max(220px,min(38dvh,280px))`. One viewport can't fail on collapse — Step 3.5 checks 5 incl. 844×390. A doctype-less fragment renders in quirks mode, opaque white canvas — start `<!DOCTYPE html><html lang="en">`+`:root{color-scheme:dark}`. The sandbox's opaque origin fails external refs silently.

**H-9 ML Gotchas**(5): bare `import{chromium}` fails global-only — resolves via `npm root -g`. A relative gradient error is a false failure near a stationary point — use absolute diff+noise floor(H-10). A scrolling explorable is fine on a phone; the stage floor is not negotiable, controls fit at 1440×900. Clinical concepts go to concept-animation even phrased "interactive". Same document/layout traps as concept-animation.

**H-10 ML gradient row** (replaces build-contract.md:103): "Anything with gradients: analytic ∇ against a central finite difference, as an ABSOLUTE difference — pass when `max|∇ᵢ−fdᵢ| ≤ max(1e-6·s, floor)`, `s`=largest `|component|` of either gradient, `floor=20·ε·max(1,|L|)/h`(ε=`Number.EPSILON`, h=fd step, L=loss). Never a relative error near a stationary point — it measures cancellation, not correctness." (`examples/learning-rate-and-conditioning.html:333-346` already implements this.)

**H-11 Handover to S19** (`atomize-book/SKILL.md:588-590`): replace the run-CA/CI-and-sync-picks-it-up text with "Run `clinical-infographic`/`concept-animation` (micky `visuals`) for the nominated chapters. Each writes `<slug>.html`+`<slug>.meta.json` into `research-notes/visuals/`; then `ingest-visual` files each one; `/sync-vault` picks them up with the rest of the import." Applied by S19-W2-1 (CX-29) — this spec's own H-11 text is the source S19-W2-1 copies verbatim, not a step here.

### 2.7 Interfaces

#### Owned: I07 — HTML artifact contract, `render-verify.md`, `check-html.mjs`, parity fixture

**I07-A Kinds.** infographic(`visuals:clinical-infographic`→`infographics`; `allow-same-origin allow-modals`, no scripts). animation(`visuals:concept-animation`, learn-hub `pk-plasma-animation`→`animations`; `allow-scripts`, opaque origin; scripted). explorable(`visuals:ml-concept-lab`→`animations`,`type:animation`; `allow-scripts`; scripted). code-explainer(`visuals:code-explainer`→held, no receiver; scripted).

**I07-B Document rules (every kind).** `<!DOCTYPE html>` first; `<html lang>`+`<meta charset="utf-8">`; `color-scheme` on `:root`/`html`: `dark` default for anim/explorable/code-explainer, exactly `light` for infographic(light-lock); ground painted; self-contained — no absolute/protocol-relative URL anywhere, everything inline; `.wrap` capped `max-width:1152px`.

**I07-C Layout grammar (animation, explorable).** Explorable swaps `.stage-wrap`→`.stage`,`.controls`→`.deck`:
```css
:root{color-scheme:dark; --bg:#0a1020; --ink:#eaf0ff}
html,body{margin:0; background:var(--bg); color:var(--ink); overflow:auto}
.wrap{min-height:100dvh; display:flex; flex-direction:column; max-width:1152px; margin:0 auto}
.wrap>*{flex:0 0 auto}
.wrap>.stage-wrap{flex:1 1 0; min-height:220px; min-height:max(220px,min(38dvh,280px)); display:flex}
svg.stage{width:100%; height:100%; max-height:100%; min-height:0}
@media (max-width:640px){ /* trim padding/h1/caption/footer type */ }
@media (prefers-reduced-motion:reduce){ *{animation:none!important; transition:none!important} }
```
Never: fixed `height` on `.wrap`; a stage with `min-height:0` and no floor; the stage rule on a one-class selector; `overflow:hidden` on `html`/`body`/`.wrap`; a bare `1fr` in a mobile grid; `position:sticky` on the stage; a very tall `viewBox`. A document opts out with a more specific selector (`.wrap>main.stage`).

**I07-D Sheet rules (infographic).** No `prefers-color-scheme:dark` block. A flex strip whose items shrink unboundedly stacks at the mobile breakpoint or gets a wrapping basis (palette/type minimums/safety-banner stay in clinical-infographic's own references, S06).

**I07-E DOM hooks.** animation+explorable need `.wrap` > `.stage-wrap`/`.stage` + `[data-controls]`(else `.wrap .controls`/`.deck`) + an `aria-live` region. animation adds `#playBtn #nextBtn #restartBtn #indicator`(text `k / N`); explorable adds `#play #step #reset #stepCount`(int), ≥1 `[data-preset]`, ≥1 `[data-check][data-pass]`.

**I07-F Accessibility.** Colour never the only signal; WCAG AA text; a real `<h1>`; SVG `role="img"`+`<title>`; captions are DOM text; real keyboard-operable controls; `prefers-reduced-motion:reduce` gives a stepped storyboard or full use by stepping.

**I07-G Verification.** Tool order: `check-html.mjs`(delegates when learn-hub valid, own port otherwise); `.meta.json` records `audit.tool`+`audit.verdict`. Frame formula: `w=min(1152,vw−(vw<640?16:32))`, `h=max(min(0.78·vh,704),min(w·10/16,vh−96))`.

| Viewport | Frame | Anim. limit | Explorable limit |
|---|---|---|---|
| 360×780 | 344×608 | ≤638 | none(scroll ok) |
| 390×844 | 374×658 | ≤659 | none |
| 430×932 | 414×704 | ≤705 | none |
| 844×390 | 812×304 | none(scroll ok) | none |
| 1440×900 | 1152×720 | ≤721 | ≤721 |

At every frame: stage ≥200px; no clipped/overlapping children (sorted by rendered top); `scrollWidth`≤w+1; no page error. Animation values=worst over the walk. Measured(P4): rebuilt CA peaks 580-627px; ML+contract 586px desktop, 779-805px phones(scroll, allowed).

**I07-H Rule ids** (`audit:visual` asked to match, §8 Q3). Static(all unless noted): `no-doctype`,`no-lang`,`no-color-scheme`,`no-painted-ground`,`external-reference`,`no-reduced-motion`(anim/explorable/code-explainer). Infographic-only static: `color-scheme-not-light`,`prefers-color-scheme-dark`,`strip-cramps`. Anim/explorable-only static: `children-can-shrink`,`stage-can-collapse`(both ported audits). Render: `no-wrap`/`no-stage`/`no-controls`,`stage-collapsed`,`child-clipped`/`children-overlap`,`controls-below-fold`,`horizontal-overflow`,`page-error`. Drive: `drive-hooks-missing`; animation `scene-walk-stuck`/`restart-not-scene-1`; explorable `step-counter-off`,`self-check-failing`,`non-finite-on-screen`. 26 codes total; each `fix` names the concrete repair.

**I07-J Parity fixture.** `fixtures/parity.json`, 6 rows: `ci-example`/`ci-template`(infographic examples, pass), `ca-example`(animation example, pass), `ml-example`(explorable example, pass), `bad-animation`(fail; `no-doctype,no-lang,no-color-scheme,no-painted-ground,children-can-shrink,stage-can-collapse`), `bad-infographic`(fail; `color-scheme-not-light,prefers-color-scheme-dark,strip-cramps`). `shared_codes`=those 9+`external-reference`,`no-reduced-motion`. Rows resolve by basename. Agreement: `check-html --own` verdict=`audit:visual` verdict=`expected`, every code in `codes ∩ shared_codes` in both. P7 confirmed both bad fixtures match I07-H exactly.

Bad fixtures (created S05-W2-1, never "fixed" later): animation=doctype-less fragment, `.wrap{height:100dvh}`, `.stage-wrap{flex:1 1 auto;min-height:0}`, no color-scheme/painted ground, valid control ids (only the 6 codes fire). Infographic=valid document but `color-scheme:light dark`(not exactly light), a dark-mode block, a `.mech` strip with no mobile stacking rule. Runs at W2 exit(S05-W2-5), in S08's `validate.py --cross-repo`, in any S16 step touching `audit:visual`.

**I07-K Consumers.** S06 calls `check-html.mjs`(W2 own-plugin copy from S05-W2-2; W3 links the family refs), adds byte-fidelity via `--source <file>` in W3 without changing any existing flag/field/id. S16's `audit:visual` implements I07-H/I07-G/I07-E. S08's `validate.py --cross-repo` runs `--parity --root <micky> --learn-hub <learn-hub>`.

#### Consumed

| Interface | Owner | ASSUMES |
|---|---|---|
| I01 | S01 | "open the output"=first line of chat hand-back; `Assumed:` never in the HTML |
| I08 | S16 | `audit:visual -- <abs file> --json --kind <k>` prints `verdict`+`issues[].code` from I07-H; exit 0/1/2; renders the 5 I07-G frames when possible |
| I09 | S15 | `research-notes/visuals/<slug>.html`+`<slug>.meta.json` per H-7; `kind` accepts `animation`/`explorable`; slug kebab-case, `-2`/`-3` on collision |
| I11 | S07 | producers call `vault-keeper` with the two files, never `sink.py` directly; H-7 is the filing sentence |
| I16 | S11 | W2-exit row adds both micky plugin paths; a cloud session can load learn-hub on a named branch |
| I17 | S12 | layout `plugins/<p>/evals/<skill>/<case>/`; tags per §4.1; alias skills exempt from ≥3-case rule |
| I20 | S08 | whitelist has `argument-hint`,`allowed-tools`,`disable-model-invocation`,`metadata`; R13 exempts test/fixture files |
| I23 | S10 | skeleton moves each skill's dirs unchanged; `concept-animation/scripts/` canonical; creates the 2 alias skills of §2.2 |

## 3. Change steps

Shorthand: `CA`=`plugins/concept-animation`,`ML`=`plugins/ml-concept-lab`,`CI`=`plugins/clinical-infographic`(micky);`LH`=learn-hub;`V`=`plugins/visuals`(post-S10).

### Wave W1

**S05-W1-1** [learn-hub] · depends on: none
- Files: edit `LH/.claude/skills/concept-animation/SKILL.md`.
- Change: line 3 `description:` → `description: >-` block scalar, same 1,000-char text.
- Commands: `python3 -c "import yaml; d=yaml.safe_load(open('LH/.claude/skills/concept-animation/SKILL.md').read().split('---')[1]); print(len(d['description']))"` → `1000`.
- Done when: the command prints `1000`.
- Rollback: `git checkout -- LH/.claude/skills/concept-animation/SKILL.md`.

### Wave W2 (repo: micky, except W2-7/-8 which touch learn-hub)

**S05-W2-1** · depends on: none
- Files: create `CA/scripts/check-html.mjs`, `CA/scripts/check-html.test.mjs`, `CA/scripts/fixtures/{bad-animation.html,bad-infographic.html,parity.json}`.
- Change: implement §2.5's CLI/JSON/exit-codes/I07-H; write the 2 bad fixtures per I07-J and the 6-row manifest (other 4 rows resolve once real examples exist).
- Commands: `node --test 'CA/scripts/*.test.mjs'`; `node CA/scripts/check-html.mjs --help`.
- Done when: tests pass; `--help` exits 0 listing 26 rule ids; `bad-animation.html --kind animation --static-only --own` exits 1 with the 6 codes.
- Rollback: `git rm -r CA/scripts`.

**S05-W2-2** · depends on: S05-W2-1
- Files: create `ML/scripts/check-html.mjs`, `CI/scripts/check-html.mjs`.
- Change: `cp CA/scripts/check-html.mjs ML/scripts/check-html.mjs`; same to `CI/scripts/`.
- Commands: `cmp CA/scripts/check-html.mjs ML/scripts/check-html.mjs`; `cmp CA/scripts/check-html.mjs CI/scripts/check-html.mjs`.
- Done when: both `cmp` exit 0, no output.
- Rollback: `git rm ML/scripts/check-html.mjs CI/scripts/check-html.mjs`.

**S05-W2-3** · depends on: S05-W2-1, S16-W2-3 (consumers before producers — the `.meta.json` filing shape this step's H-7 sentence writes against must exist first, CX-35)
- Files: edit `CA/skills/concept-animation/SKILL.md`, `.../references/animation-grammar.md`; replace `CA/examples/tms-electromagnetic-induction.html` (start from learn-hub's `vault/tms-principles/tms-electromagnetic-induction.html`, apply I07-B/I07-C); edit `CA/.claude-plugin/plugin.json` (description only, bump is W2-6).
- Change: §2.3's CA row set and grammar; description → §2.2's W2 text.
- Commands: `node CA/scripts/check-html.mjs CA/examples/tms-electromagnetic-induction.html --kind animation --own`; `python3 measure.py skill CA/skills/concept-animation/SKILL.md`.
- Done when: `check-html.mjs` prints `"verdict":"pass"`(or stated `"incomplete"`); `measure.py` reports description ≤1,024 chars, `yaml_valid:true`.
- Rollback: `git checkout -- CA/skills/concept-animation CA/examples`.

**S05-W2-4** · depends on: S05-W2-2, S16-W2-3 (consumers before producers — CX-35)
- Files: edit `ML/skills/ml-concept-lab/SKILL.md`, `.../references/{build-contract,concept-patterns}.md`; rewrite `ML/examples/learning-rate-and-conditioning.html` in place (I07-B/I07-C; algorithm unchanged, NEW-9 verified sound); rename `ML/examples/README.md`→`.../learning-rate-and-conditioning.md`.
- Change: §2.3's ML row sets (H-10, ml-4, ml-5); description → §2.2's W2 text.
- Commands: `node ML/scripts/check-html.mjs ML/examples/learning-rate-and-conditioning.html --kind explorable --own`; `grep -c "clinical-infographic" ML/skills/ml-concept-lab/SKILL.md`; `grep -c "1e-5\|relative error" ML/skills/ml-concept-lab/references/build-contract.md`.
- Done when: `check-html.mjs` prints pass/stated-incomplete; clinical grep shows only the CA handoff; gradient grep = 0.
- Rollback: `git checkout -- ML/skills ML/examples/learning-rate-and-conditioning.md && git mv ML/examples/learning-rate-and-conditioning.md ML/examples/README.md`.

**S05-W2-5** · depends on: S05-W2-3, S05-W2-4
- Files: create the 4 eval case dirs per skill under `CA/evals/concept-animation/` and `ML/evals/ml-concept-lab/` (contents §4.1).
- Change: 4 cases per skill.
- Commands: `find CA/evals/concept-animation -mindepth 1 -maxdepth 1 -type d | wc -l`; same for ML.
- Done when: both = 4. (`claude plugin eval` not run by this spec — hard constraint.)
- Rollback: `git rm -r CA/evals ML/evals`.

**S05-W2-6** · depends on: S05-W2-3, S05-W2-4, S10-W0-8
- Files: edit (not create — S10-W0-8 already backfills README/CHANGELOG/LICENSE for both plugins, CX-45) `CA/{README,CHANGELOG}.md`, `CA/LICENSE`; `ML/{README,CHANGELOG}.md`, `ML/LICENSE`; bump both `plugin.json` to `0.2.0`.
- Change: README links the worked example (closes ca-9); CHANGELOG's first entry describes the W2 rewrite.
- Commands: `python3 scripts/bump.py concept-animation minor --write`; `python3 scripts/bump.py ml-concept-lab minor --write`; `python3 scripts/validate.py`.
- Done when: both `plugin.json` read `0.2.0`; `marketplace.json` has no `version` for either entry (CX-12); `validate.py` prints `all checks passed`.
- Rollback: `git checkout -- CA/README.md CA/CHANGELOG.md CA/LICENSE CA/.claude-plugin/plugin.json ML/README.md ML/CHANGELOG.md ML/LICENSE ML/.claude-plugin/plugin.json`.

**S05-W2-8** [learn-hub] · depends on: S05-W2-6, S16-W2-5 (CX-30 — the swap verification itself moves to S11-W2-3, which merges the deletion branch only once S11's cloud-enable schedule confirms `visuals:concept-animation`/`concept-animation:concept-animation` loads from the micky path)
- Files: delete `LH/.claude/skills/concept-animation/` on a learn-hub deletion branch.
- Change: `git rm -r LH/.claude/skills/concept-animation`; push the branch (not `master`).
- Commands: `test ! -d LH/.claude/skills/concept-animation` (on the branch).
- Done when: the branch is pushed with the deletion committed; `master` is untouched until S11-W2-3 merges it.
- Rollback: delete the branch.

W2 exit: `validate.py`+`route.py` clean; `check-html.mjs --parity --root . --own` shows the 2 bad fixtures failing with exact codes and the 2 real examples passing/stating `incomplete`; learn-hub deletion branch pushed (merge is S11-W2-3's step, CX-30).

### Wave W3 (depends on S10's skeleton-PR move step, I23)

**S05-W3-1** · depends on: S10-W3-2, S01-W3-2
- Files: create `V/references/{html-artifact-contract,render-verify}.md`; verify exactly one `V/scripts/check-html.mjs` exists (S10-W3-2 already moves `CA/scripts/*` as the canonical copy and drops the `ml-concept-lab`/`clinical-infographic` duplicates — this step deletes nothing itself, CX-2); edit both SKILL.md/grammar/build-contract per §2.3's W3-trim.
- Change: write I07-A…H into `html-artifact-contract.md`; write I07-G into `render-verify.md`; replace inline document/layout text with a family-file pointer.
- Commands: `find V -name check-html.mjs | wc -l`; `node --test 'V/scripts/*.test.mjs'`.
- Done when: exactly 1 `check-html.mjs` under `V/`; tests pass; `grep -c "min-height:100dvh" V/skills/*/references/*.md` = 0.
- Rollback: `git checkout -- V/references V/skills`.

**S05-W3-2** · depends on: S05-W3-1, S12-W3-2 (CX-37)
- Files: edit `V/skills/concept-animation/SKILL.md`, `V/skills/ml-concept-lab/SKILL.md` frontmatter+Handoffs.
- Change: description → §2.2's W3 text (namespaced); Handoffs → `visuals:`/`alignment:`/`evidence:` names.
- Commands: `python3 measure.py skill V/skills/concept-animation/SKILL.md V/skills/ml-concept-lab/SKILL.md`.
- Done when: CA description ≤600 ≤1,024 hard; ML ≤585; both `yaml_valid:true`; `grep -c "concept-animation:concept-animation\|ml-concept-lab:ml-concept-lab" V/skills/*/SKILL.md`=0.
- Rollback: `git checkout -- V/skills/concept-animation/SKILL.md V/skills/ml-concept-lab/SKILL.md`.

**S05-W3-3** · depends on: S05-W3-1
- Files: edit `V/skills/ml-concept-lab/SKILL.md`, `references/build-contract.md`.
- Change: body ≤150 lines; move layout/a11y/verify-list rows into the family-file pointer; tighten anatomy/engine text (no rule removed).
- Commands: `python3 measure.py file V/skills/ml-concept-lab/SKILL.md V/skills/ml-concept-lab/references/build-contract.md V/references/html-artifact-contract.md`.
- Done when: sum of the three `est_tokens` ≤ 5,000 (arch §9).
- Rollback: `git checkout -- V/skills/ml-concept-lab`.

**S05-W3-4** · depends on: S05-W3-1, S08-W3-1 (the done-when runs `$VALIDATE`, which S08-W3-1 creates)
- Files: edit `V/.claude-plugin/plugin.json`.
- Change: `description` names both skills+the family contract; `keywords` include "animation","explorable","visualization"; version = S10's skeleton value (no independent bump).
- Commands: `$VALIDATE --repo .` (`$VALIDATE` = `python3 plugins/plugin-creator/scripts/validate.py`, live once S08-W3-1 lands — CX-11; repo-root `scripts/validate.py` is gone by this point).
- Done when: `all checks passed`.
- Rollback: `git checkout -- V/.claude-plugin/plugin.json`.

**S05-W3-5** · depends on: S05-W3-4
- Files: merge `V/README-concept-animation.md`/`README-ml-concept-lab.md` (and S06's `README-clinical-infographic.md`/`README-code-explainer.md`) and the equivalent `CHANGELOG-<p>.md` files (S10-W3-2's per-member suffix) into single `V/README.md`/`V/CHANGELOG.md`; create `V/LICENSE` (MIT) if S10-W0-8 hasn't already backfilled one for every member; delete the per-member files.
- Change: `README.md` states all four skills, the shared `check-html.mjs`/family refs, and a `## Surfaces` section naming every place this family's summary appears (I16 item 1). `CHANGELOG.md` merges the four histories, newest first. Wave exit: note, per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H38, H39, H40, H41, H43); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."
- Commands: `find V -maxdepth 1 -name 'README-*.md' -o -name 'CHANGELOG-*.md' | wc -l`; `grep -c "^## Surfaces" V/README.md`.
- Done when: the find count = 0; the grep = 1.
- Rollback: `git checkout -- V/README.md V/CHANGELOG.md V/LICENSE`.

**S05-W3-6 (new, critique P5)** · depends on: S08-W3-1 (`release.py`), S05-W3-2, S05-W3-3, S05-W3-5, S06-W3-1, S06-W3-2, S06-W3-3, S06-W3-4
- Files: `V/.claude-plugin/plugin.json`, `V/CHANGELOG.md`.
- Change: release the visuals family after its W3 rewrite — `python3 plugins/plugin-creator/scripts/release.py visuals minor --write`.
- Done when: `$VALIDATE --repo .` prints `all checks passed`; the first `## ` line of `V/CHANGELOG.md` names the `plugin.json` version; `marketplace.json` has no `version` key for `visuals`.
- Rollback: `git revert <this commit>`.

W3 exit: all 5 steps done; `--parity --root . --learn-hub <lh>` agrees on all 6 rows (or exits 3 naming the missing environment); CA/ML tokens at target; H38-H41,H43 closed; no `check-html.mjs` outside `V/scripts/`; one family README/CHANGELOG/LICENSE, no per-member copies.

## 4. Evals

### 4.1 Cases

4 cases/skill (R71 target 3-5). Full content for 3 (trigger positive, near-miss negative, output/process); 4th in a table. Paths under `plugins/concept-animation/evals/concept-animation/`(W2)→`plugins/visuals/evals/concept-animation/`(W3, moved by S10).

**CA Case 1 — `trigger-thai/`**. `prompt.md`:
```markdown
---
tags: [concept-animation, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

ช่วยทำแอนิเมชันอธิบายว่า TMS pulse ไปถึงสมองได้อย่างไร เป็นไฟล์ HTML ที่ดูได้เลย
```
`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?concept-animation"'
arm: both
---
```

**CA Case 2 — `negative-explorable/`** (near-miss, ml-concept-lab's territory). `prompt.md`:
```markdown
---
tags: [concept-animation, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

I want to play with gradient descent myself — an interactive page where I can drag the
learning rate and watch it converge or diverge.
```
`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?concept-animation"'
min: 0
max: 0
arm: both
---
```

**CA Case 3 — `output-contract/`** (I07 compliance). `prompt.md`:
```markdown
---
tags: [concept-animation, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 30
---

Animate how SSRIs increase synaptic serotonin, scene by scene. Write the HTML file.
```
`graders/layout-grammar.md`:
```markdown
---
type: regex
target: { source: file, path: "*.html" }
pattern: 'min-height:\s*100dvh'
weight: 2
---
```

4th case: `clinical-needs-source/` — tags `[concept-animation, negative]`; prompt "Animate the mechanism of clozapine-induced agranulocytosis." (no sourced report available); grader: `llm` PASS if the skill states it needs a sourced report or names the clinical facts it could not source, FAIL if it invents a mechanism number with no source stated.

**ML Case 1 — `trigger-thai/`**. `prompt.md`:
```markdown
---
tags: [ml-concept-lab, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write]
max_turns: 20
---

ทำภาพอธิบายแบบโต้ตอบให้หน่อยว่า gradient descent ทำงานยังไง อยากลองปรับ learning rate เอง
```
`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ml-concept-lab"'
arm: both
---
```

**ML Case 2 — `negative-watch-only-clinical/`** (clinical must route to concept-animation). `prompt.md`:
```markdown
---
tags: [ml-concept-lab, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Animate how lithium stabilizes mood at the cellular level — I just want to watch it play out.
```
`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?ml-concept-lab"'
min: 0
max: 0
arm: both
---
```

**ML Case 3 — `output-contract/`** (drive checks + I07). `prompt.md`:
```markdown
---
tags: [ml-concept-lab, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 30
---

Build an explorable for k-means clustering where I can drag the initial centroids and
step through iterations myself.
```
`graders/drive-hooks-present.md`:
```markdown
---
type: regex
target: { source: file, path: "*.html" }
pattern: 'id="step"[\s\S]*id="stepCount"|id="stepCount"[\s\S]*id="step"'
weight: 2
---
```

4th case: `clinical-routes-away/` — tags `[ml-concept-lab, negative]`; prompt "Make an interactive demo of how dopamine reward prediction error drives learning — let me tweak the reward signal." (clinical, phrased "interactive"); graders: `tool_used Skill min:0 max:0 arm:both`, plus `llm` PASS if the response names `concept-animation` as the right skill.

### 4.2 Conversion

Neither plugin has an `evals.json` today — all 8 cases above are new, not converted. N/A.

### 4.3 Live triggers

Family (arch §6.3): `{concept-animation, ml-concept-lab, clinical-infographic, code-explainer, gridgeist, dataviz}`. Near-miss queries (feeding S12): "make an interactive demo of backpropagation"→`ml-concept-lab`; "animate the mechanism of action of TMS"→`concept-animation`; "chart my medication adherence data"→`dataviz`; "explain this sorting algorithm's code line by line"→`code-explainer`; "one-page printable reference sheet for antipsychotic dosing"→`clinical-infographic`.

### 4.4 Commands

Smoke: `bash scripts/eval.sh --smoke visuals -- --allow-tools Write`. Release: `bash scripts/eval.sh --release visuals -- --allow-tools "Write,Bash(node *)"` (the Case-3 cases run `check-html.mjs` via `Bash(node *)`; several smoke-tagged cases also write the HTML file — factcheck F3). Neither runs from this spec (hard constraint) — documented for the executor session after S10's wrapper exists.

## 5. Acceptance criteria

1. `python3 scripts/validate.py` (micky) prints `all checks passed` after W2; `$VALIDATE --repo .` (post-S08-W3-1's move, CX-11) prints `all checks passed` after W3.
2. `test ! -d /home/user/learn-hub/.claude/skills/concept-animation` (post-W2-8).
3. `node plugins/visuals/scripts/check-html.mjs --parity --root . --own` (post-W3) exits 0/1 with `"agree":true` per checkable-without-browser row; with browser+`--learn-hub`, all 6 agree.
4. `node --test 'plugins/visuals/scripts/*.test.mjs'` (post-W3; concept-animation's copy post-W2) reports 0 failures.
5. `grep -Pc '(?<!min-)height:\s*100dvh' plugins/visuals/skills/*/references/*.md plugins/visuals/examples/*.html` = 0.
6. `measure.py skill` on both SKILL.md reports `yaml_valid:true`, description ≤1,024 chars.
7. `find plugins/visuals/evals/concept-animation -mindepth 1 -maxdepth 1 -type d | wc -l` = 4; same for `ml-concept-lab`.
8. `grep -c "vault/assets"` on both SKILL.md = 0 (ca-7 closed).
9. `grep -c "1366\|1366×768\|1366x768"` on all skills/refs = 0 (ca-2, ml-2 closed).
10. Exactly one `check-html.mjs` under `plugins/visuals/`; zero elsewhere in micky.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "animate this concept","create an animation","make an animation of X","animated explainer","show it moving","ทำแอนิเมชัน","ภาพเคลื่อนไหว" | CA description | kept |
| "/animate" | CA command → W3 alias skill | kept, moved to `skills/animate/SKILL.md` |
| "visualize this concept","interactive visualization","make an interactive demo","explorable","let me play with the parameters","ทำภาพอธิบายแบบโต้ตอบ" | ML description | kept |
| "show me how X works","animate this algorithm" | ML description | **removed**(ml-7, overlapped CA; also mis-routed clinical) |
| "/visualize" | ML command → W3 alias skill | kept, moved to `skills/visualize/SKILL.md` |
| "just animate it"/"just build it" (opt-outs) | CA/ML body, Step 0 | kept, body |
| copy's description phrases | learn-hub copy | **removed with the copy**(copy-8); micky phrase is sole survivor; filing trigger lives in `ingest-visual`(S16) |

## 7. Risks and OD sensitivity

- **K-risk**: the atomic swap (S05-W2-8, S11-W2-3) depends on S11's cloud-enable schedule reaching a state where a learn-hub branch session can load the micky path before S11-W2-3 merges the deletion branch — shared with S11 (CX-30).
- **OD9-b** (capability names only): `/animate`/`/visualize` dropped entirely; §2.2's alias blocks and §6's slash rows don't exist.
- **OD9-c** (rename to verbs): `concept-animation`→`animate`, `ml-concept-lab`→`visualize`; every SKILL.md `name:`, §4.1's regexes, §6, and I07-K change.
- **OD3-b** (14 shells, no family merge): the family refs become `shared/` files synced per plugin; `check-html.mjs` stays a 3-copy arrangement; S05-W3-1's "exactly one" criterion becomes "N byte-identical copies, checked".
- No OD5/OD13 sensitivity: no publish/digest gate, no claude.ai upload step.

## 8. Open questions

- **ASSUMES-1**(I08,S16): `audit:visual`'s JSON schema/rule-id vocabulary. Check: read S16's spec; if code names differ, add a translation table — `raw` already carries the untranslated payload.
- **ASSUMES-2**(I09,S15): `.meta.json` shape and the collision-suffix rule. Check: read S15's spec.
- **ASSUMES-3**(I11,S07): producers call `vault-keeper` with exactly two files. Check: read S07's spec.
- **ASSUMES-4**(I23,S10): S10's skeleton creates the two alias skills verbatim, moves `concept-animation/scripts/` as canonical (S05-W3-1 only verifies this landed, per CX-2 — it does not move anything itself).
- **Q3**: whether `audit:visual` reports the exact I07-H strings. Check: read S16's spec; else add a lookup table — no I07 change required.
- **Q14**: whether S11-W2-3's swap verification (CX-30 moves it there) can run headless. Not resolved — the architecture reads as requiring a live check. Check: S11's spec, once read, for a scriptable "plugin X loaded" probe.
- **ARCH-CONFLICT**: none found. The parity fixture's known-bad files are described by property (I07-J) rather than given as full byte contents — a size-budget compression of this spec's presentation, not a change to what W2-1 must create.
