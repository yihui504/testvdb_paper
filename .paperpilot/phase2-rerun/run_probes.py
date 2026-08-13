#!/usr/bin/env python3
"""Phase 2 rerun — 跑指定 (vendor, version) 的所有 scored probe，生成 output_*.log 入 session。

起容器(复用 orchestrate 逻辑) → wait health → 对该版本每 case 跑探针(RAW_LOG_DIR+PROBE_ID
触发 probe_common 抓 raw HTTP) → 从 raw log 生成可读 output_{defect_id}.log 入 session。
容器保持运行(供随后派 dev-reviewer 复现/证伪)，末尾打印容器名供清理。

用法: python run_probes.py <vendor> <version>
"""
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
PHASE2 = os.path.join(os.path.dirname(ROOT), 'phase2')
sys.path.insert(0, PHASE2)
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))
RUN = os.path.join(ROOT, 'run')

IMAGE = {'milvus': lambda v: 'milvusdb/milvus:' + ('v' + v if not v.startswith('v') else v),
         'qdrant': lambda v: 'qdrant/qdrant:' + ('v' + v if not v.startswith('v') else v),
         'weaviate': lambda v: 'semitechnologies/weaviate:' + v}
HEALTH = {'milvus': 'http://localhost:9091/healthz', 'qdrant': 'http://localhost:6333/',
          'weaviate': 'http://localhost:18080/v1/.well-known/ready'}


def sh(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def wait_health(vendor, tries=60, delay=3):
    import urllib.request
    for _ in range(tries):
        try:
            urllib.request.urlopen(HEALTH[vendor], timeout=3); return True
        except Exception:
            time.sleep(delay)
    return False


def start_container(vendor, version):
    import orchestrate as orch
    sh(['docker', 'rm', '-f', orch.CONTAINER[vendor]])
    if vendor == 'milvus':
        imgver = '2.3.22' if version == '2.3' else version  # 2.3 用 v2.3.22 镜像
        orch.ensure_milvus_infra()
        return orch.start_container('milvus', imgver)
    if vendor == 'qdrant':
        return sh(['docker', 'run', '-d', '--name', 'testvdb-qdrant', '-p', '6333:6333', '-p', '6334:6334',
                   IMAGE['qdrant'](version)])
    if vendor == 'weaviate':
        return sh(['docker', 'run', '-d', '--name', 'testvdb-weaviate', '-p', '18080:8080',
                   '-e', 'AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true',
                   '-e', 'DEFAULT_VECTORIZER_MODULE=none', '-e', 'PERSISTENCE_DATA_PATH=/var/lib/weaviate',
                   IMAGE['weaviate'](version)])


def gen_output_log(raw_log, out_log):
    if not os.path.exists(raw_log):
        open(out_log, 'w', encoding='utf-8').write('[no raw HTTP captured]\n'); return 0
    n = 0
    with open(out_log, 'w', encoding='utf-8') as f:
        for i, ln in enumerate(open(raw_log, encoding='utf-8').read().splitlines(), 1):
            try:
                r = json.loads(ln)
            except Exception:
                continue
            if r.get('kind') != 'http':
                continue
            n += 1
            f.write('=== REQ %d ===\n%s %s\n' % (i, r.get('method'), r.get('url')))
            if r.get('payload') is not None:
                f.write('payload: %s\n' % json.dumps(r['payload'], ensure_ascii=False))
            f.write('=== RESP %d ===\nstatus: %s\nbody: %s\n\n' % (i, r.get('status'), r.get('resp_body', '')))
    return n


def main():
    vendor, version = sys.argv[1], sys.argv[2]
    cases = [c for c in CASES if c['vendor'] == vendor and c['version'] == version and c['group'] in ('A', 'B', 'C')]
    print('[%s %s] %d scored cases' % (vendor, version, len(cases)))
    rc, _, err = start_container(vendor, version)
    if rc != 0:
        print('  CONTAINER FAIL:', err[-200:]); sys.exit(1)
    if not wait_health(vendor):
        print('  HEALTH FAIL'); sys.exit(1)
    print('  container ready')
    probe_dir = os.path.join(PHASE2, 'probes', vendor)
    report = []
    for c in cases:
        num = c['num']; did = '%s_%s' % (vendor, num)
        sess = os.path.join(RUN, 'results', vendor, version, str(num))
        probe = os.path.join(probe_dir, 'probe_%s.py' % did)
        env = dict(os.environ, RAW_LOG_DIR=sess, PROBE_ID=did, PYTHONIOENCODING='utf-8')
        if vendor == 'weaviate':
            env['WEAVIATE_BASE'] = 'http://localhost:18080/v1'
        try:
            r = subprocess.run([sys.executable, probe], capture_output=True, text=True,
                               timeout=180, cwd=probe_dir, env=env, errors='replace')
            status = 'OK' if r.returncode == 0 else 'EXIT_%d' % r.returncode
        except subprocess.TimeoutExpired:
            status = 'TIMEOUT'
            r = None
        raw_log = os.path.join(sess, 'raw_%s.log' % did)
        out_log = os.path.join(sess, 'output_%s.log' % did)
        nreq = gen_output_log(raw_log, out_log)
        report.append((did, status, nreq))
        print('  #%s %s reqs=%d' % (num, status, nreq), flush=True)
    print('=== container left up: testvdb-%s ===' % vendor)
    print(json.dumps(report))


if __name__ == '__main__':
    main()
