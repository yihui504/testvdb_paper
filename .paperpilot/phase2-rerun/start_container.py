#!/usr/bin/env python3
"""为 run-2/run-3 起指定 (vendor, version) 的容器（不跑探针，不覆盖 output_*.log），等健康。

供 active-mode dev-reviewer 复现/证伪用。容器名固定 testvdb-<vendor>（同版本复用）。
用法: python start_container.py <vendor> <version>
"""
import os
import sys
import time
import urllib.request

PHASE2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'phase2')
sys.path.insert(0, PHASE2)
import orchestrate as orch  # noqa: E402

HEALTH = {'milvus': 'http://localhost:9091/healthz',
          'qdrant': 'http://localhost:6333/',
          'weaviate': 'http://localhost:18080/v1/.well-known/ready'}


def wait_health(vendor, tries=120, delay=5):
    for i in range(tries):
        try:
            urllib.request.urlopen(HEALTH[vendor], timeout=3)
            print('ready: %s' % HEALTH[vendor], flush=True)
            return True
        except Exception:
            time.sleep(delay)
    print('WARN: not ready after %ds' % (tries * delay), flush=True)
    return False


def main():
    vendor, version = sys.argv[1], sys.argv[2]
    imgver = '2.3.22' if (vendor == 'milvus' and version == '2.3') else version
    rc, _, err = orch.start_container(vendor, imgver)
    if rc != 0:
        print('CONTAINER FAIL:', (err or '')[-300:], flush=True)
        sys.exit(1)
    wait_health(vendor)
    print('container up: testvdb-%s (%s)' % (vendor, imgver), flush=True)


if __name__ == '__main__':
    main()
