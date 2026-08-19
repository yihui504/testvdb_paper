"""Phase 2 probe 公共 helper: HTTP 请求 + 结构化输出 + milvus 连接.

probe 脚本约定:
- 只连 localhost 端口(milvus 19530 / qdrant 6333 / weaviate 8080),容器由外部编排起好
- 每个 probe case 调用 emit(case_id, ...) 输出一行 JSON 观察
- 脚本幂等: setup 前先清理同名资源

rerun 扩展(raw 捕获, 2026-08-14): 当环境变量 RAW_LOG_DIR 设置时, http() 与
record_raw() 把完整 req/resp 追加写入 {RAW_LOG_DIR}/raw_{PROBE_ID}.log (PROBE_ID 由
runner 设为 {vendor}_{num})。未设置 RAW_LOG_DIR 时全部静默, 行为与原 phase2 完全一致。
"""
import json
import os
import time

import requests

TIMEOUT = 30


def _raw_path():
    """返回 raw log 路径; RAW_LOG_DIR 未设返回 None。"""
    d = os.environ.get('RAW_LOG_DIR')
    if not d:
        return None
    pid = os.environ.get('PROBE_ID') or 'unknown'
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, 'raw_%s.log' % pid)


def _raw_write(record):
    p = _raw_path()
    if not p:
        return
    with open(p, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False, default=str) + '\n')


def record_raw(kind, request, response, note=None):
    """SDK/gRPC 探针(milvus)记录请求-响应。kind 如 'grpc_search'/'sdk_insert'。"""
    _raw_write({'ts': time.time(), 'kind': kind, 'request': request,
                'response': response, 'note': note})


def http(method, url, payload=None, timeout=TIMEOUT):
    """发 HTTP 请求, 返回 (status, json_or_None, text). 连接失败 status=None.

    RAW_LOG_DIR 设置时追加完整 req(method/url/payload) + resp(status/headers/body) 到 raw log。"""
    try:
        r = requests.request(method, url, json=payload, timeout=timeout)
    except Exception as e:
        if os.environ.get('RAW_LOG_DIR'):
            _raw_write({'ts': time.time(), 'kind': 'http', 'method': method,
                        'url': url, 'payload': payload, 'status': None, 'error': str(e)})
        return None, None, 'EXCEPTION: %s' % e
    try:
        body = r.json()
    except Exception:
        body = None
    if os.environ.get('RAW_LOG_DIR'):
        _raw_write({'ts': time.time(), 'kind': 'http', 'method': method, 'url': url,
                    'payload': payload, 'status': r.status_code,
                    'resp_headers': dict(r.headers), 'resp_body': r.text})
    return r.status_code, body, r.text


def emit(case_id, **obs):
    """输出一行 JSON 观察(probe_runner 采集到 output_*.log)."""
    print(json.dumps({'case_id': case_id, **obs}, ensure_ascii=False, default=str), flush=True)


def wait_ready(url, tries=60, delay=1):
    """等容器 HTTP 就绪(状态码 < 500 视为就绪)."""
    for _ in range(tries):
        try:
            if requests.get(url, timeout=2).status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(delay)
    return False


def milvus_client():
    """pymilvus MilvusClient 连 localhost:19530."""
    from pymilvus import MilvusClient
    return MilvusClient(uri='http://localhost:19530')


def milvus_drop(client, name):
    try:
        client.drop_collection(name)
    except Exception:
        pass


def milvus_create(client, name, fields, dim=4):
    """fields: [(name, dtype_str, extra), ...] dtype_str 如 INT64/FLOAT_VECTOR/JSON/VARCHAR/BOOL."""
    from pymilvus import DataType
    DT = {'INT64': DataType.INT64, 'FLOAT_VECTOR': DataType.FLOAT_VECTOR,
          'JSON': DataType.JSON, 'VARCHAR': DataType.VARCHAR, 'BOOL': DataType.BOOL,
          'DOUBLE': DataType.DOUBLE, 'INT16': DataType.INT16, 'INT32': DataType.INT32,
          'FLOAT': DataType.FLOAT}
    schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
    for fname, dtype, extra in fields:
        kwargs = {}
        if dtype == 'FLOAT_VECTOR':
            kwargs['dim'] = dim
        if 'max_length' in extra:
            kwargs['max_length'] = extra['max_length']
        if extra.get('nullable'):
            kwargs['nullable'] = True
        schema.add_field(fname, DT[dtype], **kwargs)
    client.create_collection(name, schema=schema, consistency_level='Strong')
    return client


def milvus_index(client, name, params):
    """params: dict 如 {'field_name': 'vector', 'index_type': 'FLAT', 'metric_type': 'L2', ...}.
    pymilvus>=2.6 的 MilvusClient.create_index 要求 IndexParams(list) 对象, 这里做兼容转换.
    先幂等 drop 现有索引 (快速 create_collection 会自带 AUTOINDEX)."""
    from pymilvus.milvus_client.index import IndexParams
    p = dict(params)
    field = p.pop('field_name', 'vector')
    itype = p.pop('index_type')
    try:
        client.release_collection(name)
    except Exception:
        pass
    try:
        for idx_name in client.list_indexes(name):
            client.drop_index(name, idx_name)
    except Exception:
        pass
    ips = IndexParams()
    ips.add_index(field_name=field, index_type=itype, index_name=itype + '_idx', **p)
    return client.create_index(name, ips)
