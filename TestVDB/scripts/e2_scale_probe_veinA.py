#!/usr/bin/env python3
"""E2 Vein A probe: Qdrant nested config + Milvus IVF nlist.
Test the value each GLM clause rejects; impl accepts => over-strict.
"""
from __future__ import annotations
import sys
import time
import requests

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from pymilvus import MilvusClient, DataType

S = requests.Session()
S.trust_env = False
QB = "http://localhost:6333"
CL = MilvusClient("http://localhost:19530")
DIM = 8


def qprobe(label: str, body_extra: dict) -> None:
    cname = "e2_veina"
    try:
        S.delete(f"{QB}/collections/{cname}?timeout=5", timeout=10)
    except Exception:
        pass
    time.sleep(0.3)
    body = {"vectors": {"size": 4, "distance": "Cosine"}}
    body.update(body_extra)
    r = S.put(f"{QB}/collections/{cname}?timeout=10", json=body, timeout=25)
    try:
        ok = r.status_code == 200 and r.json().get("result", True) is not False
    except Exception:
        ok = r.status_code == 200
    print(f"  [qdrant] {label:40} HTTP={r.status_code} ACCEPTED={ok}  {r.text[:60]}")
    time.sleep(0.2)


def main() -> None:
    print("=== Qdrant Vein A: nested config (default-based) ===\n")
    # optimizers_config: indexing_threshold (clause >=0) -> test -1
    qprobe("indexing_threshold=20000 (ctl)", {"optimizers_config": {"indexing_threshold": 20000}})
    qprobe("indexing_threshold=-1 (viol >=0)", {"optimizers_config": {"indexing_threshold": -1}})
    # max_optimization_threads (clause >=0) -> test -1
    qprobe("max_opt_threads=-1 (viol >=0)", {"optimizers_config": {"max_optimization_threads": -1}})
    # wal_config: wal_segments_ahead (clause >=0) -> test -1
    qprobe("wal_segments_ahead=-1 (viol >=0)", {"wal_config": {"wal_segments_ahead": -1}})
    qprobe("wal_capacity_mb=0 (ctl-ish)", {"wal_config": {"wal_capacity_mb": 32}})
    # quantization bits (clause bits>=1) -> scalar/product with bits=0
    qprobe("product quant bits=0 (viol >=1)", {"quantization_config": {"product": {"compression": "x8", "bits": 0}}})
    # hnsw max_indexing_threads (numeric) -> test -1
    qprobe("max_indexing_threads=-1", {"hnsw_config": {"max_indexing_threads": -1}})

    print("\n=== Milvus IVF nlist (clause >=1) ===\n")
    try:
        CL.drop_collection("e2_ivf_nlist")
    except Exception:
        pass
    schema = CL.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=DIM)
    CL.create_collection(collection_name="e2_ivf_nlist", schema=schema)

    def mk_ivf(nlist):
        ip = CL.prepare_index_params()
        ip.add_index(field_name="vector", index_type="IVF_FLAT", metric_type="L2", params={"nlist": nlist})
        CL.create_index(collection_name="e2_ivf_nlist", index_params=ip)

    for label, nlist in [("nlist=128 (ctl)", 128), ("nlist=0 (viol >=1)", 0), ("nlist=-1", -1)]:
        try:
            mk_ivf(nlist)
            print(f"  [milvus] {label:34} ACCEPTED")
        except Exception as e:
            print(f"  [milvus] {label:34} REJECTED  ({str(e)[:70]})")

    try:
        CL.drop_collection("e2_ivf_nlist")
    except Exception:
        pass


if __name__ == "__main__":
    main()
