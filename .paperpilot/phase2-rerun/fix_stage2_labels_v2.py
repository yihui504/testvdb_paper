#!/usr/bin/env python3
"""待办 2 落地 — 修正三方比对发现的 stage2 endpoint/defect_type 标签错配。

背景：fill_endpoints.py 从探针流量自动抽取 endpoint 时抽错（取主流量而非缺陷操作），
排雷只修了人工发现的 25 处（含 5 个 KEEP 决策）。三方比对（probe↔issue↔stage2，见
probe_issue_audit/*.json）发现 19 处残余错配，其中 5 处正是排雷阶段 KEEP 保留的。
本脚本把修正写入：三棵判定树 + tvdb_sessions v2 材料包（经 defect_id_map 反查匿名 did）。

幂等：old 值与实际不符时跳过并报告（不静默强改）。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
TREES = ('run', 'run2', 'run3')
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
ID_MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))

# 19 处修正（三方比对结论，证据见 probe_issue_audit/*.json）
FIX_ENDPOINT = {
    'milvus_47767': ('databases+drop', 'entities+search'),
    'milvus_49823': ('entities+insert', 'entities+search'),
    'milvus_49843': ('collections+alter', 'collections+create'),
    'milvus_49844': ('entities+insert', 'entities+query'),
    'milvus_49889': ('collections+create', 'collections+list'),
    'milvus_49890': ('entities+insert', 'collections+list'),
    'milvus_49929': ('entities+insert', 'indexes+create'),
    'milvus_49930': ('collections+create', 'entities+search'),
    'milvus_50193': ('collections+load', 'collections+get_stats'),
    'milvus_50194': ('entities+insert', 'entities+search'),
    'milvus_50323': ('entities+insert', 'entities+delete'),
    'milvus_50325': ('collections+list', 'collections+create'),
    'milvus_51085': ('entities+insert', 'collections+create'),
    'milvus_52309': ('entities+insert', 'entities+search'),
    'milvus_52312': ('entities+insert', 'entities+upsert'),
    'qdrant_9373': ('collections+{collection_name}+points+count', 'collections+{collection_name}+points+scroll'),
    'weaviate_11399': ('GET /schema', 'POST /schema'),
    'weaviate_11400': ('GET /schema', 'POST /schema'),
}
FIX_DEFECT_TYPE = {
    'milvus_49059': ('crash', 'behavior'),
}


def patch_file(path: str, did: str, field: str, old: str, new: str) -> str:
    """patch 单个 stage2_aggregation.json；返回 'ok' / 'skip(old-mismatch)' / 'missing'。"""
    if not os.path.isfile(path):
        return 'missing'
    agg = json.load(open(path, encoding='utf-8'))
    conf = agg.get('confirmed', {})
    if did not in conf:
        return 'missing-key'
    cur = conf[did].get(field)
    if cur != old:
        return 'skip(old=%r)' % cur
    conf[did][field] = new
    json.dump(agg, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 'ok'


def main() -> None:
    fixes = []  # 追加 MATERIAL_FIXES 记录
    applied = {}
    for did, (old, new) in FIX_ENDPOINT.items():
        vendor, num = did.split('_')
        case = next(c for c in CASES if c['vendor'] == vendor and c['num'] == int(num))
        v, ver = case['vendor'], case['version']
        # 三棵判定树
        for tree in TREES:
            p = os.path.join(ROOT, tree, 'results', v, ver, num, 'debate_logs', 'stage2_aggregation.json')
            r = patch_file(p, did, 'endpoint', old, new)
            applied.setdefault(did, {})[tree] = r
        # v2 材料包（匿名 did）
        anon = next(d for d, r in ID_MAP.items() if r['orig'] == did)
        p2 = os.path.join(V2, 'sessions', v, ver, anon, 'debate_logs', 'stage2_aggregation.json')
        applied[did]['v2'] = patch_file(p2, anon, 'endpoint', old, new)
        fixes.append({'did': did, 'type': 'FIX_LABEL_V2AUDIT', 'field': 'endpoint',
                      'old': old, 'new': new, 'trees': sorted(applied[did])})
    for did, (old, new) in FIX_DEFECT_TYPE.items():
        vendor, num = did.split('_')
        case = next(c for c in CASES if c['vendor'] == vendor and c['num'] == int(num))
        v, ver = case['vendor'], case['version']
        for tree in TREES:
            p = os.path.join(ROOT, tree, 'results', v, ver, num, 'debate_logs', 'stage2_aggregation.json')
            r = patch_file(p, did, 'defect_type', old, new)
            applied.setdefault(did, {})[tree] = r
        anon = next(d for d, r in ID_MAP.items() if r['orig'] == did)
        p2 = os.path.join(V2, 'sessions', v, ver, anon, 'debate_logs', 'stage2_aggregation.json')
        applied[did]['v2'] = patch_file(p2, anon, 'defect_type', old, new)
        fixes.append({'did': did, 'type': 'FIX_DEFECT_TYPE_V2AUDIT', 'field': 'defect_type',
                      'old': old, 'new': new, 'trees': sorted(applied[did])})

    # 追加 MATERIAL_FIXES 记录
    mf_path = os.path.join(ROOT, 'MATERIAL_FIXES.json')
    mf = json.load(open(mf_path, encoding='utf-8'))
    mf.extend(fixes)
    json.dump(mf, open(mf_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    for did, rs in applied.items():
        bad = {t: r for t, r in rs.items() if r != 'ok'}
        print('%-16s %s' % (did, 'ALL-OK' if not bad else bad))
    print('MATERIAL_FIXES: %d -> %d records' % (len(mf) - len(fixes), len(mf)))


if __name__ == '__main__':
    main()
