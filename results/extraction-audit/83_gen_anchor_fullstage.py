"""1B-light: re-run the 32 unsubmitted-anchor cases under the ACTUAL
full-stage protocol the RQ2 runs used (verbatim, incl. the v3 red lines),
with the same 32 original packs. Three independent dispatches."""
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PAPER = r"c:\Users\11428\Desktop\testvdb_paper"
PROTO_SRC = (f"{PAPER}/.paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3/"
             f"run_full1/batch1_dispatch.txt")
ANCHOR = r"C:\Users\11428\Desktop\TestVDB_artifact\rq2\analyses\unsubmitted-anchor"
OUTDIR = f"{PAPER}/.paperpilot/phase2-rerun/arms/rq2_3run/anchor_fullstage"
SRC = f"{PAPER}/.sourcedeps/qdrant/v1.18.0"
COG = ("C:/Users/11428/Desktop/tvdb_sessions/intelligence/qdrant/"
       "developer_cognition.json")

# --- lift the protocol verbatim from the dispatch the real runs used --------
proto = open(PROTO_SRC, encoding="utf-8").read()
start = proto.index("## 四视角(每案逐一评估)")
protocol = proto[start:]
# the source's old "## 产出" block sits mid-file, before the authoritative v3
# section; excise only that block (up to the next heading) and keep the rest
protocol = re.sub(r"## 产出\n.*?(?=\n## )", "", protocol, flags=re.S).rstrip()
assert "判定红线" in protocol and "聚合(固定" in protocol, \
    "v3 section missing"

cases = json.load(open(f"{ANCHOR}/.tmp_task2_packs_list.json",
                       encoding="utf-8"))
print(f"anchor cases: {len(cases)}")

os.makedirs(OUTDIR, exist_ok=True)
for run in (1, 2, 3):
    out = f"{OUTDIR}/verdicts_run{run}.jsonl"
    lines = [
        f"# 未提交锚点臂重跑（full-stage 协议，预审计包）— run {run}",
        "",
        "## 任务",
        "你是 TestVDB 确认阶段(完整形态:evidence-chain 判定 + 四视角交叉质询)"
        "的独立裁决者。对下列每个候选缺陷:先 Read 其冻结材料包(observed 执行记录"
        " + expected 契约),再按四视角分别评估,最后按固定规则聚合终判。",
        "",
        "## 每案材料",
    ]
    for c in cases:
        lines.append(f"- {c}: pack={ANCHOR}\\packs\\{c}.md | source={SRC}")
    lines.append(f"- 维护者认知(全文 Read 一次即可):{COG}")
    lines += ["", protocol, "", "## 产出",
              f"Write 一个 JSONL 文件(每行一个 JSON 对象)到 **{out}**:",
              '`{"defect_id": "<case-id>", "verdict": '
              '"CONFIRMED|FALSE_POSITIVE|HUMAN_REVIEW", "confidence": <float>, '
              '"perspectives": {"A": "CONFIRMED|REFUTED|NEUTRAL", '
              '"B": "CONFIRMED|REFUTED|NEUTRAL", '
              '"C": "CONFIRMED|WEAK_REFUTED|REFUTED|NEUTRAL", '
              '"D": "SUPPORTS_DEFECT|SUPPORTS_NOT_DEFECT|NO_SIGNAL"}, '
              '"d_evidence": "<文件:行号 一句话>", "rationale": "<一句中文依据>"}`',
              "最后返回一行摘要:<case-id>=<verdict>(逗号分隔全部)。"]
    path = f"{OUTDIR}/dispatch_run{run}.txt"
    open(path, "w", encoding="utf-8").write("\n".join(lines))
    print(f"wrote {path} ({os.path.getsize(path)} bytes) -> {out}")
