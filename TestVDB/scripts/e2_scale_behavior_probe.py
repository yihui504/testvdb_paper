#!/usr/bin/env python3
"""E2 Vein B: behavior-level doc-impl gaps (idempotency / permissiveness).

Probe operations where documentation implies an error, and record whether the
impl returns SUCCESS (by-design idempotent/permissive) => a behavior-level
doc-impl gap (candidate over-strict, like the original w1 4 behaviors).
"""
from __future__ import annotations
import sys
import time
import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from pymilvus import MilvusClient

S = requests.Session()
S.trust_env = False
QB = "http://localhost:6333"
CL = MilvusClient("http://localhost:19530")
DIM = 4


def mprobe(label: str, fn) -> None:
    try:
        fn()
        print(f"  [milvus] {label:46} SUCCESS (by-design gap)")
    except Exception as e:
        print(f"  [milvus] {label:46} ERROR  ({str(e)[:60]})")


def qprobe(label: str, method: str, path: str, **kw) -> None:
    r = S.request(method, f"{QB}{path}", timeout=15, **kw)
    gap = r.status_code < 400
    try:
        body = r.json()
        if isinstance(body, dict) and body.get("status") == "error":
            gap = False
    except Exception:
        pass
    tag = "SUCCESS (by-design gap)" if gap else "ERROR"
    print(f"  [qdrant] {label:46} HTTP={r.status_code} {tag}  {r.text[:50]}")


def main() -> None:
    # --- Milvus setup ---
    for c in ("e2b_main", "e2b_idx", "e2b_part"):
        try:
            CL.drop_collection(c)
        except Exception:
            pass
    CL.create_collection(collection_name="e2b_main", dimension=DIM, metric_type="L2")
    from pymilvus import DataType
    schema = CL.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=DIM)
    CL.create_collection(collection_name="e2b_idx", schema=schema)

    print("=== Milvus behavior probes ===\n")
    # 1. drop non-existent partition
    mprobe("drop non-existent partition", lambda: CL.drop_partition("e2b_main", "ghost_part"))
    # 2. create already-existing partition
    CL.create_partition("e2b_main", "dup_part")
    mprobe("create already-existing partition", lambda: CL.create_partition("e2b_main", "dup_part"))
    # 3. release a not-loaded collection
    mprobe("release not-loaded collection", lambda: CL.release_collection("e2b_main"))
    # 4. create already-existing index
    ip = CL.prepare_index_params()
    ip.add_index(field_name="vector", index_type="HNSW", metric_type="L2", params={"M": 8, "efConstruction": 64})
    CL.create_index(collection_name="e2b_idx", index_params=ip)
    mprobe("create already-existing index", lambda: CL.create_index(collection_name="e2b_idx", index_params=ip))
    # 5. load already-loaded collection
    CL.load_collection("e2b_main")
    mprobe("load already-loaded collection", lambda: CL.load_collection("e2b_main"))

    print("\n=== Qdrant behavior probes ===\n")
    S.put(f"{QB}/collections/e2b_q?timeout=10", json={"vectors": {"size": 4, "distance": "Cosine"}}, timeout=15)
    time.sleep(0.3)
    # 6. create already-existing collection (recreate/overwrite)
    qprobe("create already-existing collection", "PUT", "/collections/e2b_q?timeout=10",
           json={"vectors": {"size": 4, "distance": "Cosine"}})
    # 7. delete non-existent collection
    qprobe("delete non-existent collection", "DELETE", "/collections/e2b_ghost?timeout=10")
    # 8. query on non-existent collection
    qprobe("query on non-existent collection", "POST", "/collections/e2b_ghost/points/query",
           json={"query": [0.1, 0.2, 0.3, 0.4], "limit": 1})
    # 9. delete alias for non-existent collection
    qprobe("delete non-existent alias", "POST", "/collections/aliases",
           json={"delete_alias": "ghost_alias"})

    for c in ("e2b_main", "e2b_idx", "e2b_part"):
        try:
            CL.drop_collection(c)
        except Exception:
            pass
    S.delete(f"{QB}/collections/e2b_q?timeout=5", timeout=10)


if __name__ == "__main__":
    main()
