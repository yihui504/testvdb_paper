#!/usr/bin/env python3
"""Phase 2 GLM verdict prompt 生成器.

为每条 candidate 生成判定 prompt(phase2/glm-prompts/<vendor>_<n>.md)。
GLM5.2 语义判定环节: 用户将 Claude Code 模型切到 GLM5.2 后, 按批次读取 prompt 执行判定,
verdict 记录到 phase2/glm_verdicts.json。

用法:
  py gen_glm_prompts.py --vendor qdrant/qdrant [--numbers 9017,9039]
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
PROMPTS = os.path.join(ROOT, 'glm-prompts')
OUT = os.path.join(ROOT, 'output')
MANIFEST = r'C:\Users\11428\Desktop\testvdb_paper\.paperpilot\phase1-raw\manifest.json'

# Threat-2 fix: per-probe cleaned observations (factual only, verdict language
# removed). Preferred over raw probe logs when the "{vendor}_{num}" key exists.
CLEAN_OBS_PATH = os.path.join(ROOT, 'clean_observations.json')
CLEAN_OBS = {}
if os.path.exists(CLEAN_OBS_PATH):
    try:
        _co = json.load(open(CLEAN_OBS_PATH, encoding='utf-8'))
        CLEAN_OBS = {k: v for k, v in _co.items() if not k.startswith('_')}
    except (OSError, json.JSONDecodeError):
        CLEAN_OBS = {}
VENDOR_SHORT = {'milvus-io/milvus': 'milvus', 'qdrant/qdrant': 'qdrant', 'weaviate/weaviate': 'weaviate'}

JUDGE_INSTRUCTION = """You are the semantic judgment stage of TestVDB, a documentation-implementation defect detector for vector database management systems (VDBMS).

A candidate defect was reported against the VDBMS below. The evidence was collected by re-probing the reported behavior on the DB version where it was originally reported. Decide whether the observed behavior constitutes a real defect.

Judge strictly against DOCUMENTED CONTRACT and INTERNAL CONSISTENCY, not general opinions:
- CONFIRMED: the observation violates the documented contract, or shows internal inconsistency (e.g. the REST path accepts what the gRPC path rejects for the same input; documented limits/validation are silently ignored; data is silently corrupted or mis-stored; a documented error contract returns success).
- FALSE_POSITIVE: the behavior is reasonable by design, the documentation does not promise what the report claims, the observation does not actually contradict the contract, or the claim cannot be substantiated from the evidence.

Respond with STRICT JSON only, no other text:
{"verdict": "CONFIRMED" or "FALSE_POSITIVE", "rationale": "one or two sentences citing the specific contract or inconsistency"}

--- CANDIDATE EVIDENCE ---
"""


def load_log(short, num):
    p = os.path.join(OUT, f'probe_{short}_{num}.log')
    if not os.path.exists(p):
        return '(no probe log)'
    txt = open(p, encoding='utf-8', errors='replace').read()
    lines = []
    for line in txt.split('\n'):
        if line.startswith('{"case_id"'):
            try:
                e = json.loads(line)
                obs = e.get('observation') or e.get('obs') or ''
                lines.append(f'  [{e["case_id"]}] {obs}'
                             + (f' (http_status={e["http_status"]})' if 'http_status' in e else ''))
            except Exception:
                pass
    return '\n'.join(lines[:12]) if lines else '(no emit lines)'


def sanitize(text):
    """去掉 spec 文本里的 GT 泄漏(盲测要求): 括号 GT 标注、dup 前缀、维护者归因."""
    if not text:
        return text
    # "(GT is ...)" / "(GT=...)" 括号标注
    text = re.sub(r'\(GT[^)]*\)', '', text)
    # 维护者归因短语(保留其前后事实陈述)
    text = re.sub(r'[;,]\s*maintainers?\s+@?\w*\s*(?:confirmed|accepted|said|noted|labeled)[^.;]*[.]?', '', text)
    # 句子级泄漏: 含 GT/by-design/labeled/maintainer 的整句
    keep = []
    for sent in re.split(r'(?<=[.!?])\s+', text):
        low = sent.lower()
        if re.search(r'\bgt\b|by[ _-]design|labeled|labelled|maintainer', low):
            continue
        keep.append(sent)
    text = ' '.join(keep)
    # dup 前缀: "Duplicate of #123; " / "TP_FIXED_PR duplicate of #123; "
    text = re.sub(r'^(?:\w+\s+)?[Dd]uplicate of #\d+[.;]\s*', '', text)
    # 残留的 "marked BY_DESIGN" 尾巴
    text = re.sub(r'[;,]\s*marked BY_DESIGN\.?', '', text)
    return text.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vendor', required=True, choices=list(VENDOR_SHORT))
    ap.add_argument('--numbers', help='逗号分隔子集')
    args = ap.parse_args()
    short = VENDOR_SHORT[args.vendor]
    os.makedirs(PROMPTS, exist_ok=True)

    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    specs = json.load(open(os.path.join(ROOT, f'probes-spec-{short}.json'), encoding='utf-8'))
    spec_by_num = {it['number']: it for it in specs['items']}
    l1_path = os.path.join(ROOT, f'l1_verdicts_{short}.json')
    l1 = json.load(open(l1_path, encoding='utf-8')) if os.path.exists(l1_path) else {}

    items = [m for m in manifest if m['repo'] == args.vendor]
    if args.numbers:
        want = {int(x) for x in args.numbers.split(',')}
        items = [m for m in items if m['number'] in want]

    generated = []
    for it in items:
        num = it['number']
        spec = spec_by_num.get(num, {})
        if spec.get('needs_manual') and num not in (47635, 47636):  # PR 不判定
            if num in (47785, 51809):
                continue
        if it['gt_category'] in ('SELF_PR_CLOSED', 'SELF_PR_OPEN'):
            continue  # 自提 PR 不跑判定
        co = CLEAN_OBS.get(f'{short}_{num}')
        if co:
            obs = '\n'.join('  ' + line for line in co)
        else:
            obs = load_log(short, num)
        l1n = l1.get(str(num), {}).get('l1', '-')
        prompt = JUDGE_INSTRUCTION + f"""Repo: {it['repo']}
Issue number: #{num}
Reported DB version: {it['reported_version']}
Title: {it['title']}
Contract claimed in the report: {sanitize(spec.get('contract_hint', ''))}
Probe observations:
{obs}
L1 mechanical note: {l1n}
"""
        fn = os.path.join(PROMPTS, f'{short}_{num}.md')
        open(fn, 'w', encoding='utf-8').write(prompt)
        generated.append(num)
    print(f'{args.vendor}: {len(generated)} prompts -> {PROMPTS}')
    print('batch plan: 每轮 GLM 会话处理 ~20 条, 输出 JSON 追加到 glm_verdicts.json')


if __name__ == '__main__':
    main()
