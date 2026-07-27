#!/usr/bin/env python3
"""E2 scaling: probe Milvus v2.4.0 for over-strict acceptance on NEW numeric
optional-default search params (ef, nprobe, level) not in the original 12.

GLM (this run, GLM-5.1) over-formalizes each as "param >= 1" (the ambiguous
optional-default case). Live-probe the boundary value 0: impl accepts =>
the >=1 clause is over-strict.
"""
from __future__ import annotations
import sys
import time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

from pymilvus import MilvusClient, DataType

C_HNSW = "e2_scale_hnsw"
C_IVF = "e2_scale_ivf"
DIM = 8
VEC = [0.1] * DIM

cl = MilvusClient("http://localhost:19530")


def _drop(name: str) -> None:
    try:
        cl.drop_collection(name)
    except Exception:
        pass


def setup_hnsw() -> None:
    _drop(C_HNSW)
    cl.create_collection(
        collection_name=C_HNSW,
        dimension=DIM,
        metric_type="L2",
        index_type="HNSW",
        params={"M": 8, "efConstruction": 64},
    )
    cl.insert(C_HNSW, [{"id": i, "vector": [round((i + 1) * 0.01, 4)] * DIM} for i in range(5)])
    time.sleep(0.5)


def setup_ivf() -> None:
    _drop(C_IVF)
    from pymilvus import CollectionSchema, FieldSchema
    schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("id", DataType.INT64, is_primary=True)
    schema.add_field("vector", DataType.FLOAT_VECTOR, dim=DIM)
    cl.create_collection(
        collection_name=C_IVF,
        schema=schema,
    )
    ip = cl.prepare_index_params()
    ip.add_index(field_name="vector", index_name="ivf", index_type="IVF_FLAT", metric_type="L2", params={"nlist": 8})
    cl.create_index(collection_name=C_IVF, index_params=ip)
    cl.insert(C_IVF, [{"id": i, "vector": [round((i + 1) * 0.02, 4)] * DIM} for i in range(5)])
    cl.load_collection(C_IVF)
    time.sleep(0.5)


def probe(label: str, fn) -> None:
    try:
        res = fn()
        n = len(res) if isinstance(res, list) else "?"
        print(f"  {label:34} ACCEPTED (results={n})")
    except Exception as e:
        msg = str(e)[:90].replace("\n", " ")
        print(f"  {label:34} REJECTED  ({msg})")


def main() -> None:
    print("=== Milvus v2.4.0 scaling probes (NEW numeric optional-default) ===\n")
    setup_hnsw()
    print("[HNSW search ef]  (GLM over-strict candidate: ef >= 1)")
    probe("ef=64 (control)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"ef": 64}}))
    probe("ef=0  (boundary)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"ef": 0}}))
    probe("ef=-1 (negative)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"ef": -1}}))

    print("\n[IVF search nprobe]  (GLM over-strict candidate: nprobe >= 1)")
    setup_ivf()
    probe("nprobe=8 (control)", lambda: cl.search(C_IVF, data=[VEC], limit=3, search_params={"params": {"nprobe": 8}}))
    probe("nprobe=0 (boundary)", lambda: cl.search(C_IVF, data=[VEC], limit=3, search_params={"params": {"nprobe": 0}}))
    probe("nprobe=-1(negative)", lambda: cl.search(C_IVF, data=[VEC], limit=3, search_params={"params": {"nprobe": -1}}))

    print("\n[search level]  (GLM over-strict candidate: level >= 1)")
    probe("level=1 (control)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"level": 1}}))
    probe("level=0 (boundary)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"level": 0}}))

    print("\n[range search radius/range_filter]  (GLM over-strict candidates: >= 0 / numeric)")
    probe("radius=0 (range)", lambda: cl.search(C_HNSW, data=[VEC], limit=3, search_params={"params": {"radius": 0, "range_filter": 0}}))

    print("\n[HNSW index-create M / efConstruction]  (GLM over-strict candidates: >= 1)")
    _drop("e2_idx_m0")
    cl.create_collection(collection_name="e2_idx_m0", dimension=DIM, metric_type="L2")
    def _mk_idx(m, efc):
        ip = cl.prepare_index_params()
        ip.add_index(field_name="vector", index_type="HNSW", metric_type="L2", params={"M": m, "efConstruction": efc})
        cl.create_index(collection_name="e2_idx_m0", index_params=ip)
    probe("M=16,efC=64 (control)", lambda: _mk_idx(16, 64))
    probe("M=0 (boundary)", lambda: _mk_idx(0, 64))
    probe("efConstruction=0 (boundary)", lambda: _mk_idx(16, 0))

    print("\n[load replicaNumber]  (GLM over-strict candidate: replicaNumber >= 1)")
    probe("replicaNumber=0 (load)", lambda: cl.load_collection(C_HNSW, replica_number=0))

    _drop(C_HNSW); _drop(C_IVF); _drop("e2_idx_m0")


if __name__ == "__main__":
    main()
