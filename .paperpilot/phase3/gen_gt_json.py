#!/usr/bin/env python3
"""档1: 按 (target, version) 分组生成 gt.json + 人工复核表.

param 来源: issue title 点名的触发参数(REST/OpenAPI 字段规范名) + phase2 probe 佐证.
注: gt.json 的 param 仅用于 gt_reach_injector 的 reach 计数(催促时机),
    最终 reach 判定走事后 LLM 盲评对齐, 弱对齐项在复核表中标注.

产出:
- gt/{vendor}/{version}/gt.json   (实验时拷到 testvdb4exp/results/{target}/{version}/)
- gt-review.md                    人工复核表 (45 条 + 定位证据 + param)
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
CATALOG = json.load(open(HERE / "gt-bug-catalog.json", encoding="utf-8"))
ROWS = list(csv.DictReader(open(HERE / "presence-versions.csv", encoding="utf-8-sig")))

# did -> (param, 弱对齐备注)   弱对齐 = 工具侧 defect param 命名不可预知, reach 计数偏保守
PARAMS = {
    "milvus_47635":  ("load", "race bug, 无固定参数名"),
    "milvus_47729":  ("nprobe", ""),
    "milvus_47752":  ("ef", ""),
    "milvus_47755":  ("filter", "校验宽松, 命名或偏"),
    "milvus_47763":  ("fieldName", ""),
    "milvus_47766":  ("dataType", "类型混淆 bug, 命名或偏"),
    "milvus_49059":  ("metric_type", ""),
    "milvus_49823":  ("nprobe", ""),
    "milvus_49843":  ("collection.ttl.seconds", ""),
    "milvus_49889":  ("dbName", ""),
    "milvus_49890":  ("Request-Timeout", ""),
    "milvus_49930":  ("searchParams", ""),
    "milvus_50018":  ("collectionName", ""),
    "milvus_50323":  ("filter", "filter+ids 互斥"),
    "milvus_50353":  ("limit", ""),
    "milvus_50354":  ("password", ""),
    "milvus_50355":  ("autoID", ""),
    "milvus_51084":  ("consistencyLevel", ""),
    "milvus_51085":  ("vectorFieldType", ""),
    "milvus_52307":  ("json_field", "JSON 字段 bug, 命名或偏"),
    "milvus_52308":  ("id", "主键类型强转, 命名或偏"),
    "milvus_52309":  ("group_size", ""),
    "milvus_52310":  ("data", "标量强转, 命名或偏"),
    "milvus_52311":  ("group_by_field", ""),
    "milvus_52312":  ("id", "同 52308 (upsert)"),
    "milvus_52313":  ("json_field", "同 52307 (dup 对)"),
    "milvus_52314":  ("data", "同 52310 (upsert)"),
    "milvus_52315":  ("vector", ""),
    "milvus_52325":  ("strictGroupSize", ""),
    "qdrant_9017":   ("hnsw_ef", ""),
    "qdrant_9039":   ("vector", "诊断缺陷, 命名或偏"),
    "qdrant_9045":   ("wait", ""),
    "qdrant_9149":   ("shard_number", ""),
    "qdrant_9421":   ("recover", "模式不匹配 bug, 命名或偏"),
    "qdrant_9520":   ("shard_number", ""),
    "qdrant_9522":   ("lookup_from", ""),
    "qdrant_10120":  ("exact", ""),
    "weaviate_11399": ("dynamicEfMin", ""),
    "weaviate_11400": ("flatSearchCutoff", ""),
    "weaviate_11401": ("replicationFactor", ""),
    "weaviate_11729": ("desiredCount", ""),
    "weaviate_11730": ("tokenization", ""),
    "weaviate_11732": ("distance", ""),
    "weaviate_11741": ("activityStatus", ""),
    "weaviate_12041": ("match", "match.where 缺失, 命名或偏"),
}

cat = {c["did"]: c for c in CATALOG}
presence = {f'{r["repo"]}_{r["issue"]}': r for r in ROWS}
assert set(PARAMS) == set(cat) == set(presence), "三方 did 集合不一致"

groups = defaultdict(list)
for did, (param, weak) in PARAMS.items():
    row = presence[did]
    groups[(row["repo"], row["presence_version"])].append((did, param, weak, row))

out_dir = HERE / "gt"
for (vendor, version), bugs in sorted(groups.items()):
    vd = out_dir / vendor / version
    vd.mkdir(parents=True, exist_ok=True)
    gt = {
        "target": vendor,
        "version": version,
        "bugs": [
            {"id": did, "endpoint": cat[did]["endpoint"], "param": p}
            for did, p, _, _ in sorted(bugs)
        ],
    }
    (vd / "gt.json").write_text(json.dumps(gt, ensure_ascii=False, indent=1), encoding="utf-8")

md = ["# Phase 3 GT 材料复核表（45 bugs → 15 存在版本）", "",
      "定位规则: A组=fix-PR merged_at 前最近 server release(并行线取与报告版本较大者); "
      "无 merged fix-PR → 保守取报告版本; B组=报告版本。milvus \"2.3\"→v2.3.22 (phase2 约定)。", ""]
for (vendor, version), bugs in sorted(groups.items()):
    md.append(f"## {vendor} {version} ({len(bugs)} bugs)")
    md.append("")
    md.append("| did | group | rep.ver | fix-PR (merged_at) | endpoint | param | 弱对齐 |")
    md.append("|---|---|---|---|---|---|---|")
    for did, p, weak, row in sorted(bugs):
        fx = f'{row["fix_pr"].split("/")[-1]} ({row["merged_at"][:10]})' if row["fix_pr"] else "—"
        md.append(f'| {did} | {row["group"]} | {row["reported_version"].lstrip("v")} | {fx} '
                  f'| {cat[did]["endpoint"] or "—"} | `{p}` | {weak or ""} |')
    md.append("")
md.append("## 需重点 probe 验证的条目")
md.append("")
md.append("- **跨版本跳跃**: qdrant_9045 报告于 v1.12.1, 存在版本定位 v1.18.0 (fix #9070 merged 2026-05-19 前最后 release) — 跳过 6 个 minor, 中途可能已被其他改动修复, probe 必验。")
md.append("- **doc-fix 型**: milvus_50355 (milvus-docs#3513/3514) — bug=文档与实现不一致, 修复=改文档; probe 验证 v2.6.18 文档/行为仍不一致。")
md.append("- **race bug**: milvus_47635 — 低概率触发, probe 用多 collection 重试; gt.json param=load 为弱对齐占位。")
md.append("")
(HERE / "gt-review.md").write_text("\n".join(md), encoding="utf-8")
print(f"gt.json x{len(groups)} 组 -> {out_dir}/")
print(f"复核表 -> {HERE / 'gt-review.md'}")
