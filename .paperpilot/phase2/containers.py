#!/usr/bin/env python3
"""Phase 2 历史版本容器编排: 起/停单个 VDBMS 容器.

用法:
  py containers.py start <vendor> <version>    # docker run + 等就绪
  py containers.py stop                        # docker rm -f 全部 testvdb 容器
  py containers.py list                        # 列出 manifest 需要的 (vendor, version) 矩阵

镜像 tag 约定:
  milvus    -> milvusdb/milvus:v<version>   (standalone embedded etcd)
  qdrant    -> qdrant/qdrant:v<version>
  weaviate  -> semitechnologies/weaviate:<version>
"""
import argparse
import json
import subprocess
import sys
import time

MANIFEST = r'C:\Users\11428\Desktop\testvdb_paper\.paperpilot\phase1-raw\manifest.json'

# v2.3 两条 issue 的小版本未知, 用 2.3 系列末尾 tag(实跑时若 pull 失败再调)
MILVUS_23_FALLBACK = 'v2.3.22'

PORTS = {'milvus': '19530', 'qdrant': '6333', 'weaviate': '8080'}
IMAGE = {
    'milvus': lambda v: 'milvusdb/milvus:' + v,
    'qdrant': lambda v: 'qdrant/qdrant:' + v,
    'weaviate': lambda v: 'semitechnologies/weaviate:' + v,
}
HEALTH = {
    'milvus': 'http://localhost:19530/healthz',
    'qdrant': 'http://localhost:6333/',
    'weaviate': 'http://localhost:8080/v1/.well-known/ready',
}


def sh(cmd, check=True):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if check and r.returncode != 0:
        print(r.stderr)
        sys.exit(r.returncode)
    return r.stdout


def version_matrix():
    m = json.load(open(MANIFEST, encoding='utf-8'))
    matrix = {}
    for it in m:
        if it['gt_category'] in ('SELF_PR_CLOSED', 'SELF_PR_OPEN'):
            continue
        v = it['reported_version']
        if v == '2.3':
            v = MILVUS_23_FALLBACK
        key = it['repo'].split('/')[1]
        matrix.setdefault((key, v), []).append(it['number'])
    return matrix


def cmd_start(short, version):
    if short == 'milvus':
        return ['docker', 'run', '-d', '--name', 'testvdb-milvus',
                '-p', '19530:19530', '-p', '9091:9091',
                '-e', 'ETCD_USE_EMBED=true',
                '-e', 'EMBEDDED_ETCD_PORT=23790',
                '-e', 'COMMON_STORAGETYPE=local',
                '--health-cmd', 'curl -f http://localhost:9091/healthz || exit 1',
                '--health-interval', '5s', '--health-retries', '24',
                IMAGE['milvus']('v' + version if not version.startswith('v') else version),
                'milvus', 'run', 'standalone']  # entrypoint 是 tini, 必须显式给 command
    if short == 'qdrant':
        return ['docker', 'run', '-d', '--name', 'testvdb-qdrant',
                '-p', '6333:6333', '-p', '6334:6334',
                IMAGE['qdrant']('v' + version if not version.startswith('v') else version)]
    if short == 'weaviate':
        return ['docker', 'run', '-d', '--name', 'testvdb-weaviate',
                '-p', '8080:8080',
                '-e', 'AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true',
                '-e', 'DEFAULT_VECTORIZER_MODULE=none',
                '-e', 'PERSISTENCE_DATA_PATH=/var/lib/weaviate',
                IMAGE['weaviate'](version)]


def wait_health(short, tries=120, delay=5):
    import urllib.request
    url = HEALTH[short]
    for _ in range(tries):
        try:
            urllib.request.urlopen(url, timeout=2)
            print('  ready:', url)
            return True
        except Exception:
            time.sleep(delay)
    print('  WARN: not ready after %ds' % (tries * delay))
    return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('action', choices=['start', 'stop', 'list'])
    ap.add_argument('vendor', nargs='?', choices=['milvus', 'qdrant', 'weaviate'])
    ap.add_argument('version', nargs='?')
    args = ap.parse_args()

    if args.action == 'list':
        matrix = version_matrix()
        print('(vendor, version) -> issues')
        for (v, ver), nums in sorted(matrix.items()):
            print(f'  {v:8} {ver:10} {len(nums):3} issues')
        return

    if args.action == 'stop':
        sh(['docker', 'rm', '-f', 'testvdb-milvus', 'testvdb-qdrant', 'testvdb-weaviate'], check=False)
        print('stopped')
        return

    sh(['docker', 'rm', '-f', f'testvdb-{args.vendor}'], check=False)
    cmd = cmd_start(args.vendor, args.version)
    print('$', ' '.join(cmd))
    out = sh(cmd)
    print(out.strip())
    wait_health(args.vendor)


if __name__ == '__main__':
    main()
