#!/usr/bin/env python3
"""build_arms_materials.py — 构造 single-LLM / voting 两臂专属实验包。

数据基座（全部来自已冻结材料，零 LLM 参与）：
- defect_id_map.json        序号 did -> (vendor, version, orig issue)
- packets/{orig}.json       contract_segment（契约段，含 doc_quote/source_url）+ raw_observation
- tvdb_sessions/sessions/…  output_*.log（probe 原始 HTTP 记录）+ stage2_aggregation.json（endpoint/defect_type）
- tvdb_sessions/…/structured_contract.json  版本级契约（endpoint 归一化后全量抽取该 case 约束）

两臂材料面（对齐 voting 阶段 judge 的本地可见面；不含源码/intelligence/活容器/网络）：
- single-LLM: 头部(did/endpoint/defect_type) + output log 全文 + 契约约束段(全量 endpoint 匹配 + packet 段)
- voting:     candidates/{did}.json + execution_results.json + raw_knowledge.md(来源表)

输出：
- arms/single_llm/materials/{did}.md      （71，内联材料）
- arms/single_llm/MANIFEST.json
- arms/voting/sessions/{vendor}/{version}/{did}/candidates/{did}.json   （71）
- arms/voting/sessions/{vendor}/{version}/{did}/debate_logs/execution_results.json
- arms/voting/sessions/{vendor}/{version}/raw_knowledge.md              （15 版本组）
- arms/voting/MANIFEST.json

泄露控制（audit_arms_materials.py 复核）：
- 不含 GT 标签 / group / gt_category / maintainer 表态 / related_issue_numbers
- 不含 packet 的 cognition / bug_shapes / source_excerpt（源码与 GT-informed 通道，仅 dev-reviewer 臂可见）
- 不含 issue 原文 title/body（packets 输入用的 issue 文本不进两臂包）
"""
import json
import os
import re
import sys
from collections import Counter

RERUN = r'c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun'
ARMS = os.path.join(RERUN, 'arms')
SESS = r'C:/Users/11428/Desktop/tvdb_sessions/sessions'

idmap = json.load(open(os.path.join(RERUN, 'defect_id_map.json'), encoding='utf-8'))


# ---------- endpoint 归一化（短名 vs 契约模板名） ----------

METHODS = frozenset({'get', 'post', 'put', 'delete', 'patch'})


def ep_tokens(ep):
    """把 endpoint 表达式切成 {路径 token 集, 方法集}，参数段({x})丢弃。"""
    if not ep:
        return frozenset(), frozenset()
    s = ep.lower().strip()
    s = re.sub(r'https?://[^/]+', '', s)          # 绝对 URL 只留路径
    parts = re.split(r'[+/\s]+', s)
    toks, meth = set(), set()
    for p in parts:
        p = p.strip()
        if not p or p.startswith('{'):
            continue
        if p in METHODS:
            meth.add(p)
        else:
            toks.add(p)
    return frozenset(toks), frozenset(meth)


def ep_match(a, b):
    """a/b 同一 endpoint 的判定：路径 token 互相包含（短名 ⊂ 模板名），
    方法集为空视为未指定（通配），否则需一致。"""
    ta, ma = ep_tokens(a)
    tb, mb = ep_tokens(b)
    if not ta or not tb:
        return False
    if ma and mb and ma != mb:
        return False
    return ta.issubset(tb) or tb.issubset(ta)


def endpoint_constraints(contract, ep):
    """契约中该 endpoint 的全部 constraints/assertions（机械匹配，全量不截断）。"""
    out = []
    for kind, lst in contract.get('constraints', {}).items():
        for c in lst if isinstance(lst, list) else []:
            if ep_match(ep, c.get('endpoint')):
                out.append(c)
    for a in contract.get('assertions', []) or []:
        if ep_match(ep, a.get('endpoint')):
            out.append(a)
    # 去重（constraint_id / assertion id）
    seen, uniq = set(), []
    for c in out:
        k = c.get('constraint_id') or c.get('assertion_id') or json.dumps(c, sort_keys=True)[:80]
        if k not in seen:
            seen.add(k)
            uniq.append(c)
    return uniq


# ---------- 材料清洗 ----------

CLEAN_KEYS_DROP = ('gt', 'group', 'gt_category', 'gt_label', 'related_issue_numbers',
                   'maintainer', 'by_design', 'FP_BY_DESIGN', 'should_report')


def clean_constraint(c):
    """契约约束条目：保留判定相关字段，丢弃来源状态类噪声。"""
    keep = ('constraint_id', 'assertion_id', 'endpoint', 'kind', 'type',
            'description', 'assertion', 'doc_quote', 'source_url', 'confidence')
    return {k: c[k] for k in keep if c.get(k) not in (None, '')}


# ---------- 构造 ----------

def load_case(did):
    m = idmap[did]
    sd = os.path.join(SESS, m['vendor'], m['version'], did)
    agg = json.load(open(os.path.join(sd, 'debate_logs', 'stage2_aggregation.json'), encoding='utf-8'))
    entry = agg.get('confirmed', {}).get(did) or agg.get('rejected', {}).get(did) or {}
    logs = sorted(f for f in os.listdir(sd) if f.startswith('output_') and f.endswith('.log'))
    log_text = open(os.path.join(sd, logs[0]), encoding='utf-8', errors='replace').read() if logs else ''
    packet = json.load(open(os.path.join(RERUN, 'packets', f"{m['orig']}.json"), encoding='utf-8'))
    contract = json.load(open(os.path.join(SESS, m['vendor'], m['version'], 'structured_contract.json'), encoding='utf-8'))
    return {
        'did': did, 'vendor': m['vendor'], 'version': m['version'], 'orig': m['orig'],
        'endpoint': entry.get('endpoint'), 'defect_type': entry.get('defect_type'),
        'severity_level': entry.get('severity_level'),
        'log_file': logs[0] if logs else None, 'log_text': log_text,
        'packet': packet, 'contract': contract,
    }


def contract_section(case):
    """该 case 的 expected 依据 = 契约全量匹配约束 + packet 契约段(关键词 top-k)。

    两来源都给：全量匹配是 dev-reviewer 视角（完整契约文件），
    packet 段是 build_contract_segments 的定位产物；含 no_match 标记。"""
    seg = case['packet'].get('contract_segment') or {}
    cons = endpoint_constraints(case['contract'], case['endpoint'])
    lines = []
    if cons:
        lines.append(f"约束条目（{len(cons)} 条，来自 {case['vendor']} {case['version']} 契约，endpoint={case['endpoint']}）：")
        for c in cons:
            lines.append(json.dumps(clean_constraint(c), ensure_ascii=False))
    else:
        lines.append(f"[契约中无 endpoint={case['endpoint']} 的约束条目]")
    mc = seg.get('matched_constraints') or []
    if mc:
        lines.append(f"\n相关契约段（关键词定位 {len(mc)} 条）：")
        for c in mc:
            lines.append(json.dumps(clean_constraint(c), ensure_ascii=False))
    at = seg.get('api_template') or case['packet'].get('api_template') or {}
    if isinstance(at, dict) and (at.get('endpoint') or at.get('doc_quote')):
        lines.append(f"\nAPI 模板：endpoint={at.get('endpoint')} doc_quote={at.get('doc_quote')!r} source={at.get('source_url')}")
    return '\n'.join(lines), len(cons), len(mc)


def observed_section(case):
    raw = case['packet'].get('raw_observation')
    parts = []
    if raw:
        parts.append("观察摘要（probe 产出）：")
        parts.extend(f"- {line}" for line in raw)
    if case['log_text'] and case['log_text'].strip() != '[no raw HTTP captured]':
        parts.append(f"\n执行日志全文（{case['log_file']}）：")
        parts.append(case['log_text'])
    elif not raw:
        parts.append("[无可用观察记录：raw 为空且 log 未捕获（milvus_001 特例，探针未记录原始 HTTP）]")
    return '\n'.join(parts)


def build_single_llm(case, cons_n, seg_n):
    md = []
    md.append(f"=== 候选缺陷 {case['did']} ===")
    md.append(f"[vendor={case['vendor']} version={case['version']} defect_type={case['defect_type']} endpoint={case['endpoint']}]")
    md.append("")
    md.append("--- 观察到的行为（observed） ---")
    md.append(observed_section(case))
    md.append("")
    md.append("--- 契约依据（expected，来自该版本 API 契约） ---")
    sec, _, _ = contract_section(case)
    md.append(sec)
    return '\n'.join(md) + '\n'


def build_voting_files(case, cons_n, seg_n):
    """voting 臂：candidates/{did}.json（judge 输入）+ execution_results.json（log 汇总）。"""
    cand = {
        'defect_id': case['did'],
        'endpoint': case['endpoint'],
        'defect_type': case['defect_type'],
        'expected': {
            'contract_constraints': [clean_constraint(c) for c in endpoint_constraints(case['contract'], case['endpoint'])],
            'keyword_matched_segment': [clean_constraint(c) for c in (case['packet'].get('contract_segment') or {}).get('matched_constraints') or []],
            'api_template': case['packet'].get('api_template'),
        },
        'observed': {
            'raw_observation': case['packet'].get('raw_observation'),
            'log_file': case['log_file'],
        },
        'metadata': {'vendor': case['vendor'], 'version': case['version']},
    }
    execr = {
        'execution_summary': {
            'total_scripts': 1,
            'logs': [{'defect_id': case['did'], 'log_file': case['log_file'],
                      'captured_raw_http': bool(case['log_text'] and case['log_text'].strip() != '[no raw HTTP captured]')}],
        },
        'log_contents': {case['did']: case['log_text']},
    }
    return cand, execr


def build_raw_knowledge(vendor, version, contract):
    """judge-doc 的 Document Sources 表：契约 source_url 汇总（机械生成，无原文抓取）。"""
    urls = {}
    for kind, lst in contract.get('constraints', {}).items():
        for c in lst if isinstance(lst, list) else []:
            u = c.get('source_url')
            if u:
                urls.setdefault(u, {'endpoint': c.get('endpoint'), 'constraint_id': c.get('constraint_id')})
    lines = [f"# Document Sources — {vendor} {version}", '',
             '| source_url | endpoint | first constraint |', '|---|---|---|']
    for u, info in sorted(urls.items()):
        lines.append(f"| {u} | {info['endpoint']} | {info['constraint_id']} |")
    return '\n'.join(lines) + '\n', len(urls)


def main():
    manifest = {'single_llm': [], 'voting': []}
    zero_contract, seg_counts = [], Counter()
    for did in sorted(idmap):
        case = load_case(did)
        sec, cons_n, seg_n = contract_section(case)
        seg_counts[seg_n] += 1
        if cons_n == 0 and seg_n == 0:
            zero_contract.append(did)

        # single-LLM
        sl_dir = os.path.join(ARMS, 'single_llm', 'materials')
        os.makedirs(sl_dir, exist_ok=True)
        open(os.path.join(sl_dir, f'{did}.md'), 'w', encoding='utf-8').write(build_single_llm(case, cons_n, seg_n))
        manifest['single_llm'].append({'did': did, 'vendor': case['vendor'], 'version': case['version'],
                                       'contract_constraints': cons_n, 'segment_constraints': seg_n,
                                       'log_chars': len(case['log_text'])})

        # voting
        vd = os.path.join(ARMS, 'voting', 'sessions', case['vendor'], case['version'], did)
        os.makedirs(os.path.join(vd, 'candidates'), exist_ok=True)
        os.makedirs(os.path.join(vd, 'debate_logs'), exist_ok=True)
        cand, execr = build_voting_files(case, cons_n, seg_n)
        open(os.path.join(vd, 'candidates', f'{did}.json'), 'w', encoding='utf-8').write(
            json.dumps(cand, ensure_ascii=False, indent=1))
        open(os.path.join(vd, 'debate_logs', 'execution_results.json'), 'w', encoding='utf-8').write(
            json.dumps(execr, ensure_ascii=False, indent=1))
        manifest['voting'].append({'did': did, 'candidates_json': f"{case['vendor']}/{case['version']}/{did}/candidates/{did}.json"})

    # raw_knowledge per version group
    rk_report = {}
    done = set()
    for did, m in sorted(idmap.items()):
        key = (m['vendor'], m['version'])
        if key in done:
            continue
        done.add(key)
        contract = json.load(open(os.path.join(SESS, m['vendor'], m['version'], 'structured_contract.json'), encoding='utf-8'))
        md, n = build_raw_knowledge(m['vendor'], m['version'], contract)
        p = os.path.join(ARMS, 'voting', 'sessions', m['vendor'], m['version'], 'raw_knowledge.md')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, 'w', encoding='utf-8').write(md)
        rk_report[f"{m['vendor']}/{m['version']}"] = n

    manifest['summary'] = {
        'n_cases': len(idmap),
        'segment_constraint_dist': dict(sorted(seg_counts.items())),
        'zero_contract_and_segment': zero_contract,
        'raw_knowledge_urls': rk_report,
        'leak_controls': [
            'no gt/group/gt_category fields', 'no related_issue_numbers',
            'no packet cognition/bug_shapes/source_excerpt',
            'no issue title/body text', 'no intelligence files', 'no source clone paths',
        ],
    }
    json.dump(manifest, open(os.path.join(ARMS, 'MANIFEST.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(f"single_llm materials: {len(manifest['single_llm'])}")
    print(f"voting candidates: {len(manifest['voting'])}")
    print(f"raw_knowledge: {len(rk_report)} version groups, urls: {rk_report}")
    print(f"zero contract+segment (no expected basis): {len(zero_contract)} {zero_contract}")
    print(f"segment dist: {dict(sorted(seg_counts.items()))}")


if __name__ == '__main__':
    sys.exit(main())
