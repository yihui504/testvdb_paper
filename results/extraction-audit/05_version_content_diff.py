"""A1 step 5 — do the version-mismatched citations actually differ in content?

Mechanical only: fetch both versions of the two version-mismatched non-doc
artifacts and diff them. The judgement "does the difference matter for the
constraint" stays with the human; this step just removes the guesswork about
whether a difference exists at all.

  family 2: milvus constant.go  v2.6.17 (cited) vs v3.0.0 (tested)
  family 3: weaviate schema.json v1.38.0 (cited) vs v1.37.4 (tested)
"""
import difflib
import json
import os
import re
import urllib.request

BASE = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
CACHE = os.path.join(BASE, "pages")
UA = {"User-Agent": "Mozilla/5.0 (compatible; TestVDB-extraction-audit/1.0)"}

RAW = {
    "constant_v2.6.17.go": "https://raw.githubusercontent.com/milvus-io/milvus/v2.6.17/internal/distributed/proxy/httpserver/constant.go",
    "constant_v3.0.0.go": "https://raw.githubusercontent.com/milvus-io/milvus/v3.0.0/internal/distributed/proxy/httpserver/constant.go",
    "weaviate_v1.38.0.json": "https://raw.githubusercontent.com/weaviate/weaviate/v1.38.0/openapi-specs/schema.json",
    "weaviate_v1.37.4.json": "https://raw.githubusercontent.com/weaviate/weaviate/v1.37.4/openapi-specs/schema.json",
}


def get(name, url):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        open(path, "wb").write(data)
    return open(path, encoding="utf-8", errors="replace").read()


def const_diff():
    a = get("constant_v2.6.17.go", RAW["constant_v2.6.17.go"]).splitlines()
    b = get("constant_v3.0.0.go", RAW["constant_v3.0.0.go"]).splitlines()
    d = list(difflib.unified_diff(a, b, "v2.6.17", "v3.0.0", lineterm="", n=0))
    changed = [l for l in d if l[:1] in "+-" and l[:3] not in ("+++", "---")]

    def consts(lines):
        out = {}
        for l in lines:
            m = re.match(r'\s*(\w+)\s*=\s*"([^"]*)"', l)
            if m:
                out[m.group(1)] = m.group(2)
        return out
    ca, cb = consts(a), consts(b)
    only_a = sorted(set(ca) - set(cb))
    only_b = sorted(set(cb) - set(ca))
    revalued = sorted(k for k in set(ca) & set(cb) if ca[k] != cb[k])
    return {
        "lines_a": len(a), "lines_b": len(b), "diff_lines": len(d),
        "added": sum(1 for l in changed if l.startswith("+")),
        "removed": sum(1 for l in changed if l.startswith("-")),
        "consts_only_in_cited": only_a, "consts_only_in_tested": only_b,
        "consts_revalued": revalued,
        "revalued_pairs": [(k, ca[k], cb[k]) for k in revalued],
        "diff_head": d[:60],
    }


def spec_diff():
    a = json.loads(get("weaviate_v1.38.0.json", RAW["weaviate_v1.38.0.json"]))
    b = json.loads(get("weaviate_v1.37.4.json", RAW["weaviate_v1.37.4.json"]))
    pa, pb = a.get("paths", {}), b.get("paths", {})
    only_a, only_b = sorted(set(pa) - set(pb)), sorted(set(pb) - set(pa))
    common = sorted(set(pa) & set(pb))
    op_diff = []
    for p in common:
        oa, ob = pa[p], pb[p]
        for meth in sorted(set(oa) | set(ob)):
            if meth.startswith("x-") or not isinstance(oa.get(meth), dict):
                continue
            sa = json.dumps(oa.get(meth), sort_keys=True)
            sb = json.dumps(ob.get(meth), sort_keys=True)
            if sa != sb:
                op_diff.append({"path": p, "method": meth,
                                "cited_len": len(sa), "tested_len": len(sb)})
    return {"paths_cited": len(pa), "paths_tested": len(pb),
            "only_in_cited": only_a, "only_in_tested": only_b,
            "common": len(common), "operations_differing": len(op_diff),
            "op_diff_head": op_diff[:40],
            "components_equal": json.dumps(a.get("components", {}), sort_keys=True)
                                == json.dumps(b.get("components", {}), sort_keys=True)}


def main():
    out = {}
    print("=" * 72, "\n族 2 · milvus constant.go  v2.6.17(引用) vs v3.0.0(受测)")
    c = const_diff()
    out["constant_go"] = c
    print(f"  行数 {c['lines_a']} -> {c['lines_b']}；diff 行 {c['diff_lines']}"
          f"（+{c['added']} / -{c['removed']}）")
    print(f"  仅在引用版存在的常量: {len(c['consts_only_in_cited'])}")
    print(f"  仅在受测版存在的常量: {len(c['consts_only_in_tested'])}")
    print(f"  取值/文案改变的常量: {len(c['consts_revalued'])}")
    for k, x, y in c["revalued_pairs"][:12]:
        print(f"     {k}: {x[:56]!r} -> {y[:56]!r}")

    print("\n" + "=" * 72, "\n族 3 · weaviate schema.json  v1.38.0(引用) vs v1.37.4(受测)")
    s = spec_diff()
    out["weaviate_schema"] = s
    print(f"  paths: 引用 {s['paths_cited']} / 受测 {s['paths_tested']}；共有 {s['common']}")
    print(f"  仅在引用版: {len(s['only_in_cited'])}  仅在受测版: {len(s['only_in_tested'])}")
    print(f"  **内容不同的 operation 数: {s['operations_differing']}**")
    print(f"  components 完全相同: {s['components_equal']}")
    for o in s["op_diff_head"][:12]:
        print(f"     {o['method'].upper():<7} {o['path']}")

    json.dump(out, open(os.path.join(BASE, "version_content_diff.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n[wrote] {BASE}\\version_content_diff.json")


if __name__ == "__main__":
    main()
