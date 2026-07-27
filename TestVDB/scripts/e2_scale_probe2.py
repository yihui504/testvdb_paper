#!/usr/bin/env python3
"""E2 scaling probe round 2: confirm over-strict for the pipeline-matched GLM clauses.

Milvus: level=-1 (clause level>=0), radius=-1 / range_filter=-1 (clause >=0).
Qdrant: HNSW m=0,1 (clause m>=2), ef_construct=0 (clause >=1), full_scan_threshold=-1 (clause >=0).
impl accepts the value the clause rejects => over-strict confirmed.
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
C_HNSW = "e2_scale_hnsw2"
DIM = 8
VEC = [0.1] * DIM


def mprobe(label: str, fn) -> None:
    try:
        res = fn()
        n = len(res) if isinstance(res, list) else "?"
        print(f"  [milvus] {label:34} ACCEPTED (results={n})")
    except Exception as e:
        print(f"  [milvus] {label:34} REJECTED  ({str(e)[:80]})")


def qprobe(label: str, body_extra: dict) -> None:
    cname = "e2_hnsw_test"
    try:
        S.delete(f"{QB}/collections/{cname}", timeout=10)
    except Exception:
        pass
    body = {"vectors": {"size": 4, "distance": "Cosine"}}
    body.update(body_extra)
    r = S.put(f"{QB}/collections/{cname}?timeout=10", json=body, timeout=20)
    try:
        ok = r.status_code == 200 and r.json().get("result", True) is not False
    except Exception:
        ok = r.status_code == 200
    print(f"  [qdrant] {label:34} HTTP={r.status_code} ACCEPTED={ok}  {r.text[:70]}")
    time.sleep(0.2)


def main() -> None:
    # --- Milvus setup ---
    try:
        CL.drop_collection(C_HNSW)
    except Exception:
        pass
    CL.create_collection(collection_name=C_HNSW, dimension=DIM, metric_type="L2",
                         index_type="HNSW", params={"M": 8, "efConstruction": 64})
    CL.insert(C_HNSW, [{"id": i, "vector": [round((i + 1) * 0.01, 4)] * DIM} for i in range(5)])
    time.sleep(0.5)

    print("=== Milvus: pipeline-matched GLM clauses ===\n")
    # level >= 0  -> reject value -1
    mprobe("level=0 (control, >=0)", lambda: CL.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"level": 0}}))
    mprobe("level=-1 (violates >=0)", lambda: CL.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"level": -1}}))
    # radius/range_filter >= 0 -> reject -1
    mprobe("radius=-1,rf=-1 (violates >=0)", lambda: CL.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"radius": -1, "range_filter": -1}}))

    print("\n=== Qdrant: HNSW config GLM clauses ===\n")
    qprobe("m=16 (control)", {"hnsw_config": {"m": 16}})
    qprobe("m=0 (violates m>=2)", {"hnsw_config": {"m": 0}})
    qprobe("m=1 (violates m>=2)", {"hnsw_config": {"m": 1}})
    qprobe("ef_construct=0 (violates >=1)", {"hnsw_config": {"ef_construct": 0}})
    qprobe("full_scan_threshold=-1 (viol >=0)", {"hnsw_config": {"full_scan_threshold": -1}})

    try:
        CL.drop_collection(C_HNSW)
    except Exception:
        pass


if __name__ == "__main__":
    main()
