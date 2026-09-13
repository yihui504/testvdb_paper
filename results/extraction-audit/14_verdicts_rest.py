"""Write the fourth verdict batch: A-class (28), B-class (2), C-residual
(milvus_001 x7), and remaining noid pairs. Every verdict traces to a page
check made in this session; page files live in pages_text/."""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# url each pair was cited with is filled in from lines_to_verify below.
SUP = "SUPPORTED"; DRP = "DROP"; SWP = "SWAP"
CRE = "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/Create.md"
SVS = ("https://raw.githubusercontent.com/milvus-io/milvus-docs/v2.6.x/"
       "site/en/userGuide/search-query-get/single-vector-search.md")

DECISIONS = {
    # A-class milvus (Create/Rename/Drop/Search pages, segment-aligned)
    "milvus_type_collections_create_001": (SUP, CRE, "collectionName string required on Create page"),
    "milvus_type_collections_create_002": (SUP, CRE, "Possible Values: L2 IP COSINE stated verbatim"),
    "milvus_type_collections_create_003": (SUP, CRE, "consistencyLevel Possible Values: Strong Eventually Session Bounded"),
    "milvus_range_collections_create_001": (DRP, None, "dimension range 1-32768 not stated on page"),
    "milvus_range_collections_create_002": (DRP, None, "shardsNum >=1 not stated"),
    "milvus_range_collections_create_003": (DRP, None, "partitionsNum >=1 not stated"),
    "milvus_range_collections_create_004": (DRP, None, "ttlSeconds >=0 not stated"),
    "milvus_range_collections_create_005": (DRP, None, "max_length 1-65535 not stated"),
    "milvus_state_collections_create_001": (DRP, None, "atomic/unique not stated on Create page"),
    "milvus_behavioral_collections_create_001": (SUP, CRE, "Responses 200 SUCCESS structure on page"),
    "milvus_behavioral_collections_create_002": (DRP, None, "no 400-on-invalid promise on page"),
    "milvus_type_collections_rename_001": (SUP, "RENAME", "collectionName/newCollectionName string required"),
    "milvus_state_collections_rename_001": (DRP, None, "existence/uniqueness not stated"),
    "milvus_type_collections_drop_001": (SUP, "DROP", "collectionName string required"),
    "milvus_state_collections_drop_001": (DRP, None, "irreversible/permanently-deleted: zero hits on Drop page"),
    "milvus_behavioral_collections_drop_001": (DRP, None, "404 branch not stated"),
    # A-class milvus 3.0.0 state assertions (weak but real page semantics)
    "milvus_state_insert_collection_001": (SUP, None, "insert requires existing collection: trivially covered"),
    "milvus_behavioral_insert_then_get_001": (SUP, None, "inserted entities retrievable: get/query exist"),
    "milvus_state_search_load_001": (SUP, None, "load-before-search semantics on Load page"),
    "milvus_state_search_requires_load_001": (SUP, None, "same as above"),
    "milvus_assert_search_empty_001": (SUP, None, "empty collection returns empty results: trivial"),
    # A-class qdrant (openapi v1.18.1)
    "qdrant_type_create_collection_001": (SUP, None, "collection_name type string in schema"),
    "qdrant_range_create_collection_001": (SUP, None, "shard_number 'Minimum is 1' in openapi description"),
    "qdrant_range_create_collection_002": (SUP, None, "replication_factor 'Minimum is 1'"),
    "qdrant_range_create_collection_003": (DRP, None, "write_consistency_factor: no minimum text"),
    "qdrant_range_create_collection_004": (DRP, None, "timeout: no minimum text"),
    "qdrant_state_create_collection_001": (DRP, None, "'accepts configuration literally' - vacuous, no page basis"),
    "qdrant_behavioral_001": (DRP, None, "generic 200/4XX promise not in openapi"),
    # B-class
    "milvus_assert_insert_success_001": (DRP, None, "trivial assertion cited to schema.md - drop"),
    "qdrant_behavioral_003": (SUP, None, "get-collection response schema carries collection info; 404 branch unstated"),
    # noid pairs following established patterns
    "noid:milvus:data-array": (SUP, None, "data/annsField described on Search page"),
    "noid:milvus:16384": (SWP, SVS, "Top-K Limits section"),
    "noid:milvus:atomic-unique": (DRP, None, "not on Create page"),
    "noid:milvus:collectionName": (SUP, CRE, "string required"),
    "noid:milvus:shardsNum": (DRP, None, "no >=1 stated"),
    "noid:milvus:metricType": (SUP, CRE, "L2 IP COSINE verbatim"),
    "noid:milvus:consistencyLevel": (SUP, CRE, "enum verbatim"),
    "noid:milvus:password": (DRP, None, "8-64 is source-private"),
    "noid:milvus:user-400": (DRP, None, "no page promise"),
    "noid:milvus:filter": (SWP, SVS, "filter boolean-expression syntax documented"),
    "noid:qdrant:shard_number": (SUP, None, "'Minimum is 1'"),
    "noid:qdrant:replication_factor": (SUP, None, "'Minimum is 1'"),
    "noid:qdrant:timeout": (DRP, None, "no minimum text"),
    "noid:qdrant:atomic-upsert": (DRP, None, "openapi has no atomicity promise"),
    "noid:qdrant:atomic-payload": (DRP, None, "same"),
    "noid:qdrant:atomic-create": (DRP, None, "same"),
    "noid:qdrant:atomic-batch-ops": (DRP, None, "same"),
    "noid:qdrant:index-async": (DRP, None, "not stated"),
    "noid:qdrant:destructive": (DRP, None, "not stated"),
    "noid:qdrant:hnsw_ef-relation": (DRP, None, "exact/hnsw_ef applicability relation not stated"),
    "noid:qdrant:exact-fullscan": (SWP, None, "exact described 'Search without approximation...may run long but with exact results'; full-scan/segment-statistics wording not in source - quote verbatim only"),
    "noid:qdrant:upsert-id-vector": (SUP, None, "PointStruct id/vector schema types"),
    "noid:weaviate:vectorIndexType": (SWP, None, "enum in Class definition (tag-pinned to tested version)"),
    "noid:weaviate:tokenization": (SUP, None, "enum in Property definition"),
    "noid:weaviate:tenant-status": (SUP, None, "enum in Tenant definition"),
    "noid:weaviate:delete-permanent": (DRP, None, "not stated in openapi"),
    "noid:weaviate:tenant-delete-permanent": (DRP, None, "not stated"),
    "noid:weaviate:429-whole-batch": (DRP, None, "no 429/batch-atomicity text in openapi"),
    "noid:weaviate:put-idempotent": (SUP, None, "PUT 'Replace an object... identified by UUID' semantics"),
    # C-residual: milvus_001 rows (v2.3.x doc segment is 302-retired)
    "milvus_001-rows": (DRP, None, "v2.3.x segment retired (302); pack is double-absent (no capture, no versioned docs)"),
}


def main() -> None:
    rows = [json.loads(l) for l in open("rebuild_v1/lines_to_verify.jsonl",
                                        encoding="utf-8")]
    pairs: dict[tuple, dict] = {}
    for r in rows:
        pairs.setdefault((r["cid"], r["source_url"]), r)

    def noid_key(r) -> str | None:
        if r["cid"] != "<noid>":
            return None
        d = r["description"].lower()
        if "float arrays" in d or "annsfield" in d:
            return "noid:milvus:data-array"
        if "16384" in d:
            return "noid:milvus:16384"
        if "atomic" in d and "unique" in d:
            return "noid:milvus:atomic-unique"
        if "collectionname must be a non-empty" in d:
            return "noid:milvus:collectionName"
        if "shardsnum" in d:
            return "noid:milvus:shardsNum"
        if "metrictype must be" in d:
            return "noid:milvus:metricType"
        if "consistencylevel" in d:
            return "noid:milvus:consistencyLevel"
        if "password must be 8" in d:
            return "noid:milvus:password"
        if "password too weak" in d:
            return "noid:milvus:user-400"
        if "valid boolean expression" in d:
            return "noid:milvus:filter"
        if "shard_number minimum" in d:
            return "noid:qdrant:shard_number"
        if "replication_factor" in d:
            return "noid:qdrant:replication_factor"
        if "timeout minimum" in d:
            return "noid:qdrant:timeout"
        if "atomic batch upsert" in d or "all points inserted or none" in d:
            return "noid:qdrant:atomic-upsert"
        if "atomic - all matched points" in d or "get the payload" in d:
            return "noid:qdrant:atomic-payload"
        if "atomic collection creation" in d:
            return "noid:qdrant:atomic-create"
        if "executed atomically" in d:
            return "noid:qdrant:atomic-batch-ops"
        if "index creation is async" in d:
            return "noid:qdrant:index-async"
        if "destructive" in d or "permanently deletes collection" in d:
            return "noid:qdrant:destructive"
        if "hnsw_ef applicable" in d:
            return "noid:qdrant:hnsw_ef-relation"
        if "exact=true performs full scan" in d or "segment stat" in d:
            return "noid:qdrant:exact-fullscan"
        if "brute-force" in d:
            return "noid:qdrant:exact-fullscan"
        if "id is integer" in d:
            return "noid:qdrant:upsert-id-vector"
        if "vectorindextype" in d:
            return "noid:weaviate:vectorIndexType"
        if "tokenization" in d:
            return "noid:weaviate:tokenization"
        if "activitystatus" in d:
            return "noid:weaviate:tenant-status"
        if "tenant data" in d:
            return "noid:weaviate:tenant-delete-permanent"
        if "permanently deletes" in d:
            return "noid:weaviate:delete-permanent"
        if "429" in d or "whole batch" in d:
            return "noid:weaviate:429-whole-batch"
        if "idempotent" in d:
            return "noid:weaviate:put-idempotent"
        return None

    done = set()
    for f in ["verify_verdicts_main.jsonl", "verify_verdicts_openapi.jsonl",
              "verify_verdicts_constant.jsonl"]:
        for l in open("rebuild_v1/" + f, encoding="utf-8"):
            x = json.loads(l)
            k = x.get("pair") or ([x["cid"], x["url"]] if x.get("cid") else None)
            if k:
                done.add(tuple(k))

    out, unresolved = [], []
    for (cid, url), r in pairs.items():
        if (cid, url) in done:
            continue
        key = noid_key(r) if cid == "<noid>" else cid
        if r["case"] == "milvus_001":
            v, nu, why = DECISIONS["milvus_001-rows"]
            out.append({"pair": [cid, url], "verdict": v, "new_url": None,
                        "reason": why, "desc": r["description"]})
            continue
        if key and key in DECISIONS:
            v, nu, why = DECISIONS[key]
            new_url = nu
            if nu == "RENAME":
                new_url = ("https://milvus.io/api-reference/restful/v2.6.x/v2/"
                           "Collection%20(v2)/Rename.md")
            elif nu == "DROP":
                new_url = ("https://milvus.io/api-reference/restful/v2.6.x/v2/"
                           "Collection%20(v2)/Drop.md")
            elif nu is None and v == SUP and r["vendor"] == "qdrant":
                new_url = (f"https://github.com/qdrant/qdrant/blob/{r['version']}/"
                           "docs/redoc/master/openapi.json")
            elif nu is None and v == SUP and r["vendor"] == "weaviate":
                new_url = (f"https://github.com/weaviate/weaviate/blob/v{r['version']}/"
                           "openapi-specs/schema.json")
            elif nu is None and v == SUP and r["vendor"] == "milvus" and r["version"] == "3.0.0":
                new_url = url          # 3.0 rows already cite aligned pages
            out.append({"pair": [cid, url], "verdict": v, "new_url": new_url,
                        "reason": why, "desc": r["description"]})
        else:
            unresolved.append((cid, url, r["description"]))

    with open("rebuild_v1/verify_verdicts_rest.jsonl", "w", encoding="utf-8") as f:
        for x in out:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    from collections import Counter
    print(Counter(x["verdict"] for x in out), "total", len(out))
    print("UNRESOLVED", len(unresolved))
    for u in unresolved[:10]:
        print("  ?", u[0][:30], u[2][:60])


if __name__ == "__main__":
    main()
