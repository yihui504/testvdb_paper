#!/usr/bin/env python3
"""Phase 2 实跑编排: 按 (vendor, version) 分组起历史版本容器, 顺序跑该组全部 probe.

用法:
  py orchestrate.py --vendor milvus-io/milvus [--versions 2.6.17,3.0.0]

流程(单 vendor):
  for version in 该 vendor 的版本组:
    确保镜像存在(pull)
    docker run 容器 -> wait health -> 跑该组 probe 脚本 -> docker rm -f
  写 output/run_summary_<short>.json(格式同 probe_runner)

L1 gate 随后由外部统一执行(每 vendor 一次, 输出 l1_verdicts_<short>.json)。
3 个 vendor 端口不冲突(milvus 19530 / qdrant 6333 / weaviate 8080), 可并行跑 3 个实例。
"""
import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PROBES = os.path.join(ROOT, 'probes')
OUT = os.path.join(ROOT, 'output')
MANIFEST = r'C:\Users\11428\Desktop\testvdb_paper\.paperpilot\phase1-raw\manifest.json'
VENDOR_SHORT = {'milvus-io/milvus': 'milvus', 'qdrant/qdrant': 'qdrant', 'weaviate/weaviate': 'weaviate'}

MILVUS_23_FALLBACK = 'v2.3.22'
IMAGE = {
    'milvus': lambda v: 'milvusdb/milvus:' + ('v' + v if not v.startswith('v') else v),
    'qdrant': lambda v: 'qdrant/qdrant:' + ('v' + v if not v.startswith('v') else v),
    'weaviate': lambda v: 'semitechnologies/weaviate:' + v,
}
HEALTH = {
    'milvus': 'http://localhost:9091/healthz',  # metrics 端口, 2.3~3.0 全有; 19530 在 2.3 无 REST
    'qdrant': 'http://localhost:6333/',
    # 8080 被用户 dify 环境的 weaviate 占用 -> host 端口 18080
    'weaviate': 'http://localhost:18080/v1/.well-known/ready',
}
# weaviate probe 通过 WEAVIATE_BASE 环境变量读 BASE(默认 8080)
PORT_MAP = {'milvus': ['-p', '19530:19530', '-p', '9091:9091'],
            'qdrant': ['-p', '6333:6333', '-p', '6334:6334'],
            'weaviate': ['-p', '18080:8080']}
CONTAINER = {'milvus': 'testvdb-milvus', 'qdrant': 'testvdb-qdrant', 'weaviate': 'testvdb-weaviate'}
MILVUS_NET = 'testvdb-net'
ETCD_NAME = 'testvdb-etcd'
MINIO_NAME = 'testvdb-minio'


def sh(cmd):
    """返回 (rc, stdout, stderr), 不退出."""
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def ensure_milvus_infra(fresh_etcd=True):
    """长驻 testvdb-net + etcd + minio; milvus 每版本 fresh etcd 防跨版本 metadata 冲突."""
    rc, out, _ = sh(['docker', 'network', 'inspect', MILVUS_NET])
    if rc != 0:
        sh(['docker', 'network', 'create', MILVUS_NET])
    if fresh_etcd:
        sh(['docker', 'rm', '-f', ETCD_NAME])
    rc, out, _ = sh(['docker', 'ps', '--format', '{{.Names}}'])
    if ETCD_NAME not in out:
        sh(['docker', 'run', '-d', '--name', ETCD_NAME, '--network', MILVUS_NET,
            '-e', 'ETCD_AUTO_COMPACTION_MODE=revision', '-e', 'ETCD_AUTO_COMPACTION_RETENTION=1000',
            '-e', 'ETCD_QUOTA_BACKEND_BYTES=4294967296', '-e', 'ETCD_SNAPSHOT_COUNT=50000',
            'quay.io/coreos/etcd:v3.5.5',
            'etcd', '-advertise-client-urls=http://127.0.0.1:2379',
            '-listen-client-urls', 'http://0.0.0.0:2379', '--data-dir', '/etcd'])
    if MINIO_NAME not in out:
        sh(['docker', 'run', '-d', '--name', MINIO_NAME, '--network', MILVUS_NET,
            '-e', 'MINIO_ACCESS_KEY=minioadmin', '-e', 'MINIO_SECRET_KEY=minioadmin',
            'minio/minio:RELEASE.2023-03-20T20-16-18Z',
            'minio', 'server', '/minio_data', '--console-address', ':9001'])
    time.sleep(6)


def start_container(short, version):
    name = CONTAINER[short]
    sh(['docker', 'rm', '-f', name])
    if short == 'milvus':
        # 实测配方 (v2.6.10, Docker Desktop): 外部 etcd+minio + DEPLOY_MODE=STANDALONE + ETCD_USE_EMBED=false
        ensure_milvus_infra()
        cmd = ['docker', 'run', '-d', '--name', name, '--network', MILVUS_NET, '-m', '4g',
               '-p', '19530:19530', '-p', '9091:9091',
               '-e', 'ETCD_USE_EMBED=false',
               '-e', 'ETCD_ENDPOINTS=%s:2379' % ETCD_NAME,
               '-e', 'MINIO_ADDRESS=%s:9000' % MINIO_NAME,
               '-e', 'DEPLOY_MODE=STANDALONE',
               IMAGE[short](version), 'milvus', 'run', 'standalone']
        return sh(cmd)
    cmd = ['docker', 'run', '-d', '--name', name] + PORT_MAP[short]
    if short == 'weaviate':
        cmd += ['-e', 'AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true',
                '-e', 'DEFAULT_VECTORIZER_MODULE=none',
                '-e', 'PERSISTENCE_DATA_PATH=/var/lib/weaviate']
    cmd.append(IMAGE[short](version))
    return sh(cmd)


def wait_health(short, tries=120, delay=5):
    url = HEALTH[short]
    for _ in range(tries):
        try:
            urllib.request.urlopen(url, timeout=2)
            print(f'    ready: {url}', flush=True)
            return True
        except Exception:
            time.sleep(delay)
    print(f'    WARN: not ready after {tries * delay}s', flush=True)
    return False


def run_probe(short, num, timeout=180):
    script = os.path.join(PROBES, short, f'probe_{short}_{num}.py')
    log = os.path.join(OUT, f'probe_{short}_{num}.log')
    print(f'  #{num} ...', flush=True)
    env = dict(os.environ)
    if short == 'weaviate':
        env['WEAVIATE_BASE'] = 'http://localhost:18080/v1'
    try:
        r = subprocess.run([sys.executable, script], capture_output=True, text=True,
                           timeout=timeout, encoding='utf-8', errors='replace', env=env)
    except subprocess.TimeoutExpired:
        open(log, 'w', encoding='utf-8').write(f'TIMEOUT after {timeout}s\n')
        print('    TIMEOUT', flush=True)
        return {'number': num, 'status': 'TIMEOUT'}
    open(log, 'w', encoding='utf-8').write(r.stdout + '\n--- STDERR ---\n' + r.stderr)
    status = 'OK' if r.returncode == 0 else f'EXIT_{r.returncode}'
    emits = r.stdout.count('{"case_id"')
    print(f'    exit={r.returncode} emits={emits}', flush=True)
    return {'number': num, 'status': status, 'emit_lines': emits}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vendor', required=True, choices=list(VENDOR_SHORT))
    ap.add_argument('--versions', help='逗号分隔版本子集(默认全量)')
    args = ap.parse_args()
    short = VENDOR_SHORT[args.vendor]
    os.makedirs(OUT, exist_ok=True)

    manifest = json.load(open(MANIFEST, encoding='utf-8'))
    groups = {}
    for it in manifest:
        if it['repo'] != args.vendor:
            continue
        if it['gt_category'] in ('SELF_PR_CLOSED', 'SELF_PR_OPEN'):
            continue
        v = it['reported_version']
        if v == '2.3':
            v = MILVUS_23_FALLBACK
        groups.setdefault(v, []).append(it)
    if args.versions:
        want = set(args.versions.split(','))
        groups = {v: g for v, g in groups.items() if v in want}

    summary = {'vendor': args.vendor, 'runs': []}
    total = sum(len(g) for g in groups.values())
    print(f'[{short}] {len(groups)} versions, {total} issues', flush=True)
    for version in sorted(groups):
        items = groups[version]
        print(f'[{short}] version {version}: {len(items)} issues', flush=True)

        # 确保镜像存在
        rc, out, err = sh(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'])
        if IMAGE[short](version) not in out:
            print(f'  pulling {IMAGE[short](version)} ...', flush=True)
            rc, out, err = sh(['docker', 'pull', IMAGE[short](version)])
            if rc != 0:
                print(f'  FAIL pull: {err[-300:]}', flush=True)
                for it in items:
                    summary['runs'].append({'number': it['number'], 'status': 'IMG_PULL_FAIL',
                                            'gt': it['gt_category'], 'version': it['reported_version']})
                continue

        rc, out, err = start_container(short, version)
        if rc != 0:
            print(f'  FAIL docker run: {err[-300:]}', flush=True)
            for it in items:
                summary['runs'].append({'number': it['number'], 'status': 'CONTAINER_FAIL',
                                        'gt': it['gt_category'], 'version': it['reported_version']})
            continue
        ready = wait_health(short)
        for it in items:
            rec = {'gt': it['gt_category'], 'version': it['reported_version']}
            rec.update(run_probe(short, it['number']))
            summary['runs'].append(rec)
        sh(['docker', 'rm', '-f', CONTAINER[short]])

    path = os.path.join(OUT, f'run_summary_{short}.json')
    json.dump(summary, open(path, 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
    ok = sum(1 for r in summary['runs'] if r['status'] == 'OK')
    print(f'[{short}] done: {ok}/{len(summary["runs"])} OK -> {path}', flush=True)


if __name__ == '__main__':
    main()
