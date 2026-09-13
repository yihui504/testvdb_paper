"""Batch C-pass: full breakdown of the 79 true-MISMATCH pairs, mechanical
resolution of constant.go pairs, index.md pairs, and LANDING pairs.

Outputs rebuild_v1/c_pass_worksheet.jsonl - one record per pair with a
mechanical resolution proposal for the human to confirm.
"""
import json
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = "https://api.qdrant.tech/v-1-18-x/api-reference"
ROOT_TXT = "pages_text/api.qdrant.tech_v-1-18-x_api-reference.txt"


def version_token(url: str) -> str | None:
    m = re.search(r"/v[-]?(\d+\.\d+(?:\.\d+)?|x)[./-]", url)
    if m:
        return m.group(1)
    m = re.search(r"/v-(\d+)-(\d+)(?:-|/)", url)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def aligned(url_ver: str | None, tested: str) -> str:
    if url_ver is None:
        return "page-unversioned"
    u, t = url_ver.split("."), tested.split(".")
    if u == t:
        return "aligned"
    if len(u) == 3 and u[2] == "x" and u[:2] == t[:2]:
        return "aligned-segment"
    if len(u) == 2 and len(t) >= 2 and u == t[:2]:
        return "aligned-segment"
    return "MISMATCH"


def main() -> None:
    rows = [json.loads(l) for l in open("rebuild_v1/lines_to_verify.jsonl",
                                        encoding="utf-8")]
    pairs: dict[tuple, dict] = {}
    for r in rows:
        k = (r["cid"], r["source_url"])
        pairs.setdefault(k, r)

    mis_groups: dict[str, list] = defaultdict(list)
    for r in pairs.values():
        uv = version_token(r["source_url"])
        if aligned(uv, r["version"]) != "MISMATCH":
            continue
        if "constant.go" in r["source_url"]:
            g = "constant.go tag v2.6.17"
        elif r["version"] == "2.3":
            g = "milvus tested 2.3 (milvus_001)"
        elif r["vendor"] == "qdrant":
            g = "qdrant_001 1.12.1"
        elif r["vendor"] == "weaviate":
            g = "weaviate 1.37.4 -> v1.38.0 tag"
        else:
            g = f"other ({r['case']})"
        mis_groups[g].append(r)
    print("79 真 MISMATCH 对构成:")
    for g, lst in sorted(mis_groups.items(), key=lambda kv: -len(kv[1])):
        print(f"  {len(lst):>3}  {g}")

    # ---- constant.go independent constraints: propose doc-page replacement
    print("\n== constant.go 对（换文档页判定素材）==")
    root_text = open(ROOT_TXT, encoding="utf-8").read()
    out = []
    for r in pairs.values():
        if "constant.go" not in r["source_url"]:
            continue
        out.append({"pair": [r["cid"], r["source_url"]], "group": "constant.go",
                    "proposal": "swap to doc page or drop (G3: src-as-doc)",
                    "desc": r["description"], "assertion": r["assertion"],
                    "cases": []})
        print(f"  {r['cid'][:46]} | {r['description'][:60]}")

    # ---- index.md pairs: nprobe/ef -> Search page
    print("\n== index.md 对（换 Search.md 判定素材）==")
    search_txt = None
    try:
        search_txt = open(
            "pages_text/milvus.io_api-reference_restful_v2.6.x_v2_Vector (v2)_Search.txt",
            encoding="utf-8").read()
    except FileNotFoundError:
        cand = [f for f in __import__("os").listdir("pages_text")
                if "Search" in f and "milvus" in f.lower()]
        print("  (search page file candidates:", cand, ")")
    for r in pairs.values():
        if r["source_url"] != "https://milvus.io/docs/index.md":
            continue
        hit = bool(search_txt) and bool(re.search(
            r"nprobe|ef\s|ef\s*=|search_params", search_txt, re.I))
        out.append({"pair": [r["cid"], r["source_url"]], "group": "index.md",
                    "proposal": "swap to Vector (v2)/Search.md (v-segment of tested version)",
                    "kw_in_search_page": hit, "desc": r["description"],
                    "assertion": r["assertion"], "cases": []})
        print(f"  {r['cid'][:46]} | nprobe/ef 在 Search 页: {hit}")

    # ---- LANDING pairs: search root text, propose subpage slug
    print("\n== LANDING 对（根页检索+子页映射建议）==")
    for r in pairs.values():
        if not r["source_url"].rstrip("/").endswith("/api-reference"):
            continue
        blob = " ".join([r["assertion"], r["description"], r["cid"]])
        words = [w for w in re.findall(r"[a-z_]{4,}", blob.lower())
                 if w not in {"must", "should", "with", "that", "this",
                              "when", "than", "from", "into", "only",
                              "error", "returns", "return", "string",
                              "integer", "boolean", "collection", "vector",
                              "point", "points", "search", "query"}]
        found = [w for w in words if w in root_text.lower()]
        slug_hint = ""
        m = re.search(r"[a-z]+_([a-z]+)_?\d*$", r["cid"])
        if m:
            slug_hint = m.group(1)
        out.append({"pair": [r["cid"], r["source_url"]], "group": "LANDING",
                    "proposal": f"resolve subpage under {ROOT}; slug hint: {slug_hint}",
                    "kw_in_root": found[:8], "desc": r["description"],
                    "assertion": r["assertion"], "cases": []})

    with open("rebuild_v1/c_pass_worksheet.jsonl", "w", encoding="utf-8") as f:
        for rec in out:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\n[wrote] rebuild_v1/c_pass_worksheet.jsonl ({len(out)} records)")

    # stats recap for the report
    n_land = sum(1 for r in pairs.values()
                 if r["source_url"].rstrip("/").endswith("/api-reference"))
    print(f"LANDING 对总数: {n_land}")


if __name__ == "__main__":
    main()
