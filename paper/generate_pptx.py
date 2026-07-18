#!/usr/bin/env python3
"""Generate a 28-page GEAR-style .pptx for TestVDB (compressed from 34).

Merges: P7-P9 (naive oracles)→1 table; P16+P17→1; P18+P19→1; P22 cut; P25+P26→1.
Output: paper/TestVDB_slides.pptx (28 slides, 16:9).
"""
from __future__ import annotations
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

FIG = os.path.join(os.path.dirname(__file__), "figures")
OUT = os.path.join(os.path.dirname(__file__), "TestVDB_slides.pptx")
CJK = "微软雅黑"

HEADER_BG = RGBColor(0x1B, 0x3A, 0x5C)
ACCENT_BLUE = RGBColor(0x2E, 0x5C, 0x8A); ACCENT_ORANGE = RGBColor(0xD9, 0x8E, 0x48)
ACCENT_GREEN = RGBColor(0x4A, 0x8C, 0x5C); ACCENT_RED = RGBColor(0xB0, 0x50, 0x50)
TEXT_DARK = RGBColor(0x33, 0x33, 0x33); TEXT_GREY = RGBColor(0x66, 0x66, 0x66)
LIGHT_BG = RGBColor(0xF0, 0xF4, 0xF8); WHITE = RGBColor(0xFF, 0xFF, 0xFF)

prs = Presentation()
prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def header(slide, title, num, section):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, Inches(1.05))
    bar.fill.solid(); bar.fill.fore_color.rgb = HEADER_BG; bar.line.fill.background()
    tb = slide.shapes.add_textbox(Inches(0.45), Inches(0.12), Inches(10.5), Inches(0.85))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.text = title; p.font.size = Pt(22); p.font.bold = True; p.font.color.rgb = WHITE
    pb = slide.shapes.add_textbox(Inches(10.8), Inches(0.12), Inches(2.3), Inches(0.45))
    pp = pb.text_frame.paragraphs[0]; pp.text = f"P{num} / 28  {section}"; pp.alignment = PP_ALIGN.RIGHT
    pp.font.size = Pt(11); pp.font.color.rgb = RGBColor(0xBB, 0xCC, 0xDD)
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(1.05), prs.slide_width, Inches(0.06))
    strip.fill.solid(); strip.fill.fore_color.rgb = ACCENT_ORANGE; strip.line.fill.background()

def bullets(slide, items, top=1.5, left=0.7, width=12, height=5.5, size=16):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame; tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        text, color = (item if isinstance(item, tuple) else (item, TEXT_DARK))
        p.text = "•  " + text; p.font.size = Pt(size); p.font.color.rgb = color; p.space_after = Pt(10)

def table(slide, headers, rows, top=1.5, left=0.6, width=12.1, height=5.2):
    nrows = len(rows) + 1; ncols = len(headers)
    g = slide.shapes.add_table(nrows, ncols, Inches(left), Inches(top), Inches(width), Inches(height)).table
    g.first_row = True; g.horz_banding = False
    for j, h in enumerate(headers):
        c = g.cell(0, j); c.text = h; c.fill.solid(); c.fill.fore_color.rgb = ACCENT_BLUE
        for p in c.text_frame.paragraphs:
            p.font.bold = True; p.font.size = Pt(13); p.font.color.rgb = WHITE; p.alignment = PP_ALIGN.CENTER
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            c = g.cell(i + 1, j); c.text = str(val); c.fill.solid()
            c.fill.fore_color.rgb = LIGHT_BG if i % 2 == 0 else WHITE
            for p in c.text_frame.paragraphs:
                p.font.size = Pt(11.5); p.font.color.rgb = TEXT_DARK

def image(slide, name, top=1.35, left=1.4, width=10.5):
    slide.shapes.add_picture(os.path.join(FIG, name), Inches(left), Inches(top), Inches(width))

def big_number(slide, number, label, sub=None, top=2.2):
    tb = slide.shapes.add_textbox(Inches(1), Inches(top), Inches(11.3), Inches(2.5))
    p = tb.text_frame.paragraphs[0]; p.text = number; p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(96); p.font.bold = True; p.font.color.rgb = ACCENT_ORANGE
    lb = slide.shapes.add_textbox(Inches(1), Inches(top + 2.3), Inches(11.3), Inches(1))
    lp = lb.text_frame.paragraphs[0]; lp.text = label; lp.alignment = PP_ALIGN.CENTER; lp.font.size = Pt(20); lp.font.color.rgb = TEXT_DARK
    if sub:
        sb = slide.shapes.add_textbox(Inches(1), Inches(top + 3.1), Inches(11.3), Inches(1))
        sp = sb.text_frame.paragraphs[0]; sp.text = sub; sp.alignment = PP_ALIGN.CENTER; sp.font.size = Pt(14); sp.font.color.rgb = TEXT_GREY

def two_col(slide, lt, li, rt, ri, lc=ACCENT_RED, rc=ACCENT_GREEN):
    lb = slide.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(6), Inches(0.6))
    lp = lb.text_frame.paragraphs[0]; lp.text = lt; lp.font.size = Pt(16); lp.font.bold = True; lp.font.color.rgb = lc
    bullets(slide, li, top=2.0, left=0.7, width=5.8, height=4.8, size=14)
    dv = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(1.6), Inches(0.04), Inches(5))
    dv.fill.solid(); dv.fill.fore_color.rgb = RGBColor(0xDD, 0xDD, 0xDD); dv.line.fill.background()
    rb = slide.shapes.add_textbox(Inches(6.9), Inches(1.4), Inches(6), Inches(0.6))
    rp = rb.text_frame.paragraphs[0]; rp.text = rt; rp.font.size = Pt(16); rp.font.bold = True; rp.font.color.rgb = rc
    bullets(slide, ri, top=2.0, left=7.0, width=5.8, height=4.8, size=14)

def slide(num, section, title):
    s = prs.slides.add_slide(BLANK); header(s, title, num, section); return s

# === 28 slides ===

# P1 title
s = prs.slides.add_slide(BLANK)
bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
bg.fill.solid(); bg.fill.fore_color.rgb = HEADER_BG; bg.line.fill.background()
tb = s.shapes.add_textbox(Inches(0.8), Inches(2.4), Inches(11.7), Inches(2.2))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.text = "TestVDB"; p.font.size = Pt(54); p.font.bold = True; p.font.color.rgb = WHITE
p2 = tf.add_paragraph(); p2.text = "Source-Grounded Falsification of LLM-Derived Behavioral Claims for Documentation-Implementation Consistency Testing of Vector Databases"
p2.font.size = Pt(22); p2.font.color.rgb = RGBColor(0xCC, 0xDD, 0xEE)
meta = s.shapes.add_textbox(Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.5))
for i, line in enumerate(["Authors (TBD)", "Affiliation", "Venue / Session (TBD)"]):
    p = meta.text_frame.paragraphs[0] if i == 0 else meta.text_frame.add_paragraph()
    p.text = line; p.font.size = Pt(16); p.font.color.rgb = RGBColor(0xAA, 0xCC, 0xDD)

# P2-P3 opening
s = slide(2, "Opening", "VDBMSs store the embeddings that retrieval-augmented LLMs depend on")
image(s, "fig1_rag_arch.png", top=1.6, left=1.5, width=10.3)

s = slide(3, "Opening", "VDBMS defects are costly, and most are functional")
table(s, ["Source", "Finding"],
      [["Empirical bug study (Xie et al. 2025)", "> 50% of VDBMS bugs are functional failures"],
       ["Testing roadmap (Wang et al. 2025)", "~43% attributed to incorrect behavior; oracle is a key challenge"],
       ["VDBFuzz (Wang et al. 2026)", "only dedicated VDBMS fuzzer — uses crash as oracle"]], top=2.0)

# P4-P6 problem
s = slide(4, "Problem", "Documentation-implementation defects: the API silently accepts what the docs prescribe rejecting")
bullets(s, [
    ("Documentation-implementation consistency — does the API's accept/reject behavior match its documentation?", TEXT_DARK),
    ("Correctness — is a returned result mathematically right (ANN recall, ranking)?", TEXT_DARK),
    ("TestVDB targets documentation-implementation consistency; result correctness remains open.", TEXT_DARK),
    ("The documented boundary is natural-language prose, not a formal grammar.", ACCENT_ORANGE),
])

s = slide(5, "Problem", "A negative score threshold disables a filter and returns all matches")
image(s, "fig2_cases.png", top=1.5, left=1.2, width=11)

s = slide(6, "Problem", "37 of 38 acknowledged defects do not crash, so fuzzers miss them")
big_number(s, "37 / 38", "acknowledged defects produce no crash",
           "crash-based fuzzers (e.g. VDBFuzz) cannot reach this class")

# P7 merged naive oracles (was P7-P9)
s = slide(7, "Naive oracles", "Three classical oracles cannot reach the documentation-implementation residual")
table(s, ["Oracle", "What it catches", "Why it misses the residual"],
      [["Differential testing", "math invariants across vendors", "cross-vendor accept/reject diverges by design; no reference"],
       ["Metamorphic relations", "result correctness (top-k, recall)", "output relation, not input-acceptance decision"],
       ["Property-based testing", "math + schema (if OpenAPI)", "needs machine-checkable property + OpenAPI; VDBMS serves none"]])

# P8 Table 1 recap
s = slide(8, "Naive oracles", "The documentation-implementation residual leaves only an LLM as the practical oracle")
table(s, ["Candidate oracle", "Reaches", "Why it misses the residual"],
      [["Crash (VDBFuzz)", "crash / hang", "37 of 38 acknowledged do not crash"],
       ["Differential testing", "math invariants across vendors", "accept/reject diverges by design"],
       ["Metamorphic relations", "result correctness", "output relation, not input-acceptance"],
       ["Property-based testing", "math + schema", "needs machine-checkable property + OpenAPI"],
       ["REST doc/spec oracles", "status / field assertions", "reliable from low-ambiguity structured sources"],
       ["LLM-derived oracle (TestVDB)", "accept/reject vs API documentation", "residual needs semantic judgment"]])

# P9-P13 core insight
s = slide(9, "Core insight", "But an LLM oracle is unreliable in two distinct ways")
bullets(s, [
    ("Layer 1 — family-specific: judge confirms the extractor's biases (self-preference)", ACCENT_BLUE),
    ("Layer 2 — task-intrinsic: different families infer the same wrong claim (doc ambiguity)", ACCENT_ORANGE),
    ("cross-model validation mitigates layer 1 only", TEXT_DARK),
    ("source-grounded falsification resolves layer 2 (and also covers layer 1)", ACCENT_GREEN),
])

s = slide(10, "Core insight", "The source-ambiguity gap: structured sources yield assertions, ambiguous docs yield claims")
image(s, "fig3_source_ambiguity_gap.png", top=1.3, left=0.8, width=11.7)

s = slide(11, "Core insight", "Family-specific errors: the judge confirms the extractor's biases")
bullets(s, [
    "when one LLM family both extracts claims and judges conformance, the two roles share biases",
    "the judge tends to confirm the extractor's errors — self-preference phenomenon",
    "instance: Panickssery et al. (2024); Wataoka & Takahashi (2024)",
    ("mitigation: cross-model validation — a second family judges", ACCENT_GREEN),
])

s = slide(12, "Core insight", "Task-intrinsic errors: different families infer the same wrong claim")
image(s, "fig4_two_layer_venn.png", top=1.3, left=0.9, width=11.5)

s = slide(13, "Core insight", "Cross-model validation covers family-specific, not task-intrinsic")
two_col(s, "family-specific",
        ["consistencyLevel — GLM strict enum, DeepSeek disagrees", "cross-model catches the divergence"],
        "task-intrinsic",
        ["timeout — GLM and DeepSeek both extract '>= 1'", "cross-model sees agreement (both wrong)", "only source falsifies"],
        lc=ACCENT_BLUE, rc=ACCENT_ORANGE)

# P14 merged evidence + transition (was P16+P17)
s = slide(14, "Evidence", "On 12 over-strict parameter clauses: cross-model catches 7, source catches 12 — the residual needs the implementation")
table(s, ["Over-strict clause", "TI", "Cross-model", "Source"],
      [["shardsNum >= 1", "yes", "missed", "caught"],
       ["metricType strict enum", "no", "missed", "caught"],
       ["consistencyLevel strict enum", "no", "caught", "caught"],
       ["data non-empty", "yes", "missed", "caught"],
       ["limit >= 1", "no", "caught", "caught"],
       ["timeout >= 1 (Qdrant)", "yes", "caught", "caught"],
       ["group_size >= 1 (Qdrant)", "yes", "missed", "caught"],
       ["score_threshold in [0,1] (Qdrant)", "yes", "missed", "caught"],
       ["Total", "5", "7 / 12", "12 / 12"]], top=1.4, height=5.0)
note = s.shapes.add_textbox(Inches(0.6), Inches(6.6), Inches(12), Inches(0.6))
nt = note.text_frame.paragraphs[0]
nt.text = "Extended to n=29 (behavior + explicit-bound subtypes); see P23. Source = the implementation, the most accessible ground truth."
nt.font.size = Pt(11); nt.font.color.rgb = TEXT_GREY

# P15-P16 pipeline (merged P18+P19 → 1; P20 → 1)
s = slide(15, "Method", "TestVDB pipeline: extract claims, judge, falsify against source")
image(s, "fig5_pipeline.png", top=1.4, left=0.5, width=12.3)

s = slide(16, "Method", "A novelty gate removes duplicates and known issues — full 5-stage pipeline")
bullets(s, [
    "five-stage pipeline: extract -> attack -> judge -> dev-review (source falsify) -> novelty",
    "dev-reviewer applies three anchors: clean reproduction, source-grounding (primary), threat-model cross-check",
    "runs as a multi-agent system on the Claude Code runtime; ~$10^4 LLM calls, ~$10/target",
])

# P17 falsification rule
s = slide(17, "Method", "The falsification rule: if source shows shardsNum=0 selects the default, the over-strict clause is falsified")
two_col(s, "Over-strict clause (from LLM)",
        ["shardsNum >= 1", "probe: create collection shardsNum=0 -> API returns 200", "LLM verdict: 'violation'"],
        "Source-grounded falsification",
        ["source: if shardsNum == 0 { use default }", "0 selects the default — clause is over-strict", "verdict falsified -> FP killed", "opposite of MASTOR (as currently designed)"],
        lc=ACCENT_RED, rc=ACCENT_GREEN)

# P18-P24 evaluation
s = slide(18, "Evaluation", "Four research questions")
table(s, ["RQ", "Question"],
      [["RQ1", "how many documentation-implementation defects does TestVDB surface?"],
       ["RQ2", "does source-grounded falsification suppress false positives?"],
       ["RQ3", "can cross-model validation resolve task-intrinsic errors, or is source needed?"],
       ["RQ4", "does the model-free invariant subclass find real bugs on its own?"]])

s = slide(19, "Evaluation", "Five VDBMSs; 111 submitted, 38 acknowledged")
table(s, ["VDBMS", "Submitted", "Acknowledged"],
      [["Milvus", "51", "22"], ["Weaviate", "30", "3"], ["Qdrant", "26", "13"],
       ["MeiliSearch", "3", "0"], ["Chroma", "1", "0"], ["Total", "111", "38"]])

# P20 merged 85% + VDBFuzz (was P25+P26)
s = slide(20, "Evaluation", "~85% are documentation-implementation defects; VDBFuzz found 0 crashes on the same version")
two_col(s, "Composition (not prevalence)",
        ["~85% doc-implementation defects", "~10% classical-addressable", "~5% concurrency", "89% on acknowledged subset"],
        "VDBFuzz head-to-head (Qdrant v1.18.2)",
        ["we ran VDBFuzz: 26,000 requests", "0 crashes, 0 non-200 responses", "TestVDB found doc-implementation defects", "disjoint defect classes"],
        lc=ACCENT_BLUE, rc=ACCENT_GREEN)

s = slide(21, "Evaluation", "The source anchor suppresses 81% of false positives (up from 31%) at 96.7% TP")
big_number(s, "81%", "false positives suppressed by the source anchor",
           "up from 31% with the other two anchors alone; 96.7% true-positive retention (n=30)")

s = slide(22, "Evaluation", "Precision scales with the source anchor: 25.5% -> 45.6% -> 69.2%")
image(s, "fig7_ablation.png", top=1.5, left=2.5, width=8.3)

s = slide(23, "Evaluation", "RQ3 at n=29: source catches all 16 over-strict; 0/13 on explicit bounds; cross-model kappa=1.0")
table(s, ["Subtype", "n", "Task-intrinsic", "Cross-model", "Source"],
      [["Parameter over-strict", "12", "5 / 12", "7 / 12", "12 / 12"],
       ["Behavior over-strict", "4", "4 / 4", "0 / 4", "4 / 4"],
       ["Explicit-bound negative", "13", "0 / 13", "-", "-"],
       ["Within-vendor contrast", "-", "56% vs 0%", "-", "-"],
       ["Cross-model kappa (n=20)", "20", "-", "kappa = 1.0", "-"]], top=1.5)

s = slide(24, "Evaluation", "A model-free invariant subclass finds bugs on its own")
table(s, ["Invariant", "Observation", "Cross-vendor"],
      [["COSINE distance bound", "distance > 1.0 for identical vectors", "Milvus + Qdrant"],
       ["Index completeness", "index returns 2 of 25 matching points", "Milvus + Qdrant"],
       ["Payload filter field", "filter on absent field returns points missing it", "Milvus + Qdrant"]])

# P25-P28 closing
s = slide(25, "Related work", "Prior work stays in low-ambiguity sources; TestVDB enters the ambiguous regime")
table(s, ["Line of work", "Representative", "Difference"],
      [["VDBMS testing", "VDBFuzz / roadmap / bug study", "crash vs doc-implementation; we build on their agenda"],
       ["REST-API oracle", "AGORA+ / SATORI / MASTOR", "low-ambiguity sources (OpenAPI/trace/source); we use NL docs"],
       ["Doc-derived oracle", "Toradocu / Doc2OracLL / AugmenTest / Konstantinou / ChatAssert / Testora", "trust LLM as arbiter; we falsify with source"],
       ["DB correctness", "NoREC / TLP / DQE / DDLCheck", "reference semantics exists; ours lacks it"],
       ["LLM-judge reliability", "Panickssery / Wataoka / Haldar", "orthogonal — we address via source grounding"]],
     top=1.4, height=5.6)

s = slide(26, "Threats", "Threats: over-strict subset (n=16) most contingent; mechanism correlative, not causal")
bullets(s, [
    ("Internal: over-strict subset (n=16) is most contingent; retrospective + yield are broader base", TEXT_DARK),
    ("External: statistical claims rest on Milvus + Qdrant; others breadth-only", TEXT_DARK),
    ("Construct: mechanism (doc-style vs over-formalization) is correlative, validated by within-vendor contrast + falsifiable prediction", TEXT_DARK),
    ("Cross-model: DeepSeek on 20 candidates kappa=1.0 — not family-specific when source is explicit", ACCENT_GREEN),
])

s = slide(27, "Conclusion", "The boundary between extractable and interpretable is where LLM-dependent testing is heading")
bullets(s, [
    "documentation-implementation consistency is a defect class where accept/reject decisions resist deterministic checking",
    "LLM errors split: family-specific (cross-model) + task-intrinsic (source)",
    "source-grounded falsification resolves the task-intrinsic layer",
    "generalizes beyond VDBMSs — any NL-doc system enters this setting (future work)",
])

s = slide(28, "Conclusion", "TestVDB — four core results")
image(s, "fig8_summary.png", top=1.4, left=1.5, width=10.3)


prs.save(OUT)
print(f"[wrote] {OUT}  ({len(prs.slides._sldIdLst)} slides)")
