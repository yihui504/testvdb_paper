"""probe for milvus-io/milvus#49890  [Bug]: REST API v2 accepts non-integer `Request-Timeout` header values
version: 2.6.16 | gt: TP_FIXED_PR | class: param_validation
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from probe_common import http, emit, wait_ready, milvus_client, milvus_drop, milvus_create, milvus_index

BASE = 'http://localhost:19530'


def _drop(name):
    http('POST', BASE + '/v2/vectordb/collections/drop', {'collectionName': name, 'dbName': 'default'})


def _create(name, **kw):
    p = {'collectionName': name}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/collections/create', p)


def _insert(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/insert', p)


def _upsert(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/upsert', p)


def _search(name, data, **kw):
    p = {'collectionName': name, 'data': data}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/search', p)


def _query(name, **kw):
    p = {'collectionName': name}
    p.update(kw)
    return http('POST', BASE + '/v2/vectordb/entities/query', p)


def _describe(name):
    return http('POST', BASE + '/v2/vectordb/collections/describe', {'collectionName': name, 'dbName': 'default'})


def _load(name):
    return http('POST', BASE + '/v2/vectordb/collections/load', {'collectionName': name, 'dbName': 'default'})


def _idx_create(name, index_params):
    return http('POST', BASE + '/v2/vectordb/indexes/create',
                {'collectionName': name, 'indexParams': index_params})


def _emit_case(case_id, resp, note):
    s, b, t = resp
    code = (b or {}).get('code') if isinstance(b, dict) else None
    try:
        raw = str(b or t)[:400]
    except Exception:
        raw = str(t)[:400]
    emit(case_id, http_status=s, resp_code=code, raw=raw,
         observation=note + ' (http=%s code=%s)' % (s, code))

def main():
    wait_ready('http://localhost:19530/healthz')

    import requests as _req
    def _hdr(hv):
        try:
            r = _req.post(BASE + '/v2/vectordb/collections/list', json={},
                          headers={'Request-Timeout': hv}, timeout=30)
            try:
                b = r.json()
            except Exception:
                b = None
            return r.status_code, b, r.text
        except Exception as e:
            return None, None, 'EXCEPTION: %s' % e
    s, bd, t = _hdr('3.5')
    _emit_case('c1', (s, bd, t),
               'Request-Timeout float 3.5 header; defect if code 0 (float should be rejected)')
    s, bd, t = _hdr('abc')
    _emit_case('c2', (s, bd, t), 'Request-Timeout non-integer abc header; defect if code 0')
    s, bd, t = _hdr('10')
    _emit_case('c3', (s, bd, t), 'control Request-Timeout valid integer 10; expect code 0')


    print('probe_milvus_49890 done')

if __name__ == '__main__':
    main()
