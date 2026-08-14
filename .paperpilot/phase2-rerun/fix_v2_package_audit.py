#!/usr/bin/env python3
"""v2 材料包深入审核的修复落地（audit_materials_v2.py 发现的 3 类问题）。

  1. related_issue_numbers 含样本号（71/71 = 自身号）→ 全部置空。
     SOP 解禁 github.com：匿名 defect_id 挡不住 related_issue_numbers 这个真实号，
     dev-reviewer 可 WebFetch 查自身 issue 的 maintainer 状态（= GT）。真实流程里
     attack 输出的 related_issue_numbers 是内部编号，无 GitHub 语义 → 置空不偏离形态。
  2. qdrant 1.18.3 structured_contract.json 含实验元数据 → 清理。
     - 每个 endpoint 条目的 `_provenance_runs`（实验侧 run 溯源，真实契约无此字段）
     - `_note`（"v2.5.2 手工补 — …（C+D 实验失败根因）"——实验失败分析，dev-reviewer 不该看到）
     - generation.knowledge_extractor_agent 里的 "(3 independent runs: run1/run2/run3)"
  3. 删除 6 个 raw_*.log 中间文件。fill_raw_v2 已把 raw 转换进 output_*.log
     （=== REQ/RESP === 格式），raw 是冗余中间产物；session 目录形态应只有 output_*.log。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
ID_MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))

CONTRACT = os.path.join(V2, 'sessions', 'qdrant', '1.18.3', 'structured_contract.json')


def fix_related_issue_numbers() -> list:
    """71 个 stage2 的 related_issue_numbers → []。返回修复记录。"""
    fixes = []
    for did, r in ID_MAP.items():
        p = os.path.join(V2, 'sessions', r['vendor'], r['version'], did,
                         'debate_logs', 'stage2_aggregation.json')
        agg = json.load(open(p, encoding='utf-8'))
        conf = agg['confirmed'][did]
        old = conf.get('related_issue_numbers', [])
        if old:
            conf['related_issue_numbers'] = []
            json.dump(agg, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
            fixes.append({'did': did, 'type': 'FIX_RELATED_ISSUE_NUMS_V2AUDIT',
                          'field': 'related_issue_numbers', 'old': old, 'new': [], 'trees': ['v2']})
    return fixes


def fix_contract_metadata() -> list:
    """清理 qdrant 1.18.3 契约的实验元数据字段。"""
    d = json.load(open(CONTRACT, encoding='utf-8'))
    fixes = []

    def clean(node):
        if isinstance(node, dict):
            for k in ('_provenance_runs', '_note'):
                if k in node:
                    fixes.append({'did': 'qdrant/1.18.3 contract', 'type': 'FIX_CONTRACT_METADATA_V2AUDIT',
                                  'field': k, 'old': node.pop(k), 'new': None, 'trees': ['v2']})
            for v in node.values():
                clean(v)
        elif isinstance(node, list):
            for it in node:
                clean(it)

    clean(d)
    gen = d.get('generation', {})
    if gen.get('knowledge_extractor_agent') != 'testvdb:knowledge-extractor':
        fixes.append({'did': 'qdrant/1.18.3 contract', 'type': 'FIX_CONTRACT_METADATA_V2AUDIT',
                      'field': 'generation.knowledge_extractor_agent',
                      'old': gen.get('knowledge_extractor_agent'), 'new': 'testvdb:knowledge-extractor',
                      'trees': ['v2']})
        gen['knowledge_extractor_agent'] = 'testvdb:knowledge-extractor'
    json.dump(d, open(CONTRACT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return fixes


def drop_raw_intermediates() -> list:
    """删除 fill_raw 遗留的 raw_*.log 中间文件（内容已进 output_*.log）。"""
    fixes = []
    for did, r in ID_MAP.items():
        p = os.path.join(V2, 'sessions', r['vendor'], r['version'], did, 'raw_%s.log' % did)
        if os.path.isfile(p):
            os.remove(p)
            fixes.append({'did': did, 'type': 'FIX_DROP_RAW_INTERMEDIATE_V2AUDIT',
                          'field': 'raw_%s.log' % did, 'old': 'present', 'new': 'removed', 'trees': ['v2']})
    return fixes


def main() -> None:
    fixes = fix_related_issue_numbers() + fix_contract_metadata() + drop_raw_intermediates()
    mf_path = os.path.join(ROOT, 'MATERIAL_FIXES.json')
    mf = json.load(open(mf_path, encoding='utf-8'))
    mf.extend(fixes)
    json.dump(mf, open(mf_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('applied %d fixes -> MATERIAL_FIXES %d records' % (len(fixes), len(mf)))
    for f in fixes[:5]:
        print(' ', f['type'], f.get('did'), f.get('field'), '| old=%r new=%r' % (f.get('old'), f.get('new')))


if __name__ == '__main__':
    main()
