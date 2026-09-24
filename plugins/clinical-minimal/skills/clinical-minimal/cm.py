"""Clinical Minimal — build .docx / .pptx / .xlsx on the personal design system.

Usage (from any folder):
    import sys; sys.path.insert(0, r"<this skill's folder>")
    import cm

Source of truth for every value here: tokens.json in the Design System artifact
(https://claude.ai/artifact/KajoGXvYsTqqxyVZpPgqk8); human summary in C:/Users/User/Design system/DESIGN.md.
"""
from __future__ import annotations

from pathlib import Path

# ---------------------------------------------------------------- tokens
C = {
    "surface": "FFFFFF", "surface_alt": "F5F7F8", "surface_sunken": "ECEFF2",
    "hairline": "D5DBE0", "hairline_strong": "8A949E",
    "ink": "1B232B", "ink_muted": "4A5561", "ink_subtle": "636E7A",
    "teal_700": "0B6A73", "teal_600": "0E7C86", "teal_100": "CDE7EA", "teal_50": "E8F4F5",
    "on_accent": "FFFFFF",
    "positive": "1E7B45", "positive_bg": "E7F3EC",
    "negative": "B42318", "negative_bg": "FBEAE8",
    "warning": "A15C07", "warning_bg": "FBF1E1",
}
DATA = ["0E7C86", "3E5C9A", "D08C2E", "B5475B", "6B8F71", "8A949E"]  # data-1 … data-6
FONT = "Leelawadee UI"  # Thai + Latin, ships with Windows and Office
MONO = "Consolas"

CALLOUT = {  # kind: (label, background, label colour)
    "key": ("KEY POINT", C["teal_50"], C["teal_700"]),
    "caution": ("! CAUTION", C["warning_bg"], C["warning"]),
    "evidence": ("EVIDENCE", C["surface_alt"], C["ink_muted"]),
}


def delta_text(value: float, fmt: str = "{:.1f}%") -> str:
    """Signed value with its direction glyph: ▲ 6.9% / ▼ 4.4%. Colour alone never carries direction."""
    return ("▲ " if value >= 0 else "▼ ") + fmt.format(abs(value))


# ================================================================ DOCX
def _docx():
    import docx  # noqa: F401  (import on demand so pptx-only work needs no python-docx)
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
    return docx, WD_TABLE_ALIGNMENT, WD_ALIGN_PARAGRAPH, OxmlElement, qn, Cm, Pt, RGBColor


def _rpr_fonts(rpr, font: str, size_pt: float | None = None):
    """Set Latin, East-Asian and complex-script (Thai) slots, plus the Thai size, on a w:rPr."""
    _, _, _, OxmlElement, qn, *_ = _docx()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.insert(0, rfonts)
    for slot in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
        rfonts.set(qn(slot), font)
    for theme in ("w:asciiTheme", "w:hAnsiTheme", "w:eastAsiaTheme", "w:cstheme"):
        rfonts.attrib.pop(qn(theme), None)  # theme fonts (Heading styles) would override the names
    if size_pt is not None:
        szcs = rpr.find(qn("w:szCs"))
        if szcs is None:
            szcs = OxmlElement("w:szCs")
            rpr.append(szcs)
        szcs.set(qn("w:val"), str(int(size_pt * 2)))
    lang = rpr.find(qn("w:lang"))
    if lang is None:
        lang = OxmlElement("w:lang")
        rpr.append(lang)
    lang.set(qn("w:bidi"), "th-TH")


def _style(doc, name, size, bold=False, color="ink", before=0, after=6, font=FONT, line=1.15):
    *_, Pt, RGBColor = _docx()
    st = doc.styles[name]
    st.font.name = font
    st.font.size = Pt(size)
    st.font.bold = bold
    st.font.italic = False
    st.font.color.rgb = RGBColor.from_string(C[color])
    _rpr_fonts(st.element.get_or_add_rPr(), font, size)
    pf = st.paragraph_format
    pf.space_before, pf.space_after, pf.line_spacing = Pt(before), Pt(after), line
    return st


def _border(el, side: str, color: str, eighths: int, tag="w:pBdr"):
    """Add one border line (size in eighths of a point) to a paragraph (w:pPr) or cell (w:tcPr)."""
    _, _, _, OxmlElement, qn, *_ = _docx()
    box = el.find(qn(tag))
    if box is None:
        box = OxmlElement(tag)
        el.append(box)
    b = OxmlElement(f"w:{side}")
    b.set(qn("w:val"), "single"); b.set(qn("w:sz"), str(eighths))
    b.set(qn("w:space"), "4" if tag == "w:pBdr" else "0"); b.set(qn("w:color"), color)
    box.append(b)
    shd = el.find(qn("w:shd"))
    if tag == "w:tcBorders" and shd is not None:
        shd.addprevious(box)  # schema order: tcBorders before shd


def _shade(cell, fill: str):
    _, _, _, OxmlElement, qn, *_ = _docx()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear"); shd.set(qn("w:color"), "auto"); shd.set(qn("w:fill"), fill)
    cell._tc.get_or_add_tcPr().append(shd)


def _run(par, text, size=None, bold=None, color=None, font=FONT):
    *_, Pt, RGBColor = _docx()
    r = par.add_run(text)
    r.font.name = font
    if size: r.font.size = Pt(size)
    if bold is not None: r.font.bold = bold
    if color: r.font.color.rgb = RGBColor.from_string(C.get(color, color))
    _rpr_fonts(r._element.get_or_add_rPr(), font, size)
    return r


def _field(par, instr: str, size=9, color="ink_subtle"):
    """Insert a Word field (PAGE, NUMPAGES) as a run."""
    _, _, _, OxmlElement, qn, *_ = _docx()
    r = _run(par, "", size=size, color=color)
    for kind, text in (("begin", None), (None, instr), ("separate", None), (None, "1"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar"); el.set(qn("w:fldCharType"), kind)
        elif text == instr:
            el = OxmlElement("w:instrText"); el.set(qn("xml:space"), "preserve"); el.text = f" {instr} "
        else:
            el = OxmlElement("w:t"); el.text = text
        r._element.append(el)


def new_document(title: str, meta: str = "", rule: bool = True):
    """A4 document with every style set, the title, meta line, teal rule and footer. Letters: rule=False."""
    docx, _, WD_ALIGN, _, qn, Cm, Pt, _ = _docx()
    doc = docx.Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21), Cm(29.7)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Cm(2))
    _style(doc, "Normal", 11)
    _style(doc, "Title", 24, bold=True, after=2, line=1.0)
    _style(doc, "Heading 1", 18, bold=True, before=18, after=6)
    _style(doc, "Heading 2", 14, bold=True, color="teal_700", before=12, after=4)
    _style(doc, "Heading 3", 12, bold=True, before=9, after=3)
    _style(doc, "List Bullet", 11, after=3)
    _style(doc, "List Number", 11, after=3)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3"):
        ppr = doc.styles[name].element.get_or_add_pPr()
        for old in ppr.findall(qn("w:pBdr")):
            ppr.remove(old)  # the default Title style carries a blue bottom border
    p = doc.add_paragraph(style="Title"); p.add_run(title)
    if meta:
        _run(doc.add_paragraph(), meta, size=9, color="ink_muted").font.bold = False
    if rule:
        r = doc.add_paragraph()
        _border(r._p.get_or_add_pPr(), "bottom", C["teal_600"], 18)
        r.paragraph_format.space_after = Pt(12)
    # footer: title left, n / N right
    fppr = doc.styles["Footer"].element.get_or_add_pPr()
    for old in fppr.findall(qn("w:tabs")):
        fppr.remove(old)  # default center/right tabs would catch the 	 before ours
    fp = sec.footer.paragraphs[0]
    from docx.enum.text import WD_TAB_ALIGNMENT
    fp.paragraph_format.tab_stops.add_tab_stop(Cm(17), alignment=WD_TAB_ALIGNMENT.RIGHT)
    _run(fp, title, size=9, color="ink_subtle"); _run(fp, "\t", size=9)
    _field(fp, "PAGE"); _run(fp, " / ", size=9, color="ink_subtle"); _field(fp, "NUMPAGES")
    return doc


def h1(doc, text): return doc.add_heading(text, level=1)
def h2(doc, text): return doc.add_heading(text, level=2)
def h3(doc, text): return doc.add_heading(text, level=3)


def para(doc, text: str = "", bold_lead: str = ""):
    """Body paragraph; bold_lead prints a bold lead-in ("Plan: ") before the text."""
    p = doc.add_paragraph()
    if bold_lead: _run(p, bold_lead, bold=True)
    if text: _run(p, text)
    return p


def bullets(doc, items, numbered=False):
    for it in items:
        doc.add_paragraph(it, style="List Number" if numbered else "List Bullet")


def source(doc, text: str):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = docx_pt(2)
    _run(p, text, size=9, color="ink_subtle")
    return p


def docx_pt(v):
    return _docx()[6](v)


def callout(doc, text: str, kind: str = "key", label: str | None = None):
    """Key point / Caution / Evidence block: a one-cell tinted table with a small label."""
    _, _, _, _, qn, Cm, Pt, _ = _docx()
    lab, fill, lab_color = CALLOUT[kind]
    t = doc.add_table(rows=1, cols=1)
    cell = t.cell(0, 0)
    _shade(cell, fill)
    cell.width = Cm(17)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    _run(p, label or lab, size=9, bold=True, color=lab_color)
    q = cell.add_paragraph(); q.paragraph_format.space_after = Pt(2)
    _run(q, text)
    _spacer(doc)
    return t


def table(doc, header, rows, numeric=(), total=False, widths_cm=None, font_size=10):
    """DataTable: teal-50 header, hairline rows, zebra, right-aligned mono numbers, optional bold total (last row)."""
    _, WD_TABLE_ALIGNMENT, WD_ALIGN, OxmlElement, qn, Cm, Pt, _ = _docx()
    t = doc.add_table(rows=1 + len(rows), cols=len(header))
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    trpr = t.rows[0]._tr.get_or_add_trPr()
    hdr = OxmlElement("w:tblHeader"); hdr.set(qn("w:val"), "true"); trpr.append(hdr)
    for r_i, values in enumerate([header] + list(rows)):
        is_head, is_total = r_i == 0, total and r_i == len(rows)
        for c_i, v in enumerate(values):
            cell = t.cell(r_i, c_i)
            if widths_cm: cell.width = Cm(widths_cm[c_i])
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            num = c_i in numeric and not is_head
            if c_i in numeric: p.alignment = WD_ALIGN.RIGHT
            color = None
            s = str(v)
            if num and s.startswith("▲"): color = "positive"
            if num and s.startswith("▼"): color = "negative"
            _run(p, s, size=font_size, bold=is_head or is_total, color=color,
                 font=MONO if num else FONT)
            tcpr = cell._tc.get_or_add_tcPr()
            if is_head:
                _shade(cell, C["teal_50"]); _border(tcpr, "bottom", C["hairline_strong"], 8, "w:tcBorders")
            elif is_total:
                _border(tcpr, "top", C["hairline_strong"], 8, "w:tcBorders")
            else:
                if r_i % 2 == 0: _shade(cell, C["surface_alt"])
                _border(tcpr, "bottom", C["hairline"], 6, "w:tcBorders")
    _spacer(doc)
    return t


def _spacer(doc, pt=6):
    """Small fixed-height gap after a table (Word needs a paragraph between blocks)."""
    Pt = _docx()[6]
    pf = doc.add_paragraph().paragraph_format
    pf.space_before = pf.space_after = Pt(0)
    pf.line_spacing = Pt(pt)


# ================================================================ PPTX
W_IN, H_IN, MARGIN = 13.333, 7.5, 0.5


def _pptx():
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
    from pptx.enum.shapes import MSO_SHAPE
    from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
    from pptx.util import Inches, Pt
    return Presentation, CategoryChartData, RGBColor, XL_CHART_TYPE, XL_LEGEND_POSITION, MSO_SHAPE, MSO_ANCHOR, PP_ALIGN, Inches, Pt


def _pfont(font, name=FONT, size=None, bold=None, color=None):
    """Font on a pptx run/paragraph, including the complex-script (Thai) and East-Asian slots."""
    *_, Pt = _pptx()
    RGB = _pptx()[2]
    font.name = name
    if size: font.size = Pt(size)
    if bold is not None: font.bold = bold
    if color: font.color.rgb = RGB.from_string(C.get(color, color))
    rpr = font._element if hasattr(font, "_element") else font._rPr
    for tag in ("a:ea", "a:cs"):
        from pptx.oxml.ns import qn
        el = rpr.find(qn(tag))
        if el is None:
            el = rpr.makeelement(qn(tag), {})
            rpr.append(el)
        el.set("typeface", name)


def new_deck():
    Presentation, *_, Inches, _ = _pptx()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(W_IN), Inches(H_IN)
    return prs


def _blank(prs):
    return prs.slides.add_slide(prs.slide_layouts[6])


def text(slide, x, y, w, h, content, size=18, bold=False, color="ink", align="left", anchor="top",
         font=FONT, line=1.1, space_after=6):
    """Textbox in inches. content: str, or list of str (one paragraph each; '• ' prefix makes a bullet)."""
    _, _, _, _, _, _, MSO_ANCHOR, PP_ALIGN, Inches, Pt = _pptx()
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}[anchor]
    for i, line_text in enumerate([content] if isinstance(content, str) else content):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "right": PP_ALIGN.RIGHT, "center": PP_ALIGN.CENTER}[align]
        p.line_spacing = line
        p.space_after = Pt(space_after)
        r = p.add_run(); r.text = line_text
        _pfont(r.font, font, size, bold, color)
    return tb


def rect(slide, x, y, w, h, fill, line=None, rounded=False):
    _, _, RGB, _, _, MSO_SHAPE, _, _, Inches, Pt = _pptx()
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
                                 Inches(x), Inches(y), Inches(w), Inches(h))
    if rounded: shp.adjustments[0] = 0.06
    shp.fill.solid(); shp.fill.fore_color.rgb = RGB.from_string(C.get(fill, fill))
    if line:
        shp.line.color.rgb = RGB.from_string(C.get(line, line)); shp.line.width = Pt(0.75)
    else:
        shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def _chrome(prs, slide, source_text=None):
    """Source bottom-left and page number bottom-right, both slide-footnote in ink-subtle."""
    n = len(prs.slides)
    if source_text:
        text(slide, MARGIN, H_IN - 0.45, 9, 0.3, source_text, size=10, color="ink_subtle")
    text(slide, W_IN - MARGIN - 1, H_IN - 0.45, 1, 0.3, str(n), size=10, color="ink_subtle", align="right")


def title_slide(prs, title, subtitle="", date="", image=None, credit_text=None):
    """Title slide. With image: teal panel (left 45%) holds all text, photo fills the right 55%."""
    s = _blank(prs)
    if image:
        panel = W_IN * 0.45
        rect(s, 0, 0, panel, H_IN, "teal_600")
        picture(s, image, panel, 0, W_IN - panel, H_IN)
        text(s, MARGIN + 0.1, 0.9, panel - 2 * MARGIN, 3.9, title, size=48, bold=True, color="on_accent",
             anchor="bottom", line=0.95)
        if subtitle:
            text(s, MARGIN + 0.1, 5.0, panel - 2 * MARGIN, 0.9, subtitle, size=20, color="on_accent")
        if date:
            text(s, MARGIN + 0.1, 5.95, panel - 2 * MARGIN, 0.4, date, size=14, color="on_accent")
        if credit_text:
            text(s, MARGIN + 0.1, H_IN - 0.45, panel - 2 * MARGIN, 0.3, credit_text, size=9, color="on_accent")
        return s
    panel = W_IN * 0.4
    rect(s, 0, 0, panel, H_IN, "teal_600")
    text(s, MARGIN, 1.2, panel - 2 * MARGIN, H_IN - 2.0, title, size=42, bold=True, color="on_accent",
         anchor="bottom", line=1.0)
    if subtitle:
        text(s, panel + MARGIN, H_IN - 2.2, W_IN - panel - 2 * MARGIN, 1.0, subtitle, size=20,
             color="ink", anchor="bottom")
    if date:
        text(s, panel + MARGIN, H_IN - 1.1, 5, 0.4, date, size=12, color="ink_subtle")
    return s


def section_slide(prs, title, number: str = "", image=None, credit_text=None, kicker="", fit=False):
    """Section divider. With image: large title on the left half, photo bleeds off the right half.
    fit=True for labelled diagrams: shown whole inside the right half instead of cropped."""
    s = _blank(prs)
    if image:
        half = W_IN / 2
        if fit:
            picture_fit(s, image, half + 0.3, 0.4, half - 0.6, H_IN - 0.8)
        else:
            picture(s, image, half, 0, half, H_IN)
        if number:
            text(s, MARGIN + 0.2, 2.0, 4, 0.5, number, size=20, bold=True, color="teal_700")
        rect(s, MARGIN + 0.2, 2.7, 0.9, 0.1, "teal_600")
        text(s, MARGIN + 0.2, 2.95, half - 2 * MARGIN - 0.2, 2.0, title, size=48, bold=True, line=0.95)
        if kicker:
            text(s, MARGIN + 0.2, 4.6, half - 2 * MARGIN - 0.2, 1.2, kicker, size=18, color="ink_muted")
        if credit_text:
            text(s, MARGIN + 0.2, H_IN - 0.45, half - 2 * MARGIN, 0.3, credit_text, size=9, color="ink_subtle")
        return s
    rect(s, MARGIN, 3.0, 0.6, 0.08, "teal_600")
    if number:
        text(s, MARGIN, 2.45, 4, 0.4, number, size=14, bold=True, color="teal_700")
    text(s, MARGIN, 3.25, W_IN - 2 * MARGIN, 1.5, title, size=32, bold=True)
    _chrome(prs, s)
    return s


def content_slide(prs, title, bullets_=None, source_text=None):
    """Takeaway title + up to 6 bullet lines. Returns the slide; the body box spans y 1.55–6.6 in."""
    s = _blank(prs)
    text(s, MARGIN, 0.4, W_IN - 2 * MARGIN, 1.0, title, size=28, bold=True, anchor="top", line=1.0)
    s.body = None
    if bullets_:
        s.body = text(s, MARGIN, 1.6, W_IN - 2 * MARGIN, 4.9, ["•  " + b for b in bullets_], size=18,
                      line=1.15, space_after=10)
    _chrome(prs, s, source_text)
    return s


def kpi_slide(prs, title, kpis, source_text=None):
    """kpis: up to 3 of (value, label, delta_or_None, 'pos'|'neg'|None). First value is teal-600, rest ink."""
    s = content_slide(prs, title, None, source_text)
    kpis = kpis[:3]
    gap, w = 0.25, (W_IN - 2 * MARGIN - 0.25 * 2) / 3
    s.tiles = []
    for i, (value, label, delta, direction) in enumerate(kpis):
        x = MARGIN + i * (w + gap)
        since = len(s.shapes)
        rect(s, x, 2.0, w, 2.6, "surface", line="hairline", rounded=True)
        text(s, x + 0.3, 2.3, w - 0.6, 1.0, value, size=48, bold=True, color="teal_600" if i == 0 else "ink")
        text(s, x + 0.3, 3.35, w - 0.6, 0.5, label, size=16, color="ink_muted")
        if delta:
            text(s, x + 0.3, 3.85, w - 0.6, 0.5, delta, size=14, bold=True,
                 color={"pos": "positive", "neg": "negative"}.get(direction, "ink_muted"))
        s.tiles.append(new_shapes(s, since))
    return s


def table_slide(prs, title, header, rows, numeric=(), source_text=None, col_widths=None, size=14):
    s = content_slide(prs, title, None, source_text)
    s.table = add_table(s, MARGIN, 1.7, W_IN - 2 * MARGIN, header, rows, numeric, col_widths, size)
    return s


def add_table(slide, x, y, w, header, rows, numeric=(), col_widths=None, size=14, row_h=0.45):
    """DataTable anywhere on a slide (inches). Returns the graphic frame (animate it as one piece)."""
    from pptx.oxml.ns import qn
    _, _, RGB, _, _, _, _, PP_ALIGN, Inches, Pt = _pptx()
    n_r, n_c = len(rows) + 1, len(header)
    gt = slide.shapes.add_table(n_r, n_c, Inches(x), Inches(y), Inches(w), Inches(row_h * n_r))
    tbl = gt.table
    tbl.first_row = True; tbl.horz_banding = False
    style_id = tbl._tbl.tblPr.find(qn("a:tableStyleId"))
    if style_id is not None:
        tbl._tbl.tblPr.remove(style_id)  # built-in style would add white grid borders
    if col_widths:
        for i, cw in enumerate(col_widths): tbl.columns[i].width = Inches(cw)
    for r_i, values in enumerate([header] + list(rows)):
        for c_i, v in enumerate(values):
            cell = tbl.cell(r_i, c_i)
            cell.fill.solid()
            fill = "teal_50" if r_i == 0 else ("surface_alt" if r_i % 2 == 0 else "surface")
            cell.fill.fore_color.rgb = RGB.from_string(C[fill])
            cell.margin_left = cell.margin_right = Inches(0.1)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.RIGHT if c_i in numeric else PP_ALIGN.LEFT
            r = p.add_run(); r.text = str(v)
            sv = str(v)
            color = "positive" if sv.startswith("▲") else "negative" if sv.startswith("▼") else "ink"
            _pfont(r.font, MONO if (c_i in numeric and r_i) else FONT, size, r_i == 0, color)
            _cell_bottom(cell, C["hairline_strong"] if r_i == 0 else C["hairline"], 12700 if r_i == 0 else 9525)
    return gt


def _cell_bottom(cell, color, emu):
    """No left/right/top lines, one bottom rule; inserted before the cell fill as the schema requires."""
    from pptx.oxml.ns import qn
    tcpr = cell._tc.get_or_add_tcPr()
    for i, side in enumerate(("a:lnL", "a:lnR", "a:lnT", "a:lnB")):
        ln = tcpr.makeelement(qn(side), {"w": str(emu if side == "a:lnB" else 0)})
        if side == "a:lnB":
            fill = ln.makeelement(qn("a:solidFill"), {})
            fill.append(fill.makeelement(qn("a:srgbClr"), {"val": color}))
        else:
            fill = ln.makeelement(qn("a:noFill"), {})
        ln.append(fill)
        tcpr.insert(i, ln)


def chart_slide(prs, title, categories, series: dict, kind="bar", source_text=None, number_format="General",
                legend=True):
    """Flat 2D bar/line chart in data-1…data-6 order. series: {name: [values]} — first is the subject."""
    _, CategoryChartData, RGB, XL, XL_LEGEND, _, _, _, Inches, Pt = _pptx()
    s = content_slide(prs, title, None, source_text)
    cd = CategoryChartData(); cd.categories = categories
    for name, vals in series.items(): cd.add_series(name, vals)
    ctype = {"bar": XL.COLUMN_CLUSTERED, "hbar": XL.BAR_CLUSTERED, "line": XL.LINE_MARKERS,
             "stacked": XL.COLUMN_STACKED}[kind]
    gf = s.shapes.add_chart(ctype, Inches(MARGIN), Inches(1.6), Inches(W_IN - 2 * MARGIN), Inches(5.0), cd)
    style_chart(gf.chart, kind, number_format, legend and len(series) > 1)
    s.chart = gf
    return s


def style_chart(chart, kind="bar", number_format="General", legend=True):
    """Apply palette, hairline gridlines, no border, Leelawadee UI labels to a python-pptx chart."""
    _, _, RGB, _, XL_LEGEND, _, _, _, _, Pt = _pptx()
    chart.font.size = Pt(12); chart.font.name = FONT
    chart.font.color.rgb = RGB.from_string(C["ink_subtle"])
    for i, ser in enumerate(chart.plots[0].series):
        col = RGB.from_string(DATA[i % len(DATA)])
        if kind == "line":
            ser.format.line.color.rgb = col; ser.format.line.width = Pt(2.25); ser.smooth = False
            ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = col
            ser.marker.format.line.color.rgb = col
        else:
            ser.format.fill.solid(); ser.format.fill.fore_color.rgb = col
            ser.format.line.fill.background()
    if kind != "line":
        chart.plots[0].gap_width = 60
        if kind != "stacked": chart.plots[0].overlap = -10
    va, ca = chart.value_axis, chart.category_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGB.from_string(C["hairline"])
    va.major_gridlines.format.line.width = Pt(0.75)
    va.format.line.fill.background()
    va.tick_labels.number_format = number_format; va.tick_labels.number_format_is_linked = False
    ca.format.line.color.rgb = RGB.from_string(C["hairline_strong"])
    ca.tick_labels.font.color.rgb = RGB.from_string(C["ink"])
    chart.has_legend = legend
    if legend:
        chart.legend.position = XL_LEGEND.TOP; chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(12)


# ---------------------------------------------------------------- PPTX: pictures, diagrams
def picture(slide, path, x, y, w, h):
    """Photo cropped to fill the box exactly (object-fit: cover). Inches."""
    from PIL import Image
    Inches = _pptx()[-2]
    iw, ih = Image.open(path).size
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    box_ratio, img_ratio = w / h, iw / ih
    if img_ratio > box_ratio:
        pic.crop_left = pic.crop_right = (1 - box_ratio / img_ratio) / 2
    else:
        pic.crop_top = pic.crop_bottom = (1 - img_ratio / box_ratio) / 2
    return pic


def picture_fit(slide, path, x, y, w, h):
    """Diagram or figure scaled to fit inside the box without cropping, centred. Inches."""
    from PIL import Image
    Inches = _pptx()[-2]
    iw, ih = Image.open(path).size
    scale = min(w / iw, h / ih)
    pw, ph = iw * scale, ih * scale
    return slide.shapes.add_picture(str(path), Inches(x + (w - pw) / 2), Inches(y + (h - ph) / 2),
                                    Inches(pw), Inches(ph))


def credit(slide, text_, x, y, w=4.0, align="left", color="ink_subtle"):
    """Image credit, 9pt ('Image: site.com'). Required under every picture taken from the web."""
    return text(slide, x, y, w, 0.25, text_, size=9, color=color, align=align)


def new_shapes(slide, since):
    """Shapes added after len(slide.shapes) was `since`: groups one build step."""
    return list(slide.shapes)[since:]


def box(slide, x, y, w, h, content, fill="teal_50", color="ink", size=16, bold=False, line=None,
        rounded=True, align="center"):
    """Diagram node: tinted rectangle with centred text (str, or list: first line bold-able, rest smaller)."""
    _, _, _, _, _, _, MSO_ANCHOR, PP_ALIGN, Inches, Pt = _pptx()
    shp = rect(slide, x, y, w, h, fill, line, rounded)
    tf = shp.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.1)
    tf.margin_top = tf.margin_bottom = Inches(0.05)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, line_text in enumerate([content] if isinstance(content, str) else content):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER}[align]
        r = p.add_run()
        r.text = line_text
        _pfont(r.font, FONT, size if i == 0 else size - 2, bold if i == 0 else False, color)
    return shp


def _connector(slide, x1, y1, x2, y2, color, width_pt):
    from pptx.enum.shapes import MSO_CONNECTOR
    _, _, RGB, *_, Inches, Pt = _pptx()
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    c.line.color.rgb = RGB.from_string(C.get(color, color))
    c.line.width = Pt(width_pt)
    return c


def arrow(slide, x1, y1, x2, y2, color="hairline_strong", width_pt=1.5):
    """Straight connector with a triangle head at (x2, y2). Inches."""
    c = _connector(slide, x1, y1, x2, y2, color, width_pt)
    ln = c.line._get_or_add_ln()
    ln.append(ln.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}tailEnd",
                             {"type": "triangle", "w": "med", "len": "med"}))
    return c


def line(slide, x1, y1, x2, y2, color="hairline", width_pt=1.0):
    return _connector(slide, x1, y1, x2, y2, color, width_pt)


def forest_plot(slide, rows, x=MARGIN, y=1.75, w=W_IN - 2 * MARGIN, row_h=0.62, lo=0.02, hi=2.0,
                ticks=(0.05, 0.1, 0.25, 0.5, 1, 2), label_w=4.3, est_w=2.9,
                left_label="Favours lithium", right_label="Favours control"):
    """Log-scale forest plot built from shapes. rows: (label, estimate, ci_low, ci_high).
    CI excluding 1 = teal (data-1); crossing 1 = gray (data-6). Returns one shape list per row."""
    import math
    px, pw = x + label_w, w - label_w - est_w

    def X(v):
        return px + pw * (math.log(v) - math.log(lo)) / (math.log(hi) - math.log(lo))

    top, bottom = y, y + row_h * len(rows)
    line(slide, X(1), top - 0.1, X(1), bottom + 0.05, "hairline_strong", 1.25)
    line(slide, px, bottom + 0.05, px + pw, bottom + 0.05, "hairline_strong", 1.0)
    for t in ticks:
        line(slide, X(t), bottom + 0.05, X(t), bottom + 0.12, "hairline_strong", 1.0)
        text(slide, X(t) - 0.4, bottom + 0.15, 0.8, 0.3, f"{t:g}", size=12, color="ink_subtle", align="center")
    text(slide, px, bottom + 0.5, X(1) - px - 0.1, 0.3, "← " + left_label, size=12, color="ink_muted",
         align="right")
    text(slide, X(1) + 0.1, bottom + 0.5, 3.0, 0.3, right_label + " →", size=12, color="ink_muted")
    groups = []
    for i, (label, est, lo_ci, hi_ci) in enumerate(rows):
        since = len(slide.shapes)
        cy = top + row_h * i + row_h / 2
        sig = hi_ci < 1 or lo_ci > 1
        col = DATA[0] if sig else DATA[5]
        text(slide, x, cy - 0.2, label_w - 0.1, 0.4, label, size=16, anchor="middle")
        line(slide, X(max(lo_ci, lo)), cy, X(min(hi_ci, hi)), cy, col, 2.0)
        rect(slide, X(est) - 0.08, cy - 0.08, 0.16, 0.16, col)
        text(slide, x + w - est_w + 0.1, cy - 0.2, est_w - 0.1, 0.4, f"{est:.2f} ({lo_ci:.2f}–{hi_ci:.2f})",
             size=15, font=MONO, color="ink" if sig else "ink_muted", align="right", anchor="middle")
        groups.append(new_shapes(slide, since))
    return groups


def range_bar(slide, zones, vmin, vmax, x=MARGIN, y=2.4, w=W_IN - 2 * MARGIN, h=0.9, ticks=(), unit=""):
    """Horizontal scale split into zones: (start, end, label, fill, text_colour).
    Returns one shape list per zone."""
    def X(v):
        return x + w * (v - vmin) / (vmax - vmin)

    groups = []
    for start, end, label, fill, tcol in zones:
        since = len(slide.shapes)
        box(slide, X(start), y, X(end) - X(start), h, label, fill=fill, color=tcol, size=13, bold=True,
            rounded=False)
        groups.append(new_shapes(slide, since))
    for t in ticks:
        line(slide, X(t), y + h, X(t), y + h + 0.12, "hairline_strong", 1.0)
        text(slide, X(t) - 0.4, y + h + 0.15, 0.8, 0.3, f"{t:g}", size=13, font=MONO, color="ink_muted",
             align="center")
    if unit:
        text(slide, x + w - 5, y + h + 0.45, 5, 0.3, unit, size=12, color="ink_subtle", align="right")
    return groups


def timeline(slide, events, x=MARGIN + 0.3, y=3.3, w=W_IN - 2 * MARGIN - 0.6, label_w=2.0, size=14,
             head_lines=1):
    """Horizontal timeline. events: (when, headline, detail). Keep headlines short (head_lines=2 if they
    must wrap). Returns one shape list per event."""
    line(slide, x, y, x + w, y, "hairline_strong", 1.5)
    n = len(events)
    groups = []
    for i, (when, head, detail) in enumerate(events):
        since = len(slide.shapes)
        cx = x + (w * i / (n - 1) if n > 1 else w / 2)
        rect(slide, cx - 0.11, y - 0.11, 0.22, 0.22, "teal_600", rounded=True)
        text(slide, cx - label_w / 2, y - 0.85, label_w, 0.5, when, size=20, bold=True, color="teal_700",
             align="center", anchor="bottom")
        head_h = 0.3 * head_lines + 0.1
        text(slide, cx - label_w / 2, y + 0.3, label_w, head_h, head, size=size, bold=True, align="center")
        text(slide, cx - label_w / 2, y + 0.4 + head_h, label_w, 1.4, detail, size=size - 2, color="ink_muted",
             align="center", line=1.05)
        groups.append(new_shapes(slide, since))
    return groups


def download_image(url, path):
    """Save one web image (browser user-agent; many sites refuse python's). Returns the path.
    For Google Images results picked in the built-in browser (see SKILL.md)."""
    import urllib.request
    ua = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/128 Safari/537.36"}
    data = urllib.request.urlopen(urllib.request.Request(url, headers=ua), timeout=30).read()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(data)
    return Path(path)


# ---------------------------------------------------------------- PPTX: motion
_EFFECTS = {  # name: (presetID, presetSubtype, filter)
    "fade": (10, 0, "fade"),
    "wipe": (22, 8, "wipe(left)"),  # reveals left to right: bars, timelines, forest rows
    "rise": (22, 4, "wipe(up)"),    # reveals bottom to top: columns
}


def transition(slide, kind="fade", speed="med"):
    """Slide transition: 'fade' (standard) or 'push'."""
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls, qn
    sld = slide._element
    for old in sld.findall(qn("p:transition")):
        sld.remove(old)
    inner = {"fade": "<p:fade/>", "push": '<p:push dir="u"/>'}[kind]
    tr = parse_xml(f'<p:transition {nsdecls("p")} spd="{speed}">{inner}</p:transition>')
    timing = sld.find(qn("p:timing"))
    if timing is not None:
        timing.addprevious(tr)
    else:
        sld.append(tr)


def _effect_xml(ids, shape, para, node, preset, sub, filt, dur_ms):
    spid = shape.shape_id
    tgt = (f'<p:spTgt spid="{spid}"><p:txEl><p:pRg st="{para}" end="{para}"/></p:txEl></p:spTgt>'
           if para is not None else f'<p:spTgt spid="{spid}"/>')
    a, b, c = next(ids), next(ids), next(ids)
    return (f'<p:par><p:cTn id="{a}" presetID="{preset}" presetClass="entr" presetSubtype="{sub}" fill="hold" '
            f'grpId="0" nodeType="{node}"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>'
            f'<p:set><p:cBhvr><p:cTn id="{b}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/>'
            f'</p:stCondLst></p:cTn><p:tgtEl>{tgt}</p:tgtEl><p:attrNameLst><p:attrName>style.visibility'
            f'</p:attrName></p:attrNameLst></p:cBhvr><p:to><p:strVal val="visible"/></p:to></p:set>'
            f'<p:animEffect transition="in" filter="{filt}"><p:cBhvr><p:cTn id="{c}" dur="{dur_ms}"/>'
            f'<p:tgtEl>{tgt}</p:tgtEl></p:cBhvr></p:animEffect></p:childTnLst></p:cTn></p:par>')


def animate(slide, steps, effect="fade", dur_ms=500):
    """Click-by-click entrance build. steps: list; a step is a shape, a list of shapes, or
    (shape, paragraph_index) tuples. Everything in one step appears together on one click.
    Call once per slide after all shapes exist. Bullets one by one: animate(s, bullets(s.body))."""
    from pptx.oxml import parse_xml
    from pptx.oxml.ns import nsdecls, qn
    preset, sub, filt = _EFFECTS[effect]
    ids = iter(range(3, 100000))
    clicks, bld = [], {}
    for step in steps:
        targets = step if isinstance(step, list) else [step]
        effects = []
        for j, t in enumerate(targets):
            shape, para = t if isinstance(t, tuple) else (t, None)
            effects.append(_effect_xml(ids, shape, para, "clickEffect" if j == 0 else "withEffect",
                                       preset, sub, filt, dur_ms))
            tag = shape._element.tag.split("}")[1]
            if tag == "sp":
                bld[shape.shape_id] = "p" if para is not None else bld.get(shape.shape_id, "whole")
            elif tag == "graphicFrame":
                bld[shape.shape_id] = "graphic"
        o, i2 = next(ids), next(ids)
        clicks.append(f'<p:par><p:cTn id="{o}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/>'
                      f'</p:stCondLst><p:childTnLst><p:par><p:cTn id="{i2}" fill="hold"><p:stCondLst>'
                      f'<p:cond delay="0"/></p:stCondLst><p:childTnLst>{"".join(effects)}</p:childTnLst>'
                      f'</p:cTn></p:par></p:childTnLst></p:cTn></p:par>')
    blds = "".join(
        f'<p:bldGraphic spid="{k}" grpId="0"><p:bldAsOne/></p:bldGraphic>' if v == "graphic"
        else f'<p:bldP spid="{k}" grpId="0" build="p"/>' if v == "p"
        else f'<p:bldP spid="{k}" grpId="0" animBg="1"/>' for k, v in bld.items())
    bld_xml = f"<p:bldLst>{blds}</p:bldLst>" if blds else ""
    xml = (f'<p:timing {nsdecls("p")}><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" '
           f'nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" '
           f'dur="indefinite" nodeType="mainSeq"><p:childTnLst>{"".join(clicks)}</p:childTnLst></p:cTn>'
           f'<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond>'
           f'</p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl>'
           f'</p:cond></p:nextCondLst></p:seq></p:childTnLst></p:cTn></p:par></p:tnLst>{bld_xml}</p:timing>')
    sld = slide._element
    for old in sld.findall(qn("p:timing")):
        sld.remove(old)
    ext = sld.find(qn("p:extLst"))
    if ext is not None:
        ext.addprevious(parse_xml(xml))
    else:
        sld.append(parse_xml(xml))


def numbered_cards(slide, items, x=MARGIN, y=1.7, w=W_IN - 2 * MARGIN, h=None, gap=0.15, size=18):
    """Numbered rows (teal number badge + tinted text band): a visual alternative to a bullet list.
    Returns one shape list per row, ready for animate()."""
    h = h or min(0.95, (6.5 - y - gap * (len(items) - 1)) / len(items))
    groups = []
    for i, item in enumerate(items):
        since = len(slide.shapes)
        top = y + i * (h + gap)
        box(slide, x, top, h, h, str(i + 1), fill="teal_600", color="on_accent", size=size + 4, bold=True)
        box(slide, x + h + 0.1, top, w - h - 0.1, h, item, fill="teal_50" if i % 2 == 0 else "surface_alt",
            size=size, align="left")
        groups.append(new_shapes(slide, since))
    return groups


def bullets_steps(body):
    """One step per paragraph of a text box: animate(s, bullets_steps(s.body))."""
    return [(body, i) for i in range(len(body.text_frame.paragraphs))]


def finish_deck(prs, kind="fade"):
    """Standard transition on every slide. Call right before prs.save()."""
    for sl in prs.slides:
        transition(sl, kind)


# ================================================================ XLSX
FMT = {"int": "#,##0", "num": "#,##0.00", "pct": "0.0%", "x": '0.0"x"', "date": "d mmm yyyy",
       "delta_pct": '"▲ "0.0%;"▼ "0.0%;0.0%', "delta_num": '"▲ "#,##0.00;"▼ "#,##0.00;0.00',
       "thb": '"฿"#,##0', "text": "@"}


def _xl():
    from openpyxl import Workbook
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    return Workbook, CellIsRule, Alignment, Border, Font, PatternFill, Side


def xfont(color="ink", bold=False, size=10, mono=False):
    return _xl()[4](name=MONO if mono else FONT, size=size, bold=bold, color=C.get(color, color))


def xfill(color):
    return _xl()[5](fill_type="solid", start_color=C.get(color, color), end_color=C.get(color, color))


def new_workbook():
    """Workbook whose first sheet is 'Summary'. Set gridlines off per sheet via sheet_header."""
    Workbook, *_ = _xl()
    wb = Workbook()
    wb.active.title = "Summary"
    return wb


def sheet_header(ws, title, note, headers, widths=None, numeric=()):
    """Row 1 title band, row 2 note, row 3 header; freezes B4, gridlines off. Returns first data row (4)."""
    _, _, Alignment, Border, _, _, Side = _xl()
    ws.sheet_view.showGridLines = False
    n = len(headers)
    for c in range(1, n + 1):
        ws.cell(1, c).fill = xfill("surface_sunken")
    ws.cell(1, 1, title).font = xfont(bold=True, size=14)
    ws.row_dimensions[1].height = 26
    ws.cell(1, 1).alignment = Alignment(vertical="center")
    ws.cell(2, 1, note).font = xfont("ink_subtle", size=9)
    line = Border(bottom=Side(style="thin", color=C["hairline_strong"]))
    for c, h in enumerate(headers, start=1):
        cell = ws.cell(3, c, h)
        cell.font = xfont(bold=True); cell.fill = xfill("teal_50"); cell.border = line
        cell.alignment = Alignment(horizontal="right" if (c - 1) in numeric else "left", vertical="center")
    ws.row_dimensions[3].height = 20
    for c in range(1, n + 1):
        ws.column_dimensions[ws.cell(3, c).column_letter].width = (widths[c - 1] if widths else 14)
    ws.freeze_panes = "B4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    return 4


def write_rows(ws, rows, start=4, formats=None, inputs=()):
    """Write rows from `start`. formats: {col_index: FMT key}; inputs: col indexes styled as editable
    (teal-700 on surface-alt). Formulas ('=…') stay ink. Hairline bottom border on every row."""
    _, _, Alignment, Border, _, _, Side = _xl()
    formats = formats or {}
    line = Border(bottom=Side(style="thin", color=C["hairline"]))
    for r_off, row in enumerate(rows):
        r = start + r_off
        for c_i, v in enumerate(row):
            cell = ws.cell(r, c_i + 1, v)
            key = formats.get(c_i)
            is_num = key not in (None, "text")
            cell.font = xfont("teal_700" if c_i in inputs else "ink", mono=is_num)
            if c_i in inputs: cell.fill = xfill("surface_alt")
            if key: cell.number_format = FMT[key]
            cell.alignment = Alignment(horizontal="right" if is_num else "left")
            cell.border = line
    return start + len(rows)


def total_row(ws, row, label, values, formats=None):
    """Bold total row with a hairline-strong top rule. values: list for columns 2… (formulas welcome)."""
    _, _, Alignment, Border, _, _, Side = _xl()
    formats = formats or {}
    top = Border(top=Side(style="thin", color=C["hairline_strong"]))
    for c_i, v in enumerate([label] + list(values)):
        cell = ws.cell(row, c_i + 1, v)
        key = formats.get(c_i)
        cell.font = xfont(bold=True, mono=key not in (None, "text"))
        cell.border = top
        if key:
            cell.number_format = FMT[key]; cell.alignment = Alignment(horizontal="right")


def delta_colors(ws, cell_range):
    """Colour ▲ values positive and ▼ values negative (pair with FMT['delta_pct'|'delta_num'])."""
    _, CellIsRule, *_ = _xl()
    ws.conditional_formatting.add(cell_range, CellIsRule(operator="greaterThan", formula=["0"],
                                                         font=xfont("positive", mono=True)))
    ws.conditional_formatting.add(cell_range, CellIsRule(operator="lessThan", formula=["0"],
                                                         font=xfont("negative", mono=True)))


def _xl_text(size_pt, color):
    """Chart text properties: Leelawadee UI at size/colour (openpyxl charts default to Calibri)."""
    from openpyxl.chart.text import RichText
    from openpyxl.drawing.text import CharacterProperties, Font as DFont, Paragraph, ParagraphProperties
    cp = CharacterProperties(sz=int(size_pt * 100), solidFill=C[color], latin=DFont(typeface=FONT),
                             cs=DFont(typeface=FONT))
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])


def xl_chart(ws, anchor, data_ref, cats_ref, title=None, kind="bar", y_format=None, width=18, height=9):
    """Native Excel bar/line chart in the palette. data_ref/cats_ref: openpyxl Reference objects
    (data_ref includes the header row: titles_from_data=True)."""
    from openpyxl.chart import BarChart, LineChart
    from openpyxl.chart.shapes import GraphicalProperties
    from openpyxl.drawing.line import LineProperties
    ch = LineChart() if kind == "line" else BarChart()
    if kind != "line":
        ch.type = "col"; ch.gapWidth = 60
    ch.add_data(data_ref, titles_from_data=True)
    ch.set_categories(cats_ref)
    ch.title = title
    ch.style = 1
    ch.width, ch.height = width, height
    for i, s in enumerate(ch.series):
        col = DATA[i % len(DATA)]
        if kind == "line":
            s.graphicalProperties.line.solidFill = col; s.graphicalProperties.line.width = 28575
            s.smooth = False
        else:
            s.graphicalProperties.solidFill = col; s.graphicalProperties.line.noFill = True
    ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["hairline"], w=9525))
    ch.y_axis.spPr = GraphicalProperties(ln=LineProperties(noFill=True))
    ch.x_axis.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["hairline_strong"], w=9525))
    ch.x_axis.delete = False; ch.y_axis.delete = False
    ch.y_axis.numFmt = y_format or "#,##0"
    ch.y_axis.number_format = y_format or "#,##0"
    for ax in (ch.x_axis, ch.y_axis):
        ax.txPr = _xl_text(9, "ink_subtle")
    ch.legend.position = "t"
    if len(ch.series) == 1: ch.legend = None
    ch.graphical_properties = GraphicalProperties(ln=LineProperties(noFill=True))
    ws.add_chart(ch, anchor)
    return ch
