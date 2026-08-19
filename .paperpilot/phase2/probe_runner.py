#!/usr/bin/env python3
"""Phase 2 probe_runner: 按 manifest 批量执行 probe 脚本, 采集输出到 output_*.log.

用法:
  py probe_runner.py --vendor milvus-io/milvus [--numbers 52307,52310] [--timeout 180]

容器由外部编排起好(历史版本镜像), 脚本只连 localhost 端口。
输出: phase2/output/probe_<vendor>_<n>.log + exit code 记录在 phase2/output/run_summary.json
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(ROOT, 'probes')
OUT = os.path.join(ROOT, 'output')
MANIFEST = r'C:\Users\11428\Desktop\testvdb_paper\.paperpilot\phase1-raw\manifest.json'

VENDOR_SHORT = {'milvus-io/milvus': 'milvus', 'qdrant/qdrant': 'qdrant', 'weaviate/weaviate': 'weaviate'}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vendor', required=True, choices=list(VENDOR_SHORT))
    ap.add_argument('--numbers', help='逗号分隔的 issue 编号子集(默认全量)')
    ap.add_argument('--timeout', type=int, default=180)
    args = ap.parse_args()

    short = VENDOR_SHORT[args.vendor]
    os.makedirs(OUT, exist_ok=True)

    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    items = [m for m in manifest if m['repo'] == args.vendor]
    if args.numbers:
        want = {int(x) for x in args.numbers.split(',')}
        items = [m for m in items if m['number'] in want]

    probe_dir = os.path.join(PROBES, short)
    summary = {'vendor': args.vendor, 'runs': []}
    for it in items:
        num = it['number']
        script = os.path.join(probe_dir, f'probe_{short}_{num}.py')
        log = os.path.join(OUT, f'probe_{short}_{num}.log')
        if not os.path.exists(script):
            print(f'SKIP #{num}: no probe script ({it["gt_category"]})')
            summary['runs'].append({'number': num, 'status': 'NO_SCRIPT',
                                    'gt': it['gt_category'], 'version': it['reported_version']})
            continue
        print(f'RUN #{num} (v{it["reported_version"]}) ...', flush=True)
        try:
            r = subprocess.run([sys.executable, script], capture_output=True, text=True,
                               timeout=args.timeout, encoding='utf-8', errors='replace')
        except subprocess.TimeoutExpired:
            open(log, 'w', encoding='utf-8').write('TIMEOUT after %ds\n' % args.timeout)
            summary['runs'].append({'number': num, 'status': 'TIMEOUT',
                                    'gt': it['gt_category'], 'version': it['reported_version']})
            continue
        open(log, 'w', encoding='utf-8').write(r.stdout + '\n--- STDERR ---\n' + r.stderr)
        summary['runs'].append({'number': num, 'status': 'OK' if r.returncode == 0 else 'EXIT_%d' % r.returncode,
                                'gt': it['gt_category'], 'version': it['reported_version'],
                                'emit_lines': r.stdout.count('{"case_id"')})
        print(f'  exit={r.returncode} emits={r.stdout.count(chr(123)+chr(34)+"case_id")}')

    json.dump(summary, open(os.path.join(OUT, 'run_summary.json'), 'w', encoding='utf-8'),
              indent=2, ensure_ascii=False)
    ok = sum(1 for r in summary['runs'] if r['status'] == 'OK')
    print(f'\ndone: {ok}/{len(summary["runs"])} OK -> {OUT}')


if __name__ == '__main__':
    main()
