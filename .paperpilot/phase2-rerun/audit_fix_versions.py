#!/usr/bin/env python3
"""待办 1 — A 组 28 case 的 fix-PR 合入信息拉取（GitHub API，未认证 60/hr 限流内）。

对每个 A 组 case 的 fix PR（PR 编号来自 phase1-raw/verify-report.md 证据表）：
  拉取 pulls/{n} → merged_at / merge_commit_sha / base.ref / title / state
11741 缺 PR → 拉 issue timeline 找 cross-referenced PR。
结果缓存 pr_cache.json，可断点续跑。
"""
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(ROOT, 'pr_cache.json')
UA = {'User-Agent': 'testvdb-audit', 'Accept': 'application/vnd.github+json'}

# repo -> PR 编号（去重），来自 verify-report.md 的 28 个 TP_FIXED_PR 证据表
PRS = {
    'milvus-io/milvus': [47782, 50195, 51088, 51168, 3513, 3514, 52346, 52261, 50714, 50731],
    'qdrant/qdrant': [9320, 9058, 9070, 9178, 9431, 9442, 9526, 9531, 10128, 10141],
    'weaviate/weaviate': [11824, 12049, 11439, 11429, 11543, 11975, 12457],
}
# 11741 无 PR 证据 → 拉 timeline 找 cross-ref
TIMELINE_ISSUES = [('weaviate/weaviate', 11741)]


def api_get(url: str) -> tuple:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8')
            return json.loads(body), r.headers
    except urllib.error.HTTPError as e:
        print('HTTP %s %s' % (e.code, url), flush=True)
        return None, e.headers


def load_cache() -> dict:
    if os.path.isfile(CACHE):
        return json.load(open(CACHE, encoding='utf-8'))
    return {}


def save_cache(c: dict) -> None:
    json.dump(c, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def main() -> None:
    cache = load_cache()
    # PR 详情
    for repo, prs in PRS.items():
        for pr in prs:
            key = 'pr:%s:%d' % (repo, pr)
            if key in cache and cache[key] is not None:
                continue
            d, hdr = api_get('https://api.github.com/repos/%s/pulls/%d' % (repo, pr))
            if d is None:
                cache[key] = None
                save_cache(cache)
                continue
            cache[key] = {
                'number': d.get('number'), 'title': d.get('title'), 'state': d.get('state'),
                'merged': bool(d.get('merged_at')), 'merged_at': d.get('merged_at'),
                'merge_commit_sha': d.get('merge_commit_sha'),
                'base_ref': (d.get('base') or {}).get('ref'),
                'base_sha': (d.get('base') or {}).get('sha'),
                'created_at': d.get('created_at'), 'closed_at': d.get('closed_at'),
            }
            save_cache(cache)
            remain = hdr.get('X-RateLimit-Remaining')
            print('%-28s #%-6d merged=%s %s %s (limit=%s)' % (
                repo, pr, cache[key]['merged'], cache[key]['merged_at'], cache[key]['base_ref'], remain), flush=True)
            if int(remain) < 5:
                print('rate limit low, stop; rerun to resume', flush=True)
                sys.exit(0)
            time.sleep(0.7)
    # timeline
    for repo, num in TIMELINE_ISSUES:
        key = 'timeline:%s:%d' % (repo, num)
        if key in cache:
            continue
        d, hdr = api_get('https://api.github.com/repos/%s/issues/%d/timeline?per_page=100' % (repo, num))
        if d is None:
            cache[key] = None
            save_cache(cache)
            continue
        refs = []
        for ev in d:
            if ev.get('event') == 'cross-referenced':
                src = ev.get('source', {}).get('issue', {})
                refs.append({'pr_number': src.get('number'), 'title': src.get('title'),
                             'state': src.get('state'), 'repo': src.get('repository', {}).get('full_name')})
        cache[key] = refs
        save_cache(cache)
        print('timeline %s#%d cross-refs: %s' % (repo, num, json.dumps(refs, ensure_ascii=False)), flush=True)
    print('done -> %s' % CACHE)


if __name__ == '__main__':
    main()
