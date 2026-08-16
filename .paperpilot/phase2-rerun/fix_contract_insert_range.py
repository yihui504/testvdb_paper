#!/usr/bin/env python3
"""fixI：过时断言修复 milvus_range_entities_insert_001（"len(data) <= 100"）。

判据（独立于 GT，四源闭合）：
- 源码：handler_v2.go:1267/1351 `req.NumRows = uint32(len(httpReq.Data))` 直接赋值无行数校验；
  断言 source_url 指向的 constant.go（213 行）不存在任何 100/maxRow 常量——断言与其"源"矛盾
- 实测：200/500 entities 均返回 200（fixG/fixH 两轮 025 判词 Step1/4 复现）
- 文档：50324 内 yihui504 公开核验 v2.6.x REST insert 文档并无 entity count 上限（v1 旧文档才有）
  ——"100 上限"= formalizer 从 v1 迁移的过时断言
材料树逐版本修改 + MATERIAL_FIXES 留痕 + 备份。
"""
import glob
import json
import os
import shutil

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
FIXLOG = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/MATERIAL_FIXES.json'
BACKUP = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/clean_run_fixes/fixH/pre_contract_fixI'

FIX = {
    'milvus_range_entities_insert_001': {
        'description': 'REST insert has no fixed row-count limit; request size is bounded by '
                       'payload-size limits, not by an entity count',
        'assertion': 'no fixed upper bound on len(data); inserts of any row count that fits the '
                     'request payload are accepted (HTTP 200)',
    },
}


def patch_file(path):
    d = json.load(open(path, encoding='utf-8'))
    changed = []

    def walk(o):
        if isinstance(o, dict):
            cid = str(o.get('constraint_id') or o.get('assertion_id') or o.get('invariant_id') or '')
            if cid in FIX:
                for k, v in FIX[cid].items():
                    if o.get(k) != v:
                        o[k] = v
                        changed.append(cid)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    walk(d)
    if changed:
        shutil.copy2(path, os.path.join(BACKUP, os.path.basename(os.path.dirname(path)) + '_' + os.path.basename(path) + '.bak'))
        json.dump(d, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    return changed


def main():
    os.makedirs(BACKUP, exist_ok=True)
    total = []
    for path in sorted(glob.glob(os.path.join(V2, 'sessions', 'milvus', '*', 'structured_contract.json'))):
        ver = path.split(os.sep)[-2]
        if patch_file(path):
            total.append(ver)
    log = json.load(open(FIXLOG, encoding='utf-8')) if os.path.isfile(FIXLOG) else []
    log.append({
        'id': len(log) + 1, 'date': '2026-08-16', 'run': 'fixI',
        'type': 'contract_assertion_correction',
        'target': 'milvus_range_entities_insert_001 (%d versions)' % len(total),
        'old': '"len(data) <= 100" max-entities-per-insert',
        'new': 'no fixed row-count limit; bounded by payload size only',
        'scope': 'milvus structured_contract.json across version dirs; rationale independent of GT: '
                 'handler_v2.go direct assignment without count check + constant.go (cited source) '
                 'contains no such constant + observed 200/500 accepted + v2 docs contain no count '
                 'limit (publicly verified in milvus#50324) - stale v1-doc assertion migrated by '
                 'formalizer',
        'backup': BACKUP,
    })
    json.dump(log, open(FIXLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('patched in %d versions (%s)' % (len(total), ','.join(total)))
    print('MATERIAL_FIXES -> %d entries' % len(log))


if __name__ == '__main__':
    main()
