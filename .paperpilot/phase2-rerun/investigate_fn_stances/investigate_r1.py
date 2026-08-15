#!/usr/bin/env python3
"""信息不可达 FN 锚点调查 第一轮：search 宽召回 + 本体 issue 表态抓取。

目的：为 7 个现象类找"同类现象的历史维护者表态"（不限于原 issue），
     存原始数据到 raw/，供三条件（§9）检验。

现象类（class）：
  A milvus 数值精度/数学边界       本体 49059 (milvus_008)
  B milvus REST v2 空串/无效参数    本体 49889 (milvus_012) + 50018 (milvus_017)
  C milvus 文档-行为不一致         本体 50355 (milvus_031)
  E qdrant 无效值静默回退默认      本体 9017 (qdrant_002, GT=TP) vs 9027 (qdrant_003 相关, 方向待核实)
  F qdrant 5xx→4xx 错误码语义     本体 9421 (qdrant_014)
  G weaviate 5xx→4xx 错误码语义   本体 12041 (weaviate_010)

milvus_001 (47635) = 材料形态（空日志），不调查。
"""
import json
import os
import time
import urllib.request

TOKEN = os.environ['GITHUB_TOKEN']
OUT = os.path.dirname(os.path.abspath(__file__)) + '/raw'
os.makedirs(OUT, exist_ok=True)

HDRS = {'User-Agent': 'testvdb-investigate',
        'Authorization': 'Bearer ' + TOKEN,
        'Accept': 'application/vnd.github+json'}


def get(url):
    for attempt in range(3):
        req = urllib.request.Request(url, headers=HDRS)
        try:
            with urllib.request.urlopen(req) as r:
                remaining = r.headers.get('X-RateLimit-Remaining', '?')
                return json.load(r), remaining
        except urllib.error.HTTPError as e:
            if e.code in (403, 429):
                reset = int(e.headers.get('X-RateLimit-Reset', time.time() + 60))
                wait = max(reset - time.time(), 5) + 1
                print('  rate limit, sleep %.0fs' % wait)
                time.sleep(wait)
                continue
            if e.code == 404:
                return None, '404'
            raise
    raise RuntimeError('retries exhausted: ' + url)


def search(kind, q, n=30):
    url = ('https://api.github.com/search/%s?q=%s&per_page=%d&sort=created&order=desc'
           % (kind, urllib.parse.quote(q), n))
    d, rem = get(url)
    time.sleep(2.5)  # search: 30 req/min
    items = (d or {}).get('items', [])
    print('  %-6s %-60s -> %d hits (total %s) [rem %s]'
          % (kind, q[:60], len(items), (d or {}).get('total_count'), rem))
    return items


def issue_detail(repo, num):
    """issue/PR 详情 + 评论 + timeline events，识别维护者表态。"""
    key = '%s_%d' % (repo.replace('/', '_'), num)
    base = 'https://api.github.com/repos/%s' % repo
    detail, _ = get(base + '/issues/' + str(num))
    comments, _ = get(base + '/issues/%d/comments?per_page=100' % num)
    timeline, _ = get(base + '/issues/%d/timeline?per_page=100' % num)
    time.sleep(1.0)
    out = {'detail': detail, 'comments': comments, 'timeline': timeline}
    with open(os.path.join(OUT, key + '.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    # 摘要打印：维护者身份(author_association in MEMBER/OWNER/COLLABORATOR)的表态
    maint = {'MEMBER', 'OWNER', 'COLLABORATOR', 'CONTRIBUTOR'}
    lines = []
    for c in (comments or []):
        if c.get('author_association') in maint:
            body = c['body'].replace('\n', ' ')[:200]
            lines.append('  [%s|%s] %s' % (c['user']['login'], c['author_association'], body))
    for ev in (timeline or []):
        if ev.get('event') in ('closed', 'referenced', 'cross-referenced', 'merged'):
            actor = (ev.get('actor') or {}).get('login', '?')
            assoc = ev.get('source', {}).get('issue', {}).get('author_association', '')
            commit = ev.get('commit_id') or ''
            src = ev.get('source', {}).get('issue', {}).get('number', '')
            lines.append('  <%s:%s> commit=%s src=%s assoc=%s' % (ev['event'], actor, commit[:12], src, assoc))
    print('== %s#%d (%s) %s' % (repo, num,
                                (detail or {}).get('state'),
                                ((detail or {}).get('title') or '')[:70]))
    for ln in lines[:25]:
        print(ln)
    return out


# ---------- 第一部分：本体 issue 表态抓取 ----------
BODIES = [
    ('milvus-io/milvus', 49059),   # A 本体
    ('milvus-io/milvus', 49889),   # B 本体 1
    ('milvus-io/milvus', 50018),   # B 本体 2
    ('milvus-io/milvus', 50355),   # C 本体
    ('qdrant/qdrant', 9017),       # E 本体 (TP)
    ('qdrant/qdrant', 9027),       # E 方向核实（score_threshold）
    ('qdrant/qdrant', 9421),       # F 本体
    ('weaviate/weaviate', 12041),  # G 本体
]

# ---------- 第二部分：search 宽召回 ----------
SEARCHES = [
    ('A', 'issues', 'repo:milvus-io/milvus cosine distance precision'),
    ('A', 'issues', 'repo:milvus-io/milvus metric distance range wrong result'),
    ('B', 'issues', 'repo:milvus-io/milvus "empty string" in:title,body label:bug'),
    ('B', 'issues', 'repo:milvus-io/milvus REST validation parameter missing in:title,body'),
    ('C', 'issues', 'repo:milvus-io/milvus documentation inconsistent behavior in:title,body'),
    ('E', 'issues', 'repo:qdrant/qdrant silently ignored invalid parameter'),
    ('F', 'issues', 'repo:qdrant/qdrant "returns 500"'),
    ('F', 'issues', 'repo:qdrant/qdrant status code 400 client error'),
    ('G', 'issues', 'repo:weaviate/weaviate "returns 500"'),
    ('G', 'issues', 'repo:weaviate/weaviate "should return" 422 OR 400'),
]


def main():
    import os.path
    print('===== Part 1: 本体 issue 表态（已抓，跳过） =====')

    print()
    print('===== Part 2: search 宽召回 =====')
    hits = {}
    for cls, kind, q in SEARCHES:
        items = search(kind, q)
        slim = [{'n': i['number'], 'title': i['title'][:110], 'state': i['state'],
                 'pr': 'pull_request' in i, 'assoc': i.get('author_association'),
                 'labels': [l['name'] for l in i.get('labels', [])][:4],
                 'closed': (i.get('closed_at') or '')[:10]}
                for i in items]
        hits.setdefault(cls, []).append({'query': q, 'items': slim})
    with open(os.path.join(OUT, '_search_round1.json'), 'w', encoding='utf-8') as f:
        json.dump(hits, f, ensure_ascii=False, indent=1)
    print('saved _search_round1.json')


if __name__ == '__main__':
    main()
