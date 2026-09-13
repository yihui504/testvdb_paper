# -*- coding: utf-8 -*-
"""Figure 1 -- cartoon / sticker variant (style E).

Same geometry and same information content as pipeline-v6 (already validated
against figure1-requirements.md); only the visual language changes:

  * candy (macaron) fills + one shared deep-indigo ink outline -> sticker look
  * very large corner radii, pill shapes, soft outer shadows
  * round-capped strokes, dotted (round-dot) dashes, chunky arrowheads
  * circular stage badges instead of the 1-2-3-4 glyphs
  * a few *informative* pictograms (document, gear, bolt, cylinder,
    magnifier, five-link chain) -- each maps to a real concept, no filler art
  * Trebuchet MS for labels, Consolas kept for filenames (semantic: artifact)

Black/white safety is preserved: the two independent information sources are
still separated by POSITION and by dotted line style, not by colour.
"""
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from pptx.enum.dml import MSO_LINE_DASH_STYLE

DOT = MSO_LINE_DASH_STYLE.ROUND_DOT
MONO = "Consolas"
SANS = "Trebuchet MS"
EMU_CM = 360000

# ---------------- candy palette ----------------
INK = "3B3B5C"          # shared outline / headline ink
INK_SOFT = "9A9AB8"     # secondary rules, small grey text
GRAY_TXT = "7A7A96"

CREAM, CREAM_LINE, CREAM_TEXT = "FFF6DE", "E0B85C", "8A6220"   # documents
MINT, MINT_LINE, MINT_DARK = "E4F6EC", "6FC79A", "2E7D52"      # stage 1
SKY, SKY_LINE, SKY_DARK = "E9F3FE", "7FB2E8", "2A6DB0"         # stage 2
PEACH, PEACH_LINE, PEACH_DARK = "FDEEE2", "F0A468", "A55A1E"   # stage 3
LILAC, LILAC_LINE, LILAC_DARK = "EDE8FC", "9B8AE8", "53409E"   # stage 4
PINK_LINE = "EE9AB4"
TEAL, TEAL_LINE, TEAL_DARK = "DFF5F1", "45BFAE", "1F7A6C"      # impl. source
WHITE = "FFFFFF"

LANE = [("F4FCF7", "A8DCC0"), ("F3F8FE", "AFCCEE"),
        ("FEF8F2", "F2CBA8"), ("F8F6FE", "C3BAEE")]

prs = Presentation()
prs.slide_width = Cm(40)
prs.slide_height = Cm(13.3)
slide = prs.slides.add_slide(prs.slide_layouts[6])
shapes = slide.shapes


def C(h):
    return RGBColor.from_string(h)


def setline(sp, hexc, w, dash=None, cap=None):
    sp.line.color.rgb = C(hexc)
    sp.line.width = Pt(w)
    ln = sp.line._get_or_add_ln()
    if dash:
        sp.line.dash_style = dash
    if cap:
        ln.set('cap', cap)


def soft_shadow(sp, blur=0.10, dist=0.045, alpha=26):
    spPr = sp._element.spPr
    for e in spPr.findall(qn('a:effectLst')):
        spPr.remove(e)
    eff = spPr.makeelement(qn('a:effectLst'), {})
    sh = spPr.makeelement(qn('a:outerShdw'), {
        'blurRad': str(int(blur * EMU_CM)), 'dist': str(int(dist * EMU_CM)),
        'dir': '5400000', 'algn': 'tl', 'rotWithShape': '0'})
    clr = spPr.makeelement(qn('a:srgbClr'), {'val': INK})
    clr.append(clr.makeelement(qn('a:alpha'), {'val': str(int(alpha * 1000))}))
    sh.append(clr)
    eff.append(sh)
    spPr.append(eff)


def box(x, y, w, h, fill, line, lw=1.4, adj=0.22, shape=None, shadow=True):
    st = shape or (MSO_SHAPE.ROUNDED_RECTANGLE if adj else MSO_SHAPE.RECTANGLE)
    sp = shapes.add_shape(st, Cm(x), Cm(y), Cm(w), Cm(h))
    if st == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            sp.adjustments[0] = adj
        except Exception:
            pass
    if fill is None:
        sp.fill.background()
    else:
        sp.fill.solid(); sp.fill.fore_color.rgb = C(fill)
    setline(sp, line, lw)
    sp.shadow.inherit = False
    if shadow:
        soft_shadow(sp)
    tf = sp.text_frame
    tf.word_wrap = True
    tf.margin_left = Cm(0.12); tf.margin_right = Cm(0.12)
    tf.margin_top = Cm(0.04); tf.margin_bottom = Cm(0.04)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return sp


def put(sp, items, align=PP_ALIGN.CENTER):
    tf = sp.text_frame
    for i, it in enumerate(items):
        text, size, bold, italic, color = it[0], it[1], it[2], it[3], it[4]
        font = it[5] if len(it) > 5 else SANS
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(0); p.space_after = Pt(0); p.line_spacing = 1.0
        r = p.add_run(); r.text = text
        r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
        r.font.color.rgb = C(color); r.font.name = font
    return sp


def tbox(x, y, w, h, items, align=PP_ALIGN.CENTER, fill=None):
    tb = shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Cm(0.03); tf.margin_right = Cm(0.03)
    tf.margin_top = Cm(0.0); tf.margin_bottom = Cm(0.0)
    if fill:
        tb.fill.solid(); tb.fill.fore_color.rgb = C(fill)
    else:
        tb.fill.background()
    tb.line.fill.background()
    tb.shadow.inherit = False
    return put(tb, items, align)


def conn(x1, y1, x2, y2, color=INK, w=1.4, dash=None, tail=False, cap='rnd'):
    c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Cm(x1), Cm(y1), Cm(x2), Cm(y2))
    setline(c, color, w, dash, cap)
    c.shadow.inherit = False
    if tail:
        ln = c.line._get_or_add_ln()
        ln.append(ln.makeelement(qn('a:tailEnd'),
                                 {'type': 'triangle', 'w': 'lg', 'len': 'lg'}))
    return c


def elbow(pts, color=INK, w=1.4, dash=None):
    for i in range(len(pts) - 1):
        conn(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
             color, w, dash, tail=(i == len(pts) - 2))


def badge(x, y, d, fill, text, tsize=10.5):
    sp = shapes.add_shape(MSO_SHAPE.OVAL, Cm(x), Cm(y), Cm(d), Cm(d))
    sp.fill.solid(); sp.fill.fore_color.rgb = C(fill)
    setline(sp, INK, 1.1)
    sp.shadow.inherit = False
    soft_shadow(sp, 0.07, 0.035, 24)
    tf = sp.text_frame
    tf.word_wrap = False
    for a in ('margin_left', 'margin_right', 'margin_top', 'margin_bottom'):
        setattr(tf, a, Cm(0.0))
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    return put(sp, [(text, tsize, True, False, WHITE)])


def doc_icon(x, y, w, h):
    sp = shapes.add_shape(MSO_SHAPE.FOLDED_CORNER, Cm(x), Cm(y), Cm(w), Cm(h))
    sp.fill.solid(); sp.fill.fore_color.rgb = C(CREAM)
    setline(sp, CREAM_LINE, 1.25)
    sp.shadow.inherit = False
    soft_shadow(sp, 0.07, 0.035, 22)
    for k in (0.30, 0.48, 0.66):
        conn(x + w * 0.17, y + h * k, x + w * 0.70, y + h * k, INK_SOFT, 0.9)
    return sp


def magnifier(cx, cy, d=0.66, lw=2.1):
    ov = shapes.add_shape(MSO_SHAPE.OVAL, Cm(cx - d / 2), Cm(cy - d / 2), Cm(d), Cm(d))
    ov.fill.background(); setline(ov, INK, lw)
    ov.shadow.inherit = False
    r = d * 0.354
    conn(cx + r * 0.8, cy + r * 0.8, cx + r * 0.8 + 0.30, cy + r * 0.8 + 0.30, INK, lw)


# ================= top: external input E1 + automation legend =================
tbox(23.6, 0.42, 15.9, 0.5,
     [("reading · generation · adjudication by LLM agents · execution & checks deterministic",
       8, False, True, GRAY_TXT)], align=PP_ALIGN.RIGHT)
doc_icon(0.55, 0.42, 1.05, 1.20)
e1 = box(2.0, 0.35, 8.6, 1.35, CREAM, CREAM_LINE, 1.6)
put(e1, [("API documentation", 10.5, True, False, CREAM_TEXT),
         ("natural-language prose", 8, False, False, GRAY_TXT)])
elbow([(6.3, 1.70), (6.3, 1.98), (4.5, 1.98), (4.5, 2.30)])

# ================= stage containers + badges =================
ST_Y, ST_H = 2.30, 7.60
stages = [(0.5, 8.0, "Behavioral Specification Extraction", MINT_LINE, "1"),
          (9.0, 8.0, "Test Script Generation", SKY_LINE, "2"),
          (17.5, 6.6, "Sandboxed Execution", PEACH_LINE, "3"),
          (24.6, 14.9, "Bug Confirmation \u2014 builder / auditor split", LILAC_LINE, "4")]
for i, (sx, sw, title, bl, num) in enumerate(stages):
    st = box(sx, ST_Y, sw, ST_H, LANE[i][0], LANE[i][1], 1.25, adj=0.045, shadow=False)
    put(st, [(title, 10.5, True, False, INK)], align=PP_ALIGN.LEFT)
    st.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    st.text_frame.margin_left = Cm(1.18); st.text_frame.margin_top = Cm(0.19)
    badge(sx + 0.24, ST_Y + 0.10, 0.78, bl, num, 11)

# ================= stage 1 =================
t1 = box(1.1, 3.60, 6.8, 1.30, WHITE, INK)
put(t1, [("knowledge extractor", 10, True, False, INK),
         ("Crawl4AI · coverage + version checks", 7.8, False, True, GRAY_TXT)])
a1 = box(1.1, 5.20, 6.8, 0.85, WHITE, CREAM_LINE, 1.5)
put(a1, [("knowledge.json", 9.5, True, False, CREAM_TEXT, MONO)])
t2 = box(1.1, 6.35, 6.8, 1.30, WHITE, INK)
put(t2, [("specification extractor", 10, True, False, INK),
         ("categorize · evidence-tier · verify source", 7.8, False, True, GRAY_TXT)])
a2 = box(1.1, 7.95, 6.8, 1.15, WHITE, CREAM_LINE, 1.5)
put(a2, [("specifications.json", 9.5, True, False, CREAM_TEXT, MONO),
         ("typed · tiered · source-verified · level", 7.5, False, True, GRAY_TXT)])
for y1, y2 in [(4.90, 5.20), (6.05, 6.35), (7.65, 7.95)]:
    conn(4.5, y1, 4.5, y2, tail=True)

# ================= stage 2 =================
g1 = box(9.6, 3.60, 6.8, 1.30, WHITE, INK)
put(g1, [("strategy registry", 10, True, False, INK),
         ("pre-bound: trigger \u2192 strategy", 7.8, False, True, GRAY_TXT)])
g2 = box(9.6, 5.20, 6.8, 1.30, WHITE, INK)
put(g2, [("attack agents", 10, True, False, INK),
         ("boundary · state · semantic", 8, False, False, GRAY_TXT)])
g3 = box(9.6, 6.80, 6.8, 1.30, WHITE, INK)
put(g3, [("scenario construction", 10, True, False, INK),
         ("system-level · no-match fallback", 7.8, False, True, GRAY_TXT)])
gt = box(9.9, 8.30, 6.2, 0.90, SKY, SKY_LINE, 1.5, adj=0.5)
put(gt, [("5 generation gates", 9.5, True, False, SKY_DARK)])
for y1, y2 in [(4.90, 5.20), (6.50, 6.80), (8.10, 8.30)]:
    conn(13.0, y1, 13.0, y2, tail=True)
# pictograms: gear = pre-bound registry, bolt = attack agents
gr = shapes.add_shape(MSO_SHAPE.GEAR_6, Cm(15.40), Cm(3.78), Cm(0.85), Cm(0.85))
gr.fill.solid(); gr.fill.fore_color.rgb = C(SKY); setline(gr, INK, 1.1)
gr.shadow.inherit = False
bo = shapes.add_shape(MSO_SHAPE.LIGHTNING_BOLT, Cm(15.55), Cm(5.42), Cm(0.68), Cm(0.88))
bo.fill.solid(); bo.fill.fore_color.rgb = C("FFE9A8"); setline(bo, INK, 1.1)
bo.shadow.inherit = False

# ================= stage 3 =================
cy = box(18.0, 4.00, 5.6, 2.00, WHITE, INK, 1.5, shape=MSO_SHAPE.CAN)
put(cy, [("Docker-pinned VDBMS", 9.5, True, False, INK),
         ("target @ version", 8, False, True, GRAY_TXT)])
a3 = box(18.0, 6.60, 5.6, 1.15, WHITE, CREAM_LINE, 1.5)
put(a3, [("raw HTTP logs", 9.5, True, False, CREAM_TEXT, MONO),
         ("+ atomic .done markers", 7.5, False, True, GRAY_TXT)])
conn(20.8, 6.00, 20.8, 6.60, tail=True)

# ================= stage 4 =================
b4 = box(25.2, 3.50, 5.9, 3.00, MINT, MINT_LINE, 1.5)
put(b4, [("evidence builder", 10, True, False, MINT_DARK)] +
        [(u"· " + t, 7.8, False, False, "3B6B50") for t in
         ("doc verification", "execution evidence", "contract grounding",
          "chain trace", "source grounding (grep clone)")], align=PP_ALIGN.LEFT)
b4.text_frame.vertical_anchor = MSO_ANCHOR.TOP
b4.text_frame.margin_left = Cm(0.28); b4.text_frame.margin_top = Cm(0.16)

ch = box(31.55, 4.35, 3.50, 1.30, WHITE, CREAM_LINE, 1.5)
put(ch, [("evidence_chain.json", 8, True, False, CREAM_TEXT, MONO),
         ("five sections", 7.3, False, True, GRAY_TXT)])

a4 = box(35.45, 3.50, 3.85, 3.00, PEACH, PEACH_LINE, 1.5)
put(a4, [("chain auditor", 10, True, False, PEACH_DARK),
         ("4 mechanical checks", 7.8, False, False, "8A5A2A"),
         ("4 perspectives:", 7.8, True, False, "8A5A2A"),
         ("A contract", 7.8, False, False, "8A5A2A"),
         ("B physical", 7.8, False, False, "8A5A2A"),
         ("C cognition", 7.8, False, False, "8A5A2A"),
         ("D source", 7.8, False, False, "8A5A2A")], align=PP_ALIGN.LEFT)
a4.text_frame.vertical_anchor = MSO_ANCHOR.TOP
a4.text_frame.margin_left = Cm(0.24); a4.text_frame.margin_top = Cm(0.16)

vd = box(29.6, 7.70, 7.4, 1.25, LILAC, LILAC_LINE, 1.75, adj=0.30)
put(vd, [("verdict: Confirmed / Refuted", 10, True, False, LILAC_DARK),
         ("Neutral \u2192 human review", 8, False, False, "6B5C9E")])

conn(31.10, 5.00, 31.55, 5.00, tail=True)
conn(35.05, 5.00, 35.45, 5.00, tail=True)
elbow([(38.00, 6.50), (38.00, 8.32), (37.00, 8.32)])
elbow([(35.70, 6.50), (35.70, 7.00), (28.15, 7.00), (28.15, 6.50)],
      INK_SOFT, 1.3, dash=DOT)
tbox(30.55, 6.82, 2.6, 0.36, [("rebuild \u2264 3", 7.5, True, True, INK_SOFT)],
     fill=LANE[3][0])

# five-link chain pictogram under evidence_chain.json
_d, _gap, _x0, _yc = 0.40, 0.275, 31.75, 6.10
_dots = [MINT_LINE, SKY_LINE, CREAM_LINE, PINK_LINE, LILAC_LINE]
for i, dc in enumerate(_dots):
    cx = _x0 + i * (_d + _gap)
    if i:
        conn(cx - _gap, _yc, cx, _yc, INK, 1.1)
    o = shapes.add_shape(MSO_SHAPE.OVAL, Cm(cx), Cm(_yc - _d / 2), Cm(_d), Cm(_d))
    o.fill.solid(); o.fill.fore_color.rgb = C(dc)
    setline(o, INK, 1.0); o.shadow.inherit = False
# (decorative magnifier removed: every pictogram must map to a real concept)

# ================= cross-stage flows =================
elbow([(4.5, 9.10), (4.5, 10.15), (9.3, 10.15), (9.3, 4.25), (9.6, 4.25)])
tbox(4.9, 10.20, 2.0, 0.36, [("constraints", 8.5, True, False, SKY_DARK)])
elbow([(13.0, 9.20), (13.0, 10.15), (17.75, 10.15), (17.75, 5.00), (18.0, 5.00)])
tbox(13.4, 10.20, 1.2, 0.36, [("probes", 8.5, True, False, SKY_DARK)])
elbow([(20.8, 7.75), (20.8, 10.15), (24.9, 10.15), (24.9, 5.60), (25.2, 5.60)])
tbox(21.1, 10.20, 1.5, 0.36, [("outputs", 8.5, True, False, SKY_DARK)])

# ================= E2: implementation source =================
e2 = box(28.4, 10.50, 7.6, 1.50, TEAL, TEAL_LINE, 2.25)
put(e2, [("implementation source", 10.5, True, False, TEAL_DARK),
         ("pinned clone · falsification anchor \u2014", 7.8, False, True, "2A8A7A"),
         ("independent of the documentation", 7.8, False, True, "2A8A7A")])
elbow([(29.0, 10.50), (29.0, 10.05), (26.2, 10.05), (26.2, 6.50)],
      TEAL_DARK, 1.5, dash=DOT)
tbox(26.45, 9.62, 3.0, 0.36, [("source grounding", 8, True, False, TEAL_DARK)],
     align=PP_ALIGN.LEFT)
elbow([(35.2, 10.50), (35.2, 10.05), (38.6, 10.05), (38.6, 6.50)],
      TEAL_DARK, 1.5, dash=DOT)
tbox(35.45, 9.62, 3.0, 0.36, [("D perspective", 8, True, False, TEAL_DARK)],
     align=PP_ALIGN.LEFT)

# ================= running example =================
tbox(0.5, 12.42, 39.0, 0.5,
     [("Running example (Qdrant #10369): constraint qdrant_state_recommend_001 \u2192 "
       "state-agent scenario (delete\u2013recreate lookup collection at size 8) \u2192 "
       "200 with silently wrong scores, required 400 \u2192 source grounding: dimension "
       "check absent on the lookup_from path \u2192 Confirmed (maintainer accepted)",
       7, False, True, GRAY_TXT)])

OUT = r"C:\Users\11428\Desktop\testvdb_paper\figures\pipeline-style-E-cartoon.pptx"
prs.save(OUT)
print("saved", OUT)
