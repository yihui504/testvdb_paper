#!/usr/bin/env python3
"""第二轮：候选 issue/PR 详情抓取 + PR merged 状态核实。

A 类: milvus 49264(fix PR of 49059), 48204, 32262, 52338
C 类: milvus 46683, 46494
E 类: qdrant 9142, 9553 (9027 原文已在 raw/)
F 类: qdrant 9442 (fix PR of 9421)
G 类: weaviate 12049, 12040, 11878, 11712, 12262, 11661, 5556
"""
import json
import os
import time
import urllib.request

TOKEN = os.environ['GITHUB_TOKEN']
OUT = os.path.dirname(os.path.abspath(__file__)) + '/raw'

HDRS = {'User-Agent': 'testvdb-investigate',
        'Authorization': 'Bearer ' + TOKEN,
        'Accept': 'application/vnd.github+json'}
MAINT = {'MEMBER', 'OWNER', 'COLLABORATOR', 'CONTRIBUTOR'}


def get(url):
    for _ in range(3):
        req = urllib.request.Request(url, headers=HDRS)
        try:
            with urllib.request.urlopen(req) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                reset = int(e.headers.get('X-RateLimit-Reset', time.time() + 60))
                time.sleep(max(reset - time.time(), 5) + 1)
                continue
            if e.code == 404:
                return None
            raise
    raise RuntimeError(url)


def fetch(repo, num):
    base = 'https://api.github.com/repos/%s' % repo
    detail = get(base + '/issues/' + str(num))
    if detail is None:
        print('== %s#%d 404' % (repo, num))
        return
    comments = get(base + '/issues/%d/comments?per_page=100' % num) or []
    timeline = get(base + '/issues/%d/timeline?per_page=100' % num) or []
    pr, merged = None, None
    if 'pull_request' in detail:
        pr = get(base + '/pulls/' + str(num))
        merged = (pr or {}).get('merged')
    time.sleep(0.8)
    key = '%s_%d' % (repo.replace('/', '_'), num)
    with open(os.path.join(OUT, key + '.json'), 'w', encoding='utf-8') as f:
        json.dump({'detail': detail, 'comments': comments, 'timeline': timeline,
                   'pr': pr}, f, ensure_ascii=False, indent=1)
    kind = 'PR' if pr else 'I'
    state = detail.get('state') or '?'
    if pr:
        state += ('/MERGED' if merged else '/unmerged')
    print('== %s#%d [%s] %s' % (repo, num, kind, state))
    print('   ', detail.get('title', '')[:95])
    for c in comments:
        if c.get('author_association') in MAINT:
            print('   [%s|%s] %s' % (c['user']['login'], c['author_association'],
                                     c['body'].replace('\n', ' ')[:220]))
    for ev in timeline:
        if ev.get('event') == 'closed' and ev.get('actor'):
            print('   <closed by %s>' % ev['actor']['login'])


R2 = [
    ('milvus-io/milvus', 49264),
    ('milvus-io/milvus', 48204),
    ('milvus-io/milvus', 32262),
    ('milvus-io/milvus', 52338),
    ('milvus-io/milvus', 46683),
    ('milvus-io/milvus', 46494),
    ('qdrant/qdrant', 9142),
    ('qdrant/qdrant', 9553),
    ('qdrant/qdrant', 9442),
    ('weaviate/weaviate', 12049),
    ('weaviate/weaviate', 12040),
    ('weaviate/weaviate', 11878),
    ('weaviate/weaviate', 11712),
    ('weaviate/weaviate', 12262),
    ('weaviate/weaviate', 11661),
    ('weaviate/weaviate', 5556),
]

for repo, num in R2:
    fetch(repo, num)
print('done')
