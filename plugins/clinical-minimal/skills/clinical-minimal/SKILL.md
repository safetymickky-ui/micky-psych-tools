---
name: clinical-minimal
description: >-
  The user's personal design system ("Clinical Minimal") for every Word, PowerPoint and Excel file Claude makes for them. Use whenever the user asks for a .docx, .pptx or .xlsx, or for a document, report, handout, summary, letter, memo, slide deck, presentation, lecture, journal club, spreadsheet, tracker, budget or model, in English or Thai ("ทำเอกสาร", "ทำสไลด์", "ทำ Excel", "ทำรายงาน", "ทำ presentation"). Also use when another skill (docx, pptx, xlsx, comprehensive-review, deep-stock-research, company-valuation, etc.) is about to produce an Office file: this skill decides how it looks; that skill decides what it says. Not for web pages, apps or Markdown-only notes.
---

# Clinical Minimal

White page, one clinical teal accent, Leelawadee UI, structure from rules and space. Every Office file for this user follows it. No personal name, logo or branding goes on files.

- Brand book and live specimens: https://claude.ai/artifact/KajoGXvYsTqqxyVZpPgqk8 (Design System artifact; read `project/README.md` there for the full rules)
- Project folder with `DESIGN.md` and worked examples (author's PC, if present): `C:\Users\User\Design system\`
- `SKILL_DIR` below means this skill's folder: the "Base directory for this skill" shown when it loads.
- Helpers: `cm.py` in `SKILL_DIR`. Render check: `render.ps1` (docx/xlsx → PDF), `slidecheck.py` (decks, per slide). Picture selection: `imgpick.py`.
- Reference deck using every slide feature (author's PC, if present): `C:\Users\User\Design system\output\lithium_journal_club.py`

## User preferences (from their feedback — these win over defaults)

1. **English by default** for every file, even when the request is typed in Thai. Use Thai only when the user asks for it.
2. **Decks are visual.** Every content slide carries a visual: chart, diagram, table, timeline, forest plot, KPI tiles, numbered cards or a picture. A slide that is only a bullet list is a defect; convert it (`numbered_cards` at minimum).
3. **Motion.** Every deck gets fade transitions (`finish_deck`) and click-by-click builds on content slides (`animate`), so the presenter reveals one idea at a time.
4. **Pictures from the web.** Title and section slides carry a large related picture; add pictures to content slides where they help. Source them from Google Images through the selection algorithm below; relevance is judged on the picture as placed. The user's use is personal and non-commercial: credit every picture's source site on the slide and list all sources on the References slide.
5. **Big title and section slides.** Title 48pt on a teal panel beside a full-height picture; section dividers 48pt beside a half-slide picture.
6. **Verified, relevant output.** Every slide passes `slidecheck.py` plus a full-size visual review, and every picture passes `imgpick.py` (specific subject, clean, fills its box). Bad renders and off-topic pictures were the complaint that created these tools.

## Workflow

1. **Pick the template from the topic** (table below). If the user named a format, use it; otherwise choose the one the topic row says.
2. **Verify facts first.** Medical content: pull numbers from PubMed abstracts (or the source the user gave), never from memory; every figure gets a source line.
3. **Get pictures** (decks, and documents if the user asks) with the selection algorithm in "Pictures" below. Never place a picture that has not passed `imgpick.py choose`.
4. **Build** with `cm.py`. Never hand-style what a helper already does. Write the deck as one script beside the output (like the reference deck) so edits are a re-run.
5. **Verify every slide** (decks): see "Slide verification" below. The deck is not done until `slidecheck.py` exits 0: no FAIL and every slide marked pass on its current layout. Word/Excel: run `render.ps1`, Read the PDF, fix overflow and clipped tables.
6. **Deliver** the file path and mention anything assumed or unverified in one line. Leave the `_check/` and `img/_cand/` folders out of what you hand over (they are working files).

```python
import sys; sys.path.insert(0, r"<SKILL_DIR>")  # the Base directory shown when this skill loads
import cm
```

```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "<SKILL_DIR>/render.ps1" out.docx out.pptx out.xlsx
```

Needs `python-docx`, `python-pptx`, `openpyxl`, `pillow` (`pip install python-docx python-pptx openpyxl pillow`). Rendering needs Microsoft Office on this PC.

## Topic → template

| Topic | Format | Skeleton |
| --- | --- | --- |
| Case summary | docx | ID & CC · HPI · Past/Family/Social · MSE · Formulation (bio-psycho-social) · Diagnosis & DDx · Management plan · Key point callout |
| Evidence / topic review | docx | Summary · Question (PICO) · Search · Evidence table · Synthesis · Clinical bottom line · References |
| Lecture, journal club, teaching | pptx | Title (picture) · Roadmap diagram · History timeline · one section per question, each opening with a picture divider · Take-home cards · Discussion cards · References + image credits |
| Drug comparison | docx table or xlsx | One row per drug: mechanism, dose, efficacy, key adverse effects, monitoring, cost |
| Stock one-pager | docx | Verdict line · Business · Moat · Financials table · Valuation · Risks · Sell triggers |
| Valuation model | xlsx | Summary · Inputs · Financials · DCF · Multiples · Sensitivity |
| Investment pitch | pptx | Title (picture) · Thesis in one line · KPI slide · 3–4 evidence slides (charts) · Risks · Decision |
| Budget, tracker, log | xlsx | Summary · Monthly · Categories · Log |
| Plan, schedule | xlsx or docx | Goal · Milestones table (date, owner, status chip) · Notes |
| Letter, memo | docx | `new_document(title, meta, rule=False)` · Date · To · Subject · Body · Sign-off |

## Which visual for which content (decks)

| Content | Visual | Helper |
| --- | --- | --- |
| Several effect sizes with CIs | Forest plot (log scale) | `forest_plot` |
| Ranking or comparison of values | Bar chart, subject bar teal, others gray | `chart_slide(kind="hbar")` + point colours |
| Trend over time | Line chart | `chart_slide(kind="line")` |
| Trial arms / events | Column chart + HR table side by side | `add_chart` + `add_table` |
| Mechanism, pathway, cause → effect | Box-and-arrow diagram | `box`, `arrow` |
| Decision rule, algorithm | Flowchart | `box`, `arrow` |
| History, schedule, monitoring plan | Timeline | `timeline` |
| Ranges, thresholds, therapeutic window | Zoned range bar | `range_bar` |
| 3–4 headline numbers | KPI tiles | `kpi_slide` or `rect` + `text` |
| Severity levels | Staircase of tinted boxes | `box` |
| Key messages, questions | Numbered cards | `numbered_cards` |
| Reference numbers | Table | `table_slide` / `add_table` |

## Pictures: selection algorithm (`imgpick.py`)

Irrelevant pictures come from vague queries and from judging thumbnails instead of the picture as placed. So every picture goes through brief → search → filter → score → judge → choose.

1. **Brief.** Write `img/brief.json` beside the deck, one slot per picture (format in the `imgpick.py` docstring). For each slot set:
   - `subject`: what must be **visible**, concretely and specific to that slide ("course of bipolar disorder: manic and depressive episodes over time"), never the section word ("Efficacy").
   - `must` / `any` / `avoid` terms. Put known traps in `avoid`: supplements for a prescribed drug (`orotate`), look-alike products (`heparin` tubes for a lithium level), off-focus anatomy (`arterial`), `battery`.
   - `kind`: `photo` (cropped to fill) or `diagram` (shown whole, `fit=True`). `box`: placed size in inches (title picture 7.33 × 7.5, section photo 6.67 × 7.5, section diagram 6.07 × 6.7).
2. **Search.** In the built-in browser run at least two queries per slot on `https://www.google.com/search?tbm=isch&q=<query>` (one batch of navigate + javascript calls for all slots). Extract up to 12 results per query with `javascript_tool`:
   ```js
   const h=document.documentElement.innerHTML;const re=/\["(https?:\/\/(?!encrypted-tbn)[^"]+?)",(\d+),(\d+)\],null,0,"[^"]*",null,0,\{"2000":\[null,"([^"]*)"[^\]]*\][\s\S]{0,200}?"2003":\[null,"[^"]*","([^"]*)","([^"]*)"/g;const o=[];const s=new Set();let m;while((m=re.exec(h))&&o.length<12){const u=m[1].replace(/\\u003d/g,'=').replace(/\\u0026/g,'&');if(s.has(u))continue;s.add(u);o.push([u,+m[3],+m[2],m[6].slice(0,60),m[5].split('?')[0].slice(0,90),m[4]])}JSON.stringify(o)
   ```
   Rows are `[url, width, height, page title, page url, domain]`; paste them into the slot's `candidates`. If Google shows a CAPTCHA or consent wall, stop and tell the user; never bypass it.
3. **Filter and score** (automatic): `python <SKILL_DIR>/imgpick.py fetch img/brief.json [slot]`. It rejects stock/social sites, `avoid` terms, anything under 90 ppi at the placed size, failed downloads and near-duplicates. It scores the rest on text relevance, source trust (official and medical-education sites high, shops and product pages low), resolution, crop loss, sharpness and **fill** (share of the placed box that is not flat background). It writes `img/_cand/<slot>/sheet.png` showing the top 8 **exactly as they will sit in the box**.
4. **Judge** (you, visually): Read each sheet. Score each candidate on subject 0–3, clean 0–2 and crop 0–2 with the rubric in the `imgpick.py` docstring, then `python <SKILL_DIR>/imgpick.py judge img/brief.json <slot> "3=3,1,2 5=2,2,2 1=0"`. Be strict:
   - subject 3 only if it shows this slide's specific subject; generic pills, labs, brains or mental-health art are 1;
   - clean 0 for brand packaging as the subject, ad copy, watermarks, or paragraphs of text that can't be read at the placed size;
   - crop 0 for a subject that is cut off or small in a big empty field (fill under ~25%).
5. **Choose**: `python <SKILL_DIR>/imgpick.py choose img/brief.json`. A winner needs subject ≥ 2, clean ≥ 1 and crop ≥ 1. The final score is 35% automatic + 65% your judgement. It copies winners to `img/<slot>.jpg|png` and records url, page, site, scores and a ready `credit` in `img/sources.json`.
6. **No winner:** search again with more specific queries, or switch the slot's `kind` (a good diagram cropped as a photo fails on crop), then `fetch` that slot again. After two failed rounds, give the slide a drawn diagram instead of a picture.
7. **Place** with `cm.picture` (photo) or `cm.picture_fit` / `section_slide(..., fit=True)` (diagram). Credit each one on the slide with `cm.credit(slide, "Image: <site>", …)` (short site name, one line). List every source on the References slide under "Images (personal, non-commercial teaching use)".

## Slide verification (`slidecheck.py`)

Every deck, every slide, before delivery:

1. `python <SKILL_DIR>/slidecheck.py deck.pptx`. PowerPoint itself lays the deck out (`slideprobe.ps1`), so line breaks, text bounds and table heights are real, not estimated.
   - **FAIL:** text overflowing its box or the slide, a word broken across lines, a content title wrapping, text colliding with text, a footer or source line on two lines, a picture under 72 ppi or stretched, a picture without a credit, a content slide with no visual.
   - **WARN:** display title over 3 lines, a one-word last line, labels under 12pt, text on a picture/chart/table, a line through text, a picture under 110 ppi, over half the content area empty, no builds, no transition.

   Output goes to `<deck dir>/_check/<deck>/`: `slide-NN.png`, `slide-NN.flag.png` (issues boxed and numbered), `sheet.png`, `report.md`.
2. **Fix every FAIL** in the deck script, rebuild, re-run. Treat WARNs as fix-unless-deliberate.
3. **Visual pass, one slide at a time:** Read each `slide-NN.png` at full size (not only the contact sheet) and check the six points printed by the script:
   - clipping and collisions;
   - readability, including labels inside pictures;
   - picture relevance and crop;
   - balance and empty space;
   - that the visual proves the title;
   - consistency with neighbouring slides.
4. Record it: `python <SKILL_DIR>/slidecheck.py deck.pptx --mark 2-10,12 pass` or `--mark 11 fix "arrowheads pile up"`. Fix and re-run. A mark is tied to the slide's current layout, so any change to a slide re-opens its review.
5. Done when the script exits 0 (no FAIL, every slide pass). Rules the check keeps catching:
   - source lines fit one line (use short author–year and put full references on the References slide);
   - 48pt display titles need every word to fit the 5-inch panel;
   - notes under diagrams need their full height.

## Helper API (cm.py)

**Word** — `doc = cm.new_document(title, meta)` sets A4, 2cm margins, every style, the title, meta line, teal rule and footer (title · n / N). Then `cm.h1/h2/h3(doc, text)`, `cm.para(doc, text, bold_lead="")`, `cm.bullets(doc, items, numbered=False)`, `cm.callout(doc, text, "key"|"caution"|"evidence")`, `cm.table(doc, header, rows, numeric=(col idx…), total=False, widths_cm=None)`, `cm.source(doc, text)`, `doc.save(path)`. Number H1s yourself ("1. Summary").

**PowerPoint: slides** — `prs = cm.new_deck()` (16:9, inches, content area x 0.5–12.83, y 1.6–6.6).
- `cm.title_slide(prs, title, subtitle, date, image=path, credit_text="Image: site")`
- `cm.section_slide(prs, title, "01", image=path, kicker="one line", credit_text=..., fit=False)`
- `cm.content_slide(prs, takeaway_title, bullets=None, source)` → slide with `.body`
- `cm.kpi_slide(prs, title, [(value, label, delta, "pos"|"neg"|None)], source)` → `.tiles` (one shape list per tile)
- `cm.table_slide(prs, title, header, rows, numeric=(…), source)` → `.table`; `cm.add_table(slide, x, y, w, header, rows, numeric, col_widths, size, row_h)` anywhere
- `cm.chart_slide(prs, title, categories, {series: values}, kind="bar"|"hbar"|"line"|"stacked", source, number_format)` → `.chart`; `cm.style_chart(chart, …)` for charts you add yourself

**PowerPoint: visuals** — `cm.picture`, `cm.picture_fit`, `cm.credit`, `cm.box(slide, x, y, w, h, text_or_lines, fill, color, size, bold, align)`, `cm.arrow(x1, y1, x2, y2)`, `cm.line`, `cm.forest_plot(slide, [(label, est, lo, hi)], …)`, `cm.range_bar(slide, [(start, end, label, fill, text_colour)], vmin, vmax, ticks, unit)`, `cm.timeline(slide, [(when, head, detail)], head_lines=1)`, `cm.numbered_cards(slide, items)`, `cm.text`, `cm.rect`. Diagram helpers return one shape list per element, ready for `animate`. Use `cm.new_shapes(slide, since)` to group shapes you add by hand.

**PowerPoint: motion** — `cm.animate(slide, steps, effect="fade"|"wipe"|"rise")`: each step is a shape, a list of shapes, or `(shape, paragraph_index)`; one step per click. `cm.bullets_steps(slide.body)` reveals bullets one by one. Call `animate` once per slide, after the slide's shapes exist. `cm.finish_deck(prs)` right before `prs.save()` adds the fade transition to every slide. Use `wipe` for bars, forest rows, timelines and range bars; `fade` for everything else. Title and section slides: no builds.

**Excel** — `wb = cm.new_workbook()` (first sheet "Summary"). `row = cm.sheet_header(ws, title, note, headers, widths, numeric=(…))` gives title band, header row, freeze at B4, no gridlines, landscape fit-to-width. `cm.write_rows(ws, rows, row, formats={col: "int"|"num"|"pct"|"x"|"date"|"thb"|"delta_pct"|"delta_num"|"text"}, inputs=(cols…))`, `cm.total_row(ws, row, "Total", values, formats)`, `cm.delta_colors(ws, "F4:F20")`, `cm.xl_chart(ws, "H3", data_ref, cats_ref, kind="bar"|"line", y_format)`. Formulas as strings (`"=B4*D4"`); never hard-code a computed number.

**Tokens** — `cm.C[...]` colours (hex without #), `cm.DATA` series colours in order, `cm.FONT`, `cm.MONO`, `cm.delta_text(v)` → "▲ 6.9%".

## Rules that are easy to break

- **Titles fit on one line** (about 55 characters at 28pt). A title that wraps pushes into the body; shorten it, don't shrink it.
- **Thai text** (when asked for): set the font in the complex-script slot too (the helpers do). Runs you create by hand go through `cm._run` (docx) or `cm._pfont` (pptx).
- **Colour:** white `surface`; text `ink`, `ink_muted`, `ink_subtle`. `teal_600` is the accent; accent text uses `teal_700`; tint backgrounds `teal_50` / `surface_alt`; warnings `warning_bg`; danger `negative_bg`.
- **Direction is never colour alone:** gains ▲ and `positive`, losses ▼ and `negative`. Use ▲/▼ only for true better/worse or up/down.
- **Charts:** `DATA[0]` teal is always the subject, `DATA[5]` gray is other/benchmark. Flat 2D, horizontal hairline gridlines, no border, data labels on bars, max six series.
- **Text size:** body text on slides 18pt or larger; diagram labels, table cells and chart labels 12pt or larger; only source lines and image credits go smaller (9–10pt).
- **Slides:** title is the takeaway sentence; one idea per slide; source bottom-left; page number bottom-right. No clip-art, emoji, stock watermarks or gratuitous effects (no spins, bounces, flying text).
- **Documents:** open with a 3–5 line summary; ≤ 2 callouts per page; every figure has a source line; no text boxes or page borders.
- **Sheets:** Summary sheet first; inputs `teal_700` on `surface_alt`, formulas `ink`; numbers right-aligned in Consolas with fixed formats; no merged cells in data ranges.
- **Voice:** conclusion first, sentence case, exact numbers with units, no emoji, no exclamation marks.

## Changing the system

This skill ships as the `clinical-minimal` plugin in the `micky-psych-tools` marketplace
(github.com/safetymickky-ui/micky-psych-tools). Edit it in a clone of that repo, never the installed copy in
the plugin cache; follow the repo's CLAUDE.md (validate, `scripts/route.py`, `scripts/bump.py`, never
hand-edit versions), then `claude plugin marketplace update micky-psych-tools` and
`claude plugin update clinical-minimal@micky-psych-tools`.

The artifact's `tokens.json` is the source of truth for colours, fonts and rules. When the user changes one:
update the artifact (read, edit, republish), then mirror it in `cm.py` `C`/`DATA`/`FONT`, `DESIGN.md` in the
project folder, and this file. When the user gives feedback on a deliverable that should apply to future work,
add it under "User preferences" above.
