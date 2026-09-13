"""M3 — assemble the final rebuilt packs from the original 81 plus the four
verdict batches, then re-run gates G1-G8 mechanically and write the rebuild
completion report.

Pack layout (frozen schema, G8-clean):
  header line                     verbatim
  --- observed ---                verbatim (milvus_001 stays as-is, flagged)
  --- contract ---                rebuilt rows: keep/SWAP with source_type +
                                  evidence_tier annotations; DROPped rows gone;
                                  case-level archaeology sections for the 4
                                  main-assertion and empty-contract packs
  --- maintainer attitude ---     verbatim where present
  VERDICT line                    verbatim
"""
import glob
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

MAT = r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/arms/materials_complete"
AUD = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
OUT = AUD + r"/rebuild_final"
SEG_RE = re.compile(r"^---\s*(.+?)\s*---\s*$", re.M)
JSON_LINE = re.compile(r"^\{.*\"source_url\".*\}$")
ISSUE_NO = re.compile(r"#\d{4,6}")
V26_METRIC = ("https://raw.githubusercontent.com/milvus-io/milvus-docs/v2.6.x/"
              "site/en/userGuide/search-query-get/metric.md")
V30_GROUPING = ("https://raw.githubusercontent.com/milvus-io/milvus-docs/99af7351/"
                "site/en/userGuide/search-query-get/grouping-search.md")
UPsert = ("https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/"
          "Upsert.md")


def seg_kind(name: str) -> str:
    if "观察" in name:
        return "observed"
    if "补充契约依据" in name:
        return "archaeology"
    if "补充契约行" in name:
        return "bulk"
    if "维护者态度" in name:
        return "maintainer"
    if "契约依据" in name:
        return "core"
    return "other"


def split_pack(txt: str) -> dict[str, str]:
    marks = [(m.start(), m.group(1)) for m in SEG_RE.finditer(txt)]
    segs = {"_head": txt[: marks[0][0]] if marks else txt}
    for i, (pos, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
        segs[name] = txt[pos:end]
    return segs


def source_type(url: str) -> str:
    if "openapi" in url or "schema.json" in url:
        return "structured-spec"
    if any(d in url for d in ("milvus.io", "api.qdrant.tech",
                              "weaviate.io", "milvus-docs")):
        return "documentation"
    if "github.com" in url or "raw.githubusercontent" in url:
        return "documentation"     # milvus-docs raw pages are documentation
    return "documentation"


def tier_of(row_text: str) -> str:
    if "Possible Values" in row_text or "enum" in row_text.lower():
        return "explicit"
    return "inferred_from_behavior"


# ---------------- case-level archaeology sections ----------------
CASE_SECTIONS = {
    "milvus_013": [
        "[本版本文档中无 endpoint=collections+list 的约束条目]",
        "[本版本文档中无 Request-Timeout 的类型约束条目]",
        "已核查的引用页（2.6.x REST API 参考，实测可访问，来源类型=documentation）：",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Drop.md",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Load.md",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Rename.md",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Get.md",
        "- https://milvus.io/api-reference/restful/v2.6.x/v2/Vector%20(v2)/Search.md",
        "核查结论：上述页面的 Parameters 表仅将 Authorization 列为 header 参数；Request-Timeout",
        "仅出现在 curl 示例行中，不含任何类型或取值约束的描述。",
    ],
    "qdrant_016": [
        "[v1.18.2 openapi 及其派生文档中无 lookup_from.collection 的存在性约束条目]",
        "openapi 中 lookup_from 的全部语义（原文）：\"The location used to lookup vectors.",
        "If not specified - use current collection. Note: the other collection should",
        "have the same vector size as the current collection\"",
        "来源：https://github.com/qdrant/qdrant/blob/v1.18.2/docs/redoc/master/openapi.json （structured-spec，tag-pinned）",
    ],
    "milvus_012": [
        "描述性依据（documentation，v2.6.x 段）：dbName 参数文档描述为",
        "\"The name of an existing database.\"（string，无 required 标注，无非空/拒绝语义声明）",
        "来源：https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/List.md",
    ],
    "milvus_017": [
        "描述性依据（documentation，v2.6.x 段）：collectionName 参数文档描述为",
        "\"The name of an existing collection. If specified, only returns aliases of the",
        "specified collection. If not specified, returns aliases of all collections.\"",
        "（无 required 标注）",
        "来源：https://milvus.io/api-reference/restful/v2.6.x/v2/Alias%20(v2)/List.md",
    ],
    "qdrant_014": [
        "[v-1-18-x 文档对 POST /cluster/recover 无行为约束条目]",
        "该页仅含端点签名与示例响应，无 standalone 模式前提或错误行为的任何声明。",
        "来源：https://api.qdrant.tech/v-1-18-x/api-reference/distributed/recover-current-peer",
    ],
    "milvus_001": [
        "[受测版本 2.3.0 的版本文档段已下线（v2.3.x → 302），约束依据无法核查]",
        "观察证据：原始执行未捕获任何 HTTP 交互（output_milvus_001.log = \"[no raw HTTP captured]\"）。",
    ],
}

CASE_ROWS = {
    # case -> single rebuilt contract row (dict), for empty-pack archaeology
    "milvus_008": {"constraint_id": "milvus_metric_cosine_range_001",
                   "endpoint": "entities+search",
                   "description": "COSINE metric: similarity distance value range",
                   "assertion": "COSINE: similarity distance value range is [-1, 1]; a greater value indicates a greater similarity",
                   "source_url": V26_METRIC, "source_type": "documentation",
                   "evidence_tier": "explicit"},
    "milvus_038": {"constraint_id": "milvus_state_group_by_field_001",
                   "endpoint": "entities+search",
                   "description": "group_by_field enables Grouping Search",
                   "assertion": "documentation presents group_by_field as grouping search results over a scalar field's values (examples: docId, category); no normative statement about vector-field values being rejected",
                   "source_url": V30_GROUPING, "source_type": "documentation",
                   "evidence_tier": "inferred_from_behavior"},
    "milvus_034": {"constraint_id": "milvus_upsert_schema_match_001",
                   "endpoint": "entities+upsert",
                   "description": "data must match collection schema (page verbatim)",
                   "assertion": "\"data: An entity object or an array of entity objects. Note that the keys in an entity object should match the collection schema\"",
                   "source_url": UPsert, "source_type": "documentation",
                   "evidence_tier": "explicit"},
    "milvus_039": {"constraint_id": "milvus_upsert_schema_match_001",
                   "endpoint": "entities+upsert",
                   "description": "data must match collection schema (page verbatim)",
                   "assertion": "\"the keys in an entity object should match the collection schema\" (schema declares id Int64)",
                   "source_url": UPsert, "source_type": "documentation",
                   "evidence_tier": "explicit"},
    "milvus_041": {"constraint_id": "milvus_upsert_schema_match_001",
                   "endpoint": "entities+upsert",
                   "description": "data must match collection schema (page verbatim)",
                   "assertion": "\"the keys in an entity object should match the collection schema\" (observed: string->DOUBLE, 'true'->BOOL, 1->BOOL, '42'->INT16 all accepted)",
                   "source_url": UPsert, "source_type": "documentation",
                   "evidence_tier": "explicit"},
    "qdrant_018": {"constraint_id": "qdrant_count_exact_001",
                   "endpoint": "points+count",
                   "description": "exact semantics (page verbatim)",
                   "assertion": "\"exact boolean, defaults true: If true, count exact number of points. If false, count approximate number of points faster. Approximate count might be unreliable during the indexing process\"",
                   "source_url": "https://api.qdrant.tech/v-1-18-x/api-reference/points/count-points",
                   "source_type": "documentation", "evidence_tier": "explicit"},
    "qdrant_023": {"constraint_id": "qdrant_snapshot_recover_001",
                   "endpoint": "snapshots+recover",
                   "description": "recover restores collection state from snapshot",
                   "assertion": "PUT /collections/{name}/snapshots/recover recovers the collection from the given snapshot location",
                   "source_url": "https://api.qdrant.tech/v-1-19-x/api-reference/snapshots/recover-from-snapshot",
                   "source_type": "documentation", "evidence_tier": "explicit"},
}

# packs whose contract sections come only from CASE_SECTIONS/CASE_ROWS
CASE_ARCH = set(CASE_SECTIONS) | set(CASE_ROWS)


def load_verdicts() -> dict[tuple[str, str], dict]:
    v: dict[tuple[str, str], dict] = {}
    for f in ("verify_verdicts_openapi.jsonl", "verify_verdicts_constant.jsonl",
              "verify_verdicts_rest.jsonl"):
        for l in open(AUD + "/rebuild_v1/" + f, encoding="utf-8"):
            x = json.loads(l)
            v[tuple(x["pair"])] = x
    return v


def norm_path(endpoint: str) -> list[str]:
    e = re.sub(r"\{[^}]*\}", " ", endpoint)
    e = re.sub(r"\b(get|post|put|patch|delete)\b", " ", e, flags=re.I)
    return [t.lower() for t in re.split(r"[+/ \-]+", e) if t.lower()]


def _stem(t: str) -> str:
    return t.rstrip("s") if len(t) > 3 else t


def g4_match(pack_ep: str, row_ep: str | None) -> bool:
    if not row_ep:
        return False
    p, r = norm_path(pack_ep), norm_path(row_ep)
    if not p or not r:
        return False
    shorter = min(len(p), len(r))
    if p[:shorter] == r[:shorter]:
        return True
    if len(p) == 1 and any(_stem(p[0]) == _stem(t) for t in r):
        return True
    return False


def fix_url(url: str) -> str:
    """qdrant repo tags carry a v prefix; SWAP verdicts wrote bare versions."""
    return re.sub(r"(qdrant/qdrant/blob/)(\d)", r"\1v\2", url)


def main() -> None:
    os.makedirs(OUT + "/packs", exist_ok=True)
    verdicts = load_verdicts()
    stats = Counter()
    gate = {"G1": Counter(), "G2": Counter(), "G3": Counter(), "G4": Counter(),
            "G5": Counter(), "G6": Counter(), "G8": Counter()}
    audit_rows = []

    for path in sorted(glob.glob(MAT + "/*.md")):
        case = os.path.basename(path)[:-3]
        txt = open(path, encoding="utf-8").read()
        segs = split_pack(txt)
        head = segs["_head"]
        h = re.search(r"endpoint=([^\]]+)\]", head)
        pack_ep = h.group(1) if h else ""
        hv = re.search(r"version=(\S+)", head)
        pack_ver = hv.group(1) if hv else ""

        observed = maintainer = other_tail = ""
        kept_rows: list[str] = []
        for name, body in segs.items():
            if name == "_head":
                continue
            k = seg_kind(name)
            if k == "observed":
                observed = body
            elif k == "maintainer":
                maintainer = body
            elif k in ("core", "bulk", "archaeology"):
                if case in CASE_ARCH:
                    continue            # rebuilt wholesale below
                for line in body.splitlines():
                    line = line.strip()
                    if not JSON_LINE.match(line):
                        continue
                    obj = json.loads(line)
                    cid = obj.get("constraint_id") or obj.get("assertion_id") or "<noid>"
                    url = obj.get("source_url", "")
                    if not g4_match(pack_ep, obj.get("endpoint")):
                        stats["dropped_g4"] += 1
                        continue
                    vd = verdicts.get((cid, url))
                    if vd is None:
                        stats["verdict_missing"] += 1
                        continue
                    if vd["verdict"] == "DROP":
                        stats["dropped"] += 1
                        continue
                    if "constant.go" in url:
                        continue
                    if vd.get("new_url"):
                        u = fix_url(vd["new_url"])
                        # repo-tag artifacts: pin to THIS pack's tested version
                        u = re.sub(r"(qdrant/qdrant/blob/)v?[\d.]+",
                                   rf"\g<1>v{pack_ver}", u)
                        u = re.sub(r"(weaviate/weaviate/blob/)v?[\d.]+",
                                   rf"\g<1>v{pack_ver}", u)
                        obj["source_url"] = u
                    elif cid in ("qdrant_state_query_points_010",
                                 "qdrant_behavioral_010",
                                 "qdrant_behavioral_017"):
                        obj["source_url"] = (f"https://github.com/qdrant/qdrant/"
                                             f"blob/v{pack_ver}/docs/redoc/"
                                             "master/openapi.json")
                    elif cid == "weaviate_behavioral_schema_create_001":
                        obj["source_url"] = (f"https://github.com/weaviate/"
                                             f"weaviate/blob/v{pack_ver}/"
                                             "openapi-specs/schema.json")
                    obj["source_type"] = source_type(obj["source_url"])
                    obj["evidence_tier"] = tier_of(
                        json.dumps(obj, ensure_ascii=False))
                    obj.pop("_audit", None)
                    obj.pop("_provenance", None)
                    kept_rows.append(json.dumps(obj, ensure_ascii=False))
                    stats["kept"] += 1
            else:
                other_tail += body

        # case-level rebuild for archaeology packs
        arch_lines = []
        if case in CASE_ROWS:
            arch_lines.append(json.dumps(CASE_ROWS[case], ensure_ascii=False))
        if case in CASE_SECTIONS:
            arch_lines += CASE_SECTIONS[case]

        # assemble
        out = [head.rstrip()]
        out.append(observed.rstrip())
        out.append("--- 契约依据（expected，M3 重建版） ---")
        body_lines = kept_rows + arch_lines
        if not body_lines:
            out.append(f"[经端点过滤与依据核查后，无 endpoint={pack_ep} 的可核查约束行]")
            gate["G1"][f"empty-{case}"] += 1
        out.extend(body_lines)
        if maintainer:
            out.append(maintainer.rstrip())
        out.append(other_tail.rstrip())
        open(f"{OUT}/packs/{case}.md", "w", encoding="utf-8").write(
            "\n".join(x for x in out if x.strip()) + "\n")
        audit_rows.append({"case": case, "rows_kept": len(kept_rows),
                           "arch": len(arch_lines)})
        stats["packs"] += 1

    # ---- gate re-checks (mechanical, on the rebuilt packs)
    ISSUE = re.compile(r"#\d{4,6}")
    for path in sorted(glob.glob(OUT + "/packs/*.md")):
        case = os.path.basename(path)[:-3]
        t = open(path, encoding="utf-8").read()
        m = re.search(r"version=(\S+)", t)
        ver = m.group(1) if m else ""
        m = re.search(r"endpoint=([^\]]+)\]", t)
        pack_ep = m.group(1) if m else ""
        obs = re.search(r"---\s*观察到的行为.*?\n(.*?)---\s*契约依据", t, re.S)
        gate["G5"]["ok" if obs and len(obs.group(1)) > 100 else
                  ("degenerate:" + case if case == "milvus_001" else "FAIL:" + case)] += 1
        for line in t.splitlines():
            line = line.strip()
            if not JSON_LINE.match(line):
                continue
            try:
                o = json.loads(line)
            except json.JSONDecodeError:
                continue
            url = o.get("source_url", "")
            if "constant.go" in url or ".go" in url:
                gate["G8"]["FAIL:" + case] += 1
            if "openapi" in url or "schema.json" in url:
                gate["G3"]["spec"] += 1
            else:
                gate["G3"]["doc"] += 1
            mm = re.search(r"/v[-]?(\d+\.\d+)", url)
            if not mm:
                mm = re.search(r"/v-(\d+)-(\d+)(?:-|/)", url)
                segv = f"{mm.group(1)}.{mm.group(2)}" if mm else None
            else:
                segv = mm.group(1)
            if segv:
                gate["G1"]["aligned" if ver.startswith(segv) else
                          ("MISMATCH:" + case)] += 1
            else:
                gate["G1"]["unversioned"] += 1
            if "api-reference\n" in url or url.rstrip("/").endswith("/api-reference"):
                gate["G2"]["landing-FAIL"] += 1
            else:
                gate["G2"]["ok"] += 1
            if "milvus.io/docs/index" in url:
                gate["G2"]["unresolvable-FAIL"] += 1
        body_no_maint = re.sub(r"---\s*维护者态度.*?(?=VERDICT|$)", "", t,
                               flags=re.S)
        hits = ISSUE.findall(body_no_maint)
        if hits:
            gate["G6"]["FAIL:" + case] += 1

    json.dump(audit_rows, open(OUT + "/assembly_audit.json", "w",
                               encoding="utf-8"), ensure_ascii=False, indent=1)
    print("stats:", dict(stats))
    print()
    for g, c in gate.items():
        print(g, dict(c))


if __name__ == "__main__":
    main()
