# -*- coding: utf-8 -*-
"""Analyze verify_all_out.json: compare bib fields vs authoritative sources.

Verdicts: ok / mismatch / not_found / no_id / unknown
"""
import json, io, re, sys

IN = r'C:\Users\11428\Desktop\testvdb_paper\resources\working_memory\verify_all_out.json'
OUT = r'C:\Users\11428\Desktop\testvdb_paper\resources\working_memory\verify_verdicts.json'

def normalize(s):
    if not s:
        return ''
    s = s.lower()
    s = re.sub(r'[^a-z0-9]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()

def title_sim(a, b):
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    wa, wb = set(a.split()), set(b.split())
    return len(wa & wb) / max(len(wa), len(wb), 1)

def fam(s):
    s = s.strip()
    if not s:
        return ''
    if ',' in s:
        return s.split(',')[0].strip().rstrip('.')
    parts = s.split()
    return parts[-1].strip().rstrip('.')

def fams_of_list(authors):
    out = []
    for a in authors:
        f = fam(a)
        if f:
            out.append(f.lower())
    return out

def best_hit_title(title, hits):
    best, bs = None, 0.0
    for h in hits:
        s = title_sim(title, h.get('title', ''))
        if s > bs:
            bs, best = s, h
    return best, bs

def analyze(rec):
    key = rec['key']
    bib_title = rec.get('bib_title', '')
    bib_year = rec.get('bib_year', '')
    bib_surnames = [f.lower() for f in rec.get('bib_surnames', [])]
    checks = rec.get('checks', [])
    dblp = rec.get('dblp', {})
    openalex = rec.get('openalex', [])
    url_check = rec.get('url_check')

    verdicts = []

    # --- DOI check ---
    for c in checks:
        if c.get('src') == 'crossref_doi':
            if 'error' in c:
                verdicts.append({'src': 'doi', 'status': 'unknown', 'detail': 'API error: ' + c['error'][:100]})
            else:
                ts = title_sim(bib_title, c.get('title', ''))
                auth_fams = fams_of_list(c.get('authors', []))
                fam_match = bool(set(auth_fams) & set(bib_surnames))
                year = c.get('year')
                issues = []
                if ts < 0.6:
                    issues.append('title mismatch (sim=%.2f)' % ts)
                if not fam_match:
                    issues.append('no author-family overlap')
                if year and bib_year and abs(int(year) - int(bib_year)) > 1:
                    issues.append('year %s vs bib %s' % (year, bib_year))
                status = 'ok' if not issues else 'mismatch'
                verdicts.append({'src': 'doi', 'status': status,
                                 'title_sim': round(ts, 2), 'auth_fams': auth_fams[:8],
                                 'auth_year': year, 'venue': c.get('venue'),
                                 'issues': issues})

    # --- arXiv checks ---
    arxiv_abs = next((c for c in checks if c.get('src') == 'arxiv_abs'), None)
    sem = next((c for c in checks if c.get('src') == 'semantic_arxiv'), None)

    if arxiv_abs is not None:
        if 'error' in arxiv_abs:
            verdicts.append({'src': 'arxiv_abs', 'status': 'not_found' if arxiv_abs['error'] == '404_not_found' else 'unknown',
                             'detail': arxiv_abs['error']})
        else:
            ts = title_sim(bib_title, arxiv_abs.get('title', ''))
            auth_fams = fams_of_list(arxiv_abs.get('authors', []))
            fam_match = bool(set(auth_fams) & set(bib_surnames))
            issues = []
            if ts < 0.6:
                issues.append('title mismatch (sim=%.2f)' % ts)
            if not fam_match:
                issues.append('no author-family overlap')
            date = arxiv_abs.get('date', '')
            ay = date[:4] if date else ''
            if ay and bib_year and abs(int(ay) - int(bib_year)) > 1:
                issues.append('year %s vs bib %s' % (ay, bib_year))
            status = 'ok' if not issues else 'mismatch'
            verdicts.append({'src': 'arxiv_abs', 'status': status,
                             'title_sim': round(ts, 2), 'auth_fams': auth_fams[:8],
                             'auth_year': ay, 'date': date, 'issues': issues})

    if sem is not None:
        if 'error' not in sem:
            ts = title_sim(bib_title, sem.get('title', ''))
            auth_fams = fams_of_list(sem.get('authors', []))
            fam_match = bool(set(auth_fams) & set(bib_surnames))
            issues = []
            if ts < 0.6:
                issues.append('title mismatch (sim=%.2f)' % ts)
            if not fam_match:
                issues.append('no author-family overlap')
            if sem.get('year') and bib_year and abs(int(sem['year']) - int(bib_year)) > 1:
                issues.append('year %s vs bib %s' % (sem['year'], bib_year))
            status = 'ok' if not issues else 'mismatch'
            verdicts.append({'src': 'semantic', 'status': status,
                             'title_sim': round(ts, 2), 'auth_fams': auth_fams[:8],
                             'auth_year': sem.get('year'), 'issues': issues})
        else:
            verdicts.append({'src': 'semantic', 'status': 'unknown' if sem['error'] != 'not_found_404' else 'not_found',
                             'detail': sem['error']})

    # --- title-only fallback: DBLP + OpenAlex ---
    if 'dblp' in rec or 'openalex' in rec:
        dblp_hits = dblp.get('hits', []) if isinstance(dblp, dict) else []
        oa_hits = openalex if isinstance(openalex, list) else []
        dbest, dsim = best_hit_title(bib_title, dblp_hits)
        obest, osim = best_hit_title(bib_title, oa_hits)
        best = dbest if dsim >= osim else obest
        bsim = max(dsim, osim)
        srcname = 'dblp' if dsim >= osim else 'openalex'
        if best is None:
            status = 'unknown' if ('error' in (dblp or {}) and 'error' in (openalex or [])) else 'not_found'
            verdicts.append({'src': 'title', 'status': status, 'detail': 'no hit (dblp err=%s, oa err=%s)' % (
                'error' in (dblp or {}), isinstance(openalex, dict) and 'error' in openalex)})
        else:
            issues = []
            if bsim < 0.6:
                issues.append('title sim only %.2f' % bsim)
            auth_fams = fams_of_list(best.get('authors', []))
            fam_match = bool(set(auth_fams) & set(bib_surnames))
            if not fam_match:
                issues.append('no author-family overlap')
            by = best.get('year')
            if by and bib_year and abs(int(by) - int(bib_year)) > 1:
                issues.append('year %s vs bib %s' % (by, bib_year))
            status = 'ok' if not issues else 'mismatch'
            verdicts.append({'src': 'title/' + srcname, 'status': status,
                             'title_sim': round(bsim, 2), 'auth_fams': auth_fams[:8],
                             'auth_year': by, 'venue': best.get('venue'), 'issues': issues})

    # --- URL check (@misc/@online) ---
    if url_check:
        verdicts.append({'src': 'url', 'status': 'ok' if url_check.get('ok') else 'not_found',
                         'detail': 'HTTP %s' % url_check.get('status')})

    if not verdicts:
        verdicts.append({'src': 'none', 'status': 'no_id',
                         'detail': 'no DOI/arXiv/URL; no search attempted'})

    return verdicts

with io.open(IN, encoding='utf-8') as f:
    recs = json.load(f)

out = []
for rec in recs:
    vs = analyze(rec)
    # overall status: not_found > mismatch > unknown > ok (priority)
    order = {'not_found': 3, 'mismatch': 2, 'unknown': 1, 'no_id': 1, 'ok': 0}
    overall = max(vs, key=lambda v: order.get(v['status'], 0))
    out.append({'key': rec['key'], 'type': rec['type'],
                'bib_title': rec.get('bib_title', ''),
                'bib_year': rec.get('bib_year', ''),
                'bib_arxiv': rec.get('bib_arxiv'),
                'bib_doi': rec.get('bib_doi'),
                'overall': overall['status'],
                'verdicts': vs})
    print('%-22s %-10s %s' % (rec['key'], overall['status'], ' | '.join(
        '%s:%s' % (v['src'], v['status']) for v in vs)))

with io.open(OUT, 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print('\nWROTE', OUT)
