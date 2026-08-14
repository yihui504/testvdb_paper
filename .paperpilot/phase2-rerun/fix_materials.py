#!/usr/bin/env python3
"""方案A：把 run1 人工清洗认定的 endpoint 修正持久化写回材料（run/run2/run3 三棵树）。

两类：
  FIX_LABEL(A): fill_endpoints 抽取偏差→标签错，改为 run1 curated 判定词认定的 endpoint
  KEEP_LABEL(C): 标签本来就对（=run1 认定），但 raw 流量不含缺陷操作（probe↔issue 错配）→ 标签保持，重判时需带提示
产出 MATERIAL_FIXES.json 供追溯。run/ 只改输入标签，历史 dev_review.json 判词不动。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# A 类: case -> run1 认定 endpoint
FIX_LABEL = {
    'milvus_47763': 'entities+insert',
    'milvus_49928': 'collections+create',
    'milvus_50192': 'collections+rename',
    'milvus_50319': 'entities+search',
    'milvus_50321': 'collections+create',
    'milvus_50322': 'collections+drop',
    'milvus_50351': 'collections+create',
    'milvus_50352': 'collections+create',
    'milvus_51084': 'collections+create',
    'milvus_52307': 'entities+upsert',
    'milvus_52311': 'entities+search',
    'milvus_52314': 'entities+upsert',
    'milvus_52325': 'entities+search',
    'milvus_47635': 'entities+search',      # THIN, run1 rationale: search TopK=0
    'milvus_50355': 'entities+upsert',      # probe↔issue 错配(autoID upsert), run1 认定
    'weaviate_11401': '/schema',
    'weaviate_11436': '/schema',
    'weaviate_11732': '/schema',
    'qdrant_9416': 'collections+{collection_name}+points',
    'qdrant_9417': 'collections+{collection_name}+points',
}
# C 类: 标签保持, 流量缺缺陷操作
KEEP_LABEL = ['milvus_49889', 'milvus_49929', 'milvus_50325', 'milvus_51085', 'qdrant_9373']

CASES = {(x['vendor'], x['num']): x for x in json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8')) if x['group'] in 'ABC'}


def sess_rel(vendor, version, num):
    return 'results/%s/%s/%d' % (vendor, version, num)


def main():
    record = []
    for did, new_ep in FIX_LABEL.items():
        v, n = did.rsplit('_', 1)
        c = CASES[(v, int(n))]
        entry = {'did': did, 'type': 'FIX_LABEL', 'old': None, 'new': new_ep, 'trees': []}
        for tree in ('run', 'run2', 'run3'):
            p = os.path.join(ROOT, tree, sess_rel(v, c['version'], int(n)), 'debate_logs', 'stage2_aggregation.json')
            agg = json.load(open(p, encoding='utf-8'))
            cand = list(agg['confirmed'].values())[0]
            old = cand.get('endpoint')
            if entry['old'] is None:
                entry['old'] = old
            elif entry['old'] != old:
                print('!! 树间不一致', did, tree, old)
            cand['endpoint'] = new_ep
            cand['note'] = ('rerun candidate — endpoint fixed per run1 adjudication (material fix, '
                            'fill_endpoints extraction bias); no GT/rationale leaked')
            json.dump(agg, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            entry['trees'].append(tree)
        record.append(entry)
    for did in KEEP_LABEL:
        v, n = did.rsplit('_', 1)
        record.append({'did': did, 'type': 'KEEP_LABEL_TRAFFIC_DEFECT', 'old': None, 'new': None, 'trees': ['run', 'run2', 'run3']})
    out = os.path.join(ROOT, 'MATERIAL_FIXES.json')
    json.dump(record, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('FIX_LABEL written: %d | KEEP_LABEL: %d' % (len(FIX_LABEL), len(KEEP_LABEL)))
    for e in record:
        if e['type'] == 'FIX_LABEL':
            print('  %-15s %-30s -> %s' % (e['did'], (e['old'] or '')[:30], e['new']))


if __name__ == '__main__':
    main()
