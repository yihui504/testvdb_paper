#!/usr/bin/env python3
"""Phase 2 rerun — 给 endpoint 空的 case 从探针脚本抽 endpoint 补上。

REST 探针: 从 http() 的 URL 字面量抽 path(BASE+'...')，挑"被测操作"非 setup。
milvus SDK 探针: mc.search/insert/... 方法 → milvus endpoint 标签。
归一化成各 vendor 的 endpoint 格式(milvus entities+search / qdrant collections+{collection_name}+points+search / weaviate 路径)。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(os.path.dirname(ROOT), 'phase2', 'probes')
RUN = os.path.join(ROOT, 'run')

MIL_SDK_MAP = {  # mc.X → milvus endpoint
    'search': 'entities+search', 'query': 'entities+query', 'insert': 'entities+insert',
    'upsert': 'entities+upsert', 'delete': 'entities+delete',
    'create_collection': 'collections+create', 'drop_collection': 'collections+drop',
    'create_index': 'indexes+create',
}
# 被测操作优先级(高=更像 attack), setup 类降权
OP_PRIORITY = ['search', 'query', 'scroll', 'count', 'upsert', 'insert', 'delete',
               'points', 'objects', 'schema', 'batch', 'classification', 'replication']


def norm_milvus_rest(path):
    # /v2/vectordb/entities/search → entities+search
    m = re.search(r'/v2/vectordb/(.+)', path)
    if m:
        return m.group(1).replace('/', '+')
    return path.strip('/').replace('/', '+')


def norm_qdrant(path):
    # /collections/<col>/points/search → collections+{collection_name}+points+search
    p = re.sub(r'/collections/[^/]+', '/collections/{collection_name}', path)
    parts = [x for x in p.strip('/').split('/') if x]
    return '+'.join(parts)


def norm_weaviate(path, method):
    p = path.replace('/v1', '').strip('/')
    return ('%s /%s' % (method, p)) if p else method


def extract_rest(script, vendor):
    # 抽所有 path 字面量(以 / 开头)
    paths = set(re.findall(r"""['"](/v?[0-9]?[^'"]*?)['"]""", script))
    paths = {p for p in paths if any(op in p.lower() for op in OP_PRIORITY) and 'localhost' not in p}
    # 按被测操作优先级挑(空则走末尾 collection 回退)
    best, bestscore = '', -1
    for p in paths:
        sc = max((OP_PRIORITY.index(op) for op in OP_PRIORITY if op in p.lower()), default=-1)
        # setup(collections/create|drop 单独) 降权
        if re.search(r'/collections/(create|drop)(/|$)', p) and 'points' not in p and 'entities' not in p:
            sc -= 5
        if sc > bestscore:
            best, bestscore = p, sc
    if not best:
        # 回退: collection create/PUT 类(shard_number/replication 等在 create 上测)
        if re.search(r"/collections/[^'\" ]+['\"]", script) or "'/collections/'" in script:
            if vendor == 'milvus':
                return 'collections+create'
            if vendor == 'qdrant':
                return 'collections+{collection_name}'
            return 'POST /schema'
        return ''
    if vendor == 'milvus':
        return norm_milvus_rest(best)
    if vendor == 'qdrant':
        return norm_qdrant(best)
    # weaviate: method 取出现最多的
    meths = re.findall(r"http\(['\"]([A-Z]+)['\"]", script)
    return norm_weaviate(best, meths[-1] if meths else 'POST')


def extract_milvus_sdk(script):
    methods = re.findall(r'mc\.([a-z_]+)\(', script)
    # 挑被测操作(非 setup)
    setup = {'create_schema', 'flush', 'load_collection', 'release_collection', 'drop_collection',
             'create_collection', 'create_index', 'has_collection', 'list_indexes'}
    cand = [m for m in methods if m not in setup and m in MIL_SDK_MAP]
    if not cand:
        cand = [m for m in methods if m in MIL_SDK_MAP]
    if not cand:
        return ''
    return MIL_SDK_MAP[cand[-1]]


def main():
    manifest = json.load(open(os.path.join(RUN, '_manifest.json'), encoding='utf-8'))
    filled = 0
    for e in manifest:
        if e['endpoint']:
            continue
        vendor, num = e['vendor'], e['num']
        p = os.path.join(PROBES, vendor, 'probe_%s_%s.py' % (vendor, num))
        if not os.path.isfile(p):
            continue
        script = open(p, encoding='utf-8', errors='replace').read()
        has_sdk = 'mc.' in script and vendor == 'milvus'
        has_http = 'http(' in script
        ep = ''
        if has_sdk and (not has_http or script.count('mc.') >= script.count('http(')):
            ep = extract_milvus_sdk(script)
        if not ep and has_http:
            ep = extract_rest(script, vendor)
        if not ep:
            continue
        e['endpoint'] = ep
        # patch session stage2_aggregation
        agg_path = os.path.join(e['session_dir'], 'debate_logs', 'stage2_aggregation.json')
        agg = json.load(open(agg_path, encoding='utf-8'))
        agg['confirmed'][e['defect_id']]['endpoint'] = ep
        json.dump(agg, open(agg_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        filled += 1
    json.dump(manifest, open(os.path.join(RUN, '_manifest.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    import collections
    byv = collections.defaultdict(lambda: [0, 0])
    for e in manifest:
        byv[e['vendor']][1] += 1
        byv[e['vendor']][0] += bool(e['endpoint'])
    print('filled this pass:', filled)
    print('endpoint filled per vendor:', {k: '%d/%d' % tuple(v) for k, v in byv.items()})
    print('still empty:', [e['defect_id'] for e in manifest if not e['endpoint']])


if __name__ == '__main__':
    main()
