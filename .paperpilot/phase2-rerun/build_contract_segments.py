#!/usr/bin/env python3
"""Phase 2 rerun — 抽取每 case 的相关契约段 + api_template(Phase 2.1 + 2.2 自动化)。

对 71 scored case,用 title + issue body + round1 rationale 提关键词,
在对应版本契约(missing 版本用 version_map 派生到最近版本)的 constraints/assertions/
endpoint_registry 里匹配,取 top 相关约束 + endpoint 模板,写 contracts/segments/{vendor}_{num}.json。

匹配用于**定位**契约原文(放进 packet 的是契约文本本身,不是 rationale)。
未命中 -> segment 标 no_contract_match,judge 视为 verdict_A=NEUTRAL。
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTRACTS = os.path.join(ROOT, 'contracts')
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
VMAP = json.load(open(os.path.join(CONTRACTS, 'version_map.json'), encoding='utf-8'))

# round1 rationale(仅用于关键词,不进 packet)
RATIONALE = {}
for short in ('milvus', 'qdrant', 'weaviate'):
    p = os.path.join(os.path.dirname(ROOT), 'phase2', f'round1_{short}.tsv')
    if not os.path.exists(p):
        continue
    for line in open(p, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 4:
            RATIONALE['%s_%s' % (short, parts[1])] = parts[3]

STOP = set('''a an the of to in on for and or with without is are be been was were not no
           by as at from that this it its if then else must should may can will into via per
           missing validation accepts rejected returns returned accepted violates violation
           documented doc docs documentation value values parameter params param field fields
           bug defect issue feature request response status code http rest grpc sdk collection
           collections search query insert upsert delete create drop describe index payload
           data result results count offset filter vector vectors schema name type
           integer string number positive negative default silent silently normal normalized
           while which same across reported claim reproduction reproduced
           is it in on or to do no be an as at by of if id ip'''.split())


def keywords(*texts):
    toks = set()
    for t in texts:
        if not t:
            continue
        for m in re.findall(r'[A-Za-z_][A-Za-z0-9_]{1,}', t):
            w = m.lower()
            if len(w) >= 2 and w not in STOP:
                toks.add(w)
        # camelCase split + snake_case parts
        for m in re.findall(r'[a-z]+(?:[A-Z][a-z]+)+', t):
            toks.add(m.lower())
    return toks


def flatten_constraints(contract):
    """返回 [(kind, item), ...], item 含 constraint_id/endpoint/description/assertion-text/source_url/doc_quote。"""
    out = []
    c = contract.get('constraints', {})
    for cat in ('type_constraints', 'range_constraints', 'state_constraints'):
        for it in c.get(cat, []):
            out.append((cat, it))
    for it in contract.get('assertions', []):
        out.append(('assertion', it))
    return out


def ctext(item):
    parts = [cid(item), item.get('description', ''), item.get('assertion', '') or item.get('expr', '') or '',
             item.get('doc_quote', '') or '', item.get('endpoint', '') or '',
             item.get('expected_behavior', '') or '']
    return ' '.join(p or '' for p in parts)


def cid(item):
    return item.get('constraint_id') or item.get('assertion_id') or item.get('invariant_id') or item.get('contract_id') or '?'


def match_endpoint(endpoint_registry, kws):
    best, bestscore = None, 0
    for ep in endpoint_registry:
        text = (ep.get('path', '') + ' ' + ep.get('method', '') + ' ' + ep.get('description', '') + ' ' + (ep.get('doc_quote', '') or '')).lower()
        sc = len(kws & set(re.findall(r'[a-z0-9_]+', text)))
        if sc > bestscore:
            best, bestscore = ep, sc
    return best, bestscore


def main():
    seg_dir = os.path.join(CONTRACTS, 'segments')
    os.makedirs(seg_dir, exist_ok=True)
    coverage = []
    cache = {}

    def load_contract(vendor, version):
        vm = VMAP[vendor][version]
        f = vm['file']
        key = (vendor, f)
        if key not in cache:
            cache[key] = json.load(open(os.path.join(CONTRACTS, vendor, f + '.json'), encoding='utf-8'))
        return cache[key], vm

    scored = [c for c in CASES if c['group'] in ('A', 'B', 'C')]
    for case in scored:
        vendor = case['vendor']
        num = case['num']
        version = case['version']
        did = '%s_%s' % (vendor, num)
        contract, vm = load_contract(vendor, version)
        kws = keywords(case.get('title'), case.get('body'), RATIONALE.get(did))
        cons = flatten_constraints(contract)
        scored_cons = []
        for kind, it in cons:
            atext = ((it.get('assertion') or it.get('expr') or '') + ' ' + cid(it)).lower()
            dtext = ((it.get('description') or '') + ' ' + (it.get('doc_quote') or '') + ' ' + (it.get('endpoint') or '')).lower()
            aw = set(re.findall(r'[a-z0-9_]+', atext))
            dw = set(re.findall(r'[a-z0-9_]+', dtext))
            a_sc = len(kws & aw)   # 参数名出现在 assertion/expr/id 里 = 强信号
            d_sc = len(kws & dw)   # 仅 description/doc_quote 共现 = 弱信号
            if a_sc >= 1 or d_sc >= 2:
                scored_cons.append((a_sc * 3 + d_sc, kind, it))
        scored_cons.sort(key=lambda x: -x[0])
        top = scored_cons[:4]
        ep, epscore = match_endpoint(contract.get('endpoint_registry', []), kws)
        seg = {
            'defect_id': did,
            'vendor': vendor,
            'version': version,
            'contract_file': vm['file'],
            'derived': vm['derived'],
            'derived_note': vm.get('note'),
            'keywords_used': sorted(kws)[:25],
            'matched_constraints': [
                {'score': sc, 'kind': kind, 'id': cid(it),
                 'endpoint': it.get('endpoint'), 'assertion': it.get('assertion') or it.get('expr'),
                 'description': it.get('description'), 'doc_quote': it.get('doc_quote'),
                 'source_url': it.get('source_url'), 'confidence': it.get('confidence'),
                 'evidence_tier': it.get('evidence_tier')}
                for sc, kind, it in top
            ],
            'api_template': {'endpoint': ep.get('path') if ep else None,
                             'method': ep.get('method') if ep else None,
                             'description': ep.get('description') if ep else None,
                             'doc_quote': ep.get('doc_quote') if ep else None,
                             'match_score': epscore} if ep else None,
        }
        json.dump(seg, open(os.path.join(seg_dir, did + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        coverage.append({'defect_id': did, 'n_kw': len(kws), 'n_matched': len(top),
                         'top_score': top[0][0] if top else 0, 'endpoint_score': epscore,
                         'derived': vm['derived']})

    json.dump(coverage, open(os.path.join(seg_dir, '_coverage.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    n_total = len(coverage)
    n_match = sum(1 for c in coverage if c['n_matched'] > 0)
    n_ep = sum(1 for c in coverage if c['endpoint_score'] > 0)
    n_nomatch = [c['defect_id'] for c in coverage if c['n_matched'] == 0]
    print('cases: %d | contract-matched: %d (%.0f%%) | endpoint-matched: %d | no-contract-match: %d' %
          (n_total, n_match, 100 * n_match / n_total, n_ep, len(n_nomatch)))
    print('no-contract-match:', n_nomatch)
    weak = [c['defect_id'] for c in coverage if c['n_matched'] > 0 and c['top_score'] <= 1]
    print('weak(top_score<=1):', weak)


if __name__ == '__main__':
    main()
