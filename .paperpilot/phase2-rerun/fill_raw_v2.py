#!/usr/bin/env python3
"""为 6 个空日志 case（REST v2 可达）补真实 raw HTTP 日志进 materials_v2。

根因：原探针用 pymilvus SDK（gRPC）或裸 requests，probe_common 的 raw 捕获（挂 http()）记不到。
真实 attack agent 对 milvus 用 REST v2 → 本脚本用 probe_common.http 按 issue 声称操作重放，
生成与真实形态一致的 raw + output log 写入 materials_v2/sessions/{vendor}/{ver}/{did}/。

用法: python fill_raw_v2.py <milvus version>   （需该版本容器已 healthy）
47635(2.3) 无 REST v2，保持空日志（真实形态：该版本 attack 只能 pymilvus gRPC）。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PHASE2 = os.path.join(os.path.dirname(ROOT), 'phase2', 'probes')
sys.path.insert(0, PHASE2)
import probe_common  # noqa: E402

BASE = 'http://localhost:19530'
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
DID_MAP = {r['orig']: did for did, r in json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8')).items()}


def h(method, path, payload=None):
    return probe_common.http(method, BASE + path, payload)


def gen_output(did, sess_dir):
    """raw_*.log → output_{did}.log（与 run_probes.gen_output_log 同格式）。"""
    raw = os.path.join(sess_dir, 'raw_%s.log' % did)
    out = os.path.join(sess_dir, 'output_%s.log' % did)
    if not os.path.exists(raw):
        open(out, 'w', encoding='utf-8').write('[no raw HTTP captured]\n')
        return 0
    n = 0
    with open(out, 'w', encoding='utf-8') as f:
        for i, ln in enumerate(open(raw, encoding='utf-8').read().splitlines(), 1):
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r.get('kind') != 'http':
                continue
            n += 1
            f.write('=== REQ %d ===\n%s %s\n' % (i, r.get('method'), r.get('url')))
            if r.get('headers'):
                f.write('headers: %s\n' % json.dumps(r['headers'], ensure_ascii=False))
            if r.get('payload') is not None:
                f.write('payload: %s\n' % json.dumps(r['payload'], ensure_ascii=False))
            f.write('=== RESP %d ===\nstatus: %s\nbody: %s\n\n' % (i, r.get('status'), r.get('resp_body', '')))
    return n


def session_for(orig):
    did = DID_MAP[orig]
    r = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))[did]
    return did, os.path.join(V2, 'sessions', r['vendor'], r['version'], did)


def dim_create(name, dim=8, metric='L2'):
    """最小 create（REST v2 quick-setup）。"""
    return h('POST', '/v2/vectordb/collections/create',
             {'collectionName': name, 'dimension': dim, 'metricType': metric, 'dbName': 'default'})


def common_setup(name, dim=8, metric='L2', index_type='IVF_FLAT', index_params=None, n=10):
    dim_create(name, dim, metric)
    data = [{'id': i, 'vector': [0.1] * dim} for i in range(n)]
    h('POST', '/v2/vectordb/entities/insert', {'collectionName': name, 'dbName': 'default', 'data': data})
    h('POST', '/v2/vectordb/indexes/create',
      {'collectionName': name, 'dbName': 'default',
       'indexParams': [{'fieldName': 'vector', 'indexName': 'idx_vec', 'metricType': metric,
                        'indexType': index_type,
                        'params': index_params or {'nlist': 8}}]})
    h('POST', '/v2/vectordb/collections/load', {'collectionName': name, 'dbName': 'default'})


def probe_47729(name):
    """nprobe=0 accepted（IVF search）。"""
    common_setup(name, index_type='IVF_FLAT')
    h('POST', '/v2/vectordb/entities/search',
      {'collectionName': name, 'dbName': 'default',
       'data': [[0.1] * 8], 'limit': 3, 'searchParams': {'nprobe': 0}, 'outputFields': ['id']})


def probe_47752(name):
    """ef=0 accepted（HNSW search）。"""
    common_setup(name, index_type='HNSW', index_params={'M': 8, 'efConstruction': 64})
    h('POST', '/v2/vectordb/entities/search',
      {'collectionName': name, 'dbName': 'default',
       'data': [[0.1] * 8], 'limit': 3, 'searchParams': {'ef': 0}, 'outputFields': ['id']})


def probe_47755(name):
    """delete filter 结构非法（filter='123' 非布尔表达式）。"""
    dim_create(name)
    h('POST', '/v2/vectordb/entities/insert', {'collectionName': name, 'dbName': 'default',
                                               'data': [{'id': i, 'vector': [0.1] * 8, 'age': i * 10} for i in range(5)]})
    h('POST', '/v2/vectordb/entities/delete', {'collectionName': name, 'dbName': 'default', 'filter': '123'})


def probe_47767(name):
    """drop 不存在的 database。"""
    h('POST', '/v2/vectordb/databases/drop', {'dbName': name})


def probe_49059(name):
    """COSINE 相同向量 distance 是否 >1。"""
    common_setup(name, dim=4, metric='COSINE', index_type='FLAT', index_params={})
    h('POST', '/v2/vectordb/entities/search',
      {'collectionName': name, 'dbName': 'default',
       'data': [[0.1] * 4], 'limit': 3, 'outputFields': ['*']})


def probe_49890(name):
    """Request-Timeout header 非整数被接受。裸 requests 不记 raw → 手动写平铺 raw 行。"""
    import requests as _req
    import time
    raw_p = os.path.join(os.environ['RAW_LOG_DIR'], 'raw_%s.log' % os.environ['PROBE_ID'])
    with open(raw_p, 'a', encoding='utf-8') as rf:
        for hv in ('3.5', 'abc', '10'):
            try:
                r = _req.post(BASE + '/v2/vectordb/collections/list', json={},
                              headers={'Request-Timeout': hv}, timeout=30)
                rf.write(json.dumps({'ts': time.time(), 'kind': 'http', 'method': 'POST',
                                     'url': BASE + '/v2/vectordb/collections/list',
                                     'payload': {}, 'headers': {'Request-Timeout': hv},
                                     'status': r.status_code, 'resp_body': r.text}, ensure_ascii=False) + '\n')
            except Exception as e:
                rf.write(json.dumps({'ts': time.time(), 'kind': 'http', 'method': 'POST',
                                     'url': BASE + '/v2/vectordb/collections/list',
                                     'payload': {}, 'headers': {'Request-Timeout': hv},
                                     'status': None, 'error': str(e)}, ensure_ascii=False) + '\n')


PROBES = {
    'milvus_47729': probe_47729,
    'milvus_47752': probe_47752,
    'milvus_47755': probe_47755,
    'milvus_47767': probe_47767,
    'milvus_49059': probe_49059,
    'milvus_49890': probe_49890,
}
VERSION_OF = {'milvus_47729': '2.6.10', 'milvus_47752': '2.6.10', 'milvus_47755': '2.6.10',
              'milvus_47767': '2.6.10', 'milvus_49059': '2.6.12', 'milvus_49890': '2.6.16'}


def main():
    version = sys.argv[1]
    probe_common.wait_ready('http://localhost:19530/healthz')
    for orig, probe_fn in PROBES.items():
        if VERSION_OF[orig] != version:
            continue
        did, sess = session_for(orig)
        os.makedirs(sess, exist_ok=True)
        os.environ['RAW_LOG_DIR'] = sess
        os.environ['PROBE_ID'] = did
        name = 'repro_' + orig.split('_')[1]
        try:
            probe_fn(name)
            status = 'OK'
        except Exception as e:
            print('  %s EXC: %s' % (orig, str(e)[:80]))
            status = 'EXC'
        nreq = gen_output(did, sess)
        print('%s (%s): %s reqs=%d' % (orig, did, status, nreq), flush=True)


if __name__ == '__main__':
    main()
