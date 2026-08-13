#!/usr/bin/env python3
"""Phase 2 rerun — 审计喂给 dev-reviewer 的信息有无问题（聚焦 24 flips）。

对每个 flip 查：
  1. output_*.log 是否非空、有无 setup 失败(create/load/index/drop 出 408/500/timeout)
  2. stage2 endpoint 标签 是否出现在实际 HTTP 流量路径里（错配=输入问题）
  3. req 数（0=SDK 探针无 raw，证据薄）
  4. dev 实际 review 的是不是真缺陷（看 rationale/files 是否对题）
输出每 flip 的输入健康判定：OK / ENDPOINT_MISMATCH / THIN(SDK无raw) / SETUP_FAILED / 等。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(ROOT, 'run')
ROWS = json.load(open(os.path.join(ROOT, 'analysis_rows.json'), encoding='utf-8'))
FLIPS = [r['did'] for r in ROWS if r.get('gt') and r['verdict'] != r['gt']]


def sess_of(did):
    v, num = did.split('_')
    # find version from cases_index
    ci = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
    e = next(x for x in ci if x['vendor'] == v and x['num'] == int(num))
    return os.path.join(RUN, 'results', v, e['version'], num), e


def parse_output(path):
    """返回 (req_count, distinct_paths, setup_errors)。"""
    if not os.path.isfile(path):
        return 0, [], ['NO_OUTPUT_LOG']
    txt = open(path, encoding='utf-8', errors='replace').read()
    if '[no raw HTTP captured]' in txt or not txt.strip():
        return 0, [], ['EMPTY']
    reqs = re.findall(r'=== REQ \d+ ===\n([A-Z]+) (http://[^\n]+)', txt)
    paths = []
    for m, url in reqs:
        p = url.split('localhost', 1)[-1]
        p = re.sub(r'/v[12]/vectordb/', '/', p)   # 归一 milvus /v2/vectordb
        p = re.sub(r'/v1(/.*)?', r'\1', p)         # 归一 weaviate /v1
        paths.append(p)
    distinct = sorted(set(paths))                  # 真实路径段(用于匹配)
    # setup 失败：create/load/index/drop 返回 408/500/timeout
    setup_err = []
    for kw in ('create', 'load', 'index', 'drop'):
        if re.search(r'=== REQ \d+ ===\n[A-Z]+ [^\n]*%s[^\n]*\n=== RESP[^\n]*\nstatus: (408|500|None)' % kw, txt, re.I):
            setup_err.append(kw + '_fail')
    return len(reqs), distinct, setup_err


def endpoint_in_traffic(ep, paths):
    """stage2 endpoint 标签是否匹配实际流量路径。"""
    if not ep:
        return 'NO_ENDPOINT_LABEL'
    toks = [t for t in re.split(r'[+/ ]', ep) if t and t not in ('{collection_name}', '{x}', 'POST', 'GET', 'PUT', 'DELETE', 'PATCH')]
    if not toks:
        return 'UNPARSEABLE'
    # 任一实际路径包含所有 token(顺序无关) 即算匹配
    for p in paths:
        pl = p.lower()
        if all(t.lower() in pl for t in toks):
            return 'MATCH'
    return 'MISMATCH'


def main():
    print('=== 输入审计: %d flips ===' % len(FLIPS))
    problems = []
    for did in FLIPS:
        sess, e = sess_of(did)
        agg = json.load(open(os.path.join(sess, 'debate_logs', 'stage2_aggregation.json'), encoding='utf-8'))
        ep = agg['confirmed'][did]['endpoint']
        nreq, paths, setup_err = parse_output(os.path.join(sess, 'output_%s.log' % did))
        align = endpoint_in_traffic(ep, paths)
        # 判定
        flags = []
        if setup_err:
            flags.append('SETUP_FAILED(%s)' % ','.join(setup_err))
        if nreq == 0:
            flags.append('THIN(SDK无raw)')
        if align == 'MISMATCH':
            flags.append('ENDPOINT_MISMATCH')
        if align == 'NO_ENDPOINT_LABEL':
            flags.append('NO_ENDPOINT')
        status = 'OK' if not flags else '⚠ ' + '|'.join(flags)
        if flags:
            problems.append(did)
        print('%-16s ep=%-28s reqs=%-3d align=%-9s %s' % (did, (ep or '')[:28], nreq, align, status))
        if flags:
            print('                   实际流量路径:', paths[:4])
    print('\n=== 输入有问题的 flips: %d / %d ===' % (len(problems), len(FLIPS)))
    print(problems)


if __name__ == '__main__':
    main()
