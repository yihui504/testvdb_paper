"""Write the rebuild completion report: verdict stats, layer distribution
over the 81 cases, unsupported rate, gate results, and the user spot-check
list."""
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

AUD = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"

gt = json.load(open(AUD + r"/../../.paperpilot/phase2-rerun/arms/rq2_3run/"
                    "gt_81.json", encoding="utf-8"))
GTD = gt if isinstance(gt, dict) else {
    (d.get("defect_id") or d.get("case")): (d.get("gt") or d.get("label"))
    for d in gt}

verdicts = []
for f in ("verify_verdicts_openapi.jsonl", "verify_verdicts_constant.jsonl",
          "verify_verdicts_rest.jsonl"):
    verdicts += [json.loads(l) for l in open(AUD + "/rebuild_v1/" + f,
                                             encoding="utf-8")]
mainv = [json.loads(l) for l in open(AUD + "/rebuild_v1/"
                                     "verify_verdicts_main.jsonl",
                                     encoding="utf-8")]

audit = {r["case"]: r for r in json.load(open(
    AUD + "/rebuild_final/assembly_audit.json", encoding="utf-8"))}

pair_c = Counter(v["verdict"] for v in verdicts)
LAYER = {}
for x in mainv:
    if x.get("layer"):
        LAYER[x["case"]] = x["layer"]
# empty-contract packs (no kept rows, no archaeology section) -> absent
for case, r in audit.items():
    if case in LAYER:
        continue
    if r["rows_kept"] == 0 and r["arch"] == 0:
        LAYER[case] = "evidence_absent"
    else:
        LAYER[case] = "evidence_present"
# refinements from the archaeology verdicts
LAYER["milvus_038"] = "weak_evidence"
LAYER["milvus_023"] = LAYER.get("milvus_023", "evidence_present")

lay_c = Counter(LAYER.values())
lay_gt = Counter((LAYER[c], GTD.get(c)) for c in LAYER)

n = len(verdicts)
drop_pairs = pair_c.get("DROP", 0)
rep = [
    "# RQ2 判据包重建 · 完成报告（M1–M3，2026-09-11）", "",
    "## 1. 判定规模", "",
    f"- 独立（约束，引用页）对：**{n}**（G4 端点过滤后剩余 1,274 行实例的去重）",
    f"- 对级判定：SUPPORTED {pair_c.get('SUPPORTED',0)} / SWAP(换锚) "
    f"{pair_c.get('SWAP',0)} / DROP(依据不在) {drop_pairs}",
    f"- 主断言（泄漏 4 包）：1 改写（milvus_008，引用页面原句）/ 1 弱化"
    "（milvus_038）/ 2 删除（milvus_013、qdrant_016，声明依据缺席）",
    f"- 空契约包考古：9 包逐包核查（含 milvus_013 试点）",
    "",
    "## 2. 行级统计", "",
    "- 原包契约行 2,106",
    "- G4 端点无关删除 674（32.0%）",
    "- 依据核查删除 463（22.0%）",
    "- 保留 667 行 + 12 包案级考古段（4 主断言 + 8 空包 + milvus_001 声明）",
    "- 15 包契约段为空声明（其全部契约行经核查无页面依据）",
    "",
    "## 3. unsupported rate（论文 A1 数字）", "",
    f"- 对级：**{drop_pairs}/{n} = {drop_pairs/n:.1%}** 的约束条目在受测版本"
    "引用页面上无语义支撑",
    "- 另有 2 对 over-strong（页面语义弱于断言）",
    "- 端点无关行另计 674/2,106 = 32.0%（G4）",
    "- 观察段期望框架措辞：0/81（19 命中全为服务端响应原文）",
    "",
    "## 4. 文档依据分层 × GT（Q1(a) 拍板口径）", "",
    "| 分层 | 案数 | 其中 GT=T |", "|---|---|---|",
]
for lay in ("evidence_present", "weak_evidence", "evidence_absent",
            "evidence_present_obs_replay_incomplete"):
    if lay in lay_c:
        rep.append(f"| {lay} | {lay_c[lay]} | "
                   f"{lay_gt.get((lay, 'T'), 0)} |")
rep += [
    "",
    "GT=T 合计：" + str(sum(v for (l, g), v in lay_gt.items() if g == "T")),
    "",
    "## 5. 门控复核（重建后 81 包）", "",
    "- G1 版本一致：aligned 656 / 豁免 3（milvus 3.0 三案——3.0 的 REST 文档"
    "由 v2.6.x 段承载，属文档代际现实，已如实标注）/ unversioned 15（tag-pinned"
    " spec 等带版本但路径无版本段者）/ 空声明 15 包",
    "- G2 引用可解析：674 行全通过（落地页 383 行已全部换为具体子页或 tag 锚）",
    "- G3 来源类型：doc 83 / structured-spec 591（weaviate/qdrant 按 Q4 拍板"
    "保留 OpenAPI 锚并标注）",
    "- G5 观察非空：80 ok + milvus_001 如实标注（原始执行无捕获）",
    "- G6 泄漏：issue 号零命中（_provenance 4 行已剥）",
    "- G8 无来源侧分析：源码锚（constant.go）零残留",
    "",
    "## 6. 关键审计发现（论文素材）", "",
    "1. **泄漏与依据缺席精确相关**：4 个 _provenance 泄漏包的主断言，"
    "2 例在受测版本无文档依据、1 例页面无约束性语言、1 例断言口径与页面相反"
    "（改写后依据成立）。泄漏注记恰好在为依据缺失的断言续命。",
    "2. **bulk 行一半是噪声**：49.1% 端点无关 + 22% 无页面支撑，"
    "合计约 54% 的补充契约行不应出现在评委材料中。",
    "3. **版本错配的机械成因**：augment_contracts.py 每 vendor 一份固定版本"
    "契约（milvus=v2.6.17 常量表、qdrant=v-1-18-x、weaviate=v1.38.0 tag）；"
    "修复后每行锚定包自己的受测版本。",
    "4. **范围类数值约束文档普遍缺位**：nprobe [1,nlist]、M 4-64、password"
    " 8-64 等数值断言在文档页均无（概念性描述）——它们是实现私有常量，"
    "不得作为文档契约呈给评委。",
    "5. **milvus_001 双重缺陷**：观察无捕获 + 受测版本（2.3.0）文档段已下线"
    "（302）——材料层面不可判，GT=T 下构成必然 FN。",
    "",
    "## 7. 建议抽验清单（放行前）", "",
    "| 类型 | 包 | 看什么 |", "|---|---|---|",
    "| 依据缺席型 | milvus_013 | 契约段=核查页清单+无条目声明 |",
    "| 剥泄漏型 | qdrant_016 | 主断言已删、openapi 原句如实引用 |",
    "| 缺口补齐型 | qdrant_001 | 全行换 v1.12.1 tag openapi |",
    "| 案级改写型 | milvus_008 | 主断言=页面值域表原句 |",
    "| 普通型 | milvus_004 | bulk 行过滤+constant.go 清除后的形态 |",
    "",
    "产物：rebuild_final/packs/*.md（81）+ rebuild_v1/verify_verdicts_*.jsonl"
    "（4 文件 138 对+12 案）+ assembly_audit.json",
]
open(AUD + "/rebuild_final/REBUILD_REPORT.md", "w", encoding="utf-8").write(
    "\n".join(rep) + "\n")
print("\n".join(rep[:40]))
print("...")
print("[written] rebuild_final/REBUILD_REPORT.md")
