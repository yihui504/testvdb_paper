#!/usr/bin/env python3
"""fixB：milvus developer_cognition 补第二条裁决准绳锚点（系统内校验不对称）。

杠杆1（通道一致性，fixA 已采纳）的自然推广：同一约束被系统内某一端点/客户端
（REST/gRPC/SDK/另一端点）执行而此处不执行 = 偶发校验缺口而非设计选择。
支撑：47763(ACK, insert/query 字段名不对称)、50323(ACK, SDK 报 Ambiguous 而 REST 静默)、
50018(ACK, aliases/list 与其他端点不对称) —— >=2 个独立维护者行为，作用于现象类。
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
V2 = r'C:/Users/11428/Desktop/tvdb_sessions/intelligence/milvus/developer_cognition.json'
SRC = os.path.join(ROOT, 'intel', 'milvus', 'developer_cognition.json')
ANCHOR = ('Validation asymmetry within the system: the same constraint enforced by one endpoint '
          'or client (REST/gRPC/SDK/peer endpoint) but not another indicates an accidental '
          'validation gap rather than a design choice')


def patch(path):
    d = json.load(open(path, encoding='utf-8'))
    bs = d['developer_cognition_signals']['blindspot_indicators']
    if ANCHOR in bs:
        return 'already'
    bs.append(ANCHOR)
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return 'added'


states = [patch(p) for p in (V2, SRC)]
fx_path = os.path.join(ROOT, 'MATERIAL_FIXES.json')
fx = json.load(open(fx_path, encoding='utf-8'))
fx.append({
    'type': 'FIX_INTEL_BLINDSPOT_ANCHOR_FIXB',
    'target': 'intelligence/milvus/developer_cognition.json (v2+src)',
    'field': 'developer_cognition_signals.blindspot_indicators[+1]',
    'old': 'cross-channel criterion only (fixA)',
    'new': ANCHOR,
    'scope': 'milvus only; generalization of fixA lever to endpoint/client asymmetry; rationale: docs/phase2-fixa-report.md',
    'date': '2026-08-15',
})
json.dump(fx, open(fx_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('v2=%s src=%s | MATERIAL_FIXES %d' % (*states, len(fx)))
