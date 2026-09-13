# -*- coding: utf-8 -*-
"""Generate TestVDB pipeline figure as .pptx in LQM design language."""
from pptx import Presentation
from pptx.util import Cm, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
import copy

# LQM palette
INK = RGBColor(0x1A, 0x1A, 0x1A)      # near-black text
GRAY = RGBColor(0x7F, 0x7F, 0x7F)     # secondary text
BLUE = RGBColor(0x00, 0x70, 0xC0)     # code emphasis / flow
BROWN = RGBColor(0xAC, 0x95, 0x6E)    # artifacts / files
GREEN = RGBColor(0x92, 0xD0, 0x50)    # pass / confirmed
HILITE = RGBColor(0x9D, 0xC3, 0xE6)   # highlight capsule
LINEC = RGBColor(0x40, 0x40, 0x40)    # connectors
BOX_FILL = RGBColor(0xFF, 0xFF, 0xFF)
BOX_LINE = RGBColor(0x59, 0x59, 0x59)

prs = Presentation()
prs.slide_width = Cm(40)
prs.slide_height = Cm(15)
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank

def box(x, y, w, h, lines, fill=BOX_FILL, line=BOX_LINE, lw=1.0, dash=None, round_=True):
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if round_ else MSO_SHAPE.RECTANGLE,
        Cm(x), Cm(y), Cm(w), Cm(h))
    if round_:
        try: shp.adjustments[0] = 0.10
        except Exception: pass
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    shp.line.color.rgb = line; shp.line.width = Pt(lw)
    if dash:
        ln = shp.line._get_or_add_ln()
        d = ln.makeelement(qn('a:prstDash'), {'val': dash}); ln.append(d)
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Cm(0.15); tf.margin_right = Cm(0.15)
    tf.margin_top = Cm(0.08); tf.margin_bottom = Cm(0.08)
    first = True
    for text, size, bold, color, mono in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = text
        f = r.font; f.size = Pt(size); f.bold = bold; f.color.rgb = color
        f.name = 'Consolas' if mono else 'Calibri'
    return shp

def textbox(x, y, w, h, text, size, bold, color, mono=False, align=PP_ALIGN.LEFT):
    tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = bold; f.color.rgb = color
    f.name = 'Consolas' if mono else 'Calibri'
    return tb

def arrow(x1, y1, x2, y2, color=LINEC, w=2.0, dash=None, arrowhead=True):
    conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Cm(x1), Cm(y1), Cm(x2), Cm(y2))
    conn.line.color.rgb = color; conn.line.width = Pt(w)
    conn.shadow.inherit = False
    ln = conn.line._get_or_add_ln()
    if dash:
        d = ln.makeelement(qn('a:prstDash'), {'val': dash}); ln.append(d)
    if arrowhead:
        te = ln.makeelement(qn('a:tailEnd'), {'type': 'triangle', 'w': 'med', 'len': 'med'}); ln.append(te)
    return conn

def capsule(x, y, w, h, text, size=11, fill=HILITE, line=None):
    shp = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Cm(x), Cm(y), Cm(w), Cm(h))
    try: shp.adjustments[0] = 0.5
    except Exception: pass
    shp.fill.solid(); shp.fill.fore_color.rgb = fill
    if line: shp.line.color.rgb = line; shp.line.width = Pt(0.75)
    else: shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = Cm(0.02); tf.margin_bottom = Cm(0.02)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    f = r.font; f.size = Pt(size); f.bold = True; f.color.rgb = INK; f.name = 'Calibri'
    return shp

# ---------- stage titles ----------
textbox(1.0, 0.5, 9.0, 1.0, '① Specification Extraction', 16.5, True, INK)
textbox(11.8, 0.5, 8.5, 1.0, '② Test Script Generation', 16.5, True, INK)
textbox(21.8, 0.5, 7.5, 1.0, '③ Sandboxed Execution', 16.5, True, INK)
textbox(29.6, 0.5, 9.6, 1.0, '④ Bug Confirmation', 16.5, True, INK)
textbox(29.6, 1.35, 9.6, 0.7, 'builder / auditor split', 10.5, False, GRAY)

# ---------- external input ----------
box(1.0, 2.6, 5.4, 1.5, [('API documentation', 12.5, True, INK, False),
                          ('natural-language prose', 10, False, GRAY, False)])
arrow(3.7, 4.1, 3.7, 4.9)

# ---------- stage 1 column ----------
b_kex = box(1.0, 4.9, 5.4, 1.7, [('knowledge extractor', 12.5, True, INK, False),
                                  ('Crawl4AI · coverage + version checks', 9.5, False, GRAY, False)])
b_kj = box(1.6, 7.35, 4.2, 1.1, [('knowledge.json', 12.5, True, BROWN, True)])
b_sex = box(1.0, 9.2, 5.4, 1.7, [('specification extractor', 12.5, True, INK, False),
                                  ('categorize · evidence-tier · verify source', 9.5, False, GRAY, False)])
b_sj = box(1.6, 11.6, 4.2, 1.1, [('specifications.json', 12.5, True, BROWN, True)])
arrow(3.7, 6.6, 3.7, 7.35)   # kex -> kj
arrow(3.7, 8.45, 3.7, 9.2)   # kj -> sex
arrow(3.7, 10.9, 3.7, 11.6)  # sex -> sj

# ---------- stage 2 column ----------
b_reg = box(11.8, 4.9, 5.8, 1.7, [('strategy registry', 12.5, True, INK, False),
                                   ('pre-bound: trigger → strategy', 9.5, False, GRAY, False)])
b_atk = box(11.8, 7.6, 5.8, 1.7, [('attack agents', 12.5, True, INK, False),
                                   ('boundary · state · semantic', 9.5, False, GRAY, False)])
b_scn = box(11.8, 10.3, 5.8, 1.7, [('scenario construction', 12.5, True, INK, False),
                                    ('system-level · no-match fallback', 9.5, False, GRAY, False)])
capsule(12.9, 13.0, 4.6, 1.0, '5 generation gates', 11.5)
arrow(14.7, 6.6, 14.7, 7.6)
arrow(14.7, 9.3, 14.7, 10.3)
arrow(14.7, 12.0, 14.7, 13.0)

# ---------- stage 3 ----------
b_vdb = box(21.8, 4.9, 5.6, 2.4, [('Docker-pinned VDBMS', 12.5, True, INK, False),
                                   ('target @ version', 10, False, GRAY, False),
                                   ('(no code runs inside)', 9.5, False, GRAY, False)])
b_log = box(22.3, 8.2, 4.6, 1.1, [('raw HTTP logs', 12.5, True, BROWN, True)])
textbox(22.3, 9.35, 4.6, 0.7, '+ atomic .done markers', 9.5, False, GRAY, False, align=PP_ALIGN.CENTER)
arrow(24.6, 7.3, 24.6, 8.2)

# ---------- stage 4 ----------
b_eb = box(29.6, 2.6, 6.2, 4.6, [
    ('evidence builder', 12.5, True, INK, False),
    ('doc verification', 10, False, INK, False),
    ('execution evidence', 10, False, INK, False),
    ('contract grounding', 10, False, INK, False),
    ('chain trace', 10, False, INK, False),
    ('source grounding', 10, False, INK, False)])
b_ca = box(36.6, 2.6, 3.0, 4.6, [
    ('chain', 12.5, True, INK, False),
    ('auditor', 12.5, True, INK, False),
    ('4 checks', 10, False, GRAY, False),
    ('A contract', 10, False, INK, False),
    ('B physical', 10, False, INK, False),
    ('C cognition', 10, False, INK, False),
    ('D source', 10, False, INK, False)])
b_chain = box(33.2, 7.6, 3.6, 1.1, [('evidence_chain.json', 11.5, True, BROWN, True)])
b_verdict = box(30.3, 9.6, 6.6, 1.7, [('verdict: Confirmed / Refuted', 12, True, INK, False),
                                       ('Neutral → human review', 10, False, GRAY, False)])
arrow(32.7, 7.2, 34.0, 7.6)          # eb -> chain
arrow(35.8, 8.4, 36.4, 7.2)          # chain -> ca (up-right)
arrow(37.9, 7.2, 36.5, 9.6)          # ca -> verdict
arrow(34.0, 5.6, 36.6, 5.6, dash='dash')  # rebuild (eb<-ca dashed)
textbox(34.0, 5.9, 3.0, 0.6, 'rebuild ≤3', 9.5, False, GRAY, align=PP_ALIGN.CENTER)

# ---------- implementation source ----------
b_src = box(29.6, 12.4, 6.6, 1.4, [('implementation source (pinned clone)', 11.5, True, BLUE, False)],
            fill=RGBColor(0xEE, 0xF4, 0xFB), line=BLUE, lw=1.2)
textbox(36.4, 12.75, 3.4, 0.9, 'falsification\nanchor', 9.5, True, BLUE)
arrow(33.0, 12.4, 33.3, 11.3, color=BLUE, w=1.75)      # src -> verdict area
arrow(36.8, 12.4, 37.9, 7.2, color=BLUE, w=1.75, dash='sysDash')  # src -> ca

# ---------- inter-stage flows ----------
arrow(6.4, 12.15, 11.8, 8.6)   # sj -> registry
textbox(7.4, 11.1, 3.2, 0.7, 'constraints', 10, True, BLUE)
arrow(17.6, 8.45, 21.8, 6.2)   # atk/gates -> vdb
textbox(18.7, 7.4, 2.6, 0.7, 'probes', 10, True, BLUE)
arrow(26.9, 8.75, 29.6, 5.2)   # logs -> eb
textbox(27.2, 6.9, 3.0, 0.7, 'outputs', 10, True, BLUE)

prs.save(r'C:\Users\11428\Desktop\testvdb_paper\figures\pipeline-v5.pptx')
print('saved figures/pipeline-v5.pptx')
