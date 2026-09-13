# -*- coding: utf-8 -*-
"""Figure 1 style variants for TestVDB pipeline hero figure.

Geometry is identical to pipeline-v6 (already validated); only the visual
language differs.  Four styles:

  A  wireframe   -- minimal monochrome, hairline gray rules, print-safest
  B  lanes       -- soft tinted stage lanes + left accent bars (modern LLM-paper look)
  C  scholarly   -- single blue-gray ramp, density encodes node type (top-conf sober)
  D  tikz        -- square corners, hairline black, double-ruled artifacts (LaTeX-native look)

Outputs per style: <name>.pptx  and  <name>.png (4724x1572 px).
"""
import sys
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.oxml.ns import qn
from pptx.enum.dml import MSO_LINE_DASH_STYLE

DASH = MSO_LINE_DASH_STYLE.DASH
MONO = "Consolas"
OUT = r"C:\Users\11428\Desktop\testvdb_paper\figures"

STYLES = {
    "A": dict(
        name="wireframe",
        rounded=True, adj=0.08, lw=0.75, lw_main=0.9,
        stage_fill="FFFFFF", stage_line="BFBFBF", stage_lw=0.75, accent=None,
        stage_dash=True, title="000000",
        node_fill="FFFFFF", node_line="595959", node_lw=0.9,
        node_text="000000", node_sub="7F7F7F", node_sub_it=True,
        art_fill="FFFFFF", art_line="404040", art_lw=1.1, art_double=True,
        art_text="000000", art_sub="7F7F7F",
        gate_fill="F2F2F2", gate_line="595959", gate_lw=0.9, gate_text="000000",
        bld_fill="FFFFFF", bld_line="595959", bld_lw=0.9, bld_text="000000", bld_item="404040",
        aud_fill="FFFFFF", aud_line="595959", aud_lw=0.9, aud_text="000000", aud_item="404040",
        vd_fill="FFFFFF", vd_line="000000", vd_lw=1.25,
        e1_fill="FAFAFA", e1_line="7F7F7F", e1_lw=0.9,
        e2_fill="FFFFFF", e2_line="000000", e2_lw=1.75, e2_text="000000", e2_sub="000000",
        main="404040", flow_label="000000", loop="7F7F7F", accent_line="000000",
        accent_dash=DASH, gray="595959",
    ),
    "B": dict(
        name="lanes",
        rounded=True, adj=0.12, lw=0.75, lw_main=1.1,
        stage_fill="F7FAFD", stage_line="D6E3F0", stage_lw=0.75, accent="4472A4",
        stage_dash=False, title="1F3864",
        node_fill="FFFFFF", node_line="8FA9C4", node_lw=0.9,
        node_text="1F3864", node_sub="7F8C99", node_sub_it=True,
        art_fill="FFF8EA", art_line="E0BE86", art_lw=0.9, art_double=False,
        art_text="8A6D3B", art_sub="9C8461",
        gate_fill="9DC3E6", gate_line="2E75B6", gate_lw=0.9, gate_text="1F3864",
        bld_fill="F1F8F1", bld_line="A8CFA8", bld_lw=0.9, bld_text="1E4620", bld_item="375623",
        aud_fill="FEF6EA", aud_line="EFC79A", aud_lw=0.9, aud_text="7F4F10", aud_item="7F4F10",
        vd_fill="FFFFFF", vd_line="2E75B6", vd_lw=1.25,
        e1_fill="F5F5F5", e1_line="A6A6A6", e1_lw=0.9,
        e2_fill="DDEBF7", e2_line="2E75B6", e2_lw=1.75, e2_text="1F3864", e2_sub="7030A0",
        main="4A5A6A", flow_label="0070C0", loop="8C8C8C", accent_line="7030A0",
        accent_dash=DASH, gray="7F8C99",
    ),
    "C": dict(
        name="scholarly",
        rounded=True, adj=0.06, lw=0.75, lw_main=1.0,
        stage_fill="EEF2F7", stage_line="9FB3C8", stage_lw=0.75, accent="2F5597",
        stage_dash=False, title="1B2A41",
        node_fill="FFFFFF", node_line="6C8EBF", node_lw=1.0,
        node_text="1B2A41", node_sub="5B7089", node_sub_it=True,
        art_fill="DCE6F1", art_line="6C8EBF", art_lw=1.0, art_double=False,
        art_text="1B2A41", art_sub="44546A",
        gate_fill="2F5597", gate_line="1B3A6B", gate_lw=1.0, gate_text="FFFFFF",
        bld_fill="FFFFFF", bld_line="2F5597", bld_lw=1.25, bld_text="1B2A41", bld_item="2F5597",
        aud_fill="B8CCE4", aud_line="1B3A6B", aud_lw=1.25, aud_text="1B2A41", aud_item="1B2A41",
        vd_fill="1B3A6B", vd_line="12284A", vd_lw=1.25,
        e1_fill="F5F7FA", e1_line="8496AB", e1_lw=1.0,
        e2_fill="2F5597", e2_line="1B3A6B", e2_lw=1.75, e2_text="FFFFFF", e2_sub="D6E0F0",
        main="2F5597", flow_label="1B3A6B", loop="8496AB", accent_line="1B3A6B",
        accent_dash=DASH, gray="5B7089",
    ),
    "D": dict(
        name="tikz",
        rounded=False, adj=0.0, lw=0.75, lw_main=0.85,
        stage_fill="F7F7F7", stage_line="000000", stage_lw=0.75, accent=None,
        stage_dash=False, title="000000",
        node_fill="FFFFFF", node_line="000000", node_lw=0.75,
        node_text="000000", node_sub="000000", node_sub_it=True,
        art_fill="FFFFFF", art_line="000000", art_lw=0.75, art_double=True,
        art_text="000000", art_sub="000000",
        gate_fill="E8E8E8", gate_line="000000", gate_lw=0.75, gate_text="000000",
        bld_fill="FFFFFF", bld_line="000000", bld_lw=0.75, bld_text="000000", bld_item="000000",
        aud_fill="EFEFEF", aud_line="000000", aud_lw=0.75, aud_text="000000", aud_item="000000",
        vd_fill="FFFFFF", vd_line="000000", vd_lw=1.0,
        e1_fill="FFFFFF", e1_line="000000", e1_lw=0.75,
        e2_fill="FFFFFF", e2_line="000000", e2_lw=1.5, e2_text="000000", e2_sub="000000",
        main="000000", flow_label="000000", loop="000000", accent_line="000000",
        accent_dash=DASH, gray="000000",
    ),
}

LANE_TINTS = {"B": ["EEF4FB", "EAF6F6", "F0F7EC", "FBF4EA"]}


def build(skey):
    s = STYLES[skey]
    prs = Presentation()
    prs.slide_width = Cm(40)
    prs.slide_height = Cm(13.3)
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    shapes = slide.shapes

    def setline(sp, hexc, w, dash=None):
        sp.line.color.rgb = RGBColor.from_string(hexc)
        sp.line.width = Pt(w)
        if dash:
            sp.line.dash_style = dash

    def box(x, y, w, h, fill, line, lw, rounded=None, shape=None, dash=None):
        rounded = s["rounded"] if rounded is None else rounded
        st = shape if shape else (MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE)
        sp = shapes.add_shape(st, Cm(x), Cm(y), Cm(w), Cm(h))
        if rounded and st == MSO_SHAPE.ROUNDED_RECTANGLE:
            try:
                sp.adjustments[0] = s["adj"]
            except Exception:
                pass
        if fill is None:
            sp.fill.background()
        else:
            sp.fill.solid()
            sp.fill.fore_color.rgb = RGBColor.from_string(fill)
        setline(sp, line, lw, dash)
        sp.shadow.inherit = False
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
            font = it[5] if len(it) > 5 else None
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            p.alignment = align
            p.space_before = Pt(0); p.space_after = Pt(0); p.line_spacing = 1.0
            r = p.add_run(); r.text = text
            r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
            r.font.color.rgb = RGBColor.from_string(color)
            if font:
                r.font.name = font
        return sp

    def tbox(x, y, w, h, items, align=PP_ALIGN.CENTER, fill=None):
        tb = shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = Cm(0.03); tf.margin_right = Cm(0.03)
        tf.margin_top = Cm(0.0); tf.margin_bottom = Cm(0.0)
        if fill:
            tb.fill.solid(); tb.fill.fore_color.rgb = RGBColor.from_string(fill)
        else:
            tb.fill.background()
        tb.line.fill.background()
        tb.shadow.inherit = False
        return put(tb, items, align)

    def conn(x1, y1, x2, y2, color, w, dash=None, tail=False):
        c = shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Cm(x1), Cm(y1), Cm(x2), Cm(y2))
        setline(c, color, w, dash)
        c.shadow.inherit = False
        if tail:
            ln = c.line._get_or_add_ln()
            ln.append(ln.makeelement(qn('a:tailEnd'),
                                     {'type': 'triangle', 'w': 'med', 'len': 'med'}))
        return c

    def elbow(pts, color, w, dash=None):
        for i in range(len(pts) - 1):
            conn(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                 color, w, dash, tail=(i == len(pts) - 2))

    M, LM, LP, GR = s["main"], s["flow_label"], s["accent_line"], s["loop"]
    W = s["lw_main"]

    # ---- top: external input E1 + automation legend ----
    tbox(23.6, 0.45, 15.9, 0.5,
         [("reading · generation · adjudication by LLM agents · execution & checks deterministic",
           8, False, True, s["gray"])], align=PP_ALIGN.RIGHT)
    e1 = box(2.0, 0.35, 8.6, 1.35, s["e1_fill"], s["e1_line"], s["e1_lw"])
    put(e1, [("API documentation", 10.5, True, False, s["node_text"]),
             ("natural-language prose", 8, False, False, s["node_sub"])])
    elbow([(6.3, 1.70), (6.3, 1.98), (4.5, 1.98), (4.5, 2.30)], M, W)

    # ---- stage containers ----
    ST_Y, ST_H = 2.30, 7.60
    stages = [(0.5, 8.0, u"\u2460 Behavioral Specification Extraction"),
              (9.0, 8.0, u"\u2461 Test Script Generation"),
              (17.5, 6.6, u"\u2462 Sandboxed Execution"),
              (24.6, 14.9, u"\u2463 Bug Confirmation \u2014 builder / auditor split")]
    for i, (sx, sw, title) in enumerate(stages):
        fill = s["stage_fill"]
        if skey == "B":
            fill = LANE_TINTS["B"][i]
        st = box(sx, ST_Y, sw, ST_H, fill, s["stage_line"], s["stage_lw"],
                 dash=DASH if s["stage_dash"] else None)
        put(st, [(title, 11.5, True, False, s["title"])], align=PP_ALIGN.LEFT)
        st.text_frame.vertical_anchor = MSO_ANCHOR.TOP
        st.text_frame.margin_left = Cm(0.35 if s["accent"] else 0.3)
        st.text_frame.margin_top = Cm(0.12)
        if s["accent"]:
            bar = shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(sx), Cm(ST_Y), Cm(0.16), Cm(ST_H))
            bar.fill.solid(); bar.fill.fore_color.rgb = RGBColor.from_string(s["accent"])
            bar.line.fill.background(); bar.shadow.inherit = False

    # ---- stage 1 ----
    t1 = box(1.1, 3.60, 6.8, 1.30, s["node_fill"], s["node_line"], s["node_lw"])
    put(t1, [("knowledge extractor", 10, True, False, s["node_text"]),
             ("Crawl4AI · coverage + version checks", 7.8, False, s["node_sub_it"], s["node_sub"])])
    a1 = box(1.1, 5.20, 6.8, 0.85, s["art_fill"], s["art_line"], s["art_lw"])
    put(a1, [("knowledge.json", 9.5, True, False, s["art_text"], MONO)])
    t2 = box(1.1, 6.35, 6.8, 1.30, s["node_fill"], s["node_line"], s["node_lw"])
    put(t2, [("specification extractor", 10, True, False, s["node_text"]),
             ("categorize · evidence-tier · verify source", 7.8, False, s["node_sub_it"], s["node_sub"])])
    a2 = box(1.1, 7.95, 6.8, 1.15, s["art_fill"], s["art_line"], s["art_lw"])
    put(a2, [("specifications.json", 9.5, True, False, s["art_text"], MONO),
             ("typed · tiered · source-verified · level", 7.5, False, True, s["art_sub"])])
    for y1, y2 in [(4.90, 5.20), (6.05, 6.35), (7.65, 7.95)]:
        conn(4.5, y1, 4.5, y2, M, W, tail=True)

    # ---- stage 2 ----
    g1 = box(9.6, 3.60, 6.8, 1.30, s["node_fill"], s["node_line"], s["node_lw"])
    put(g1, [("strategy registry", 10, True, False, s["node_text"]),
             ("pre-bound: trigger \u2192 strategy", 7.8, False, s["node_sub_it"], s["node_sub"])])
    g2 = box(9.6, 5.20, 6.8, 1.30, s["node_fill"], s["node_line"], s["node_lw"])
    put(g2, [("attack agents", 10, True, False, s["node_text"]),
             ("boundary · state · semantic", 8, False, False, s["node_sub"])])
    g3 = box(9.6, 6.80, 6.8, 1.30, s["node_fill"], s["node_line"], s["node_lw"])
    put(g3, [("scenario construction", 10, True, False, s["node_text"]),
             ("system-level · no-match fallback", 7.8, False, s["node_sub_it"], s["node_sub"])])
    gt = box(9.9, 8.30, 6.2, 0.90, s["gate_fill"], s["gate_line"], s["gate_lw"])
    put(gt, [("5 generation gates", 9.5, True, False, s["gate_text"])])
    for y1, y2 in [(4.90, 5.20), (6.50, 6.80), (8.10, 8.30)]:
        conn(13.0, y1, 13.0, y2, M, W, tail=True)

    # ---- stage 3 ----
    cy = box(18.0, 4.00, 5.6, 2.00, s["node_fill"], s["node_line"], s["node_lw"],
             rounded=False, shape=MSO_SHAPE.CAN)
    put(cy, [("Docker-pinned VDBMS", 9.5, True, False, s["node_text"]),
             ("target @ version", 8, False, True, s["node_sub"])])
    a3 = box(18.0, 6.60, 5.6, 1.15, s["art_fill"], s["art_line"], s["art_lw"])
    put(a3, [("raw HTTP logs", 9.5, True, False, s["art_text"], MONO),
             ("+ atomic .done markers", 7.5, False, True, s["art_sub"])])
    conn(20.8, 6.00, 20.8, 6.60, M, W, tail=True)

    # ---- stage 4 ----
    b4 = box(25.2, 3.50, 5.9, 3.00, s["bld_fill"], s["bld_line"], s["bld_lw"])
    put(b4, [("evidence builder", 10, True, False, s["bld_text"])] +
            [(u"· " + t, 7.8, False, False, s["bld_item"]) for t in
             ("doc verification", "execution evidence", "contract grounding",
              "chain trace", "source grounding (grep clone)")], align=PP_ALIGN.LEFT)
    b4.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    b4.text_frame.margin_left = Cm(0.25); b4.text_frame.margin_top = Cm(0.15)
    ch = box(31.55, 4.35, 3.50, 1.30, s["art_fill"], s["art_line"], s["art_lw"])
    put(ch, [("evidence_chain.json", 8, True, False, s["art_text"], MONO),
             ("five sections", 7.3, False, True, s["art_sub"])])
    a4 = box(35.45, 3.50, 3.60, 3.00, s["aud_fill"], s["aud_line"], s["aud_lw"])
    put(a4, [("chain auditor", 10, True, False, s["aud_text"]),
             ("4 mechanical checks", 7.8, False, False, s["aud_item"]),
             ("4 perspectives:", 7.8, False, False, s["aud_item"]),
             ("A contract · B physical", 7.8, False, False, s["aud_item"]),
             ("C cognition · D source", 7.8, False, False, s["aud_item"])],
        align=PP_ALIGN.LEFT)
    a4.text_frame.vertical_anchor = MSO_ANCHOR.TOP
    a4.text_frame.margin_left = Cm(0.2); a4.text_frame.margin_top = Cm(0.15)
    vd = box(29.6, 7.70, 7.4, 1.25, s["vd_fill"], s["vd_line"], s["vd_lw"])
    vtext = "FFFFFF" if skey == "C" else s["node_text"]
    vsub = "D6E0F0" if skey == "C" else s["node_sub"]
    put(vd, [("verdict: Confirmed / Refuted", 10, True, False, vtext),
             ("Neutral \u2192 human review", 8, False, False, vsub)])
    conn(31.10, 5.00, 31.55, 5.00, M, W, tail=True)
    conn(35.05, 5.00, 35.45, 5.00, M, W, tail=True)
    elbow([(38.00, 6.50), (38.00, 8.32), (37.00, 8.32)], M, W)
    elbow([(35.70, 6.50), (35.70, 7.00), (28.15, 7.00), (28.15, 6.50)],
          GR, W, dash=DASH)
    tbox(30.55, 6.82, 2.6, 0.36, [("rebuild \u2264 3", 7.5, False, True, GR)],
         fill=s["stage_fill"] if skey != "B" else LANE_TINTS["B"][3])

    # ---- double-ruled artifacts (style A / D) ----
    if s["art_double"]:
        for (x, y, w, h) in [(1.1, 5.20, 6.8, 0.85), (1.1, 7.95, 6.8, 1.15),
                             (18.0, 6.60, 5.6, 1.15), (31.55, 4.35, 3.50, 1.30)]:
            inner = shapes.add_shape(MSO_SHAPE.RECTANGLE, Cm(x + 0.07), Cm(y + 0.07),
                                     Cm(w - 0.14), Cm(h - 0.14))
            inner.fill.background()
            setline(inner, s["art_line"], 0.6)
            inner.shadow.inherit = False

    # ---- cross-stage flows ----
    elbow([(4.5, 9.10), (4.5, 10.15), (9.3, 10.15), (9.3, 4.25), (9.6, 4.25)], M, W)
    tbox(4.9, 10.20, 2.0, 0.36, [("constraints", 8.5, True, False, LM)])
    elbow([(13.0, 9.20), (13.0, 10.15), (17.75, 10.15), (17.75, 5.00), (18.0, 5.00)], M, W)
    tbox(13.4, 10.20, 1.2, 0.36, [("probes", 8.5, True, False, LM)])
    elbow([(20.8, 7.75), (20.8, 10.15), (24.9, 10.15), (24.9, 5.60), (25.2, 5.60)], M, W)
    tbox(21.1, 10.20, 1.5, 0.36, [("outputs", 8.5, True, False, LM)])

    # ---- E2: implementation source ----
    e2 = box(28.4, 10.50, 7.6, 1.50, s["e2_fill"], s["e2_line"], s["e2_lw"])
    put(e2, [("implementation source", 10.5, True, False, s["e2_text"]),
             ("pinned clone · falsification anchor \u2014", 7.8, False, True, s["e2_sub"]),
             ("independent of the documentation", 7.8, False, True, s["e2_sub"])])
    elbow([(29.0, 10.50), (29.0, 10.05), (26.2, 10.05), (26.2, 6.50)],
          LP, W, dash=s["accent_dash"])
    tbox(26.45, 9.62, 3.0, 0.36, [("source grounding", 8, True, False, LP)],
         align=PP_ALIGN.LEFT)
    elbow([(35.2, 10.50), (35.2, 10.05), (38.6, 10.05), (38.6, 6.50)],
          LP, W, dash=s["accent_dash"])
    tbox(35.45, 9.62, 3.0, 0.36, [("D perspective", 8, True, False, LP)],
         align=PP_ALIGN.LEFT)

    # ---- running example ----
    tbox(0.5, 12.45, 39.0, 0.5,
         [("Running example (Qdrant #10369):  constraint qdrant_state_recommend_001 \u2192 "
           "state-agent scenario (delete\u2013recreate lookup collection at size 8) \u2192 "
           "200 with silently wrong scores vs. required 400 \u2192 source grounding finds the "
           "dimension check absent on the lookup_from path \u2192 Confirmed (maintainer accepted)",
           7.5, False, True, s["gray"])])

    path = OUT + "\\pipeline-style-%s-%s.pptx" % (skey, s["name"])
    prs.save(path)
    return path, s["name"]


if __name__ == "__main__":
    for k in ("A", "B", "C", "D"):
        p, n = build(k)
        print(p)
