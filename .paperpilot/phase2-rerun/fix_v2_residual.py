#!/usr/bin/env python3
"""v2 审核残余修复（audit_materials_v2.py 第二轮发现）。

  1. qdrant 1.18.3 契约嵌套位置还有 generation 块的 run 字样（第一轮只修了顶层）：
     全局文本替换 "(3 independent runs: run1/run2/run3)" / "(3 independent runs)" → ""。
  2. 8 个 milvus output log 含裸样本号（集合名 repro_47729 / test_47763 / alias_50018 等）：
     SOP 解禁 github.com + issue 是历史 issue（maintainer 状态已定 = GT）→ 任何引向
     issue 页的线索都是实验特有泄露通道。替换裸号 → '<tracked>'（与 intelligence 清洗同占位符）。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions'

CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
SCORED = [c for c in CASES if c['group'] in ('A', 'B', 'C')]
ID_MAP = json.load(open(os.path.join(ROOT, 'defect_id_map.json'), encoding='utf-8'))
SAMPLE_NUMS = {c['num'] for c in SCORED}

CONTRACT = os.path.join(V2, 'sessions', 'qdrant', '1.18.3', 'structured_contract.json')


def fix_contract_runs() -> list:
    text = open(CONTRACT, encoding='utf-8').read()
    fixes = []
    for pat in ('(3 independent runs: run1/run2/run3)', '(3 independent runs)'):
        if pat in text:
            text = text.replace(pat, '')
            fixes.append({'did': 'qdrant/1.18.3 contract', 'type': 'FIX_CONTRACT_METADATA_V2AUDIT',
                          'field': 'generation.*', 'old': pat, 'new': '', 'trees': ['v2']})
    open(CONTRACT, 'w', encoding='utf-8').write(text)
    return fixes


def fix_log_bare_nums() -> list:
    fixes = []
    for did, r in ID_MAP.items():
        lp = os.path.join(V2, 'sessions', r['vendor'], r['version'], did, 'output_%s.log' % did)
        if not os.path.isfile(lp):
            continue
        text = open(lp, encoding='utf-8').read()
        hit = sorted(n for n in SAMPLE_NUMS if re.search(r'(?<![0-9])%d(?![0-9])' % n, text))
        if not hit:
            continue
        for n in hit:
            text = re.sub(r'(?<![0-9])%d(?![0-9])' % n, '<tracked>', text)
        open(lp, 'w', encoding='utf-8').write(text)
        fixes.append({'did': did, 'type': 'FIX_LOG_BARE_ISSUE_NUM_V2AUDIT',
                      'field': 'output_%s.log' % did, 'old': hit, 'new': '<tracked>', 'trees': ['v2']})
    return fixes


def main() -> None:
    fixes = fix_contract_runs() + fix_log_bare_nums()
    mf_path = os.path.join(ROOT, 'MATERIAL_FIXES.json')
    mf = json.load(open(mf_path, encoding='utf-8'))
    mf.extend(fixes)
    json.dump(mf, open(mf_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('applied %d fixes -> MATERIAL_FIXES %d records' % (len(fixes), len(mf)))
    for f in fixes:
        print(' ', f['type'], f.get('did'), '| old=%r' % f.get('old'))


if __name__ == '__main__':
    main()
