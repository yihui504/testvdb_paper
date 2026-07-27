#!/usr/bin/env python3
"""Generate 8 slide figures for TestVDB PPT (matplotlib drafts for review).

fig3/fig4/fig5 use real TestVDB parameters (shardsNum/timeout/consistencyLevel)
with concrete probe examples — see figures-design-notes.md for design rationale.

Outputs to paper/figures/figN_*.png at 150 dpi. English labels.
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "figures")
os.makedirs(OUT, exist_ok=True)

C_BLUE = "#2E5C8A"; C_BLUE_LT = "#D6E4F0"
C_ORANGE = "#D98E48"; C_ORANGE_LT = "#FBE3CB"
C_GREEN = "#4A8C5C"; C_GREEN_LT = "#D6E8DC"
C_RED = "#B05050"; C_GREY = "#888888"


def _box(ax, x, y, w, h, text, fc=C_BLUE_LT, ec=C_BLUE, fs=11, weight="normal"):
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                          fc=fc, ec=ec, lw=1.5)
    ax.add_patch(rect)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
            fontsize=fs, weight=weight)


def _arrow(ax, x1, y1, x2, y2, color="#333"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2),
                                 arrowstyle="->", mutation_scale=14,
                                 color=color, lw=1.4))


def save(fig, n, name):
    path = os.path.join(OUT, f"fig{n}_{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"[wrote] {path}")


# ---- fig 1: RAG / VDBMS architecture (P2) ----
def fig1():
    fig, ax = plt.subplots(figsize=(10, 3.6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.6); ax.axis("off")
    steps = [("User\nQuery", C_BLUE_LT), ("Embed", C_BLUE_LT),
             ("VDBMS\n(search)", C_ORANGE_LT), ("LLM\n(RAG)", C_BLUE_LT),
             ("Response", C_BLUE_LT)]
    for i, (label, fc) in enumerate(steps):
        ec = C_ORANGE if i == 2 else C_BLUE
        _box(ax, 0.3 + i * 1.95, 1.3, 1.6, 1.0, label, fc=fc, ec=ec,
             weight="bold" if i == 2 else "normal")
        if i < len(steps) - 1:
            _arrow(ax, 1.9 + i * 1.95, 1.8, 2.25 + i * 1.95, 1.8)
    ax.set_title("VDBMSs store the embeddings that retrieval-augmented LLMs depend on",
                 fontsize=12, weight="bold", loc="left")
    save(fig, 1, "rag_arch")


# ---- fig 2: case table (P5) ----
def fig2():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 3.2); ax.axis("off")
    ax.set_title("Three conformance defects: the API silently accepts what the docs prescribe rejecting",
                 fontsize=11, weight="bold", loc="left")
    cols = [(0.2, 2.2, "Parameter"), (2.4, 3.4, "Docs prescribe"),
            (5.8, 4.0, "API actually does")]
    for x, w, t in cols:
        _box(ax, x, 2.4, w, 0.5, t, fc=C_BLUE, ec=C_BLUE, fs=10, weight="bold")
        ax.texts[-1].set_color("white")
    rows = [
        ("nprobe=0", "reject (must be >= 1)", "accepts, search runs", "milvus #47729"),
        ("ef=0", "reject (must be >= 1)", "accepts, search runs", "milvus #47752"),
        ("score_threshold < 0", "reject (out of range)", "accepts, disables filter", "qdrant #9027"),
    ]
    for i, (p, d, a, issue) in enumerate(rows):
        y = 1.8 - i * 0.65
        fc = "#FAFAFA" if i % 2 == 0 else "white"
        for x, w, t in [(0.2, 2.2, p), (2.4, 3.4, d), (5.8, 4.0, a)]:
            _box(ax, x, y, w, 0.55, t, fc=fc, ec="#CCC", fs=9.5)
        ax.text(9.9, y + 0.27, issue, ha="right", va="center",
                fontsize=8, color=C_GREY, style="italic")
    save(fig, 2, "cases")


# ---- fig 3: source-ambiguity gap (P12) — concrete examples ----
def fig3():
    fig, ax = plt.subplots(figsize=(12, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5.5); ax.axis("off")
    ax.set_title("The source-ambiguity gap: structured sources yield assertions, ambiguous docs yield claims",
                 fontsize=11, weight="bold", loc="left")
    # left half (structured sources, reliable)
    ax.add_patch(Rectangle((0, 0), 5, 5, fc=C_GREEN_LT, alpha=0.4, ec="none"))
    ax.text(2.5, 5.2, "Structured sources  (REST-API oracle work)", ha="center",
            fontsize=10, color=C_GREEN, weight="bold")
    ax.text(2.5, 4.8, "LLM transcribes → reliable assertion", ha="center",
            fontsize=8.5, color=C_GREEN, style="italic")
    cards = [
        (3.5, "OpenAPI spec", "limit:\n  type: integer\n  minimum: 1", "limit >= 1  ✓"),
        (2.2, "execution trace", "REQ limit=5  → 200\nREQ limit=0  → 400", "limit=0 rejected  ✓"),
        (0.9, "source code", "if limit < 1 {\n  return Err }", "limit >= 1  ✓"),
    ]
    for y, title, code, assertion in cards:
        _box(ax, 0.3, y, 4.4, 1.0, "", fc="white", ec=C_GREEN)
        ax.text(0.45, y + 0.78, title, fontsize=8.5, color=C_GREEN, weight="bold")
        ax.text(0.45, y + 0.18, code, fontsize=8, family="monospace", color="#333")
        ax.text(4.55, y + 0.5, assertion, fontsize=8.5, color=C_GREEN,
                weight="bold", ha="right")
    # right half (NL doc, unreliable)
    ax.add_patch(Rectangle((7, 0), 5, 5, fc=C_ORANGE_LT, alpha=0.4, ec="none"))
    ax.text(9.5, 5.2, "Natural-language docs  (TestVDB)", ha="center",
            fontsize=10, color=C_ORANGE, weight="bold")
    ax.text(9.5, 4.8, "LLM interprets → claim may be wrong", ha="center",
            fontsize=8.5, color=C_ORANGE, style="italic")
    # doc card
    _box(ax, 7.3, 3.4, 4.4, 1.1, "", fc="white", ec=C_ORANGE)
    ax.text(7.45, 4.25, "Milvus documentation", fontsize=8.5, color=C_ORANGE, weight="bold")
    ax.text(7.45, 3.55, "shardsNum (int, optional, default 1):\n   Number of shards to create.",
            fontsize=8, family="monospace", color="#333")
    # two interpretations
    _box(ax, 7.3, 2.1, 4.4, 0.95, "", fc="#FBE3CB", ec=C_RED)
    ax.text(7.45, 2.78, "GLM extracts:", fontsize=8.5, color=C_RED, weight="bold")
    ax.text(7.45, 2.35, "shardsNum >= 1   →  over-strict  ✗", fontsize=8.5,
            family="monospace", color=C_RED)
    _box(ax, 7.3, 0.8, 4.4, 0.95, "", fc=C_GREEN_LT, ec=C_GREEN)
    ax.text(7.45, 1.48, "actual semantics:", fontsize=8.5, color=C_GREEN, weight="bold")
    ax.text(7.45, 1.05, "0 selects default  →  0 is valid  ✓", fontsize=8.5,
            family="monospace", color=C_GREEN)
    # gap in middle
    ax.text(6.0, 2.7, "GAP", fontsize=24, color=C_RED, alpha=0.45,
            weight="bold", ha="center", va="center", rotation=90)
    ax.text(6.0, 0.3, "source-ambiguity", fontsize=8, color=C_RED,
            ha="center", style="italic")
    save(fig, 3, "source_ambiguity_gap")


# ---- fig 4: two-layer errors Venn (P14) — concrete probe cards ----
def fig4():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.set_title("Two layers of unreliability — families DIVERGE vs CONVERGE on the same error",
                 fontsize=11, weight="bold", loc="left")
    # left circle: family-specific
    c1 = Circle((3, 3.5), 1.9, fc=C_BLUE_LT, ec=C_BLUE, lw=2.5, alpha=0.55)
    ax.add_patch(c1)
    ax.text(3, 6.0, "family-specific", ha="center", fontsize=11, color=C_BLUE, weight="bold")
    ax.text(3, 5.6, "(self-preference bias)", ha="center", fontsize=8.5,
            color=C_BLUE, style="italic")
    _box(ax, 1.2, 4.0, 3.6, 0.55, "param: consistencyLevel", fc="white", ec=C_BLUE, fs=8.5)
    _box(ax, 1.2, 2.7, 3.6, 1.2, "", fc=C_BLUE_LT, ec=C_BLUE)
    ax.text(3, 3.65, "GLM judge:  DEFECT (confirms own strict enum)", ha="center",
            fontsize=8, color=C_BLUE)
    ax.text(3, 3.15, "DeepSeek judge:  OK (different family)", ha="center",
            fontsize=8, color=C_BLUE)
    ax.text(3, 2.9, "→ families DIVERGE", ha="center", fontsize=8.5,
            color=C_BLUE, weight="bold")
    # right circle: task-intrinsic
    c2 = Circle((9, 3.5), 1.9, fc=C_ORANGE_LT, ec=C_ORANGE, lw=2.5, alpha=0.55)
    ax.add_patch(c2)
    ax.text(9, 6.0, "task-intrinsic", ha="center", fontsize=11, color=C_ORANGE, weight="bold")
    ax.text(9, 5.6, "(documentation ambiguity)", ha="center", fontsize=8.5,
            color=C_ORANGE, style="italic")
    _box(ax, 7.2, 4.0, 3.6, 0.55, "param: timeout", fc="white", ec=C_ORANGE, fs=8.5)
    _box(ax, 7.2, 2.7, 3.6, 1.2, "", fc=C_ORANGE_LT, ec=C_ORANGE)
    ax.text(9, 3.65, "GLM:  timeout >= 1", ha="center", fontsize=8, color=C_ORANGE)
    ax.text(9, 3.2, "DeepSeek:  timeout >= 1  (same!)", ha="center",
            fontsize=8, color=C_ORANGE)
    ax.text(9, 2.9, "→ families CONVERGE (both wrong)", ha="center",
            fontsize=8.5, color=C_ORANGE, weight="bold")
    # coverage arrows
    ax.text(3, 1.1, "cross-model validation", ha="center", fontsize=9.5,
            color=C_BLUE, weight="bold")
    _arrow(ax, 3, 1.4, 3, 1.9, color=C_BLUE)
    ax.text(9, 1.1, "source-grounded falsification", ha="center", fontsize=9.5,
            color=C_GREEN, weight="bold")
    _arrow(ax, 8.5, 1.4, 9, 1.9, color=C_GREEN)
    _arrow(ax, 5.0, 1.25, 3.7, 1.9, color=C_GREEN)  # source also covers left
    ax.text(6, 0.45, "source covers BOTH layers", ha="center", fontsize=8,
            color=C_GREEN, style="italic")
    # footnote
    ax.text(6, 0.05, "Note: task-intrinsic is extraction-level across-families stability,\n"
            "distinct from intra-judge across-runs noise (Haldar, Rating Roulette).",
            ha="center", fontsize=7, color=C_GREY, style="italic")
    save(fig, 4, "two_layer_venn")


# ---- fig 5: 5-stage pipeline (P18) — shardsNum journey ----
def fig5():
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.set_title("Pipeline — one candidate's journey (Milvus shardsNum):  source falsifies the LLM verdict",
                 fontsize=11, weight="bold", loc="left")
    stages = [
        ("S1 · Extract\n→ oracle", C_BLUE, "doc:\nshardsNum\noptional, default 1", "claims → oracle:\nshardsNum>=1\n+ N more"),
        ("S2 · Attack", C_BLUE, "clause:\nshardsNum >= 1", "probe:\nshardsNum = 0"),
        ("S3 · LLM judge", C_RED, "API response:\nHTTP 200 success", "verdict:\nDEFECT (red)"),
        ("S4 · Dev-reviewer", C_GREEN, "source code:\nif shardsNum == 0:\n  use default", "FALSIFY:\nFP killed (green)"),
        ("S5 · Novelty", C_BLUE, "surviving\ncandidates", "dedup +\nfilter known"),
    ]
    for i, (label, ec, inp, outp) in enumerate(stages):
        x = 0.2 + i * 2.75
        fc = C_GREEN_LT if i == 3 else (C_ORANGE_LT if i == 2 else C_BLUE_LT)
        _box(ax, x, 4.5, 2.4, 1.0, label, fc=fc, ec=ec, fs=10, weight="bold")
        if i < 4:
            _arrow(ax, x + 2.4, 5.0, x + 2.75, 5.0, color=ec)
        # data card (taller, input on top / output on bottom)
        _box(ax, x, 2.2, 2.4, 1.7, "", fc="#FAFAFA", ec="#CCC")
        ax.text(x + 1.2, 3.55, "input", ha="center", fontsize=7,
                color=C_GREY, weight="bold")
        ax.text(x + 1.2, 3.15, inp, ha="center", fontsize=7,
                family="monospace", color="#333")
        ax.text(x + 1.2, 2.65, "output", ha="center", fontsize=7,
                color=C_GREY, weight="bold")
        ax.text(x + 1.2, 2.4, outp, ha="center", fontsize=7,
                family="monospace", color=ec, weight="bold")
    # source callout above S4
    sx = 0.2 + 3 * 2.75 + 1.2
    ax.text(sx, 6.0, "implementation source code", ha="center",
            fontsize=9, color=C_GREEN, weight="bold")
    _arrow(ax, sx, 5.75, sx, 5.25, color=C_GREEN)
    # overturn annotation: S3 red → S4 green
    ax.annotate("", xy=(0.2 + 3 * 2.75, 2.0), xytext=(0.2 + 2 * 2.75 + 2.4, 2.0),
                arrowprops=dict(arrowstyle="->", lw=2.5, color=C_GREEN))
    ax.text(0.2 + 2.5 * 2.75 + 1.2, 1.5,
            "S3 red verdict  →  overturned by S4 green falsify\nsource-grounded falsification in action",
            ha="center", fontsize=9, color=C_GREEN, weight="bold", style="italic")
    ax.text(7, 0.4,
            "vs MASTOR: MASTOR uses source to encode implemented behavior; "
            "TestVDB uses source to falsify documented claims — opposite direction.",
            ha="center", fontsize=7.5, color=C_GREY, style="italic")
    save(fig, 5, "pipeline")


# ---- fig 6: dev-reviewer three anchors (P22) ----
def fig6():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 9); ax.set_ylim(0, 5); ax.axis("off")
    ax.set_title("Dev-reviewer: three anchors, source-grounding is primary",
                 fontsize=11, weight="bold", loc="left")
    _box(ax, 3.5, 2, 2, 1, "dev-reviewer", fc=C_BLUE, ec=C_BLUE, fs=11, weight="bold")
    ax.texts[-1].set_color("white")
    anchors = [
        (1.0, 3.8, "clean\nreproduction", C_BLUE, "kills tooling-artifact FPs"),
        (4.0, 3.8, "source-grounding\n(PRIMARY)", C_GREEN, "kills over-strict + by-design FPs"),
        (7.0, 3.8, "threat-model\ncross-check", C_BLUE, "kills known non-defects"),
    ]
    for x, y, label, ec, sub in anchors:
        _box(ax, x - 0.9, y, 1.8, 0.9, label,
             fc=C_BLUE_LT if ec == C_BLUE else C_GREEN_LT, ec=ec, fs=9.5,
             weight="bold" if ec == C_GREEN else "normal")
        _arrow(ax, x, y, 4.5, 3.0, color=ec)
        ax.text(x, y - 0.35, sub, ha="center", fontsize=7.5, color=C_GREY, style="italic")
    save(fig, 6, "anchors")


# ---- fig 7: ablation bar (P28) ----
def fig7():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = ["single-LLM\nself-judgment", "+1 source\ngrounded cycle",
              "full multi-agent\n+ source anchor"]
    vals = [25.5, 45.6, 69.2]
    colors = [C_BLUE_LT, C_ORANGE_LT, C_GREEN]
    bars = ax.bar(labels, vals, color=colors, edgecolor="#333", lw=1.2, width=0.6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v}%",
                ha="center", fontsize=12, weight="bold")
    ax.set_ylabel("End-to-end precision", fontsize=11)
    ax.set_ylim(0, 80)
    ax.set_title("Precision scales with the source anchor: 25.5% → 45.6% → 69.2%",
                 fontsize=11, weight="bold")
    ax.axhline(69.2, ls="--", color=C_GREEN, alpha=0.4)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    save(fig, 7, "ablation")


# ---- fig 8: summary 2x2 (P34) ----
def fig8():
    fig, axs = plt.subplots(2, 2, figsize=(10, 5.5))
    fig.suptitle("TestVDB — four core results", fontsize=13, weight="bold")
    axs[0, 0].pie([85, 10, 5], colors=[C_ORANGE, C_BLUE, C_GREY],
                  labels=["conformance\n85%", "classical\n10%", "concurrency\n5%"],
                  startangle=90, textprops={"fontsize": 9})
    axs[0, 0].set_title("~85% residual beyond classical oracles", fontsize=10, weight="bold")
    axs[0, 1].bar(["no source", "with source"], [31, 81],
                  color=[C_BLUE_LT, C_GREEN], edgecolor="#333")
    for i, v in enumerate([31, 81]):
        axs[0, 1].text(i, v + 2, f"{v}%", ha="center", weight="bold")
    axs[0, 1].set_ylim(0, 100); axs[0, 1].set_ylabel("FP suppressed")
    axs[0, 1].set_title("source anchor suppresses 81% of FPs", fontsize=10, weight="bold")
    for s in ["top", "right"]:
        axs[0, 1].spines[s].set_visible(False)
    axs[1, 0].bar(["optional-default\n(ambiguous)", "explicit-bound"],
                  [56, 0], color=[C_RED, C_GREEN], edgecolor="#333")
    axs[1, 0].text(0, 58, "56%", ha="center", weight="bold", color=C_RED)
    axs[1, 0].text(1, 3, "0%", ha="center", weight="bold", color=C_GREEN)
    axs[1, 0].set_ylim(0, 70); axs[1, 0].set_ylabel("over-strict rate (TI)")
    axs[1, 0].set_title("n=29: within-vendor contrast + κ=1.0 cross-model",
                        fontsize=10, weight="bold")
    for s in ["top", "right"]:
        axs[1, 0].spines[s].set_visible(False)
    axs[1, 1].axis("off")
    axs[1, 1].text(0.5, 0.65, "111 → 38", ha="center", fontsize=34,
                   weight="bold", color=C_BLUE)
    axs[1, 1].text(0.5, 0.3, "submitted → maintainer-acknowledged\nacross 5 VDBMSs",
                   ha="center", fontsize=10)
    axs[1, 1].set_title("yield at scale", fontsize=10, weight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    save(fig, 8, "summary")


# ---- fig 9: claim → oracle → judge (concept) ----
def fig9():
    fig, ax = plt.subplots(figsize=(14, 6.5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 6.5); ax.axis("off")
    ax.set_title("From claims to oracle: what the LLM produces, and what judges",
                 fontsize=11, weight="bold", loc="left")
    # doc (left)
    _box(ax, 0.2, 2.8, 2.3, 1.5, "", fc="white", ec=C_GREY)
    ax.text(1.35, 4.1, "documentation", ha="center", fontsize=9, color=C_GREY, weight="bold")
    ax.text(1.35, 3.45, "shardsNum (int,\noptional, default 1):\n Number of shards.",
            fontsize=7.5, family="monospace", ha="center", color="#333")
    # arrow: LLM extract
    _arrow(ax, 2.5, 3.55, 3.0, 3.55, color=C_BLUE)
    ax.text(2.75, 3.85, "LLM\nextract", ha="center", fontsize=7.5, color=C_BLUE, weight="bold")
    # claims (3 stacked cards showing structure: name + constraint + source)
    claims = [
        (4.7, "claim 1", "shardsNum >= 1", "from 'optional,\ndefault 1'"),
        (3.5, "claim 2", "metricType in {L2,IP,COS}", "from enum doc"),
        (2.3, "claim 3", "dimension >= 1", "from 'Must be\n>= 1'"),
    ]
    for y, label, constraint, src in claims:
        _box(ax, 3.1, y, 3.0, 1.0, "", fc=C_BLUE_LT, ec=C_BLUE)
        ax.text(3.2, y + 0.78, label, fontsize=8, color=C_BLUE, weight="bold")
        ax.text(3.2, y + 0.42, constraint, fontsize=7.5, family="monospace", color="#333")
        ax.text(3.2, y + 0.1, src, fontsize=6.8, color=C_GREY, style="italic")
    ax.text(4.6, 6.0, "claims  (LLM-derived)", ha="center", fontsize=9.5,
            color=C_BLUE, weight="bold")
    # arrow: aggregates
    _arrow(ax, 6.1, 3.55, 6.7, 3.55, color=C_BLUE)
    ax.text(6.4, 3.85, "aggregate", ha="center", fontsize=7.5, color=C_BLUE, weight="bold")
    # oracle (big card — the judgment standard, not the LLM)
    _box(ax, 6.8, 2.5, 3.2, 2.2, "", fc=C_GREEN_LT, ec=C_GREEN)
    ax.text(8.4, 4.5, "oracle", ha="center", fontsize=15, color=C_GREEN, weight="bold")
    ax.text(8.4, 3.95, "= { claim 1, claim 2,", ha="center", fontsize=8.5,
            family="monospace", color="#333")
    ax.text(8.4, 3.6, "    claim 3, ... }", ha="center", fontsize=8.5,
            family="monospace", color="#333")
    ax.text(8.4, 3.05, "the judgment standard", ha="center", fontsize=9,
            color=C_GREEN, style="italic")
    ax.text(8.4, 2.7, "(NOT the LLM itself)", ha="center", fontsize=8.5,
            color=C_RED, weight="bold")
    # arrow: judge uses oracle
    _arrow(ax, 10.0, 3.55, 10.6, 3.55, color=C_ORANGE)
    ax.text(10.3, 3.85, "judge\n(LLM)", ha="center", fontsize=7.5,
            color=C_ORANGE, weight="bold")
    # response check (right)
    _box(ax, 10.8, 2.8, 2.8, 1.5, "", fc="white", ec=C_ORANGE)
    ax.text(12.2, 4.1, "probe response", ha="center", fontsize=9,
            color=C_ORANGE, weight="bold")
    ax.text(12.2, 3.4, "conform ?\nviolate ?", fontsize=9.5, ha="center", color="#333")
    # bottom footnotes
    ax.text(7, 1.3,
            "Key:  oracle is the LLM-derived PRODUCT (a set of claims);   "
            "judge is the ACT of using the oracle.",
            ha="center", fontsize=9, color=C_GREEN, weight="bold", style="italic")
    ax.text(7, 0.7,
            "These are different — oracle != LLM.   "
            "Source-grounded falsification targets individual claims (e.g. claim 1),",
            ha="center", fontsize=8, color=C_GREY, style="italic")
    ax.text(7, 0.35, "not the oracle as a whole.",
            ha="center", fontsize=8, color=C_GREY, style="italic")
    save(fig, 9, "claim_to_oracle")


def main():
    for f in [fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9]:
        f()
    print(f"\nAll 9 figures written to {OUT}")


if __name__ == "__main__":
    main()
