#!/usr/bin/env python3
"""Recall probe #6: milvus v2.2 create_index BIN_IVF_FLAT + metric L2 -> wrong error.

Bug (held-out #6, diagnostic-quality): creating a BIN_IVF_FLAT index with metric_type=L2
on a binary vector collection should produce a clear "binary index requires binary metric
(HAMMING/JACCARD)" error, but milvus v2.2 reportedly emits a wrong/misleading message.

TestVDB recall: contract from docs = BIN_IVF_FLAT requires binary metric;
attack = create BIN_IVF_FLAT + L2; bug = misleading error.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
except ImportError:
    print("pymilvus not installed"); sys.exit(1)

connections.connect(host='localhost', port='19530')
print("connected to milvus")

# clean up
for c in ['test_bin_recall6']:
    if utility.has_collection(c):
        utility.drop_collection(c)

# binary collection (dim must be multiple of 8 for BINARY_VECTOR)
fields = [
    FieldSchema(name='pk', dtype=DataType.VARCHAR, max_length=64, is_primary=True),
    FieldSchema(name='vec', dtype=DataType.BINARY_VECTOR, dim=128),
]
schema = CollectionSchema(fields, 'recall #6 binary test')
coll = Collection('test_bin_recall6', schema)
print(f"created binary collection")

# ATTACK: create BIN_IVF_FLAT index with metric_type=L2 (wrong for binary)
print("\n--- attack: create_index BIN_IVF_FLAT + metric_type=L2 (binary needs HAMMING/JACCARD) ---")
try:
    coll.create_index('vec', {
        'index_type': 'BIN_IVF_FLAT',
        'metric_type': 'L2',
        'params': {'nlist': 128},
    })
    print(">>> index created with NO error (unexpected for binary+L2)")
    print(">>> if accepted, milvus v2.2 allows binary+L2 silently -> may be different behavior")
except Exception as e:
    err = str(e)
    print(f"ERROR: {err[:300]}")
    # check if error message is misleading (the bug)
    # correct message should mention "binary" or "HAMMING" or "metric mismatch"
    if 'binary' in err.lower() or 'hamming' in err.lower() or 'jaccard' in err.lower() or 'metric' in err.lower():
        print(">>> error message is CLEAR (mentions binary/metric) -> bug NOT present (correct diagnostic)")
    else:
        print(f">>> error message is MISLEADING (no mention of binary/metric mismatch) -> BUG REPRODUCED")
        print(">>> RECALL HIT (#6 wrong/misleading diagnostic)")
