"""A1 step 1 — mechanical inventory of the RQ2 frozen packs.

Read-only. Extracts every constraint record cited in the 81 judge packs and every
distinct source_url, then classifies each URL by *what kind of artifact it is*
(deterministic from the URL itself — no judgement about whether it supports the
assertion). Emits constraints.json / urls.json / inventory.md.

Source of truth: TestVDB_artifact/rq2/materials/*.md (the exact packs the RQ2
judges saw).
"""
import glob
import json
import os
import re
from collections import defaultdict

MAT = r"C:/Users/11428/Desktop/TestVDB_artifact/rq2/materials"
OUT = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"

# Two header variants occur in the packs: with and without defect_type.
HEADER = re.compile(
    r"\[vendor=(\S+)\s+version=(\S+)\s+(?:defect_type=(\S+)\s+)?endpoint=([^\]]+)\]"
)


def classify_url(url: str) -> str:
    """What kind of artifact the URL points at. Deterministic from the URL."""
    u = url.lower()
    if u.endswith(".go") or "/blob/" in u and u.endswith((".go", ".rs", ".java")):
        return "implementation-source"
    if "raw.githubusercontent.com" in u:
        return "doc-markdown-raw"
    if u.endswith(".json") or "openapi" in u or "schema.json" in u:
        return "structured-spec"
    if "api.qdrant.tech" in u or "milvus.io" in u or "weaviate.io" in u:
        return "vendor-documentation"
    if "github.com" in u:
        return "vendor-repo-unclassified"
    return "other"


def version_token(url: str):
    """Version fragment in a URL, in either dotted (v2.6.17, v2.6.x) or
    hyphenated (v-1-18-x) form. The hyphenated form is how api.qdrant.tech
    encodes its version, so both must parse or the page looks unversioned."""
    m = re.search(r"/v[-]?(\d+\.\d+(?:\.\d+)?|x)[./-]", url)
    if m:
        return m.group(1)
    m = re.search(r"/v-(\d+)-(\d+)(?:-|/)", url)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def main():
    os.makedirs(OUT, exist_ok=True)
    packs = sorted(glob.glob(os.path.join(MAT, "*.md")))
    constraints = {}                      # constraint_id -> record
    url_index = defaultdict(lambda: {"instances": 0, "constraint_ids": set(),
                                     "packs": set(), "vendors": set()})
    pack_meta = []
    parse_errors = []

    for path in packs:
        pack = os.path.basename(path)[:-3]
        txt = open(path, encoding="utf-8").read()
        m = HEADER.search(txt)
        if m:
            vendor, version, dtype, endpoint = m.groups()
        else:
            vendor = version = dtype = endpoint = None
            parse_errors.append(f"{pack}: no header line")
        pack_meta.append({"pack": pack, "vendor": vendor, "version": version,
                          "endpoint": endpoint, "defect_type": dtype})

        for line in txt.splitlines():
            line = line.strip()
            if not (line.startswith("{") and '"source_url"' in line):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as e:
                parse_errors.append(f"{pack}: bad JSON ({e})")
                continue
            cid = obj.get("constraint_id") or obj.get("assertion_id")
            url = (obj.get("source_url") or "").strip()
            entry = url_index[url]
            entry["instances"] += 1
            entry["packs"].add(pack)
            if vendor:
                entry["vendors"].add(vendor)
            if not cid:
                # 相关契约段 lines carry no id; keep them but do not count as
                # a distinct constraint.
                entry["constraint_ids"].add(f"<unidentified:{pack}>")
                continue
            entry["constraint_ids"].add(cid)
            rec = constraints.setdefault(cid, {
                "constraint_id": cid, "endpoints": set(), "types": set(),
                "descriptions": set(), "assertions": set(), "urls": set(),
                "confidences": set(), "packs": set(), "vendors": set(),
            })
            rec["endpoints"].add(obj.get("endpoint"))
            rec["types"].add(obj.get("type") or obj.get("kind"))
            if obj.get("description"):
                rec["descriptions"].add(obj["description"])
            if obj.get("assertion"):
                rec["assertions"].add(obj["assertion"])
            rec["urls"].add(url)
            if obj.get("confidence") is not None:
                rec["confidences"].add(obj["confidence"])
            rec["packs"].add(pack)
            if vendor:
                rec["vendors"].add(vendor)

    # serialise
    def freeze(rec):
        out = {}
        for k, v in rec.items():
            out[k] = sorted(v, key=str) if isinstance(v, set) else v
        return out

    clist = [freeze(r) for r in constraints.values()]
    clist.sort(key=lambda r: r["constraint_id"])
    for c in clist:
        c["url_kinds"] = sorted({classify_url(u) for u in c["urls"]})

    ulist = []
    for url, info in url_index.items():
        ulist.append({
            "source_url": url,
            "kind": classify_url(url),
            "url_version": version_token(url),
            "instances": info["instances"],
            "n_constraints": len({c for c in info["constraint_ids"]
                                  if not c.startswith("<unidentified")}),
            "constraint_ids": sorted(info["constraint_ids"]),
            "packs": sorted(info["packs"]),
            "vendors": sorted(info["vendors"]),
        })
    ulist.sort(key=lambda r: -r["instances"])

    json.dump(clist, open(os.path.join(OUT, "constraints.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(ulist, open(os.path.join(OUT, "urls.json"), "w",
                          encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(pack_meta, open(os.path.join(OUT, "pack_meta.json"), "w",
                              encoding="utf-8"), ensure_ascii=False, indent=1)

    by_kind = defaultdict(lambda: [0, 0])       # kind -> [instances, distinct urls]
    for u in ulist:
        by_kind[u["kind"]][0] += u["instances"]
        by_kind[u["kind"]][1] += 1

    lines = [
        "# A1 · 抽取阶段取证 — 机械清点（不判定）", "",
        f"- 包数：{len(packs)}",
        f"- 约束条目实例：{sum(u['instances'] for u in ulist)}",
        f"- **去重后独立约束：{len(clist)}**",
        f"- **去重后独立 source_url：{len(ulist)}**",
        "",
        "## 引用页性质分布（由 URL 本身决定，不含判定）", "",
        "| 性质 | 实例数 | 独立 URL 数 |", "|---|---|---|",
    ]
    for k, (inst, n) in sorted(by_kind.items(), key=lambda kv: -kv[1][0]):
        lines.append(f"| {k} | {inst} | {n} |")
    lines += ["", "## 各库约束数与包声明的测试版本", ""]
    vend = defaultdict(lambda: {"constraints": set(), "versions": set(),
                                "kinds": defaultdict(int)})
    for c in clist:
        for v in c["vendors"]:
            vend[v]["constraints"].add(c["constraint_id"])
            for k in c["url_kinds"]:
                vend[v]["kinds"][k] += 1
    for p in pack_meta:
        if p["vendor"]:
            vend[p["vendor"]]["versions"].add(p["version"])
    lines += ["| 库 | 独立约束 | 包声明版本 | 引用页性质（约束计数） |",
              "|---|---|---|---|"]
    for v, d in sorted(vend.items()):
        kinds = "、".join(f"{k}×{n}" for k, n in sorted(d["kinds"].items(), key=lambda kv: -kv[1]))
        lines.append(f"| {v} | {len(d['constraints'])} | {', '.join(sorted(d['versions']))} | {kinds} |")
    if parse_errors:
        lines += ["", "## 解析异常", ""] + [f"- {e}" for e in parse_errors[:20]]
    open(os.path.join(OUT, "inventory.md"), "w", encoding="utf-8").write(
        "\n".join(lines) + "\n")

    print("\n".join(lines))
    print(f"\n[wrote] {OUT}\\constraints.json, urls.json, pack_meta.json, inventory.md")


if __name__ == "__main__":
    main()
