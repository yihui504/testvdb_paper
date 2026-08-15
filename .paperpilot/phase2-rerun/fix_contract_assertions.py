#!/usr/bin/env python3
"""fixE 前置：契约断言修复（4 条，跨版本统一）。

判据（全部独立于 GT：源码显式意图 + 实测行为 + 文档缺失）：
- M1 milvus_invariant_create_duplicate_001 "must return 400" ← errIgnoredCreateCollection 专用常量
  + root_coord.go 注释 "create existed collection with same schema, ignore it" + 实测同 schema 200
- M2 milvus_behavioral_collections_drop_001 "returns 404 if not found" ← errIgnoredDropCollection
  + 注释 "permit drop collection one with bad collection name" + 实测 200
- Q1 qdrant_state_create_collection_001 "fully initialized" ← 源码 VectorsConfig::empty() 显式
  支持 payload-only（validate_vectors.rs None -> Ok(())）
- Q2 qdrant_state_batch_update_007 "executed atomically" ← 源码顺序执行无回滚（update.rs）且
  qdrant 文档无原子承诺（formalizer 发明断言）
材料树 structured_contract.json 逐版本修改 + MATERIAL_FIXES 留痕。
"""
import glob
import json
import os
import shutil

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
FIXLOG = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/MATERIAL_FIXES.json'
BACKUP = r'C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/clean_run_fixes/fixE/pre_contract_backup'

FIXES = {
    'milvus_invariant_create_duplicate_001': {
        'fields': {
            'description': 'Idempotent collection creation: re-creating an existing collection '
                           'with the SAME schema succeeds (HTTP 200, no-op); re-creating with '
                           'DIFFERENT parameters returns an error',
            'assertion': "create(collection, schema A) -> create(collection, schema A) returns 200 "
                         "(idempotent no-op); create(collection, schema B != A) returns error",
        },
        'evidence': 'errIgnoredCreateCollection dedicated constant + comment "create existed '
                    'collection with same schema, ignore it" (root_coord.go:903-906); observed 200 '
                    'on duplicate same-schema create across sessions',
    },
    'milvus_behavioral_collections_drop_001': {
        'fields': {
            'description': 'Drop collection returns 200 on success; dropping a non-existent '
                           'collection is treated as idempotent success (200, empty data)',
            'expected_behavior': "returns 200 with empty data on success AND on non-existent "
                                 "collection (idempotent drop, no 404)",
        },
        'evidence': 'errIgnoredDropCollection constant + comment "permit drop collection one with '
                    'bad collection name" (task.go:710-715); observed 200 on drop of missing '
                    'collection across sessions',
    },
    'qdrant_state_create_collection_001': {
        'fields': {
            'description': 'Collection creation accepts configuration literally; a collection '
                           'created without vector config is valid for payload-only use, vector '
                           'errors surface on first vector operation',
            'assertion': 'After 200 response the collection exists with the configuration as '
                         'submitted; collections without vector config support payload-only '
                         'operations (vector insert returns an error at use time)',
        },
        'evidence': 'source supports VectorsConfig::empty() (validate_vectors.rs returns Ok on '
                    'None config); payload-only collections are a supported use case',
    },
    'qdrant_state_batch_update_007': {
        'fields': {
            'description': 'Batch operations are NOT promised to be atomic; on error, operations '
                           'may be none, partially, or fully applied; writes are idempotent and '
                           'clients should retry',
            'assertion': 'Batch update operations may be partially applied on failure; atomicity '
                         'is not guaranteed; clients must retry to reach a consistent state',
        },
        'evidence': 'sequential per-op execution without transaction/rollback (update.rs:803-912); '
                    'no atomicity promise in qdrant docs (assertion was formalizer-invented)',
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
    for path in sorted(glob.glob(os.path.join(V2, 'sessions', '*', '*', 'structured_contract.json'))):
        for cid in patch_file(path):
            total.setdefault(cid, []).append(path.split(os.sep)[-2])
    log = json.load(open(FIXLOG, encoding='utf-8')) if os.path.isfile(FIXLOG) else []
    log.append({
        'id': len(log) + 1, 'date': '2026-08-16', 'run': 'fixE',
        'type': 'contract_assertion_correction',
        'target': '; '.join('%s (%d versions)' % (k, len(v)) for k, v in total.items()),
        'old': 'M1 400-on-duplicate / M2 404-on-missing-drop / Q1 fully-initialized / Q2 batch-atomic',
        'new': 'M1 idempotent-create / M2 idempotent-drop / Q1 payload-only-literal / Q2 no-atomicity',
        'scope': 'structured_contract.json across vendor version dirs; rationale independent of GT '
                 '(source-intent constants/comments + observed behavior + doc absence)',
        'backup': BACKUP,
    })
    json.dump(log, open(FIXLOG, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in total.items():
        print('%s: patched in %d versions (%s)' % (k, len(v), ','.join(sorted(set(v)))))
    print('MATERIAL_FIXES -> %d entries' % len(log))


if __name__ == '__main__':
    main()
