# -*- coding: utf-8 -*-
"""Retry failed checks with exponential backoff + arXiv export API fallback."""
import json, re, time, io
import urllib3
import requests

urllib3.disable_warnings()
UA = {"User-Agent": "RefCheck/2.1 (mailto:test@example.org)"}
IN = r'C:\Users\11428\Desktop\testvdb_paper\resources\working_memory\verify_all_out.json'
OUT = r'C:\Users\11428\Desktop\testvdb_paper\resources\working_memory\verify_retry_out.json'

S = requests.Session()
S.trust_env = False

def get(url, params=None, timeout=60):
    r = S.get(url, params=params, timeout=timeout, verify=False, headers=UA)
    r.raise_for_status()
    return r

def with_backoff(fn, attempts=4, base=3.0):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as ex:
            last = ex
            time.sleep(base * (2 ** i) + 1)
    raise last

def arxiv_export(arxiv_id):
    """export.arxiv.org API (Atom XML) — more tolerant than abs page."""
    r = with_backoff(lambda: get('https://export.arxiv.org/api/query',
                                 params={'id_list': arxiv_id, 'max_results': 1}))
    txt = r.text
    mtitle = re.search(r'<entry>.*?<title>(.*?)</title>', txt, re.S)
    authors = re.findall(r'<name>(.*?)</name>', txt)
    mpub = re.search(r'<published>(\d{4})', txt)
    mdoi = re.search(r'<arxiv:doi[^>]*>(.*?)</arxiv:doi>', txt, re.S) or \
          re.search(r'<link title="doi"[^>]*href="([^"]*)"', txt)
    return {'title': mtitle.group(1).strip() if mtitle else '',
            'authors': [a.strip() for a in authors],
            'published': mpub.group(1) if mpub else '',
            'doi': mdoi.group(1).strip() if mdoi else ''}

def arxiv_abs(arxiv_id):
    r = with_backoff(lambda: get('https://arxiv.org/abs/' + arxiv_id))
    mtitle = re.search(r'<meta name="citation_title" content="([^"]*)"', r.text)
    authors = re.findall(r'<meta name="citation_author" content="([^"]*)"', r.text)
    mdate = re.search(r'<meta name="citation_date" content="([^"]*)"', r.text)
    return {'title': mtitle.group(1) if mtitle else '',
            'authors': authors,
            'date': mdate.group(1) if mdate else ''}

def semantic_arxiv(arxiv_id):
    url = 'https://api.semanticscholar.org/graph/v1/paper/arXiv:' + arxiv_id
    def _f():
        r = S.get(url, params={'fields': 'title,authors,year,venue,externalIds'},
                  timeout=60, verify=False, headers=UA)
        if r.status_code == 404:
            return {'error': 'not_found_404'}
        r.raise_for_status()
        d = r.json()
        return {'title': d.get('title') or '',
                'authors': [a['name'] for a in d.get('authors', [])],
                'year': d.get('year'), 'venue': d.get('venue'),
                'ext': d.get('externalIds', {})}
    return with_backoff(_f, attempts=5, base=4.0)

def dblp_search(query, h=5):
    r = with_backoff(lambda: get('https://dblp.org/search/publ/api',
                                 params={'q': query, 'format': 'json', 'h': str(h)}))
    d = r.json()['result']['hits']
    total = int(d.get('@total', 0))
    out = []
    for x in d.get('hit', []):
        info = x.get('info', {})
        authors = []
        au = info.get('authors', {})
        if isinstance(au, dict):
            alist = au.get('author', [])
            if isinstance(alist, dict):
                alist = [alist]
            for a in alist:
                authors.append(a.get('text', ''))
        out.append({'title': info.get('title', ''), 'authors': authors,
                    'year': info.get('year'), 'venue': info.get('venue', ''),
                    'url': info.get('url', '')})
    return {'total': total, 'hits': out}

def openalex_search(title, per_page=4):
    r = with_backoff(lambda: get('https://api.openalex.org/works',
                                 params={'filter': 'title.search:' + title[:120],
                                         'per-page': per_page}), attempts=5, base=4.0)
    out = []
    for w in r.json().get('results', []):
        authors = [a['author']['display_name'] for a in w.get('authorships', [])]
        src = (w.get('primary_location') or {}).get('source') or {}
        out.append({'title': w.get('title') or '', 'authors': authors,
                    'year': w.get('publication_year'),
                    'venue': src.get('display_name')})
    return out

recs = json.load(io.open(IN, encoding='utf-8'))
retried = []
for rec in recs:
    key = rec['key']
    dirty = False
    arxiv = rec.get('bib_arxiv')
    doi = rec.get('bib_doi')

    # re-check arXiv (abs fetch failed)
    if arxiv:
        bad_abs = any(c.get('src') == 'arxiv_abs' and 'error' in c for c in rec.get('checks', []))
        if bad_abs:
            try:
                m = arxiv_abs(arxiv); m['src'] = 'arxiv_abs'; m['retried'] = True
                rec['checks'] = [c for c in rec['checks'] if c.get('src') != 'arxiv_abs'] + [m]
                dirty = True
                print(key, 'arxiv_abs retry OK:', m.get('title', '')[:50], flush=True)
            except Exception as ex:
                try:
                    m = arxiv_export(arxiv); m['src'] = 'arxiv_export'; m['retried'] = True
                    rec['checks'] = [c for c in rec['checks'] if c.get('src') != 'arxiv_abs'] + [m]
                    dirty = True
                    print(key, 'arxiv_export fallback OK:', m.get('title', '')[:50], flush=True)
                except Exception as ex2:
                    print(key, 'arxiv retry FAILED:', str(ex2)[:80], flush=True)
            time.sleep(2)
        bad_sem = any(c.get('src') == 'semantic_arxiv' and 'error' in c for c in rec.get('checks', []))
        if bad_sem and not doi:
            try:
                m = semantic_arxiv(arxiv); m['src'] = 'semantic_arxiv'; m['retried'] = True
                rec['checks'] = [c for c in rec['checks'] if c.get('src') != 'semantic_arxiv'] + [m]
                dirty = True
                print(key, 'semantic retry OK:', m.get('title', '')[:50], flush=True)
            except Exception as ex:
                print(key, 'semantic retry FAILED:', str(ex)[:80], flush=True)
            time.sleep(3)

    # re-run title searches
    q = re.sub(r'[^A-Za-z0-9 ]+', ' ', rec.get('bib_title', '')).strip()
    if isinstance(rec.get('dblp'), dict) and ('error' in rec['dblp'] or rec['dblp'].get('total', 0) == 0):
        try:
            rec['dblp'] = dblp_search(q[:80], h=5)
            dirty = True
            print(key, 'dblp retry OK: total=%s' % rec['dblp'].get('total'), flush=True)
        except Exception as ex:
            print(key, 'dblp retry FAILED:', str(ex)[:80], flush=True)
        time.sleep(2)
    oa = rec.get('openalex')
    if isinstance(oa, dict) and 'error' in oa:
        try:
            rec['openalex'] = openalex_search(q[:100], 4)
            dirty = True
            print(key, 'openalex retry OK: %d hits' % len(rec['openalex']), flush=True)
        except Exception as ex:
            print(key, 'openalex retry FAILED:', str(ex)[:80], flush=True)
        time.sleep(3)

    if dirty:
        retried.append(key)

with io.open(OUT, 'w', encoding='utf-8') as f:
    json.dump(recs, f, ensure_ascii=False, indent=1)
print('\nWROTE', OUT, '| retried keys:', len(retried))
