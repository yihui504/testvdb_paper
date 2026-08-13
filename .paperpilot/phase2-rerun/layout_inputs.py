#!/usr/bin/env python3
"""Phase 2 rerun — 把 71 样本还原成 dev-reviewer 真读的文件布局。

把现有产物摆进 run/ 下的真实布局(见 testvdb4exp/commands/mine.md Output):
  run/results/{target}/{version}/structured_contract.json   (从 contracts/)
  run/results/{target}/{version}/api_templates.md           (从契约 api_endpoints 生成)
  run/intelligence/{target}/{developer_cognition,bug_shapes}.json  (从 intel/)
  run/results/{target}/{version}/{num}/.srcdir              (一行: 该版本 clone 路径)
  run/results/{target}/{version}/{num}/debate_logs/stage2_aggregation.json  (1 候选=该样本, 无 GT)

不产出 output_*.log(需跑探针, 属实验期)。每样本一个 session, 候选标 severity=High
(dev-reviewer 只审 Critical/High), 确保 71 个都被审。
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
VMAP = json.load(open(os.path.join(ROOT, 'contracts', 'version_map.json'), encoding='utf-8'))
PKT_IDX = {p['defect_id']: p for p in json.load(open(os.path.join(ROOT, 'packets', '_index.json'), encoding='utf-8'))}
RUN = os.path.join(ROOT, 'run')
VDB_SRC = r'C:\Users\11428\Desktop\vdb_src'


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def contract_path(vendor, version):
    return os.path.join(ROOT, 'contracts', vendor, VMAP[vendor][version]['file'] + '.json')


def gen_api_templates_md(contract):
    lines = ['# API Templates — %s %s' % (contract.get('target'), contract.get('version')), '']
    for ep in contract.get('api_endpoints', []) or contract.get('endpoint_registry', []):
        lines.append('## %s %s' % (ep.get('method', '?'), ep.get('path', '?')))
        if ep.get('description'):
            lines.append(ep['description'])
        dq = ep.get('doc_quote')
        if dq:
            lines.append('doc: %s' % dq)
        if ep.get('source_url'):
            lines.append('source: %s' % ep['source_url'])
        lines.append('')
    return '\n'.join(lines)


def main():
    # 清重建 run/
    if os.path.isdir(RUN):
        shutil.rmtree(RUN)

    manifest = []
    contract_cache = {}
    scored = [c for c in CASES if c['group'] in ('A', 'B', 'C')]

    def load_contract(vendor, version):
        key = (vendor, version)
        if key not in contract_cache:
            contract_cache[key] = json.load(open(contract_path(vendor, version), encoding='utf-8'))
        return contract_cache[key]

    # 1) 版本级 structured_contract.json + api_templates.md；目标级 intelligence/
    versions_done = set()
    for c in scored:
        v, ver = c['vendor'], c['version']
        if (v, ver) in versions_done:
            continue
        versions_done.add((v, ver))
        contract = load_contract(v, ver)
        vdir = os.path.join(RUN, 'results', v, ver)
        os.makedirs(vdir, exist_ok=True)
        json.dump(contract, open(os.path.join(vdir, 'structured_contract.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        open(os.path.join(vdir, 'api_templates.md'), 'w', encoding='utf-8').write(gen_api_templates_md(contract))
    for v in ('milvus', 'qdrant', 'weaviate'):
        idir = os.path.join(RUN, 'intelligence', v)
        os.makedirs(idir, exist_ok=True)
        for fn in ('developer_cognition.json', 'bug_shapes.json'):
            shutil.copy(os.path.join(ROOT, 'intel', v, fn), os.path.join(idir, fn))

    # 2) 每样本一个 session: .srcdir + debate_logs/stage2_aggregation.json
    for c in scored:
        v, num, ver = c['vendor'], c['num'], c['version']
        did = '%s_%s' % (v, num)
        sess = os.path.join(RUN, 'results', v, ver, str(num))
        os.makedirs(os.path.join(sess, 'debate_logs'), exist_ok=True)
        tag = tag_for(v, ver)
        clone = '%s/%s/%s' % (VDB_SRC.replace('\\', '/'), v, tag)
        open(os.path.join(sess, '.srcdir'), 'w', encoding='utf-8').write(clone + '\n')

        seg = json.load(open(os.path.join(ROOT, 'contracts', 'segments', did + '.json'), encoding='utf-8'))
        at = seg.get('api_template') or {}
        endpoint = at.get('endpoint') or ''
        dtype = (PKT_IDX.get(did) or {}).get('defect_type') or 'unknown'
        agg = {
            'summary': 'rerun: 1 candidate (Phase 2 confirmation sample, dev-reviewer redo)',
            'aggregator': 'layout_inputs.py (rerun)',
            'confirmed': {
                did: {
                    'defect_id': did,
                    'endpoint': endpoint,
                    'defect_type': dtype,
                    'severity_level': 'High',
                    'confirmed': True,
                    'related_issue_numbers': [int(num)],
                    'note': 'rerun candidate — restore from issue; no GT/rationale leaked',
                }
            },
            'rejected': {},
        }
        json.dump(agg, open(os.path.join(sess, 'debate_logs', 'stage2_aggregation.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        clone_ok = os.path.isdir(clone.replace('/', os.sep))
        manifest.append({
            'defect_id': did, 'vendor': v, 'version': ver, 'num': num,
            'endpoint': endpoint, 'defect_type': dtype,
            'gt_group': c['group'],
            'session_dir': 'run/results/%s/%s/%s' % (v, ver, num),
            'clone': clone, 'clone_ok': clone_ok,
            'output_log': 'PENDING (experiment: run probe)',

        })

    json.dump(manifest, open(os.path.join(RUN, '_manifest.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print('sessions staged:', len(manifest))
    print('versions:', len(versions_done))
    print('clone_ok:', sum(1 for m in manifest if m['clone_ok']), '/', len(manifest))
    print('endpoint empty:', sum(1 for m in manifest if not m['endpoint']))
    print('defect_type unknown:', sum(1 for m in manifest if m['defect_type'] == 'unknown'))


if __name__ == '__main__':
    main()
