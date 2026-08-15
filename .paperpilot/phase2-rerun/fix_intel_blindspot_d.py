#!/usr/bin/env python3
"""fixD: 向 qdrant developer_cognition 注入 3 条 vendor 锚点（D2/D3/D4）。

注入位置：顶层 blindspot_indicators（与既有 10 条并列，reviewer 消费位置）
        + developer_cognition_signals.blindspot_indicators（与 fixA milvus 锚点形态一致）。
v2 材料包 + intel 源两文件同步；MATERIAL_FIXES 追加 1 条记录。
锚点内容与依据见 clean_run_fixes/fixD/FIXD_PLAN.md §2（维护者评论原文 2026-08-15 fetch 验证）。
"""
import json
import os
import shutil

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
SRC_INTEL = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/intel/qdrant/developer_cognition.json'
FIXLOG = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/MATERIAL_FIXES.json'
BACKUP = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/clean_run_fixes/fixD/pre_fixD_backup'

ANCHORS = [
    "Payload-only collections: creating a collection without vector configuration is a supported "
    "use case, errors surface on first vector use (maintainers: 'not an unusable collection, it "
    "allows payload-only collection'; named-vector CRUD added on top)",
    "Lenient filter parsing: null / single-object / array forms are all accepted by design for "
    "filter condition fields (maintainers: 'This is fine and expected... it would be a breaking "
    "change'; source supports all three forms)",
    "Batch operations are not promised to be atomic: users must assume partial application and "
    "retry (idempotent write design) (maintainers: 'batch operations are not promissed to be "
    "atomic')",
]


def inject(path, tag):
    shutil.copy2(path, os.path.join(BACKUP, 'dc_%s.bak' % tag))
    d = json.load(open(path, encoding='utf-8'))
    top = d.setdefault('blindspot_indicators', [])
    sig = d.setdefault('developer_cognition_signals', {})
    inner = sig.setdefault('blindspot_indicators', [])
    for a in ANCHORS:
        if a not in top:
            top.append(a)
        if a not in inner:
            inner.append(a)
    json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return len(top) - len(ANCHORS), len(top), len(inner)


def main():
    os.makedirs(BACKUP, exist_ok=True)
    inject(os.path.join(V2, 'intelligence', 'qdrant', 'developer_cognition.json'), 'v2')
    before, after, inner = inject(SRC_INTEL, 'src')
    print('v2: top %d->13, inner %d; src: top %d->13' % (before, inner, before))
    log = json.load(open(FIXLOG, encoding='utf-8')) if os.path.isfile(FIXLOG) else []
    log.append({
        'id': len(log) + 1, 'date': '2026-08-15', 'run': 'fixD',
        'type': 'intel_anchor_injection', 'target': 'qdrant developer_cognition.blindspot_indicators (top+inner)',
        'old': '10 anchors', 'new': '13 anchors (+D2/D3/D4)',
        'scope': 'qdrant only; milvus/weaviate untouched',
        'evidence': 'maintainer comments on issues 9416/9417/9418/9419/9371 (fetched 2026-08-15); '
                    'D1 (9027) NOT injected: single-behavior, violates anchor condition 1',
        'backup': BACKUP,
    })
    json.dump(log, open(FIXLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('MATERIAL_FIXES -> %d entries' % len(log))


if __name__ == '__main__':
    main()
