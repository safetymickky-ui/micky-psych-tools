# Spec S06: clinical-infographic and code-explainer (+ their alias skills)

| Field | Value |
|---|---|
| Repos | micky-psych-tools (`/home/user/micky-psych-tools`) |
| Units (today → target) | `plugins/clinical-infographic`(+`/infographic`) → `plugins/visuals/skills/clinical-infographic`+dmi alias `visuals:infographic`. `plugins/code-explainer`(+`/explain-code`) → `plugins/visuals/skills/code-explainer`+dmi alias `visuals:explain-code`. |
| Waves | W0 (smoke seeds, CX-4); W1 (CI: light-lock+strip+contrast+≥12px text in template AND example, H36/H37; CE: remove dead template pointers, H42); W2 (CI render/verify via `check-html.mjs`, filing via the sink); W3 (move into `visuals`; CI `lessons-learned.md`→CHANGELOG history + SKILL links the example; CE byte-fidelity flag on `check-html.mjs`, "Dark Modern" naming, ML boundary) |
| Owner decisions assumed | OD1-a, OD2-a, OD3-a, OD4-a, OD5-a, OD9-a, OD10-a, OD13-a |
| Defects closed | 16 of 16 assigned (HIGH: H36, H37, H42) |
| Interfaces owned | none |
| Interfaces consumed | I01(S01), I07(S05), I08(S16), I09(S15), I11(S07), I17(S12), I20(S08), I23(S10) |
| Depends on specs | S01, S05, S07, S08, S10, S12, S15, S16 |

## 1. Current state (measured 2026-09-24)

Repo head: micky `e4ae3d8`. Tokens=chars/4, `measure.py`.

### 1.1 Files

| Path | L/B/Tok | Role |
|---|---|---|
| `clinical-infographic/skills/clinical-infographic/SKILL.md` | 177 body/11,291/2,823(body); desc 991/248 | the skill |
| `.../references/design-system.md` | 140/8,167/2,020 | palette, diagram grammar, print/a11y rules |
| `.../references/infographic-template.html` | 248/14,198/3,527 | the skeleton to fill |
| `.../references/source-contract.md` | 89/5,180/1,283 | Step 0 content-acquisition rules |
| `.../references/lessons-learned.md` | 85/5,515/1,368 | dated retrospective |
| `clinical-infographic/examples/ppgl-perioperative-management.html`(+`.preview.png`) | 481/32,669/8,096 | worked example; unlinked from SKILL.md |
| `clinical-infographic/examples/README.md` | 27 lines | links `vault/artifacts/ppgl-perioperative-management.md`, which does not exist |
| `clinical-infographic/{.claude-plugin/plugin.json,CHANGELOG.md,commands/infographic.md,skills/.../evals/evals.json}` | v0.2.1; CHANGELOG top entry 0.2.0; 4 evals | plugin shell |
| `code-explainer/skills/code-explainer/SKILL.md` | 162 body/8,887/2,222(body); desc 863/216 | the skill |
| `.../references/explanation-contract.md` | 149/8,396/2,079 | 3 modes, fidelity, a11y, verify |
| `.../references/vscode-shell.md` | 153/9,677/2,130 | chrome, palette, layout |
| `code-explainer/{.claude-plugin/plugin.json,README.md,commands/explain-code.md,skills/.../evals/evals.json}` | v0.1.0; no CHANGELOG; 6 evals | plugin shell |

`references/explainer-template.html` (SKILL.md:30,99; README.md:86-87) does not exist — `find plugins/code-explainer -iname '*.html' -o -iname '*.png'` returns nothing at all: no template, no worked example, no preview PNG anywhere in the plugin.

### 1.2 Descriptions

| Unit | Chars/Bytes | YAML | Use-when/Not-for at | Quoted / slash triggers |
|---|---|---|---|---|
| clinical-infographic (SKILL.md:3-15) | 991/1,031 | yes | 148/798 | "make an infographic","medical summary infographic","clinical reference infographic","turn this review/report into an infographic","one-page visual summary","สรุปเป็นอินโฟกราฟิก"; unquoted `/infographic` |
| code-explainer (SKILL.md:3-14) | 863/895 | yes | 231/710 | "explain this code","explain the given code","walk me through this function","annotate this code","code walkthrough","what does this code do","อธิบายโค้ดนี้"; unquoted `/explain-code` |

### 1.3 Defects

Every id (prefixes `clinical-infographic-`,`code-explainer-`) appears once. `ci-N`/`ce-N` shorthand below.

| Id | Sev | H# | Evidence | Problem → fix | Wave |
|---|---|---|---|---|---|
| clinical-infographic-1 | H | H36 | template:100-104 `@media (prefers-color-scheme:dark){…}`; example:167 same block | Partial dark override strands ink-on-tint text invisible under OS dark theme (learn-hub is light-locked) → S06-W1-1: remove block, add `:root{color-scheme:light}` | W1 |
| clinical-infographic-2 | H | H37 | template:74-75 `.mech .node{flex:1 1 0;…min-width:0}`, mobile rule only touches `.columns`/`.safety-body`; example same, no `.mech` rule at any breakpoint | `.mech` strip cramps on phones (learn-hub `auditInfographicResponsive` flags both) → S06-W1-1: stack it at the mobile breakpoint | W1 |
| clinical-infographic-3 | M | — | design-system.md:121-123 "AA-contrast…palette"; template:40 `.col-head{color:#fff;…font-size:15px;font-weight:700}`. Computed: white-on-`#3f8a6e`(c2)=4.14:1, white-on-`#c9772e`(c3)=3.41:1; 15px bold is below the 18.66px-bold large-text threshold, so 4.5:1 is required, not 3:1 | 2 of 3 column accents fail AA → S06-W1-1: darken c2/c3 | W1 |
| clinical-infographic-4 | M | — | design-system.md:131 "no clinical text below ~12px at print size"; template has 7 sub-12px declarations (`.stat .k`:56 11px, `.foot`:64 11.5px, `.viz .cap`:73 10.5px, `.mech .node .s`:76 10.5px, `.ladder .rung`:80 11px, `.opt .cond`:84 10.3px, `.chooser .verdict`:86 11.4px); example has the same 7 plus `.stat .k`:137 10px and print `body`:161 11.5px | Template violates its own legibility minimum, both files → S06-W1-1: enforce ≥12px everywhere | W1 |
| clinical-infographic-5 | M | — | SKILL.md:126-130 "Rasterise it…*look*… Optionally OCR"; `which tesseract` → not found in this environment | Render/verify is vague prose, partly non-executable (no browser/script/viewport named, OCR names no tool) → S06-W2-1: `check-html.mjs --kind infographic` (I07, S05) | W2 |
| clinical-infographic-6 | M | — | SKILL.md:143-146 "hand it to vault-keeper…`vault/assets/`"; `vault-keeper/skills/empty-vault/SKILL.md:55-56` "assets…removed with their topic" | Filed assets dead-end (empty-vault deletes rather than hands to learn-hub `ingest-visual`) → S06-W2-1: sink filing into `research-notes/visuals/`+`.meta.json`(I09/I11) | W2 |
| clinical-infographic-7 | L | — | plugin.json:3 `"version":"0.2.1"`; CHANGELOG.md:3 top entry `## 0.2.0` | CHANGELOG stale (0.2.1 release, MEMORY.md:986, has no entry) → S06-W3-1: add it | W3 |
| clinical-infographic-8 | L | — | examples/README.md:6 "rendered from `vault/artifacts/ppgl-perioperative-management.md`"; `ls vault/artifacts` shows only `burnout-syndrome-com…`, not this file; eval 1 (evals.json id 1) depends on the same source | Dead link in the examples README, eval-1 references it too → S06-W3-1: fix the link, note the report is not in this repo's vault | W3 |
| clinical-infographic-9 | L | — | SKILL.md:50-51 "worked retrospective…read it once"; lessons-learned.md:1-2 duplicates fixes already in SKILL.md+design-system.md; ~1.4k tok whenever read | Time-bound retrospective loaded on a vague instruction, duplicates content, costs tokens → S06-W3-1: fold into CHANGELOG history, delete the file | W3 |
| clinical-infographic-10 | L | — | `grep -n examples SKILL.md` → 0 hits; `examples/ppgl-perioperative-management.html` (481 lines) sits unlinked at plugin root | SKILL never points at the worked example/preview PNG (only examples/README.md does) → S06-W3-2: SKILL links it (R13) | W3 |
| code-explainer-1 | H | H42 | SKILL.md:30,99 and README.md:86-87 all point at `references/explainer-template.html`; `references/` holds only `explanation-contract.md`,`vscode-shell.md`; file never existed (`git log --all --diff-filter=A` on it → no hits) | Primary starting artifact + worked example both don't exist; `validate.py` still passes (no dead-link rule) → S06-W1-2: remove pointers, say "build from `vscode-shell.md`+`explanation-contract.md`" | W1 |
| code-explainer-2 | M | — | explanation-contract.md:145-146 "Re-read the code…character by character, for escaping and truncation damage" | Byte-for-byte fidelity check is prose, is actually deterministic (code pane `textContent` vs source bytes+escaping) → S06-W3-3: script it as a `check-html.mjs --kind code-explainer --source <file>` flag, implemented in this spec's own step (I07-K, CX-33) | W3 |
| code-explainer-3 | L | — | SKILL.md:5 "(Dark+ theme…)"; README.md:4 "(Dark Modern…)"; vscode-shell.md:8 "Dark Modern / Dark+ only" uses Dark Modern's actual token values | Theme named 2 ways (description/evals say "Dark+", README/shell say "Dark Modern") → S06-W3-2, S06-W3-3: name it "Dark Modern" everywhere | W3 |
| code-explainer-4 | L | — | explanation-contract.md:22 "Cards are real `<button>`s"; cards carry a heading+prose per SKILL Step 2 item 5 | `<button>` content is limited to phrasing content — a heading+paragraph inside one is invalid HTML → S06-W3-3 | W3 |
| code-explainer-5 | L | — | vscode-shell.md:35-36 "panes scroll internally — the page itself never scrolls"; explanation-contract.md:130-131 "Below ~900px the panes stack" (a stacked sub-900px layout can scroll) | Fit rule (single 1366×768 check) conflicts slightly with the stacked mobile layout → S06-W3-3 | W3 |
| code-explainer-6 | L | — | `grep ml-concept-lab skills/code-explainer/SKILL.md` → 0 hits; ml-concept-lab SKILL.md:199-201 already names code-explainer; no CHANGELOG.md at plugin root | Boundary is asymmetric (ML names CE, CE doesn't name ML); no CHANGELOG → S06-W3-2: add the ml-concept-lab line; S06-W3-1: add CHANGELOG | W3 |

No deferrals; no ratchet entry past W3.

### 1.4 Other findings

`design-system.md:33` itself claims "AA-contrast" (ci-3 breaks the design system's own stated goal, not just the template). The shared HTML contract (self-contained, doctype/color-scheme, render-before-file) is ~38% of CI's non-diagram body per the architecture's accounting, and lands in `html-artifact-contract.md`(I07, owned by S05) at W3; this spec's W1/W2 steps write against that vocabulary before the family file exists. `evals.json`(CI 4, CE 6) mines into the new layout per §6.2.

## 2. Target state

### 2.1 Location and tree

**After W1** (plugins stay at today's names): `clinical-infographic/skills/clinical-infographic/references/infographic-template.html` and `examples/ppgl-perioperative-management.html` both edited in place (no new files); `code-explainer/skills/code-explainer/SKILL.md`, `README.md` edited (pointer removal only).

**After W2**: `clinical-infographic/scripts/check-html.mjs` (byte-identical copy, created by S05-W2-2, this spec's steps only call it); SKILL.md Step 2.5/Step 3 rewritten.

**After W3** (S10's skeleton moves both plugins unchanged into `plugins/visuals/`; S05's skeleton already created `references/html-artifact-contract.md`+`render-verify.md`+the canonical `scripts/check-html.mjs`): `V=plugins/visuals` gains `skills/clinical-infographic/{SKILL.md,references/{design-system,source-contract}.md}` (CI's `lessons-learned.md` deleted, its content folded into CHANGELOG), `skills/code-explainer/{SKILL.md,references/{explanation-contract,vscode-shell}.md}`, `skills/infographic/`+`skills/explain-code/` (dmi aliases), both examples moved unchanged, CHANGELOG/README entries merged into the family's. Removed in W3 (S10's skeleton): `plugins/clinical-infographic/`, `plugins/code-explainer/`, both `commands/` files.

### 2.2 Frontmatter

Both descriptions are close to today's already-compliant shape (991/863 chars, well under the 1,024 hard cap) — **no rewrite is required for length**, only the W3 namespace substitution and, for code-explainer, a Not-for/Handoffs wording pass fixing ce-6's asymmetry. Sibling names are unprefixed at W2 (`code-explainer:code-explainer`, `concept-animation:concept-animation`), `visuals:…` at W3.

**`clinical-infographic`**: unchanged at W1/W2. **W3**: `→ concept-animation:concept-animation` becomes `→ visuals:concept-animation`; `→ pubmed-research-note:pubmed-research-note` becomes `→ evidence:pubmed-research-note`. Body text is otherwise untouched — the description already reads "NEVER invents clinical facts…renders a review or decision report" and needs no new phrasing.

**`code-explainer`** — one new sentence added to Not-for at W3 (ce-6): after "...concept animations (concept-animation)" add "or an explorable a learner drives (ml-concept-lab)." Chars: 863→~910 (still well under cap).

**W3 alias skills** (dmi; S10's skeleton creates them from the I20 template): `plugins/visuals/skills/infographic/SKILL.md` (description ≤100 chars, 1-line body):
```markdown
---
name: infographic
description: "Typed shortcut: /infographic runs visuals:clinical-infographic with the given topic or source."
disable-model-invocation: true
argument-hint: "[topic, or path/title of a sourced report]"
metadata:
  profile: cc
---

Invoke `visuals:clinical-infographic` with: $ARGUMENTS
```
`plugins/visuals/skills/explain-code/SKILL.md`: same shape, `visuals:code-explainer`, `argument-hint: "[pasted code, a file path, or a function/class name]"`, description `"Typed shortcut: /explain-code runs visuals:code-explainer with the given code."`.

Kept trigger phrases: all 7 CI phrases, all 7 CE phrases — none removed (unlike S05's ml-7, no overlap defect here). Full list §6.

### 2.3 Body outline

Actions: keep|cut(reason)|move→file|script→name|new. Targets: CI SKILL.md ≤190/≤3,000 tok(today 177/2,823); CE SKILL.md ≤165/≤2,300(today 162/2,222).

**CI SKILL.md, W1**: title/prime-directive/Step0/Step1 keep verbatim. Step2's "load-bearing rules" list gains "column header contrast ≥4.5:1(WCAG AA for <18.66px bold)" and "no text below 12px" (ci-3, ci-4). Step2.5: rewrite per H-CI1 (ci-5). Step3: keep, add the example link (ci-10). Failure conditions gain "a column header or badge fails WCAG AA" and "any text renders below 12px".

**CI SKILL.md, W2**: no further body change — Step2.5's H-CI1 text (written at W1) already names `check-html.mjs`; W2 only makes the script exist (S05-W2-2) and adds filing per H-CI2 (ci-6) to Step3.

**CI SKILL.md, W3**: reference-load line drops `lessons-learned.md` entirely (file deleted); Failure conditions and Handoffs get namespaced (`vault-keeper:vault-keeper`, `comprehensive-review`→`evidence:comprehensive-review`, `pubmed-research-note`→`evidence:pubmed-research-note`).

**CI template.html + example.html, W1**: delete the `@media(prefers-color-scheme:dark)` block (template:96-104, example's equivalent block); add `color-scheme:light` to `:root`; darken `--c2`/`--c3` (§2.7-equivalent values below); add `.mech{flex-direction:column} .mech .node{flex:0 0 auto} .mech .sep{transform:rotate(90deg)}` inside each file's own existing mobile breakpoint (`@media(max-width:720px)` template, `@media(max-width:820px)` example); raise every `font-size` below 12px to 12px (8 declarations in the template, 10 in the example, listed in ci-4's evidence).

**CE SKILL.md, W1**: :30's pointer sentence → "Start from the shell in `vscode-shell.md` and the rules in `explanation-contract.md` — there is no template file; you write the HTML directly to the contract." :99's "From `references/explainer-template.html`, to the contract" → "To the contract in `explanation-contract.md`". Everything else (Steps 0-4, Handoffs, Close, Failure) keeps unchanged.

**CE README.md, W1**: :86-87 tree listing drops the `explainer-template.html`/`examples/` lines (nothing exists there); if W1 has not yet produced a real worked example, the `examples/` block is cut entirely rather than left pointing at nothing (R13).

**CE SKILL.md/explanation-contract.md/vscode-shell.md, W3**: "(Dark+ theme…)"→"(Dark Modern theme…)"(ce-3); button-card rule→`<div role="button" tabindex="0">` with a key handler, since a heading+prose inside a real `<button>` is invalid phrasing content(ce-4); fit rule keeps 1366×768 no-scroll but adds "the sub-900px stacked layout may scroll vertically, never horizontally"(ce-5); Not-for gains the ml-concept-lab line(ce-6); fidelity-check item 5 becomes H-CE1(ce-2).

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `.../design-system.md` | palette, diagram grammar, print/a11y, contrast/legibility rules | "Before Step 2, read …" | unchanged, ~2,020 tok |
| `.../source-contract.md` | Step 0 acquisition rules | "Before Step 0, read …" (unchanged citation) | unchanged, ~1,283 tok |
| `.../lessons-learned.md` | DELETED W3 (ci-9); content folded into CHANGELOG's history | n/a after W3 | 0 |
| `.../explanation-contract.md` | 3 modes, fidelity, a11y, verify | "Read both before writing a line of markup" (unchanged) | unchanged, ~2,079 tok |
| `.../vscode-shell.md` | chrome, exact palette, closed token set, layout | same | unchanged, ~2,130 tok |
| `${CLAUDE_PLUGIN_ROOT}/examples/ppgl-perioperative-management.html`(+`.preview.png`) | reference infographic | linked from SKILL.md Step 3 (new, W1) | unchanged size |

No new reference files this spec creates — I07's family files (`html-artifact-contract.md`, `render-verify.md`) are owned and written by S05; this spec's skills read them starting W3 the same way concept-animation/ml-concept-lab do (ASSUMES-1 in §8).

### 2.5 Scripts

This spec owns no scripts. It consumes `check-html.mjs`(I07, owner S05): a byte-identical copy is created inside `clinical-infographic/scripts/` by S05-W2-2 (not by any step in this spec); this spec's own CI-W2 step only calls it and updates SKILL.md text to name it. Code-explainer gets no `scripts/` directory in W1/W2 — its byte-fidelity check is written into the FAMILY `check-html.mjs` at W3 via a new `--source <file>` flag (S05 implements; this spec's W3 step states the ASSUMES and updates `explanation-contract.md`'s wording, §2.3).

`check-html.mjs --kind infographic <file> --own` (I07-A) runs static-only checks (no render/drive needed for this kind): I07-B document rules, I07-D sheet rules (no dark-mode block, `.mech`-shaped strip stacking). Exit 0 pass / 1 fail / 2 usage / 3 incomplete, per I07-G.

### 2.6 Handoffs

Exact sentences. W2 names given (unprefixed siblings); W3 substitutes `vault-keeper:vault-keeper`→unchanged, `comprehensive-review:comprehensive-review`→`evidence:comprehensive-review`, `pubmed-research-note:pubmed-research-note`→`evidence:pubmed-research-note`, `concept-animation:concept-animation`→`visuals:concept-animation`, `ml-concept-lab:ml-concept-lab`→`visuals:ml-concept-lab`.

**H-CI1 Step 2.5 render/verify** (replaces SKILL.md:124-135, ci-5):
> Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/check-html.mjs <file> --kind infographic`. It uses `npm run audit:visual` when `$LEARN_HUB_DIR` is valid, its own static-only port otherwise; the JSON `tool` field says which ran. Proceed to Step 3 only on `verdict:"pass"`. On `fail`, fix each issue's `fix` text (no dark-mode block, ≥12px text, the `.mech` strip stacks on mobile, self-contained) and re-run. This step never changes what a fact says, only whether the page renders it correctly.

**H-CI2 Step 3 filing** (I11 visual filing sentence, owner S07 §2.7, adopted verbatim per CX-8): "Run `vault-keeper:vault-keeper` (OPTIONAL). If it is not available in this session — or the sink cannot resolve a destination and this is a non-interactive run — do not stall: file via `vault-keeper` when present; if absent, write `<slug>.html` and `<slug>.meta.json` to `$LEARN_HUB_DIR/research-notes/visuals/` when its marker validates, otherwise to cwd, and say where." As a separate sentence: "Filing never publishes: the user files it into the Learn hub with `ingest-visual` ('file <asset>')." `.meta.json`: `{kind:"infographic",title:"<h1>",description:"<topic/scope>",topic_hint:"<id/phrase/null>",source_report:"<basename>",producer:"clinical-infographic",created:"<YYYY-MM-DD>",audit:{tool,verdict:"pass|incomplete"}}` (fields per I09, same shape S05's H-7 defines for animations).

**H-CE1 Step 3.5 fidelity** (replaces explanation-contract.md:145-146, ce-2, W3): "Run `node ${CLAUDE_PLUGIN_ROOT}/scripts/check-html.mjs <file> --kind code-explainer --source <original-source-file>`. It diffs the rendered code pane's text against the source bytes and reports any escaping or truncation drift as an issue. This is on top of the render checklist above, not instead of it."

### 2.7 Interfaces (consumed only — this spec owns none)

| Interface | Owner | ASSUMES |
|---|---|---|
| I01 | S01 | for an HTML deliverable, "open the output"=first line of the chat hand-back |
| I07 | S05 | `check-html.mjs --kind infographic` runs I07-B/I07-D static checks only, no render/drive (I07-A). The `--kind code-explainer --source <file>` flag is this spec's own to implement (S06-W3-3, CX-33) on top of S05-W3-1's canonical script — not an ASSUMES on S05. |
| I08 | S16 | `audit:visual --kind infographic` implements the same rule set as `check-html.mjs`'s own port (I07-K) |
| I09 | S15 | `research-notes/visuals/<slug>.html`+`<slug>.meta.json`, `kind:"infographic"` accepted, fields per H-CI2 |
| I11 | S07 | producers call `vault-keeper:vault-keeper` with the two files, never `sink.py` directly |
| I17 | S12 | layout `plugins/<p>/evals/<skill>/<case>/`; tags per §4.1; alias skills exempt from ≥3-case rule |
| I20 | S08 | whitelist has `argument-hint`,`disable-model-invocation`,`metadata`; R13's dead-link rule is what closes ci-10/ce-1 permanently at validation time |
| I23 | S10 | skeleton moves both plugins' `skills/`,`references/`,`examples/` unchanged; creates the 2 alias skills of §2.2 |

Contrast/legibility values this spec DECIDES (not from any interface): darkened `--c2:#3b8368`(white-on-c2 contrast 4.53:1, was 4.14) and `--c3:#aa6527`(4.57:1, was 3.41), computed this session (WCAG relative-luminance formula, sRGB). `--c1:#3b6ea8`(5.27:1) and `--danger:#a4304a`(6.77:1) already pass and are unchanged. These apply to BOTH `infographic-template.html` and the PPGL example (ci-3).

## 3. Change steps

Shorthand: `CI`=`plugins/clinical-infographic`, `CE`=`plugins/code-explainer`(both micky); `V`=`plugins/visuals`(post-S10).

### Wave W0

**S06-W0-1** · depends on: S12-W0-3
- Files: create `CI/evals/clinical-infographic/<case>/{prompt.md,graders/*.md}` (3 cases: trigger positive, near-miss negative, one output case, mined against today's skill; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7)).
- Change: seed the pre-rewrite smoke baseline for clinical-infographic.
- Commands / done when: S12-W0-5's check for this unit — `find . -path '*/evals/clinical-infographic/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3.
- Rollback: `git rm -r CI/evals/clinical-infographic`.

### Wave W1

**S06-W1-1** · depends on: none
- Files: edit `CI/skills/clinical-infographic/references/infographic-template.html`, `CI/examples/ppgl-perioperative-management.html`.
- Change: in EACH file — delete the `@media(prefers-color-scheme:dark)` block; add `color-scheme:light;` to the `:root{}` rule; set `--c2:#3b8368` and `--c3:#aa6527` (§2.7); add `.mech{flex-direction:column} .mech .node{flex:0 0 auto} .mech .sep{transform:rotate(90deg)}` inside the file's own single-column mobile breakpoint (`max-width:720px` template, `max-width:820px` example); raise every `font-size` value below `12px` to `12px` (ci-4's evidence lists each selector).
- Commands: `grep -c "prefers-color-scheme:dark" CI/skills/clinical-infographic/references/infographic-template.html CI/examples/ppgl-perioperative-management.html`; `grep -c "color-scheme:\s*light" <same 2 files>`; `grep -oP 'font-size:\s*\K[0-9.]+(?=px)' <same 2 files> | awk -F: '{if($2<12) print}'`; `node --input-type=module -e "const [{auditInfographicResponsive},{readFileSync}]=await Promise.all([import('$LEARN_HUB_DIR/scripts/lib/infographic-responsive.mjs'),import('fs')]); console.log(JSON.stringify(auditInfographicResponsive(readFileSync(process.argv[1],'utf8'))))" <each file>` (CX-56 — `require` is undefined under `--input-type=module`, so both dependencies load via `import()`).
- Done when: both dark-block greps = 0; both light-scheme greps ≥1; the font-size awk check prints nothing; both `auditInfographicResponsive` calls print `[]`.
- Rollback: `git checkout -- CI/skills/clinical-infographic/references/infographic-template.html CI/examples/ppgl-perioperative-management.html`.

**S06-W1-2** · depends on: none
- Files: edit `CE/skills/code-explainer/SKILL.md` (:30, :99), `CE/README.md` (:86-87).
- Change: SKILL.md:30 and :99 per §2.3's CE SKILL.md text (remove the `explainer-template.html` pointers, say "build from `vscode-shell.md`+`explanation-contract.md`"); README.md drops the `explainer-template.html`/`examples/` tree lines.
- Commands: `grep -c "explainer-template" CE/skills/code-explainer/SKILL.md CE/README.md`.
- Done when: both = 0.
- Rollback: `git checkout -- CE/skills/code-explainer/SKILL.md CE/README.md`.

**S06-W1-3** · depends on: none
- Files: create the 4 eval case dirs each under `CI/evals/clinical-infographic/` and `CE/evals/code-explainer/` (contents §4.1).
- Change: 4 cases per skill, mined per §4.2.
- Commands: `find CI/evals/clinical-infographic -mindepth 1 -maxdepth 1 -type d | wc -l`; same for `CE/evals/code-explainer`.
- Done when: both = 4. (`claude plugin eval` not run by this spec — hard constraint.)
- Rollback: `git rm -r CI/evals CE/evals`.

**S06-W1-4** · depends on: S06-W1-1, S06-W1-2
- Files: none (verification).
- Change: none.
- Commands: `python3 scripts/validate.py`.
- Done when: `all checks passed`.
- Rollback: n/a.

**S06-W1-5** · depends on: S06-W1-1, S06-W1-2, S06-W1-3
- Change: release the W1 fixes — `python3 scripts/bump.py clinical-infographic patch --write`; `python3 scripts/bump.py code-explainer patch --write`.
- Files: both plugins' `.claude-plugin/plugin.json` and `CHANGELOG.md` (entry: "Light-lock, contrast, legibility fixes (H36/H37); dead template pointers removed (H42)."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for either entry.
- Rollback: `git checkout -- CI/.claude-plugin/plugin.json CI/CHANGELOG.md CE/.claude-plugin/plugin.json CE/CHANGELOG.md`.

W1 exit: no `prefers-color-scheme:dark` block in either CI file; both pass `auditInfographicResponsive` with `[]`; no `explainer-template.html` reference anywhere in `code-explainer/`; `validate.py` clean.

### Wave W2 (CI only — code-explainer has no W2 step)

**S06-W2-1** · depends on: S05-W2-2 (creates `CI/scripts/check-html.mjs`), S16-W2-3 (consumers before producers — the `.meta.json` filing shape this step writes against must exist first, CX-35)
- Files: edit `CI/skills/clinical-infographic/SKILL.md` (Step 2.5, Step 3).
- Change: Step 2.5 → H-CI1 (§2.6, ci-5); Step 3's filing item → H-CI2 (§2.6, ci-6, `.meta.json` per I09).
- Commands: `node CI/scripts/check-html.mjs CI/examples/ppgl-perioperative-management.html --kind infographic --own`; `grep -c "vault/assets" CI/skills/clinical-infographic/SKILL.md`.
- Done when: `check-html.mjs` prints `"verdict":"pass"` (or stated `"incomplete"` if no learn-hub/browser available, exit 3); the `vault/assets` grep = 0.
- Rollback: `git checkout -- CI/skills/clinical-infographic/SKILL.md`.

**S06-W2-2** · depends on: S06-W2-1
- Change: release the W2 fix — `python3 scripts/bump.py clinical-infographic minor --write`.
- Files: `CI/.claude-plugin/plugin.json`, `CI/CHANGELOG.md` (entry: "Render/verify via `check-html.mjs`; filing via the sink."). `.claude-plugin/marketplace.json` is not touched: S10-W0-3 removed every entry `version` (I18, CX-12).
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json` has no `version` key for this entry.
- Rollback: `git checkout -- CI/.claude-plugin/plugin.json CI/CHANGELOG.md`.

W2 exit: `check-html.mjs --kind infographic` passes on both the template-derived and the PPGL example; CI's filing sentence matches H-CI2; `validate.py` clean.

### Wave W3 (depends on S10's skeleton-PR move step, I23; and on S05-W3-1 creating `V/references/{html-artifact-contract,render-verify}.md` + moving `check-html.mjs` to `V/scripts/`)

**S06-W3-1** · depends on: S10-W3-2, S05-W3-1, S05-W3-5 (S05-W3-5 merges the per-member CHANGELOG files into `V/CHANGELOG.md`, which this step edits; CX-3)
- Files: delete `V/skills/clinical-infographic/references/lessons-learned.md`; rename `V/examples/README.md` (clinical-infographic's example README; S10-W3-2 moves `examples/` to the family root, CX-32) → `V/examples/ppgl-perioperative-management.md` (S05-W2-4 already renames ML's README the same way, CX-32) and fix its dead link; edit the family CHANGELOG (path per S10's layout, ASSUMES-4).
- Change: fold `lessons-learned.md` into a dated CHANGELOG entry (ci-9); add the missing `0.2.1` entry (ci-7); fix `examples/README.md`'s (now `ppgl-perioperative-management.md`'s) dead link (ci-8).
- Commands: `test ! -f V/skills/clinical-infographic/references/lessons-learned.md`; `test -f V/examples/ppgl-perioperative-management.md`; `grep -c "0.2.1" V/CHANGELOG.md`.
- Done when: the file is gone; the renamed README exists; the CHANGELOG grep ≥1.
- Rollback: `git checkout -- V/skills/clinical-infographic V/examples V/CHANGELOG.md`.

**S06-W3-2** · depends on: S06-W3-1, S01-W3-2, S12-W3-2 (CX-37)
- Files: edit `V/skills/clinical-infographic/SKILL.md` (frontmatter, reference-load line, Handoffs, Failure), `V/skills/code-explainer/SKILL.md` (description, Not-for, Handoffs).
- Change: namespace substitution per §2.6; CI's reference-load line drops `lessons-learned.md`; CI Step 3 links the example (ci-10); CE description "(Dark+ theme…)"→"(Dark Modern theme…)"(ce-3); CE Not-for gains the ml-concept-lab line(ce-6).
- Commands: `python3 measure.py skill V/skills/clinical-infographic/SKILL.md V/skills/code-explainer/SKILL.md`; `grep -c "Dark+" V/skills/code-explainer/SKILL.md V/README.md V/skills/code-explainer/references/vscode-shell.md`; `grep -c "ml-concept-lab" V/skills/code-explainer/SKILL.md`.
- Done when: both `measure.py` calls report `yaml_valid:true`, description ≤1,024; `Dark+` grep = 0; `ml-concept-lab` grep ≥1.
- Rollback: `git checkout -- V/skills/clinical-infographic/SKILL.md V/skills/code-explainer/SKILL.md`.

**S06-W3-3** · depends on: S06-W3-2, S05-W3-1 (this plugin's own step now implements the flag itself, per CX-33 — depends on S05-W3-1 only for `check-html.mjs` existing at `V/scripts/`)
- Files: edit `V/scripts/check-html.mjs` and its test file (implement `--kind code-explainer --source <file>`, diffing the rendered code pane's text against the source bytes for escaping/truncation drift, per H-CE1); edit `V/skills/code-explainer/references/explanation-contract.md` (:22, :145-146), `V/skills/code-explainer/references/vscode-shell.md` (:8, :35-36).
- Change: button-card rule → `role="button" tabindex="0"` div (ce-4); fidelity-check item → H-CE1 (§2.6, ce-2); theme line → "Dark Modern" only (ce-3); fit rule gains the stacked-layout scroll clarification (ce-5).
- Commands: `grep -c "Cards are real \`<button>\`" V/skills/code-explainer/references/explanation-contract.md`; `grep -c "check-html.mjs --source" V/skills/code-explainer/references/explanation-contract.md`; `grep -c "Dark+" V/skills/code-explainer/references/vscode-shell.md`; `node --test 'V/scripts/*.test.mjs'`.
- Done when: first grep = 0, second ≥1, third = 0; tests pass, including a `--kind code-explainer --source <file>` case.
- Rollback: `git checkout -- V/scripts V/skills/code-explainer/references`.

**S06-W3-4** · depends on: S06-W3-1, S10-W3-2
- Files: none (verify only — S10-W3-2 creates both alias skills, text copied verbatim from this spec's §2.2, CX-1).
- Change: none. Verify `V/skills/infographic/SKILL.md` and `V/skills/explain-code/SKILL.md` match §2.2's text exactly.
- Commands: `diff <(cat V/skills/infographic/SKILL.md) <(§2.2's infographic text)`; `diff <(cat V/skills/explain-code/SKILL.md) <(§2.2's explain-code text)`.
- Done when: both files exist, `disable-model-invocation:true`, body is the 1-line `Invoke` sentence, and both diffs are empty.
- Rollback: n/a (verification only).

W3 exit: `lessons-learned.md` gone; both SKILL.md descriptions namespaced and `yaml_valid:true`; no "Dark+" anywhere; ml-concept-lab named in code-explainer's Not-for; both alias skills present; H42 closed alongside H36/H37 (already closed at W1); every Appendix-A row assigned to this spec closed; `$VALIDATE --repo .` clean (CX-11 — the repo-root `scripts/validate.py` is gone by this point, moved by S08-W3-1). Per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H36, H37, H42); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."

## 4. Evals

### 4.1 Cases

CI: 4 cases (R71 3-5). Full content for 3; 4th in a table. CE: 4 of its existing 6 evals.json ids converted with full content for 3, the rest in a table (§4.2 covers the remaining 3). Paths under `plugins/clinical-infographic/evals/clinical-infographic/`(W1-3)→`plugins/visuals/evals/clinical-infographic/`(W3, moved by S10); same pattern for code-explainer.

**CI Case 1 — `trigger-existing-report/`** (trigger positive, mined from evals.json id 1):
`prompt.md`:
```markdown
---
tags: [clinical-infographic, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 25
---

Make an infographic of the PPGL perioperative management report.
```
`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?clinical-infographic"'
arm: both
---
```

**CI Case 2 — `negative-nonclinical-chart/`** (near-miss, dataviz's territory):
`prompt.md`:
```markdown
---
tags: [clinical-infographic, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Chart our clinic's quarterly patient-volume numbers as a nice visual.
```
`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?clinical-infographic"'
min: 0
max: 0
arm: both
---
```

**CI Case 3 — `output-fidelity-and-safety/`** (output/process — fidelity + banner, mined from evals.json id 3):
`prompt.md`:
```markdown
---
tags: [clinical-infographic, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 30
---

Turn this review into an infographic. It lists two absolute contraindications, doses with
units and titration qualifiers, and one figure marked [unverified].
```
`graders/safety-banner.md`:
```markdown
---
type: regex
target: { source: file, path: "*.html" }
pattern: 'CRITICAL SAFETY'
weight: 3
---
```
`graders/no-dark-block.md`:
```markdown
---
type: regex
target: { source: file, path: "*.html" }
pattern: 'prefers-color-scheme\s*:\s*dark'
match: not_contains
weight: 2
---
```

4th case: `output-contract-light-lock/` — tags `[clinical-infographic, output, release]`; prompt "Make an infographic of the PPGL report."; graders: `regex` for `color-scheme\s*:\s*light` on the HTML; `tool_used Bash input_match:'check-html\.mjs' min:1` (the `.mech` stacking check itself is `check-html.mjs`'s job, not a regex's).

**CE Case 1 — `trigger-clear-snippet/`** (trigger positive, mined from evals.json id 1):
`prompt.md`:
```markdown
---
tags: [code-explainer, trigger, smoke]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 25
---

Explain this code:

def bisect_left(a, x):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] < x:
            lo = mid + 1
        else:
            hi = mid
    return lo
```
`graders/skill-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?code-explainer"'
arm: both
---
```

**CE Case 2 — `negative-concept-not-code/`** (near-miss, concept-animation's territory):
`prompt.md`:
```markdown
---
tags: [code-explainer, negative]
allowed_tools: [Read, Glob, Grep, Skill]
max_turns: 10
---

Make an animation of how event loops work in general — I don't have specific code, I just
want to understand the idea.
```
`graders/not-fired.md`:
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?code-explainer"'
min: 0
max: 0
arm: both
---
```

**CE Case 3 — `output-fidelity-and-defect-naming/`** (output/process — byte fidelity, mined from evals.json id 3):
`prompt.md`:
```markdown
---
tags: [code-explainer, output, release]
allowed_tools: [Read, Glob, Grep, Skill, Write, Bash(node *)]
max_turns: 30
---

Walk me through this C# function. It contains List<int>, a catch (Exception) { } that
swallows everything, and an inconsistently indented block.
```
`graders/generics-survive-escaping.md`:
```markdown
---
type: regex
target: { source: file, path: "*.html" }
pattern: 'List&lt;int&gt;'
weight: 2
---
```
`graders/defect-named.md`:
```markdown
---
type: llm
criteria: PASS if the rendered explanation names the empty catch block as a defect (swallowed exception) rather than describing it as normal error handling. FAIL if it is described as "handles errors" or similar with no defect language.
---
```

4th case: `no-invented-runtime-values/` — mined from evals.json id 4; tags `[code-explainer, negative]`; prompt names a `Math.random()*ceiling` delay and asks "show me how the variables change"; grader: `llm` PASS if the STATE trace writes the delay symbolically (e.g. `0…ceiling`), FAIL if a concrete invented millisecond value appears.

### 4.2 Conversion

| Old evals.json case (id, name) | New case dir | Notes |
|---|---|---|
| CI 1 `renders-existing-…-and-files-asset` | `trigger-existing-report/` | skeleton mined |
| CI 2 `generates-sourced-content-first…` | dropped (no case slot left; folds into Case 1's Step 0 coverage) | |
| CI 3 `fidelity-safety-banner-…` | `output-fidelity-and-safety/` | skeleton mined |
| CI 4 `does-not-fire-outside-its-lane` | `negative-nonclinical-chart/` | prompt trimmed to the chart half |
| CE 1 `fast-path-on-a-clear-snippet` | `trigger-clear-snippet/` | skeleton mined |
| CE 2 `gate-fires-on-an-ambiguous…` | dropped (gate coverage is intent-lock's own family, S01) | |
| CE 3 `fidelity-escaping-…-a-real-defect` | `output-fidelity-and-defect-naming/` | skeleton mined |
| CE 4 `no-invented-runtime-values` | `no-invented-runtime-values/` (4th-case row) | |
| CE 5 `does-not-fire-outside-its-lane` | `negative-concept-not-code/` | prompt narrowed to one near-miss |
| CE 6 `vault-only-on-explicit-request` | dropped (covered by S07's vault-keeper OPTIONAL-fallback family) | |

### 4.3 Live triggers

Family (arch §6.3): `{concept-animation, ml-concept-lab, clinical-infographic, code-explainer, gridgeist, dataviz}`. Near-miss queries (feeding S12): "one-page printable reference sheet for antipsychotic dosing"→`clinical-infographic`; "explain this sorting algorithm's code line by line"→`code-explainer`; "chart our clinic's quarterly patient-volume numbers"→`dataviz`; "make an animation of how event loops work"→`concept-animation`; "let me play with gradient descent myself"→`ml-concept-lab`.

### 4.4 Commands

Smoke: `bash scripts/eval.sh --smoke visuals -- --allow-tools "Write,Bash(node *)"` (several CI/CE cases write the HTML file and run `check-html.mjs` via `Bash(node *)` — factcheck F3). Release: `bash scripts/eval.sh --release visuals -- --allow-tools "Write,Bash(node *)"`. Neither runs from this spec (hard constraint) — documented for the executor session after S10's wrapper exists.

## 5. Acceptance criteria

1. `python3 scripts/validate.py` prints `all checks passed` after W1 and W2; `$VALIDATE --repo .` (post-S08-W3-1's move, CX-11) prints `all checks passed` after W3.
2. `grep -c "prefers-color-scheme:dark" plugins/clinical-infographic/skills/clinical-infographic/references/infographic-template.html plugins/clinical-infographic/examples/ppgl-perioperative-management.html` = 0 (post-W1).
3. `node --input-type=module -e "const [{auditInfographicResponsive},{readFileSync}]=await Promise.all([import('$LEARN_HUB_DIR/scripts/lib/infographic-responsive.mjs'),import('fs')]); console.log(JSON.stringify(auditInfographicResponsive(readFileSync(process.argv[1],'utf8'))))" <file>` prints `[]` for both CI files (post-W1; CX-56).
4. `grep -oP 'font-size:\s*\K[0-9.]+(?=px)' <file> | awk '$1<12'` prints nothing for both CI files (post-W1).
5. `grep -c "explainer-template" plugins/code-explainer/skills/code-explainer/SKILL.md plugins/code-explainer/README.md` = 0 (post-W1).
6. `node plugins/clinical-infographic/scripts/check-html.mjs <file> --kind infographic --own` reports `"verdict":"pass"` for the template-filled example (post-W2).
7. `grep -c "vault/assets" plugins/visuals/skills/clinical-infographic/SKILL.md` = 0 (ci-6 closed, post-W3).
8. `test ! -f plugins/visuals/skills/clinical-infographic/references/lessons-learned.md` (post-W3).
9. `grep -c "Dark+" plugins/visuals/skills/code-explainer/SKILL.md plugins/visuals/README.md plugins/visuals/skills/code-explainer/references/vscode-shell.md` = 0 (post-W3).
10. `find plugins/clinical-infographic/evals/clinical-infographic -mindepth 1 -maxdepth 1 -type d | wc -l` = 4 (post-W1-3); same path under `plugins/visuals/` for both skills post-W3.

## 6. Trigger lock

| Phrase | Source | Kept / moved / removed |
|---|---|---|
| "make an infographic","medical summary infographic","clinical reference infographic","turn this review/report into an infographic","one-page visual summary","สรุปเป็นอินโฟกราฟิก" | CI description | kept |
| "/infographic" | CI command → W3 alias skill | kept, moved to `skills/infographic/SKILL.md` |
| "explain this code","explain the given code","walk me through this function","annotate this code","code walkthrough","what does this code do","อธิบายโค้ดนี้" | CE description | kept |
| "/explain-code" | CE command → W3 alias skill | kept, moved to `skills/explain-code/SKILL.md` |

No phrase is removed or moved outside the two commands — neither skill's defects touch the trigger surface.

## 7. Risks and OD sensitivity

- **OD9-b** (capability names only, no alias skills): `/infographic`/`/explain-code` dropped entirely; §2.2's alias blocks and §6's slash rows don't exist.
- **OD9-c** (rename to verbs): `clinical-infographic`→`infographic`, `code-explainer`→`explain-code`; every SKILL.md `name:`, §4.1's grader regexes, and §6 change.
- No OD3 sensitivity: this spec owns no interface, so the family-merge OD doesn't change what it writes (only where S05's `check-html.mjs`/family refs physically live, which this spec only calls/links).
- No OD5/OD13 sensitivity: no publish/digest gate, no claude.ai upload step.
- **K-risk**: CI's W2 step depends on S05's `check-html.mjs` shipping `--kind infographic`; CE's W3 fidelity flag is this spec's own implementation (CX-33) on top of S05's canonical script.

## 8. Open questions

- **ASSUMES-1** (I07, owner S05): `check-html.mjs` accepts `--kind infographic` (static-only, per I07-A) at `V/scripts/`. `--kind code-explainer --source <file>` is no longer an assumption on S05 (CX-33) — S06-W3-3 implements it directly.
- **ASSUMES-2** (I09, owner S15): `.meta.json`'s exact field list and the `-2`/`-3` collision-suffix rule, reused here from S05's H-7 shape. Check: read S15's spec once written.
- **ASSUMES-3** (I11, owner S07): producers call `vault-keeper` with exactly two files. Check: read S07's spec once written.
- **ASSUMES-4** (path layout, owner S10/S08): where the merged `visuals` CHANGELOG lives. Check: read S10's skeleton-PR spec and S08's release-tooling spec once written; S06-W3-1's CHANGELOG path is written against this assumption.
- **Q-CI-mobile-check**: whether `auditInfographicResponsive` can run from a micky-only session before S16 writes `audit:visual` (S06-W1-1 assumes `$LEARN_HUB_DIR` is set, per S11's I16 schedule). If not, that part of W1-1's Done-when defers; the CSS edits still land.
- **ARCH-CONFLICT**: none found. Architecture's W1 item 5 ("light-lock + strip + contrast, H36/H37") doesn't name the ≥12px fix by hazard number — treated here as ci-4, confirmed in W1 by both the digest and the task's explicit "≥12px in template AND example" instruction.
