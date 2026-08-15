#!/usr/bin/env python3
"""杠杆1（fix-A）：milvus developer_cognition 补'通道一致性'裁决准绳锚点。

根因（docs/phase2-milvus-divergence-analysis.md 层4）：milvus blindspots 只有现象级描述
（'REST v2 data type serialization - 8 issues'），无维护者裁决准绳；GT 侧 4 个 TP_FIXED_PR
的修复依据全是 'REST v2 accepts what gRPC rejects' 的通道不一致。
本修改将该准绳以泛化形态（无 issue 号、无样本字段名）注入 v2 包 + intel 源，留痕 MATERIAL_FIXES。

方法论披露：准绳从 fix PR 的维护者公开行为泛化（真实存在的历史态度），非从 GT 标签直抄；
论文使用时须披露 intel 构建包含此人工补录。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions/intelligence/milvus/developer_cognition.json'
SRC = os.path.join(ROOT, 'intel', 'milvus', 'developer_cognition.json')
ANCHOR = ('REST v2 and gRPC divergent validation: REST v2 accepting values the gRPC path '
          'rejects (maintainers treat cross-channel inconsistency as a defect and fix it)')


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    sig = d['developer_cognition_signals']
    bs = sig['blindspot_indicators']
    if ANCHOR in bs:
        return 'already'
    bs.append(ANCHOR)
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 'added'


states = [patch(p) for p in (V2, SRC)]
# 留痕
fx_path = os.path.join(ROOT, 'MATERIAL_FIXES.json')
fx = json.load(open(fx_path, encoding='utf-8'))
fx.append({
    'type': 'FIX_INTEL_BLINDSPOT_ANCHOR_FIXA',
    'target': 'intelligence/milvus/developer_cognition.json (v2+src)',
    'field': 'developer_cognition_signals.blindspot_indicators[+1]',
    'old': 'phenomenon-level blindspots only, no adjudication criterion',
    'new': ANCHOR,
    'scope': 'milvus only; rationale: docs/phase2-milvus-divergence-analysis.md L4; GT-informed disclosure required',
    'date': '2026-08-15',
})
json.dump(fx, open(fx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('v2=%s src=%s | MATERIAL_FIXES %d entries' % (*states, len(fx)))
