#!/usr/bin/env python3
"""Phase 2 rerun — 审计喂的源码版本对不对得上 case 版本。

对每 case:
  1. expected tag (tag_for)
  2. .srcdir 指的 clone 路径（layout_inputs 写的，应正确）
  3. dev_review.json 里 source_grounding.local_clone（agent 实际 ground 的版本）
  4. dev_review.json 里 source_grounding.files_examined 首个路径（侧面印证 agent 读了哪个 clone）
flag: .srcdir 错 / agent local_clone 版本 != case 版本。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.join(ROOT, 'run')
CI = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def main():
    print('=== 源码版本审计 (全部 71) ===')
    bad_srcdir = []
    bad_agent = []
    for e in CI:
        if e['group'] not in ('A', 'B', 'C'):
            continue
        v, num, ver = e['vendor'], e['num'], e['version']
        did = '%s_%s' % (v, num)
        sess = os.path.join(RUN, 'results', v, ver, str(num))
        exp_tag = tag_for(v, ver)
        # .srcdir
        srcdir = open(os.path.join(sess, '.srcdir'), encoding='utf-8').read().strip() if os.path.isfile(os.path.join(sess, '.srcdir')) else ''
        srcdir_tag = srcdir.split('/')[-1] if srcdir else ''
        srcdir_ok = (srcdir_tag == exp_tag)
        if not srcdir_ok:
            bad_srcdir.append(did)
        # agent local_clone
        dr = os.path.join(sess, 'debate_logs', 'dev_review.json')
        agent_tag = ''
        if os.path.isfile(dr):
            try:
                d = json.load(open(dr, encoding='utf-8'))
                sg = d['verdicts'][0].get('steps', {}).get('source_grounding', {}) or d['verdicts'][0].get('source_grounding', {})
                lc = sg.get('local_clone', '') or ''
                m = re.search(r'(v?\d+\.\d+(?:\.\d+)?)', lc)
                agent_tag = m.group(1) if m else ''
            except Exception:
                pass
        agent_ok = (not agent_tag) or (agent_tag.lstrip('v') == exp_tag.lstrip('v'))
        if not agent_ok:
            bad_agent.append((did, exp_tag, agent_tag))
        flag = '' if (srcdir_ok and agent_ok) else '⚠'
        if flag:
            print('%-16s ver=%-8s exp_tag=%-9s | .srcdir→%-9s(%s) agent→%-9s(%s) %s' % (
                did, ver, exp_tag, srcdir_tag, 'ok' if srcdir_ok else 'BAD', agent_tag or '?', 'ok' if agent_ok else 'BAD', flag))
    print('\n.srcdir 错的:', bad_srcdir or 'NONE')
    print('agent ground 版本错的:', bad_agent or 'NONE')
    print('\n注: agent_tag 从 dev_review.json 的 local_clone 字段提取; 空表示 agent 没记 local_clone(无法判定, 不算错)。')


if __name__ == '__main__':
    main()
