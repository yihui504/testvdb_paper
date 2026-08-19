"""probe for milvus-io/milvus#49059  [Bug]: COSINE Metric Returns Distance > 1.0 for Identical Vectors (Precision Overflow)
version: 2.6.12 | gt: TP_ACK_CLOSED_NOFIX | class: crash
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

def main():
    wait_ready('http://localhost:19530/healthz')

    import math
    mc = milvus_client()
    milvus_drop(mc, 'test_49059')
    mc.create_collection('test_49059', dimension=128, metric_type='COSINE')
    # Faithful to reporter's repro (issue body): seed=42, 10000 L2-normalized random
    # 128-d vectors, IVF_FLAT/COSINE. The overflow arises from accumulated FP error
    # in knowhere's dot product on random (non-degenerate) vectors; degenerate
    # repeated-value vectors do not trigger it.
    import numpy as np
    np.random.seed(42)
    dim = 128
    data = np.random.rand(10000, dim).astype(np.float32)
    norms = np.linalg.norm(data, axis=1, keepdims=True)
    vectors = (data / norms).astype(np.float32)
    rows = [{'id': i, 'vector': vectors[i].tolist()} for i in range(10000)]
    mc.insert('test_49059', rows)
    mc.flush('test_49059')
    milvus_index(mc, 'test_49059', {'field_name': 'vector', 'index_type': 'IVF_FLAT',
                                         'metric_type': 'COSINE',
                                         'params': {'nlist': 128}})
    mc.load_collection('test_49059')
    # Faithful to reporter: batch-search the first 100 stored vectors (each is
    # identical to its own stored row); the overflow is sporadic across vectors,
    # so a single query usually misses it.
    q_batch = [vectors[i].tolist() for i in range(100)]
    try:
        r = mc.search('test_49059', q_batch, anns_field='vector', limit=1,
                      search_params={'metric_type': 'COSINE', 'params': {'nprobe': 10}})
        distances = [hits[0].distance for hits in r if hits]
        max_d = max(distances) if distances else None
        n_over = sum(1 for d in distances if d > 1.0)
        emit('c1', max_distance=max_d, n_over_one=n_over, n_queries=len(distances),
             observation='COSINE identical-vector search over %d queries: max_distance=%s, %d with distance>1.0 (defect if any >1.0)' % (len(distances), max_d, n_over))
    except Exception as e:
        emit('c1', exception=str(e), observation='search failed: %s' % e)


    print('probe_milvus_49059 done')

if __name__ == '__main__':
    main()
