#!/usr/bin/env python3
"""Phase 2 rerun — 组装 71 个判定包骨架(Phase 3.1p)。

每包 7 字段(1:1 对齐 dev-reviewer 输入), 输出 packets/{vendor}_{num}.md(喂 GLM/DeepSeek)
+ .json(结构化)。raw 字段用 clean_observations 占位(实验期跑容器补全 HTTP req/resp)。

双盲: 严格排除 gt / group / gt_category / title / body / 旧 rationale / GT 标签。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
SEG = os.path.join(ROOT, 'contracts', 'segments')
SRC = os.path.join(ROOT, 'source_excerpts')
INTEL = os.path.join(ROOT, 'intel')
PROBES = os.path.join(os.path.dirname(ROOT), 'phase2', 'probes')
CLEAN_OBS_PATH = os.path.join(os.path.dirname(ROOT), 'phase2', 'clean_observations.json')

COBS = {}
if os.path.exists(CLEAN_OBS_PATH):
    COBS = {k: v for k, v in json.load(open(CLEAN_OBS_PATH, encoding='utf-8')).items() if not k.startswith('_')}

COGNITION = {v: json.load(open(os.path.join(INTEL, v, 'developer_cognition.json'), encoding='utf-8'))
             for v in ('milvus', 'qdrant', 'weaviate')}
BUGSHAPES = {v: json.load(open(os.path.join(INTEL, v, 'bug_shapes.json'), encoding='utf-8'))
             for v in ('milvus', 'qdrant', 'weaviate')}


def defect_type(vendor, num):
    p = os.path.join(PROBES, vendor, 'probe_%s_%s.py' % (vendor, num))
    if not os.path.exists(p):
        return None
    try:
        head = open(p, encoding='utf-8', errors='replace').read(500)
    except Exception:
        return None
    m = re.search(r'class:\s*([^\n|]+)', head)
    return m.group(1).strip() if m else None


def fmt_constraints(seg):
    mc = seg.get('matched_constraints', [])
    if not mc:
        derived = ' [derived from %s]' % seg['contract_file'] if seg.get('derived') else ''
        return 'NO_SPECIFIC_CONTRACT: formalized contract(%s%s) silent on this param/scenario -> verdict_A=NEUTRAL.' % (seg['contract_file'], derived)
    lines = ['contract_file: %s%s' % (seg['contract_file'], ' [derived]' if seg.get('derived') else '')]
    for c in mc:
        lines.append('- [%s] %s (%s)' % (c.get('id'), c.get('assertion') or c.get('description'), c.get('endpoint') or '?'))
        if c.get('doc_quote'):
            lines.append('    doc_quote: %s' % c['doc_quote'])
        if c.get('source_url'):
            lines.append('    source: %s' % c['source_url'])
    return '\n'.join(lines)


def fmt_source(sx):
    if not sx:
        return 'SOURCE_EXCERPT_MISSING'
    st = sx.get('status')
    if st == 'clone_pending':
        return 'clone_pending (source clone for %s not yet complete; will be filled before judging)' % sx.get('tag')
    if st == 'not_found':
        return 'not_found: %s  [judge: rely on raw+contract, confidence<=0.5]' % sx.get('note', '')
    parts = ['status: found (%d raw hits)' % sx.get('n_hits', 0)]
    for e in sx.get('excerpts', []):
        parts.append('// %s  (line %s, matched: %s)' % (e['file'], e['line'], e['term_matched']))
        parts.append(e['context'])
    return '\n'.join(parts)


def fmt_api_template(seg):
    at = seg.get('api_template')
    if not at or not at.get('endpoint'):
        return 'none matched'
    return '%s %s -- %s' % (at.get('method', ''), at.get('endpoint', ''), at.get('description', '') or at.get('doc_quote', ''))


def fmt_raw(did, vendor):
    obs = COBS.get(did)
    if obs:
        body = '\n'.join('  ' + line for line in obs) if isinstance(obs, list) else '  ' + str(obs)
    else:
        body = '  [no cleaned observation available]'
    return body + '\n  [PREP PLACEHOLDER: full HTTP req/resp (REST) captured at experiment stage via probe_common raw logging]'


def main():
    out = os.path.join(ROOT, 'packets')
    os.makedirs(out, exist_ok=True)
    index = []
    scored = [c for c in CASES if c['group'] in ('A', 'B', 'C')]
    for case in scored:
        vendor, num, version = case['vendor'], case['num'], case['version']
        did = '%s_%s' % (vendor, num)
        seg = json.load(open(os.path.join(SEG, did + '.json'), encoding='utf-8'))
        sx_path = os.path.join(SRC, did + '.json')
        sx = json.load(open(sx_path, encoding='utf-8')) if os.path.exists(sx_path) else None
        dtype = defect_type(vendor, num)

        md = []
        md.append('=== PACKET: %s ===' % did)
        md.append('[vendor=%s version=%s defect_type=%s]' % (vendor, version, dtype or 'unknown'))
        md.append('')
        md.append('--- RAW ---')
        md.append(fmt_raw(did, vendor))
        md.append('')
        md.append('--- CONTRACT SEGMENT ---')
        md.append(fmt_constraints(seg))
        md.append('')
        md.append('--- SOURCE EXCERPT ---')
        md.append(fmt_source(sx))
        md.append('')
        md.append('--- COGNITION (developer_cognition.json, full vendor) ---')
        md.append(json.dumps(COGNITION[vendor], ensure_ascii=False, indent=1))
        md.append('')
        md.append('--- BUG SHAPES (bug_shapes.json, full vendor) ---')
        md.append(json.dumps(BUGSHAPES[vendor], ensure_ascii=False, indent=1))
        md.append('')
        md.append('--- API TEMPLATE ---')
        md.append(fmt_api_template(seg))
        md.append('')
        md.append('=== END PACKET ===')
        open(os.path.join(out, did + '.md'), 'w', encoding='utf-8').write('\n'.join(md))

        # 结构化 JSON(实验期补 raw 后供分析)
        pkt = {
            'defect_id': did, 'vendor': vendor, 'version': version, 'defect_type': dtype,
            'raw_observation': COBS.get(did),
            'raw_full_pending': True,  # 实验期跑容器补全
            'contract_segment': seg,
            'source_excerpt': sx,
            'cognition': COGNITION[vendor],
            'bug_shapes': BUGSHAPES[vendor],
            'api_template': seg.get('api_template'),
        }
        json.dump(pkt, open(os.path.join(out, did + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        index.append({'defect_id': did, 'defect_type': dtype,
                      'contract_matched': len(seg.get('matched_constraints', [])),
                      'source_status': (sx or {}).get('status', 'missing'),
                      'raw_has_obs': bool(COBS.get(did))})

    json.dump(index, open(os.path.join(out, '_index.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    from collections import Counter
    print('packets:', len(index))
    print('source_status:', dict(Counter(p['source_status'] for p in index)))
    print('raw_has_obs: %d/%d' % (sum(p['raw_has_obs'] for p in index), len(index)))
    print('contract_matched 0:', sum(1 for p in index if p['contract_matched'] == 0))


if __name__ == '__main__':
    main()
