# Spec S09: firecrawl (slim router + dated vendor reference) and gridgeist (metadata only)

| Field | Value |
|---|---|
| Repos | micky-psych-tools |
| Units (today → target) | `plugins/firecrawl` → `firecrawl`: skill `firecrawl` (router ≤1,500 tok) + `references/vendor-onboarding-<fetch-date>.md`; `defaultEnabled: false`. `plugins/gridgeist` → unchanged skill body/content + `UPSTREAM.md`; `agents/openai.yaml` + unused `assets/` dropped |
| Waves | W0 (firecrawl smoke seeds, S09-W0-1), W1 (firecrawl refresh: fetched stamp, never write `.env`, headless fallbacks — H12), W3 (firecrawl split: router+reference, `defaultEnabled:false`; gridgeist `UPSTREAM.md`), W5 (gridgeist usage decision) |
| Owner decisions assumed | OD12-a (slim router kept, not retired), OD10 (gridgeist decided at W5 by usage — not resolved here) |
| Defects closed | 14/14 assigned (HIGH: H12) |
| Interfaces owned | none |
| Interfaces consumed | I01 (S01), I05 (S03), I11 (S07), I16 (S11), I17 (S12), I20 (S08) |
| Depends on specs | S01 (intent-lock handoff sentence, I01), S03 (fetch-only contract text, I05), S07 (vault-keeper filing sentence, I11), S08 (house shape + validator, I20/I19), S11 (W1-exit cloud enablement, I16), S12 (eval layout, I17) |

## 1. Current state (measured 2026-09-24)

### 1.1 Files

| Path | Lines | Bytes | Est. tok | Role |
|---|---|---|---|---|
| `firecrawl/.claude-plugin/plugin.json` | 15 | 744 | 186 | manifest |
| `firecrawl/README.md` | 63 | 3,312 | 828 | docs |
| `firecrawl/CHANGELOG.md` | 28 | 1,783 | 446 | docs |
| `firecrawl/skills/firecrawl/SKILL.md` | 384 | 18,035 | body 4,214 tok; description 1,009 chars/252 tok | vendor + router |
| `firecrawl/skills/firecrawl/evals/evals.json` | 69 | 5,126 | 1,282 | 8 ungraded cases |
| `gridgeist/.claude-plugin/plugin.json` | 20 | 533 | 133 | manifest |
| `gridgeist/LICENSE` | 21 | 1,062 | 266 | MIT, vendored |
| `gridgeist/skills/gridgeist/SKILL.md` | 74 | 5,084 | body 1,079 tok; description 708 chars/177 tok | vendored skill |
| `gridgeist/skills/gridgeist/agents/openai.yaml` | 9 | 400 | 100 | Codex metadata (dropped) |
| `gridgeist/skills/gridgeist/assets/gridgeist-small.svg` | — | 800 | — | Codex icon (dropped, unused elsewhere) |
| `gridgeist/skills/gridgeist/assets/gridgeist.png` | — | 41,217 | — | Codex icon (dropped, unused elsewhere) |
| `gridgeist/skills/gridgeist/assets/gridgeist.svg` | — | 1,229 | — | unreferenced anywhere (dropped) |
| `gridgeist/skills/gridgeist/references/design-language.md` | 69 | 3,351 | 838 | kept, unchanged |
| `gridgeist/skills/gridgeist/references/review-checklist.md` | 71 | 2,894 | 724 | kept, unchanged |

Re-verified this session: `grep -rn "gridgeist.svg\|gridgeist.png\|gridgeist-small" plugins/gridgeist/` shows both small assets referenced ONLY by `agents/openai.yaml`; `gridgeist.svg` has zero references anywhere. Neither `firecrawl/` nor `gridgeist/` ships a `LICENSE`... correction: gridgeist DOES ship one (vendored, kept); firecrawl does not (added W3, self-compliance with I19's VAL-11, owner S08).

### 1.2 Descriptions

| Skill | Chars | Bytes | YAML valid? | `Use when` @ | `Not for`? | Quoted phrases |
|---|---|---|---|---|---|---|
| `firecrawl` | 1,009 | 1,011 | yes | 232 | yes | "firecrawl", "scrape this page/site/URL", "search the web", "crawl these docs", "map a site" |
| `gridgeist` | 708 | 710 | yes | 304 | yes | "redesign this page", "make this UI less generic", "review this interface", "needs a stronger grid", "Swiss style", "editorial layout" |

firecrawl's description sits at 1,009/1,024 (98.5% of the hard cap) — no headroom for the W3 boundary-clause addition without cutting elsewhere (§2.2).

### 1.3 Defects

| id | sev | H# | evidence (re-opened) | problem → fix | wave |
|---|---|---|---|---|---|
| firecrawl-1 | H | H12 | `SKILL.md:146-147` "already installed… No separate install needed"; live vendor doc (fetched 2026-09-24, this session): `firecrawl setup build` is a SEPARATE required step | Claude would skip the build-skills install; no fetched-on date to detect drift → S09-W1-1 | W1 |
| firecrawl-2 | M | — | `SKILL.md:33` install cmd; vendor SKILL.md frontmatter `name: firecrawl` (confirmed live) | The vendor's own install adds a same-named `firecrawl` skill, colliding with this one | S09-W3-1 (boundary clause, R7) | W3 |
| firecrawl-3 | M | — | `SKILL.md:270` `echo "FIRECRAWL_API_KEY=fc-..." >> .env`; `.gitignore` has no `.env` entry | Key can be committed; `.env` not ignored | S09-W1-1 (never write) + cite S10-W0-7 (`.gitignore` step) | W1 |
| firecrawl-4 | M | — | 367-line body (16,858 chars/4,214 tok); vendor sections `:19-338`, marketplace-specific `:340-384` (45 lines) | Full vendor guide loads on every trigger; marketplace-specific content is the last 12% | S09-W3-1 (split) | W3 |
| firecrawl-5 | M | — | `README.md:9` "kept verbatim"; `CHANGELOG.md` 0.1.0 lists two local adaptations; no source version/date recorded | "Verbatim" contradicts the adaptations; nothing dates the copy | S09-W1-1 (fetched stamp) + S09-W3-1 (adaptations named in the router) | W1/W3 |
| firecrawl-6 | M | — | `SKILL.md:33` `--browser` opens a GUI auth flow; `:255-260` a ```bash fence containing a raw `POST` line, not a shell command | Browser flow fails in a headless container; the "bash" is not executable as written | S09-W1-1 | W1 |
| firecrawl-7 | L | — | `SKILL.md:52` "Before doing real work, verify the install:" vs `evals.json` id 1 "verifies… only when the CLI state is unknown" | Skill and its own eval disagree on when to verify | S09-W3-1 | W3 |
| firecrawl-8 | L | — | `plugin.json` has no `dependencies`; intent-lock/vault-keeper referenced by name only | Cross-plugin deps undeclared — **by design** (T4, R56-58: no `dependencies` anywhere); fix is the OPTIONAL fallback sentence, not a manifest field | S09-W3-1 | W3 |
| firecrawl-9 | L | — | `SKILL.md:7` `"search the web"`; `marketplace.json` entry `"category": "productivity"` | Broad trigger risks capturing ordinary web searches; category is debatable | S09-W3-1 (narrow the phrase; category unchanged — no better fit exists) | W3 |
| firecrawl-10 | L | — | `evals.json` id 6 expected_output names the outdated keyless-REST scope; all 8 cases have `assertions: []` | Evals ungraded and lock in stale behavior | S09-W3-1 (eval conversion, §4) | W3 |
| gridgeist-1 | L | — | `agents/openai.yaml:1-9`; 3 asset files, 2 referenced only by it, 1 referenced nowhere | Codex-only metadata + dead assets confuse maintainers | S09-W3-2 | W3 |
| gridgeist-2 | L | — | `grep -n -i gridgeist CLAUDE.md` finds nothing; `MEMORY.md:615` documents it | Omitted from CLAUDE.md's plugin inventory | moot once S10-W3-8's CLAUDE.md rewrite drops the hand-maintained catalog (I24) — no S09 file change | — |
| gridgeist-3 | L | — | plugin root has `.claude-plugin`, `LICENSE`, `skills` only; `MEMORY.md:615-618` gives no upstream commit/tag | No evals/README/CHANGELOG; vendored revision unrecorded, can't be diffed on a future sync | S09-W3-2 (`UPSTREAM.md`, README, CHANGELOG, 3 eval cases) | W3 |
| gridgeist-4 | L | — | `marketplace.json` gridgeist description (132 chars) is minimal/imperative vs the skill description's fuller routing signal | Weaker routing signal on the surface Claude reads first | S10-W3-1 (marketplace entries lose `description`, I24) | W3 |

Count: **14/14** assigned. gridgeist-2 and firecrawl/gridgeist-4-equivalent items carry no `S09-W…` step where the fix lives entirely in another spec's unit (noted per row).

### 1.4 Other findings

- OBS (verified live, this session, `WebFetch` on `docs.firecrawl.dev/ai-onboarding`): build skills require the separate `firecrawl setup build` command (confirms firecrawl-1); the CLI skill is named `firecrawl` (confirms firecrawl-2); keyless access covers search/scrape/interact/**parse** via CLI/SDK/REST, but the **hosted MCP** surface is narrower — search/scrape/parse only, no interact (today's Path F says nothing about `parse` or the MCP/CLI distinction — a third drift point beyond the digest's original 8).
- NEW, unresolved by this session's verification: the digest's `ask` → `doctor` claim (INV firecrawl-1, phase-1 evidence dated 2026-09-23) could NOT be confirmed live — two targeted fetches this session found no "doctor" command/skill and no "firecrawl-ask" CLI command (only a `/support/ask` REST endpoint, which is what today's SKILL.md's `firecrawl-ask` skill already targets). `WebFetch` summarizes through a small model and may miss content, so this is not proof the digest was wrong — flagged **ASSUMES**, §8.
- OBS evals (marketplace-wide): the three plugins in this group ship 20 total cases, all ungraded (`assertions: []`); plugin-creator/refine-plugin ship none at all (out of scope here, see S08).
- OBS: gridgeist "Healthy; content stays verbatim to avoid forking upstream" (architecture) means SKILL.md/`references/*` are NOT rewritten by this spec — only metadata (UPSTREAM.md, README, CHANGELOG, evals) is added.

## 2. Target state

### 2.1 Location and tree (after W3)

```
plugins/firecrawl/
  .claude-plugin/plugin.json    $schema, version, author, keywords, defaultEnabled:false (R30)
  README.md  CHANGELOG.md  LICENSE          (LICENSE new — I19 VAL-13, owner S08)
  skills/firecrawl/
    SKILL.md                    router, ≤1,500 tok body (I20 house shape, owner S08)
    references/
      vendor-onboarding-<fetch-date>.md    vendor guide, W1-corrected, dated
    evals/{...}/                6 cases (was evals.json, 8 ungraded)

plugins/gridgeist/
  .claude-plugin/plugin.json    unchanged (name,version,description,author,license,keywords)
  LICENSE                       unchanged, vendored MIT
  UPSTREAM.md                   repo, sha (best-match candidate, flagged), vendoring date
  README.md  CHANGELOG.md       new (metadata only)
  skills/gridgeist/
    SKILL.md                    UNCHANGED body/content (verbatim, no fork)
    references/{design-language,review-checklist}.md   UNCHANGED
    evals/{...}/                3 new cases
  (agents/openai.yaml, assets/ — DELETED)
```

### 2.2 Frontmatter

**`firecrawl`** (router; description rewritten — same trigger surface, tighter, room for the
boundary clause within the 1,024 cap):
```yaml
---
name: firecrawl
description: >-
  Routes any general-web data request to the right Firecrawl path: live CLI search/scrape/
  interact/crawl/map, app-code SDK integration, repeatable web-data deliverables, account/
  credential setup, REST-only, or the keyless free tier. Use when the user says "firecrawl",
  "scrape this page/site/URL", "search the general web", "crawl these docs", "map a site",
  needs live web data in-session, wants Firecrawl in app code, or wants a web-powered
  deliverable (research brief, SEO audit, lead list, knowledge base). Also the marketplace's
  general-web evidence engine, called by pubmed-research-note and comprehensive-review for
  documents outside PubMed/ClinicalTrials.gov, fetch-only. Not for biomedical literature
  itself (use pubmed-research-note, comprehensive-review, or lit-watch); not for the vendor's
  own installed firecrawl skill's build/workflow onboarding (this is the marketplace-facing
  router — see the dated vendor reference under references/ for that content).
metadata:
  profile: cc
---
```
Measured (`measure.py text` on this exact draft): 965 chars / 241 tok — inside the cap;
`Use when` offset 231; `Not for` offset 677; no `I/you/your`; `has_angle_brackets: false`.
The first draft named the reference file literally as `references/vendor-onboarding-<date>.md`
inside the description — a literal `<>` pair, which itself violates the rule this house shape
exists to enforce. Caught by re-running `measure.py text` on the draft (not assumed clean);
fixed by describing the file instead of naming its angle-bracket placeholder. Narrowed
"search the web" → "search the general web" (closes -9's precision half). Added the
vendor-skill-collision boundary clause (closes -2).

**`gridgeist`**: unchanged — same frontmatter as today (§1.2), verbatim. No edit in this spec.

### 2.3 Body outline

**`firecrawl/SKILL.md`** — full split, not a line-by-line table (today's 384 lines reorganize
wholesale, not edit-in-place):

| Target section | Source | Content |
|---|---|---|
| Intro (2-3 sentences) | new | what this router does, points at the reference for the full flow |
| `## Marketplace contract` | `:340-384` (kept, rewritten) | inbound engine for evidence (I05 fetch-only contract, restated consistently with `evidence/references/engines.md`); outbound intent-lock (I01) + vault-keeper (I11) OPTIONAL handoffs (§2.6); not-chained list |
| `## Credential hygiene` | `:379-385` (kept, corrected) | `FIRECRAWL_API_KEY` from environment only; never written to a file; `.firecrawl/` gitignored (cite S10-W0-7) |
| `## Choose your path` | `:89-101` (condensed to a table) | A-F one-liners + "read references/vendor-onboarding-2026-09-24.md §Path-X for the full flow" (a fresh W1 refresh renames both the file and this line together) |
| `## Headless / no-browser fallback` | new (closes -6) | when `--browser` can't run: `init --all` without it, then Path D's non-browser key flow |
| `## Gotchas` | new (R23) | the vendor's own `firecrawl` skill collides on name (-2); the `ask`→`doctor` rename is unconfirmed as of this fetch (§8) |
| — (everything else: Paths A-F step-by-step detail, endpoints, docs links) | `:105-338` | **moved, W1-corrected**, to `references/vendor-onboarding-<fetch-date>.md` |

Target: body ≤45 lines, ≤1,500 tok (from 4,214 tok — a 65% cut, matching architecture §9's
"body ≤1.5k" target against today's measured 4.2k).

**`gridgeist/SKILL.md`**: no body outline — unchanged, verbatim (architecture: "content stays
verbatim to avoid forking upstream").

### 2.4 References

| File | Purpose | Load condition | Size target |
|---|---|---|---|
| `firecrawl/references/vendor-onboarding-<fetch-date>.md` | full vendor guide (Paths A-F, endpoints, docs links), W1-corrected | "For the full flow, read references/vendor-onboarding-2026-09-24.md" | ≈16k chars (today's body minus the 45 marketplace-specific lines, plus the W1 fixes) |
| `gridgeist/references/{design-language,review-checklist}.md` | unchanged | as today (linked from SKILL.md `:22`, `:26`) | unchanged |

### 2.5 Scripts

None. No unit in this spec ships a bundled script.

### 2.6 Handoffs

Firecrawl's router carries two OPTIONAL handoffs, both exact restatements per their owning
specs (§4.2 of the architecture; **do not paraphrase**):

> Run `alignment:intent-lock` (OPTIONAL). If it is not available in this session — or it needs
> an interactive picker and none exists here (subagent, headless, scheduled run) — do not
> stall: take the broadest reading that fits the request and open the output with one line
> `Assumed: <reading> — say if wrong.`

(Gates Path C step 1, "confirm the workflow and final artifact", per today's `:359-361`, kept.)

> File via `vault-keeper` (OPTIONAL). If absent, write to `$LEARN_HUB_DIR/research-notes/`
> when its marker validates, otherwise to cwd, and say where.

(On an explicit "vault this" about a finished Path C deliverable — kept from today's
`:362-368`, restated verbatim per I11.)

Received: pubmed-research-note and comprehensive-review call firecrawl as their general-web
engine (I05, owner S03) — firecrawl's router restates the identical fetch-only contract text
so the two never drift (§2.3 "Marketplace contract").

Gridgeist: no handoffs, in or out — unchanged.

### 2.7 Interfaces

No interfaces owned by this spec.

**Consumed (ASSUMES unless noted; owner to confirm):**

| Interface | Owner | Assumption |
|---|---|---|
| I01 | S01 | The intent-lock handoff sentence (§2.6) is copied verbatim from S01's §2.7 "Handoff" text; at firecrawl's W3 (concurrent with S01's W3 skeleton-PR-dependent rewrite), the plugin segment is `alignment:intent-lock`, not today's `intent-lock`. |
| I05 | S03 | The fetch-only contract firecrawl restates ("clean markdown + exact URL + access date; fetch only") must stay byte-consistent with `evidence/references/engines.md`'s own firecrawl line — S03's spec already states this text (read this session); this spec doesn't own it, only mirrors it. |
| I11 | S07 | The sink filing sentence (§2.6) is copied from architecture §4.2 verbatim; S07's spec (not yet written) is the owner of the exact `sink.py` resolution order — ASSUMES the sentence text doesn't change. |
| I16 | S11 | firecrawl joins `CLAUDE_CODE_PLUGIN_DIRS` at W1 exit (S11's schedule point V2) once H12 closes and the smoke suite passes; this spec's W1 step is a dependency of S11's edit, not an env-var change itself. |
| I17 | S12 | Case layout `plugins/firecrawl/evals/<skill>/<case>/` and `plugins/gridgeist/evals/<skill>/<case>/`; tags; trigger-grader regex per §4.1; `scripts/eval.sh` flags (§4.4). |
| I20 | S08 | House shape applied to firecrawl's rewritten frontmatter/body (§2.2/§2.3): `metadata.profile: cc`, standing rules first, `## Gotchas`, no version narration. Gridgeist's frontmatter is explicitly NOT touched (architecture: unchanged), so I20 applies to it only insofar as it already happens to comply (it does: single capability clause + Use-when + Not-for, no `I/you`, no `<>` — verified §1.2). |

## 3. Change steps

`$FC` = `plugins/firecrawl`; `$GG` = `plugins/gridgeist`. "Rollback: `revert`" = `git revert <this commit>`.

### W0

**S09-W0-1 (new, critique P1) · micky · firecrawl smoke seeds**
- Depends on: S12-W0-3.
- Files: create `$FC/evals/firecrawl/<case>/{prompt.md,graders/*.md}` — 3 cases re-tagged from today's `evals.json` (a trigger positive, a near-miss negative, one output case), mined against today's skill; I17 layout; every `prompt.md` carries `smoke` in `tags`; each case directory takes the name of one of §4.1's cases, so the later eval step extends these directories instead of adding new ones (critique P2, P7) (e.g. `trigger-known-url`, `negative-biomedical`, `deliverable-gated`). gridgeist gets no W0 seeds: S12 §2.6 does not list it, and it is loaded from V0 on.
- Change: the pre-rewrite smoke baseline that I16.3 condition 4 needs before S11-W1-1 enables firecrawl (V2), and that S12-W0-5 checks.
- Commands / done when: `find . -path '*/evals/firecrawl/*' -name prompt.md | xargs grep -l 'tags:.*smoke' | wc -l` ≥ 3.
- Rollback: `git rm -r $FC/evals/firecrawl`.

### W1

**S09-W1-1 · micky · firecrawl vendor refresh (H12)**
- Depends on: none.
- Files: edit `$FC/skills/firecrawl/SKILL.md`.
- Change:
  1. `:146-147` "The build skills are already installed from the same command above. No
     separate install needed." → "Build skills are a SEPARATE step: run `firecrawl setup
     build` after the base `init`. (Verified against the live vendor doc: `fetched: 2026-09-24
     https://docs.firecrawl.dev/ai-onboarding`.)"
  2. Add near the top of the body: `**Source:** vendor AI-onboarding guide, fetched: 2026-09-24
     https://docs.firecrawl.dev/ai-onboarding — re-verify before relying on any path/command
     name if this date is old.`
  3. `:255-260`: replace the bare `POST …` line inside the ```bash fence with a real command:
     `curl -s -X POST https://www.firecrawl.dev/api/auth/cli/status -H "Content-Type:
     application/json" -d "{\"session_id\":\"$SESSION_ID\",\"code_verifier\":\"$CODE_VERIFIER\"}"`.
  4. `:270` `echo "FIRECRAWL_API_KEY=fc-..." >> .env` → replace with: "Print the key and tell
     the human to export it in their shell profile or the session's environment-variable
     mechanism. Never write it to a file in this repo." (closes -3's write half).
  5. Add, after the install command: "**Headless / no-browser fallback:** if `--browser`
     cannot open a GUI (a cloud container), run `npx -y firecrawl-cli@latest init --all`
     (no `--browser`), then use Path D's non-browser key-auth flow (steps 1-4 below) to
     authorize." (closes -6's browser half).
  6. Path F: replace "Search, scrape, and interact are available keyless" with "Search,
     scrape, interact, and parse are available keyless via the CLI/SDK/REST API; the hosted
     MCP server exposes only search/scrape/parse keyless (interact needs an account there)."
     (verified live, this session).
- Commands: `python3 -c "import yaml; yaml.safe_load(open('plugins/firecrawl/skills/firecrawl/SKILL.md',encoding='utf-8').read().split('---')[1])"` ; `grep -n "fetched: 2026-09-24" plugins/firecrawl/skills/firecrawl/SKILL.md` ; `grep -c "\.env" plugins/firecrawl/skills/firecrawl/SKILL.md`
- Done when: YAML parses; the fetched-stamp grep prints 1 line; the `.env` grep shows only the
  "never write it to a file" prose, no `>> .env` write instruction.
- Rollback: `revert`.

**S09-W1-2 · DROPPED (OQ12-a): micky · release the W1 refresh.** Windows loads plugins in place from W1 entry (S11-W3-2), so this interim version bump is not needed; the change steps write their CHANGELOG entries under `## Unreleased`, and `release.py` sets the version once at W3.
- Depends on: S09-W1-1.
- Commands: `python3 scripts/bump.py firecrawl patch --write` (CX-12).
- Files: `$FC/.claude-plugin/plugin.json`, `$FC/CHANGELOG.md` (entry: "Vendor refresh: build-skills install step, headless browser fallback, .env write removed, keyless scope corrected (H12 interim)."). `.claude-plugin/marketplace.json` is NOT touched — S10-W0-3 has already stripped entry versions.
- Done when: `python3 scripts/validate.py` prints `all checks passed`; `marketplace.json`'s `firecrawl` entry carries no `version` key.
- Rollback: `revert`.

### W3

**S09-W3-1 · micky · firecrawl split into router + dated reference**
- Depends on: S09-W1-1, S08-W3-1 (house shape + validator, for the description/body checks this step must pass, CX-34), S10-W3-2 (skeleton move — CX-36), S10-W0-8 (LICENSE backfill), S12-W3-2 (CX-37). OQ6-a (2026-09-24): keep `defaultEnabled: false` (CX-51, critique P9); S11-W3-4 enables firecrawl through the cloud setup script.
- Files: create `$FC/skills/firecrawl/references/vendor-onboarding-2026-09-24.md` (the W1-corrected `:19-338` content, moved verbatim); rewrite `$FC/skills/firecrawl/SKILL.md` per §2.2/§2.3 in full (the `alignment:intent-lock` handoff name is only valid once S10-W3-2 has landed — CX-16); edit `$FC/.claude-plugin/plugin.json` (add `$schema`; add `defaultEnabled: false`, OQ6-a); edit (not create — S10-W0-8 already backfills it, CX-45) `$FC/LICENSE`; edit `$FC/README.md` (install unchanged, note the split + `defaultEnabled: false`).
- Commands: `python3 -c "import yaml,re; t=open('plugins/firecrawl/skills/firecrawl/SKILL.md',encoding='utf-8').read(); m=re.match(r'^---\n(.*?)\n---\n',t,re.S); yaml.safe_load(m.group(1)); print('OK')"` ; `wc -c plugins/firecrawl/skills/firecrawl/SKILL.md`
- Done when: YAML check prints `OK`; body est. tokens (bytes/4 on the post-frontmatter text) ≤1,500.
- Rollback: `revert`.

**S09-W3-2 · micky · gridgeist metadata (UPSTREAM.md; drop Codex file + assets; README/CHANGELOG)**
- Depends on: S10-W0-8 (README/CHANGELOG backfill for gridgeist — CX-34/CX-36 tie this wave to the skeleton and W0 tooling landing first).
- Files: create `$GG/UPSTREAM.md` (contents below); delete `$GG/skills/gridgeist/agents/openai.yaml`, `$GG/skills/gridgeist/assets/` (all 3 files); edit (not create — S10-W0-8 already backfills both, CX-45) `$GG/README.md`, `$GG/CHANGELOG.md` (add the metadata-only change entry on top of S10-W0-8's `## 0.1.0 — vendored` backfill). `$GG/skills/gridgeist/SKILL.md` and its two `references/*` files are **not edited**.
  ```markdown
  # Upstream

  - Repository: https://github.com/ohmiler/gridgeist
  - License: MIT (kept at `LICENSE`, unchanged)
  - Vendored into this marketplace: 2026-07-15 (commit `f4fc446`, this repo)
  - Best-match upstream commit by timestamp (NOT diff-verified — OWNER action below):
    `31813b49` (2026-07-14T20:58:15Z, "test: record Gridgeist evaluation runs")
  - To refresh: diff `skills/gridgeist/` against the upstream repo at HEAD, note any
    upstream changes in CHANGELOG.md, and update the commit line above.
  ```
- Commands: `test -f plugins/gridgeist/UPSTREAM.md` ; `test ! -f plugins/gridgeist/skills/gridgeist/agents/openai.yaml` ; `test ! -d plugins/gridgeist/skills/gridgeist/assets`
- Done when: all three commands succeed.
- Rollback: `revert`.

**S09-W3-3 · micky · eval conversion (both plugins)**
- Depends on: S09-W3-1, S09-W3-2.
- Files: create the 6+3 case dirs in §4.1 in full (the 3 firecrawl dirs S09-W0-1 seeded are extended, not duplicated; S10-W3-2 leaves plugin-root `evals/` in place for non-family plugins); delete `$FC/skills/firecrawl/evals/evals.json`.
- Commands: `find plugins/firecrawl plugins/gridgeist -iname 'evals.json'` (expect empty)
- Done when: empty.
- Rollback: `revert`.

**S09-W3-4 · micky · release both plugins**
- Depends on: S09-W3-1 … S09-W3-3.
- Commands: `python3 plugins/plugin-creator/scripts/release.py firecrawl minor --write` (once S08's W3 lands `release.py`; else `python3 scripts/bump.py firecrawl minor --write`, CX-12) ; same for `gridgeist patch` (metadata-only = patch, no behavior change to the skill).
- Files: both plugins' `plugin.json` + `CHANGELOG.md`.
- Done when: `$VALIDATE --repo .` (CX-11 — `python3 plugins/plugin-creator/scripts/validate.py --repo .`, live by W3) prints `all checks passed` for both; `marketplace.json` has no `version` for either entry. Per S11's I16 item 4 template: "Ready for cloud delivery: HIGH defects due by this wave closed (H12, closed at W1); handoffs carry the §4.2 fallback or target an enabled plugin; no same-named unit elsewhere; smoke suite passed (<result path>)."
- Rollback: `revert`.

### W5

**S09-W5-1 · OWNER · gridgeist usage decision (OD10)**
- Depends on: 2-4 weeks of use after W3 (architecture §10 W5).
- Actions: run `/skill-doctor` + `/doctor`; if gridgeist has fired rarely or never, flip
  `disable-model-invocation: true` on `$GG/skills/gridgeist/SKILL.md` (user-only) — the one
  frontmatter edit this spec permits deferring past W3 — else leave it model-invocable.
- Done when: the decision and its evidence (fire count from `/skill-doctor`) are recorded in
  `$GG/CHANGELOG.md` (CX-27 — `delivery-log.md`'s grammar accepts only variable rows; a usage
  note belongs in the plugin's own CHANGELOG, not there).
- Rollback: revert the dmi flip.

## 4. Evals

### 4.1 Cases

**`firecrawl` case 1, `trigger-known-url` (trigger positive):**

`evals/firecrawl/trigger-known-url/prompt.md`
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, smoke]
---

Scrape https://stripe.com/pricing into clean markdown for me.
```
`evals/firecrawl/trigger-known-url/graders/skill-fired.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?firecrawl"'
weight: 2
---
```
`evals/firecrawl/trigger-known-url/graders/path-a-not-browser.md`
```markdown
---
type: regex
target: last_message
pattern: '(scrape|Path A)'
flags: i
---
```

**`firecrawl` case 2, `negative-biomedical` (near-miss negative):**

`evals/firecrawl/negative-biomedical/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

Search the web for the evidence on sertraline versus escitalopram for panic disorder.
```
`evals/firecrawl/negative-biomedical/graders/no-firecrawl.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?firecrawl"'
min: 0
max: 0
arm: both
---
```

**`firecrawl` case 3, `deliverable-gated` (output/process — closes the Path C intent-lock check):**

`evals/firecrawl/deliverable-gated/prompt.md`
```markdown
---
max_turns: 20
allowed_tools: [Read, Glob, Grep, Skill]
tags: [output]
---

Use firecrawl to build me a competitive intel brief on the top teletherapy platforms.
```
`evals/firecrawl/deliverable-gated/graders/intent-lock-before-brief.md`
```markdown
---
type: tool_order
before: { tool: Skill, input_match: "intent-lock" }
after: { tool: Skill, input_match: "firecrawl" }
weight: 2
---
```
`evals/firecrawl/deliverable-gated/graders/optional-fallback-present.md`
```markdown
---
type: regex
target: last_message
pattern: 'OPTIONAL'
match: not_contains
---
```

**`gridgeist` case 1, `trigger-redesign` (trigger positive):**

`evals/gridgeist/trigger-redesign/prompt.md`
```markdown
---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
tags: [trigger, smoke]
---

This landing page looks like every other generic SaaS site. Redesign it with a stronger,
more distinctive grid.
```
`evals/gridgeist/trigger-redesign/graders/skill-fired.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?gridgeist"'
weight: 2
---
```

**`gridgeist` case 2, `negative-dataviz` (near-miss negative — dataviz is a different skill for charts of the user's OWN data):**

`evals/gridgeist/negative-dataviz/prompt.md`
```markdown
---
max_turns: 8
allowed_tools: [Read, Glob, Grep, Skill]
tags: [negative]
---

Chart my quarterly revenue by region as a stacked bar chart.
```
`evals/gridgeist/negative-dataviz/graders/no-gridgeist.md`
```markdown
---
type: tool_used
tool: Skill
input_match: '"skill"\s*:\s*"(?:[\w-]+:)?gridgeist"'
min: 0
max: 0
arm: both
---
```

**`gridgeist` case 3, `review-output` (output/process):**

`evals/gridgeist/review-output/prompt.md`
```markdown
---
max_turns: 15
allowed_tools: [Read, Glob, Grep, Skill]
tags: [output]
---

Review this dashboard's UI and tell me what's wrong with it before you touch anything.
```
`evals/gridgeist/review-output/graders/verdict-first.md`
```markdown
---
type: regex
target: last_message
pattern: '(Verdict|verdict)'
---
```

### 4.2 Conversion

| old evals.json case | new case dir | dropped (reason) |
|---|---|---|
| firecrawl id 1 `positive-trigger-scrape-known-url` | `trigger-known-url` | — |
| firecrawl id 3 `negative-trigger-biomedical-literature` | `negative-biomedical` | — |
| firecrawl id 2 `positive-trigger-deliverable-gated-by-intent-lock` | `deliverable-gated` | — |
| firecrawl ids 4,5,6,7,8 | — | dropped; folded into the 3 kept cases or superseded by the corrected W1 content (id 6 locked the now-fixed keyless scope, closing -10) |
| — (gridgeist has none) | 3 new cases | n/a |

### 4.3 Live triggers

Neither skill is in one of architecture §6.3's five contested families. Routing-smoke
near-misses:

1. "search the web for X" (biomedical) → `pubmed-research-note`/`comprehensive-review`, not `firecrawl`
2. "redesign this dashboard" → `gridgeist`, not `dataviz` or `clinical-infographic`
3. "make me a chart of my study's effect sizes" → `dataviz` (or `pubmed-research-note`'s own report), not `gridgeist`
4. "scrape this page" (a general request, no biomedical framing) → `firecrawl`

### 4.4 Commands

- Smoke: `bash scripts/eval.sh --smoke firecrawl` and `bash scripts/eval.sh --smoke gridgeist` (S12, I17) — smoke-tagged cases, free graders, `--ablation none --runs 1`.
- Release: `bash scripts/eval.sh --release firecrawl` / `--release gridgeist` — two arms, `--runs 1 --threshold 0.8` (OQ11-a).

## 5. Acceptance criteria

1. `python3 scripts/validate.py` exits 0 for both plugins (pre-W3); `$VALIDATE --repo .` (= `python3 plugins/plugin-creator/scripts/validate.py --repo .`, CX-11) exits 0 post-W3.
2. `grep -c "fetched: 2026-09-24" plugins/firecrawl/skills/firecrawl/SKILL.md` (pre-split) or `.../references/vendor-onboarding-2026-09-24.md` (post-split) prints `1`.
3. `grep -c "FIRECRAWL_API_KEY.*>> .env\|>> \.env" plugins/firecrawl/skills/firecrawl/SKILL.md plugins/firecrawl/skills/firecrawl/references/*.md` prints `0`.
4. `wc -c plugins/firecrawl/skills/firecrawl/SKILL.md` (post-split, body only) is under the 1,500-tok target (≤~6,000 chars incl. frontmatter).
5. `grep -c '"defaultEnabled": false' plugins/firecrawl/.claude-plugin/plugin.json` prints `1`.
6. `test -f plugins/gridgeist/UPSTREAM.md -a ! -f plugins/gridgeist/skills/gridgeist/agents/openai.yaml -a ! -d plugins/gridgeist/skills/gridgeist/assets`.
7. `diff <(git show HEAD~N:plugins/gridgeist/skills/gridgeist/SKILL.md) plugins/gridgeist/skills/gridgeist/SKILL.md` is empty (content verbatim; `N` = commits since the pre-rewrite tag).
8. `find plugins/firecrawl plugins/gridgeist -iname 'evals.json'` is empty.
9. `bash scripts/eval.sh --smoke firecrawl` and `--smoke gridgeist` score ≥ the `pre-rewrite` baseline.

## 6. Trigger lock

| phrase | source | kept / moved / removed (reason) |
|---|---|---|
| "firecrawl", "scrape this page/site/URL", "crawl these docs", "map a site" | firecrawl | kept |
| "search the web" | firecrawl | narrowed → "search the general web" (closes -9's precision half, R4) |
| "redesign this page", "make this UI less generic", "review this interface", "needs a stronger grid", "Swiss style", "editorial layout" | gridgeist | kept, unchanged (skill not rewritten) |

Net: 1 phrase narrowed, 0 removed, 0 added. No phrase moves skills.

## 7. Risks and OD sensitivity

- The firecrawl split (W3) risks losing a trigger phrase or a fetch-only-contract word in the
  move to `references/`. Mitigation: `references/vendor-onboarding-<date>.md` is a byte-move
  of the corrected W1 content, not a rewrite; §6's trigger lock covers only the frontmatter
  description, which is rewritten but diffed phrase-by-phrase above.
- OD12 (assumed a — slim router kept): under OD12-b (retire firecrawl entirely), this spec's
  W3 work is replaced by `renames: {firecrawl: null}` plus moving the fetch recipe into
  `evidence/engines.md` alone (already there per I05, owner S03) — the vendor's own skill/CLI
  distribution becomes the sole general-web path, and this spec's W1/W3/W5 steps are dropped.
- OD10 (gridgeist, resolved at W5 by usage — not sensitive to any earlier OD): a low-usage
  verdict only flips one frontmatter key (§3 S09-W5-1); no other file changes.
- The "ask → doctor" uncertainty (§1.4) risks a stale Gotchas line if the digest's claim was
  right and this session's verification missed it (WebFetch summarization limits). Low
  severity: the router's Gotchas note flags it as unconfirmed rather than asserting either way.

## 8. Open questions

1. **ASSUMES / to-verify:** the digest's `ask` → `doctor` vendor rename (INV firecrawl-1,
   fetched 2026-09-23) could not be confirmed by two targeted `WebFetch` calls to the same
   page today (2026-09-24), which found no "doctor" command and no "firecrawl-ask" CLI command
   (only a `/support/ask` REST endpoint, matching today's SKILL.md). `WebFetch` runs a small
   summarizing model and may drop content on a long page. **Settled by:** a full-text fetch
   or the CLI's own `--help`/`firecrawl-cli` package README before this line ships in the
   router's Gotchas section — if still unconfirmed, keep the router's `firecrawl-ask`
   reference (matches today's behavior and the live `/support/ask` endpoint either way).
2. **CLOSED** (I01, S01; was an ASSUMES): S09-W3-1 now explicitly depends on S10-W3-2, so the
   `alignment:intent-lock` segment is only ever written once the skeleton PR has landed
   (CX-16/CX-34/CX-36) — no ordering ambiguity remains.
3. **NEW, not in the assigned defect list:** gridgeist-4 (marketplace entry description is
   thinner than the skill's) is I24's territory (owner S10) — recorded here for S10 to pick up
   rather than fixed in this spec, since S09 does not own marketplace.json entry content.
4. **CLOSED (CX-12; moot under OQ12-a, which drops S09-W1-2).** S09-W1-2 runs after S10's W0 tooling and uses `bump.py --write`. Original question: whether S09-W1-2 should wait for S10's W0 `bump.py` rewrite (dry-run-by-default) or use
   today's `bump.py` as-is. Assumed: today's tool at W1 (same reasoning as S08-W1-2's
   equivalent open question).
5. **ARCH-CONFLICT:** none found. The upstream gridgeist commit SHA recorded in `UPSTREAM.md`
   (§3, S09-W3-2) is a timestamp best-match, not diff-verified — this is weaker evidence than
   "the sha," and is flagged as an owner action inside the file itself rather than asserted as
   fact.
6. **CLOSED (OQ6-a, 2026-09-24)** (CX-51, critique P9): firecrawl keeps `defaultEnabled: false`
   (S09-W3-1, OD12-a, rubric R30 for an external-service plugin), and S11-W3-4 adds a cloud
   setup-script enable block plus `claude plugin enable firecrawl@inline` on Windows, because a
   multi-repo session keeps no user settings (S11 ARCH-CONFLICT 1).
