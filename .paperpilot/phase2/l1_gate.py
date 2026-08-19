#!/usr/bin/env python3
"""Phase 2 L1 机械 gate: 对 probe 输出做确定性预检(与新版 TestVDB 的机械 FP 过滤层对应).

规则(保守, 只标明确机械可判的):
- EXEC_FAILED: probe 未正常产出观察(server not ready / 全 EXCEPTION / TIMEOUT) -> 需重跑
- CONTRADICT: 观察与缺陷声称方向矛盾(声称"接受非法值"但所有 case 都被拒绝;
              或声称"错误地返回成功"但所有 case 都返回错误) -> 提示 GLM 注意
- OK: 其余(观察与声称一致或不可机械判定) -> 交 GLM 语义判定

输出: phase2/l1_verdicts_<short>.json

用法:
  py l1_gate.py --vendor milvus-io/milvus
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'output')
SPECS = {v: os.path.join(ROOT, f'probes-spec-{v}.json') for v in ['milvus', 'qdrant', 'weaviate']}
VENDOR_SHORT = {'milvus-io/milvus': 'milvus', 'qdrant/qdrant': 'qdrant', 'weaviate/weaviate': 'weaviate'}


def load_specs():
    by_num = {}
    for v, p in SPECS.items():
        for it in json.load(open(p, encoding='utf-8'))['items']:
            by_num[(v, it['number'])] = it
    return by_num


def parse_emits(log_path):
    """返回 emit 行列表."""
    if not os.path.exists(log_path):
        return None
    lines = []
    for line in open(log_path, encoding='utf-8', errors='replace'):
        line = line.strip()
        if line.startswith('{"case_id"'):
            try:
                lines.append(json.loads(line))
            except Exception:
                pass
    return lines


def claim_direction(spec):
    """声称方向: accepts(非法值被接受) / noerr(错误地返回成功) / unknown."""
    t = (spec.get('title') or '').lower()
    if re.search(r'accepts|silently|coerc|no validation|missing|without', t):
        return 'accepts'
    if re.search(r'returns (valid|code=0|success)|instead of (an )?error|code 0', t):
        return 'noerr'
    return 'unknown'


def case_rejected(e):
    """case 观察是否显示"被拒绝/报错"."""
    hs = e.get('http_status')
    if hs is not None and hs >= 400:
        return True
    rc = e.get('resp_code')
    if rc is not None and rc != 0:
        return True
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vendor', required=True, choices=list(VENDOR_SHORT))
    args = ap.parse_args()
    short = VENDOR_SHORT[args.vendor]
    specs = load_specs()
    summary = json.load(open(os.path.join(OUT, f'run_summary_{short}.json'), encoding='utf-8'))
    verdicts = {}
    for run in summary['runs']:
        num = run['number']
        key = (short, num)
        spec = specs.get(key, {})
        log = os.path.join(OUT, f'probe_{short}_{num}.log')
        emits = parse_emits(log)
        if run['status'] != 'OK' or emits is None:
            verdicts[num] = {'l1': 'EXEC_FAILED', 'note': 'run status %s' % run['status']}
            continue
        if not emits:
            verdicts[num] = {'l1': 'EXEC_FAILED', 'note': 'no emit lines'}
            continue
        # 观察汇总
        rejected = [case_rejected(e) for e in emits]
        all_rejected = all(rejected) if rejected else False
        obs = '; '.join(str(e.get('observation', ''))[:150] for e in emits[:6])
        direction = claim_direction(spec)
        note = f'cases={len(emits)} all_rejected={all_rejected} dir={direction} | {obs}'
        if direction in ('accepts', 'noerr') and all_rejected:
            verdicts[num] = {'l1': 'CONTRADICT', 'note': note}
        else:
            verdicts[num] = {'l1': 'OK', 'note': note}
    out_path = os.path.join(ROOT, f'l1_verdicts_{short}.json')
    json.dump(verdicts, open(out_path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    c = {}
    for v in verdicts.values():
        c[v['l1']] = c.get(v['l1'], 0) + 1
    print(f'{short}: {c} -> {out_path}')


if __name__ == '__main__':
    main()
