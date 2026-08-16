#!/usr/bin/env python3
"""fixH 前置：M1 残留断言修复（001 消歧 + 002 去 duplicate-rejection）。

判据（独立于 GT，与 fixE M1 同源）：errIgnoredCreateCollection 专用常量 + root_coord.go
"create existed collection with same schema, ignore it" 注释 + 实测同 schema 200。
002 与 M1 已修的 milvus_invariant_create_duplicate_001 描述同一端点同一现象，方向必须一致
（材料内战残留——fixG 022 翻错判词消费 state_001 定位）。
材料树 structured_contract.json 逐版本修改 + MATERIAL_FIXES 留痕 + 备份。
"""
import glob
import json
import os
import shutil

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
FIXLOG = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/MATERIAL_FIXES.json'
BACKUP = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/clean_run_fixes/fixH/pre_contract_backup'

FIXES = {
    'milvus_state_collections_create_001': {
        'fields': {
            'description': 'Collection creation is atomic; collection names are unique within a '
                           'database, and re-creation is idempotent when the schema is unchanged',
            'assertion': 'collection creation is atomic AND collectionName is unique within dbName; '
                         're-creating an existing collection with the SAME schema is an idempotent '
                         'no-op returning 200, re-creating with a DIFFERENT schema returns an error',
        },
        'evidence': 'errIgnoredCreateCollection dedicated constant + comment "create existed '
                    'collection with same schema, ignore it" (root_coord.go); observed 200 on '
                    'duplicate same-schema create (fixE/fixG Step-1 reproductions); same phenomenon '
                    'as milvus_invariant_create_duplicate_001 already corrected by M1 (fixE)',
    },
    'milvus_behavioral_collections_create_002': {
        'fields': {
            'description': 'Create collection returns 400 on invalid parameters; duplicate name is '
                           'not an error when the schema is unchanged (idempotent no-op)',
            'expected_behavior': 'returns 400 with descriptive error message on invalid parameters; '
                                 'duplicate collection name with the same schema returns 200 '
                                 '(idempotent no-op), with a different schema returns an error',
        },
        'evidence': 'same-source as M1 (fixE): errIgnoredCreateCollection + explicit ignore comment '
                    '+ observed 200; prior "400 on duplicate name" assertion conflicted with the '
                    'M1-corrected invariant_create_duplicate_001 (internal contract inconsistency)',
    },
}


def patch_file(path):
    d = json.load(open(path, encoding='utf-8'))
    changed = []

    def walk(o):
        if isinstance(o, dict):
            cid = str(o.get('constraint_id') or o.get('assertion_id') or o.get('invariant_id') or '')
            if cid in FIXES:
                for k, v in FIXES[cid]['fields'].items():
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
    total = {}
    for path in sorted(glob.glob(os.path.join(V2, 'sessions', 'milvus', '*', 'structured_contract.json'))):
        for cid in patch_file(path):
            total.setdefault(cid, []).append(path.split(os.sep)[-2])
    log = json.load(open(FIXLOG, encoding='utf-8')) if os.path.isfile(FIXLOG) else []
    log.append({
        'id': len(log) + 1, 'date': '2026-08-16', 'run': 'fixH',
        'type': 'contract_assertion_correction',
        'target': '; '.join('%s (%d versions)' % (k, len(v)) for k, v in total.items()),
        'old': '001 unique-only (duplicate-create rejection implied) / 002 "returns 400 on duplicate name"',
        'new': '001 + idempotent same-schema no-op disambiguation / 002 duplicate no longer an error '
               'when schema unchanged',
        'scope': 'milvus structured_contract.json across version dirs; rationale independent of GT, '
                 'same-source as fixE M1 (source-intent constant/comment + observed behavior); '
                 'located via fixG control-flip verdict consumption of residual assertion',
        'backup': BACKUP,
    })
    json.dump(log, open(FIXLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in total.items():
        print('%s: patched in %d versions (%s)' % (k, len(v), ','.join(sorted(set(v)))))
    print('MATERIAL_FIXES -> %d entries' % len(log))


if __name__ == '__main__':
    main()
