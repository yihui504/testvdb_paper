#!/usr/bin/env python3
"""fixG 前置：C/G 两条裁决锚点注入（依据 investigate_fn_stances/STANCES_REPORT.md 三条件检验）。

- 锚点 C → milvus intel：文档-行为一致性（支撑 50355 docs PR 3513/3514 + 46683 docs PR 3402
  + 46494 foxspy 'fixed'，3 独立修复行为，无反向）
- 锚点 G → weaviate intel：HTTP 错误码语义（支撑 12049 MERGED 500→422 + 12040 MERGED 500→404
  + 11878 MERGED 批量错误码修正 + etiennedi MEMBER +1 on 12262，无反向）
注入位置：顶层 blindspot_indicators + developer_cognition_signals.blindspot_indicators 双处
（fixD 模式）；v2 材料树 + intel 源两文件同步；备份 + MATERIAL_FIXES 留痕。
"""
import json
import os
import shutil

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
SRC = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/intel'
FIXLOG = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/MATERIAL_FIXES.json'
BACKUP = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/clean_run_fixes/fixG/pre_fixG_backup'

ANCHOR_C = (
    "Documentation-behavior consistency: when official documentation claims a behavior or "
    "capability that the server does not exhibit (documented X, actual behavior is not-X), "
    "this is a consistency defect - maintainers' repeated disposition is to fix it, usually by "
    "correcting the docs to match verified behavior (docs PRs 3402, 3513/3514; issue 46494 "
    "closed as fixed). 'The behavior looks reasonable on its own' does not neutralize a "
    "documented claim that contradicts it"
)

ANCHOR_G = (
    "HTTP status-code semantics: server-side 5xx responses to request-side detectable errors "
    "(invalid or missing parameters, non-existent resources, mode-inapplicable operations) are "
    "treated as defects by maintainers and repeatedly fixed (500->422 merged PR 12049, "
    "500->404 merged PR 12040, batch REST handler error-code fixes merged PR 11878, 500->202 "
    "with maintainer +1 on PR 12262). 5xx is reserved for genuine internal failures; 'the "
    "validation exists and the error message is clear' does not make a 5xx status correct"
)


def inject(path, anchor, tag):
    shutil.copy2(path, os.path.join(BACKUP, 'dc_%s.bak' % tag))
    d = json.load(open(path, encoding='utf-8'))
    top = d.setdefault('blindspot_indicators', [])
    inner = d.setdefault('developer_cognition_signals', {}).setdefault('blindspot_indicators', [])
    for lst in (top, inner):
        if anchor not in lst:
            lst.append(anchor)
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return len(top), len(inner)


def main():
    os.makedirs(BACKUP, exist_ok=True)
    t1, i1 = inject(os.path.join(V2, 'intelligence', 'milvus', 'developer_cognition.json'), ANCHOR_C, 'v2_milvus')
    t2, i2 = inject(os.path.join(SRC, 'milvus', 'developer_cognition.json'), ANCHOR_C, 'src_milvus')
    t3, i3 = inject(os.path.join(V2, 'intelligence', 'weaviate', 'developer_cognition.json'), ANCHOR_G, 'v2_weaviate')
    t4, i4 = inject(os.path.join(SRC, 'weaviate', 'developer_cognition.json'), ANCHOR_G, 'src_weaviate')
    print('milvus: v2 top=%d inner=%d | src top=%d' % (t1, i1, t2))
    print('weaviate: v2 top=%d inner=%d | src top=%d' % (t3, i3, t4))
    log = json.load(open(FIXLOG, encoding='utf-8')) if os.path.isfile(FIXLOG) else []
    log.append({
        'id': len(log) + 1, 'date': '2026-08-16', 'run': 'fixG',
        'type': 'intel_anchor_injection', 'target': 'milvus+weaviate developer_cognition.blindspot_indicators (top+inner)',
        'old': 'milvus top0/inner7; weaviate top0/inner6',
        'new': 'milvus +C (doc-behavior consistency); weaviate +G (HTTP status-code semantics); both dual-site',
        'scope': 'milvus gets C only, weaviate gets G only; qdrant untouched',
        'evidence': 'investigate_fn_stances/STANCES_REPORT.md sec2: C = docs PRs 3402/3513/3514 + issue 46494 fixed '
                    '(3 independent fix behaviors); G = merged PRs 12049/12040/11878 + member +1 on 12262; '
                    'reverse-stance search clean for both; wording names no field/endpoint (condition 3)',
        'backup': BACKUP,
    })
    json.dump(log, open(FIXLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('MATERIAL_FIXES -> %d entries' % len(log))


if __name__ == '__main__':
    main()
