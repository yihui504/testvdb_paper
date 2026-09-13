"""A1 step 7 — can the 81 RQ2 packs be rebuilt from per-version contracts?

The packs were augmented from ONE pinned contract per vendor (augment_contracts.py),
which is where every version mismatch came from. A correct rebuild needs, for each
candidate, the contract of the version that candidate was tested at.

This enumerates what the 81 packs need against what contract files exist on disk.
No judgement — just coverage.
"""
import collections
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DESK = r"c:/Users/11428/Desktop"
PACK_META = os.path.join(DESK, "testvdb_paper/results/extraction-audit/pack_meta.json")
ROOTS = ["mftui/TestVDB/results", "testvdb_paper/results",
         "TestVDB_artifact/rq1/runs", "testvdb4exp"]
VENDORS = ("milvus", "qdrant", "weaviate", "chroma", "pgvector", "meilisearch")

VRE = re.compile(r"/(milvus|qdrant|weaviate|chroma|pgvector|meilisearch)[-/_]?v?(\d[\d.]*)/", re.I)


def vkey(s):
    return [int(x) for x in re.findall(r"\d+", s)] or [0]


def count_rows(obj):
    """Same bucket walk as augment_contracts.load_rows() — the searchable rows a
    rebuild could actually draw contract text from."""
    rows = 0
    for k in ("constraints", "assertions", "behavioral_contracts", "state_invariants"):
        v = obj.get(k, {})
        if isinstance(v, dict):
            rows += sum(len(g) for g in v.values() if isinstance(g, list))
        elif isinstance(v, list):
            rows += len(v)
    return rows


def main():
    packs = json.load(open(PACK_META, encoding="utf-8"))
    need = collections.defaultdict(collections.Counter)
    for p in packs:
        if p["vendor"]:
            need[p["vendor"]][p["version"]] += 1

    have = collections.defaultdict(dict)      # vendor -> version -> (path, n_assertions)
    scanned = 0
    for root in ROOTS:
        base = os.path.join(DESK, root)
        for f in glob.glob(os.path.join(base, "**", "structured_contract.json"),
                           recursive=True):
            s = f.replace("\\", "/")
            m = VRE.search(s + "/")
            if not m:
                continue
            vend, ver = m.group(1).lower(), m.group(2)
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            na = count_rows(d)
            if na == 0:
                continue
            scanned += 1
            cur = have[vend].get(ver)
            if cur is None or cur[1] < na:
                have[vend][ver] = (s, na)

    missing = collections.Counter()
    print(f"扫描到可用契约 {scanned} 份\n")
    for vend in ("milvus", "qdrant", "weaviate"):
        print(f"== {vend} ==")
        for ver, npack in sorted(need[vend].items(), key=lambda kv: vkey(kv[0])):
            av = have[vend].get(ver)
            if av:
                print(f"   OK   受测 {ver:<9} 包 {npack:<3} ← 可检索行 {av[1]}")
            else:
                print(f"   MISS 受测 {ver:<9} 包 {npack:<3} ← 无对应版本契约")
                missing[vend] += npack
        print(f"   磁盘可得版本: {', '.join(sorted(have[vend], key=vkey))}\n")
    print("缺失覆盖:", dict(missing) or "无")
    print(f"受影响包数: {sum(missing.values())} / {len(packs)}")

    json.dump({v: {k: list(x) for k, x in have[v].items()} for v in have},
              open(os.path.join(DESK, "testvdb_paper/results/extraction-audit/contracts_available.json"),
                   "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
