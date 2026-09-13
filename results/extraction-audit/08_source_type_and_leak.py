"""A1 step 8 — two open attribution questions before the quality gate is fixed.

(1) Is the Weaviate->OpenAPI-schema citation a property of the PIPELINE's own
    contract output, or an artefact of the pack reconstruction?
(2) Do the packs leak adjudication labels (issue numbers, maintainer verdicts)?
"""
import collections
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESK = r"c:/Users/11428/Desktop"
BUCKETS = ("constraints", "assertions", "behavioral_contracts", "state_invariants")


def rows_of(obj):
    rows = []
    for k in BUCKETS:
        v = obj.get(k) or {}
        if isinstance(v, dict):
            for g in v.values():
                if isinstance(g, list):
                    rows += [r for r in g if isinstance(r, dict)]
        elif isinstance(v, list):
            rows += [r for r in v if isinstance(r, dict)]
    return rows


def main():
    print("=== (1) 插件自己产出的 weaviate 契约用什么 source_url ===")
    for rel in ["mftui/TestVDB/results/weaviate/1.38.0/structured_contract.json",
                "mftui/TestVDB/results/weaviate/v1.38.2/structured_contract.json",
                "TestVDB_artifact/rq1/runs/rq1-fullrun/weaviate-v1.38.2/voided/structured_contract.json"]:
        path = os.path.join(DESK, rel)
        if not os.path.exists(path):
            print(f"  {rel}  —— 不存在")
            continue
        d = json.load(open(path, encoding="utf-8"))
        rows = rows_of(d)
        c = collections.Counter(str(r.get("source_url"))[:56] for r in rows)
        print(f"  {rel}  ({len(rows)} 行)")
        for u, n in c.most_common(4):
            print(f"      {n:>3}x {u}")

    print("\n=== (1b) 对照：qdrant / milvus 插件契约的 source_url 类型 ===")
    for rel in ["mftui/TestVDB/results/qdrant/v1.18.3/structured_contract.json",
                "mftui/TestVDB/results/milvus/v3.0.0/structured_contract.json"]:
        path = os.path.join(DESK, rel)
        if not os.path.exists(path):
            print(f"  {rel}  —— 不存在")
            continue
        d = json.load(open(path, encoding="utf-8"))
        rows = rows_of(d)
        urls = [str(r.get("source_url", "")) for r in rows]
        dom = collections.Counter(re.sub(r"^(https?://[^/]+).*", r"\1", u) for u in urls)
        print(f"  {rel}  ({len(rows)} 行)  域名分布: {dict(dom.most_common(5))}")

    print("\n=== (2) 包内标签泄漏扫描 ===")
    pat = re.compile(r"#\d{4,6}|maintainer|by-design|by design|not a bug|"
                     r"rejected|acknowledged|confirmed as", re.I)
    hits = {}
    for f in sorted(glob.glob(os.path.join(DESK, "TestVDB_artifact/rq2/materials/*.md"))):
        t = open(f, encoding="utf-8").read()
        m = pat.findall(t)
        if m:
            hits[os.path.basename(f)[:-3]] = collections.Counter(x.lower() for x in m)
    print(f"  含疑似泄漏标记的包: {len(hits)} / 81")
    agg = collections.Counter()
    for c in hits.values():
        agg.update(c)
    print(f"  命中类型汇总: {dict(agg.most_common(8))}")
    for k in list(hits)[:8]:
        print(f"     {k}: {dict(hits[k].most_common(3))}")


if __name__ == "__main__":
    main()
