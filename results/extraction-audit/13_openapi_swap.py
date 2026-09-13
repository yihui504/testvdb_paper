"""Resolve the LANDING / qdrant_001 / weaviate mismatch pairs against the
tested version's own OpenAPI artifact.

Each pair gets a mechanical proposal:
  SWAP  -> constraint text co-occurs inside one operation block of the
           tested version's openapi (replacement source_url = tag-pinned file)
  DROP  -> no block contains the semantics
Blocks = (path, method, summary+description+parameter descriptions) tuples.
"""
import glob
import json
import re
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STOP = {"must", "should", "with", "that", "this", "when", "than", "from",
        "into", "only", "error", "errors", "returns", "return", "string",
        "integer", "boolean", "value", "values", "field", "fields", "type",
        "types", "single", "request", "requests", "operation", "operations",
        "collection", "collections", "point", "points", "query", "queries",
        "result", "results", "provided", "specified", "default", "success",
        "atomic", "silently"}


def _schema_text(sch: dict, depth: int = 0) -> str:
    """Recursively collect descriptions and enum values from a schema."""
    if depth > 3 or not isinstance(sch, dict):
        return ""
    parts = [sch.get("description") or ""]
    if sch.get("enum"):
        parts.append("enum: " + " ".join(str(e) for e in sch["enum"]))
    for name, sub in (sch.get("properties") or {}).items():
        parts.append(name + " " + _schema_text(sub, depth + 1))
    if isinstance(sch.get("items"), dict):
        parts.append(_schema_text(sch["items"], depth + 1))
    return " ".join(parts)


def load_blocks(fn: str) -> list[dict]:
    d = json.load(open(fn, encoding="utf-8"))
    blocks = []
    for path, ops in (d.get("paths") or {}).items():
        for method, op in ops.items():
            if method not in ("get", "post", "put", "patch", "delete"):
                continue
            parts = [op.get("summary") or "", op.get("description") or ""]
            for p in op.get("parameters") or []:
                parts.append(p.get("description") or "")
            body = op.get("requestBody") or {}
            for c in (body.get("content") or {}).values():
                parts.append(_schema_text(c.get("schema") or {}))
            for code, resp in (op.get("responses") or {}).items():
                parts.append(f"{code}: " + str(resp.get("description") or ""))
            # Swagger 2: body param schema
            for p in op.get("parameters") or []:
                if p.get("in") == "body":
                    parts.append(_schema_text(p.get("schema") or {}))
            blocks.append({"path": path, "method": method,
                           "text": " ".join(parts)})
    # definitions / components.schemas: one block per named schema
    defs = (d.get("definitions") or
            ((d.get("components") or {}).get("schemas") or {}))
    for name, sch in defs.items():
        t = _schema_text(sch)
        if t.strip():
            blocks.append({"path": f"#def:{name}", "method": "def",
                           "text": t})
    return blocks


def feats(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z_]{4,}", s.lower()) if w not in STOP]


def best_block(feats_: list[str], blocks: list[dict]) -> tuple[int, str]:
    best_n, best_ref = 0, ""
    for b in blocks:
        t = b["text"].lower()
        n = sum(1 for w in feats_ if w in t)
        if n > best_n:
            best_n, best_ref = n, f"{b['method'].upper()} {b['path']}"
    return best_n, best_ref


Q_OPENAPI = {
    "1.12.1": "pages_text/qdrant_openapi_v1.12.1.json.txt",
    "1.18.0": "pages_text/qdrant_openapi_v1.18.0.json.txt",
    "1.18.1": "pages_text/qdrant_openapi_v1.18.1.json.txt",
    "1.18.2": "pages_text/github.com_qdrant_qdrant_blob_v1.18.2_docs_redoc_master_openapi.json.txt",
    "1.18.3": "pages_text/qdrant_openapi_v1.18.3.json.txt",
    "1.19.0": "pages_text/qdrant_openapi_v1.19.0.json.txt",
}


def main() -> None:
    rows = [json.loads(l) for l in open("rebuild_v1/lines_to_verify.jsonl",
                                        encoding="utf-8")]
    pairs: dict[tuple, list[dict]] = defaultdict(list)
    for r in rows:
        pairs[(r["cid"], r["source_url"])].append(r)

    blocks_cache: dict[str, list[dict]] = {}

    def blocks_for(vendor: str, version: str):
        if vendor == "qdrant":
            fn = Q_OPENAPI.get(version)
            if fn and fn not in blocks_cache:
                blocks_cache[fn] = load_blocks(fn)
            return blocks_cache.get(fn)
        if vendor == "weaviate":
            fn = f"pages_text/weaviate_v{version}_schema.json.txt"
            import os
            if not os.path.exists(fn):
                return None
            if fn not in blocks_cache:
                blocks_cache[fn] = load_blocks(fn)
            return blocks_cache[fn]
        return None

    out = []
    for (cid, url), rs in pairs.items():
        r = rs[0]
        vendor, version = r["vendor"], r["version"]
        is_landing = url.rstrip("/").endswith("/api-reference")
        is_q1 = vendor == "qdrant" and version == "1.12.1"
        is_w = (vendor == "weaviate" and "openapi-specs/schema.json" in url
                and f"v{version}" not in url)
        if not (is_landing or is_q1 or is_w):
            continue
        blocks = blocks_for(vendor, version)
        if not blocks:
            out.append({"pair": [cid, url], "verdict": "MANUAL",
                        "reason": f"no openapi for {vendor} {version}",
                        "desc": r["description"],
                        "cases": [x["case"] for x in rs]})
            continue
        f = feats(" ".join([r["assertion"], r["description"], cid]))
        n, ref = best_block(f, blocks)
        if vendor == "qdrant":
            new_url = (f"https://github.com/qdrant/qdrant/blob/{version}/"
                       "docs/redoc/master/openapi.json")
        else:
            new_url = (f"https://github.com/weaviate/weaviate/blob/v{version}/"
                       "openapi-specs/schema.json")
        if n >= max(2, len(f) // 3):
            verdict, detail = "SWAP", f"{n}/{len(f)} feats in {ref}"
        elif n >= 1:
            verdict, detail = "MANUAL", f"weak {n}/{len(f)} in {ref}"
        else:
            verdict, detail = "DROP", "no block hit"
        out.append({"pair": [cid, url], "verdict": verdict, "detail": detail,
                    "new_url": new_url if verdict == "SWAP" else None,
                    "desc": r["description"],
                    "cases": [x["case"] for x in rs]})

    with open("rebuild_v1/openapi_swap_worksheet.jsonl", "w",
              encoding="utf-8") as fh:
        for rec in out:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter(x["verdict"] for x in out))
    print()
    for x in out:
        if x["verdict"] == "MANUAL":
            print(f"  MANUAL {x['pair'][0][:40]:42s} {x.get('detail','')[:40]} | {x['desc'][:60]}")
    print()
    for x in out:
        if x["verdict"] == "DROP":
            print(f"  DROP   {x['pair'][0][:40]:42s} | {x['desc'][:60]}")


if __name__ == "__main__":
    main()
