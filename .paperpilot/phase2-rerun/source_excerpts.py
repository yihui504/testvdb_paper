#!/usr/bin/env python3
"""Phase 2 rerun — 为每 case 抽源码片段(Phase 3.2, dev-reviewer 源码接地的预置版)。

对 71 scored case: 从 round1 rationale 的 `param=value` 和 title camelCase 提取精确 grep 词,
在对应版本 clone(C:\\Users\\11428\\Desktop\\vdb_src\\{vendor}\\{tag})的核心源码目录里 grep,
取最相关命中(偏好 valid/check/parse/search/param 名), 抽 ±15 行上下文, 写 source_excerpts/{vendor}_{num}.md。

clone 未就位 -> clone_pending; 无命中 -> not_found(judge 依 raw+契约判, 置信度↓)。
这是 dev-reviewer agent "主动 Grep 自由探索" 的静态预置替代: judge 只读预置片段, 不能自己 Grep。
"""
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
VDB_SRC = r'C:\Users\11428\Desktop\vdb_src'
CASES = json.load(open(os.path.join(ROOT, 'cases_index.json'), encoding='utf-8'))

# round1 rationale(精确 param 名来源)
RATIONALE = {}
for short in ('milvus', 'qdrant', 'weaviate'):
    p = os.path.join(os.path.dirname(ROOT), 'phase2', 'round1_%s.tsv' % short)
    if os.path.exists(p):
        for line in open(p, encoding='utf-8'):
            parts = line.rstrip('\n').split('\t')
            if len(parts) >= 4:
                RATIONALE['%s_%s' % (short, parts[1])] = parts[3]

EXT = {'milvus': '*.go', 'qdrant': '*.rs', 'weaviate': '*.go'}
SEARCH_DIRS = {'milvus': ['internal', 'client', 'cmd', 'pkg'],
               'qdrant': ['src', 'lib', 'config'],
               'weaviate': ['cmd', 'modules', 'use', 'adapters', 'entities', 'grpc']}
# 文件路径里出现这些 = 更可能是校验/处理逻辑(加分)
PATH_BONUS = ('valid', 'check', 'parse', 'handler', 'request', 'proxy', 'search', 'filter', 'verify', 'sanitiz')
# 这些路径是配置/常量/定义层,不是校验逻辑(减分)
PATH_PENALTY = ('paramtable', 'base_param', 'param_item', 'config', 'constant', 'consts', 'mock', 'data.go')
GENERIC = set('''but and the for with from that this code returned accepted status result results
                doc documented violates violation value values reported claim reproduction reproduced
                inconsistent inconsistency properly server client
                bug bugs issue index accepts accept accepted report missing validation valid validate
                field fields error errors fail fails failure return returns http rest grpc json
                data request response silently normal normalized stored stored create insert upsert
                search query delete drop describe collection collections param parameter params'''.split())


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def search_terms(case):
    """精确 grep 词: rationale 的 param=value + title camelCase + 数字边界词。"""
    rat = RATIONALE.get('%s_%s' % (case['vendor'], case['num']), '')
    terms = []
    for m in re.findall(r'([A-Za-z_]\w*)\s*=[^=>]', rat):
        terms.append(m)
    for m in re.findall(r'[a-z]+(?:[A-Z][a-z]+)+', case.get('title') or ''):
        terms.append(m)
    for m in re.findall(r'[a-z]+(?:[A-Z][a-z]+)+', rat):
        terms.append(m)
    seen, out = set(), []
    for t in terms:
        tl = t.lower()
        if tl in GENERIC or tl in seen or len(tl) < 2:
            continue
        seen.add(tl)
        out.append(t)
    # 兜底: title 的 lowercase 名词 token(REST 类型强转等 case 无 param=value)
    if len(out) < 3:
        for m in re.findall(r'[A-Za-z][A-Za-z0-9_]{2,}', case.get('title') or ''):
            ml = m.lower()
            if ml in GENERIC or ml in seen or len(ml) < 3:
                continue
            seen.add(ml)
            out.append(m)
    return out[:5] or [case['vendor']]


def grep_term(term, clone, vendor):
    """grep -rni term in clone/searchdirs, 返回 [(file, lineno, linetext), ...]。"""
    hits = []
    inc = EXT[vendor]
    for sdir in SEARCH_DIRS[vendor]:
        path = os.path.join(clone, sdir)
        if not os.path.isdir(path):
            continue
        cmd = ['grep', '-rni', '--include=%s' % inc,
               '--exclude-dir=test', '--exclude-dir=tests', '--exclude-dir=testing',
               '--exclude-dir=vendor', '--exclude-dir=thirdparty', '--exclude-dir=third_party',
               '--exclude-dir=build', '--exclude-dir=target', '--exclude-dir=node_modules',
               '--exclude-dir=mock', '--exclude-dir=examples', '--exclude-dir=docs',
               '--exclude=*_test.go', '--exclude=*_test.rs', '--exclude=*mock*',
               term, path]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, errors='replace')
        except Exception:
            continue
        for line in r.stdout.splitlines():
            if ':' not in line:
                continue
            # Windows 盘符冒号(C:)会破坏简单 split; lineno = 第一个纯数字 part
            parts = line.split(':')
            idx = next((i for i, p in enumerate(parts) if p.isdigit()), None)
            if idx is None or idx < 1:
                continue
            f = ':'.join(parts[:idx])       # 路径(含盘符冒号)
            ln = int(parts[idx])
            txt = ':'.join(parts[idx + 1:])
            hits.append((f, ln, txt))
    return hits


def rank_hits(hits):
    """按路径相关性排序: 含 PATH_BONUS 加分; 短路径(核心代码)加分。"""
    def score(h):
        f = h[0].lower().replace('\\', '/')
        s = sum(3 for b in PATH_BONUS if b in f)
        s -= sum(4 for p in PATH_PENALTY if p in f)
        s += max(0, 3 - len(f.split('/')))  # 浅路径加分
        return s
    return sorted(hits, key=score, reverse=True)


def extract_context(filepath, lineno, radius=15):
    try:
        lines = open(filepath, encoding='utf-8', errors='replace').read().splitlines()
    except Exception:
        return None
    lo, hi = max(0, lineno - 1 - radius), min(len(lines), lineno + radius)
    return lines[lo:hi], lo


def main():
    out_dir = os.path.join(ROOT, 'source_excerpts')
    os.makedirs(out_dir, exist_ok=True)
    report = []
    scored = [c for c in CASES if c['group'] in ('A', 'B', 'C')]
    for case in scored:
        vendor, num, version = case['vendor'], case['num'], case['version']
        did = '%s_%s' % (vendor, num)
        tag = tag_for(vendor, version)
        clone = os.path.join(VDB_SRC, vendor, tag)
        terms = search_terms(case)
        rec = {'defect_id': did, 'vendor': vendor, 'version': version, 'tag': tag, 'terms': terms}
        if not os.path.isdir(clone):
            rec['status'] = 'clone_pending'
            json.dump(rec, open(os.path.join(out_dir, did + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            report.append(rec)
            continue
        chosen_hits, chosen_term = [], None
        for t in terms:  # 优先级序: param 名优先; 第一个有命中的 term 胜出(防泛词 flood)
            h = grep_term(t, clone, vendor)
            if h:
                chosen_hits, chosen_term = h, t
                break
        if not chosen_hits:
            rec['status'] = 'not_found'
            rec['note'] = 'no source hit for terms %s (judge relies on raw+contract)' % terms
            json.dump(rec, open(os.path.join(out_dir, did + '.json'), 'w', encoding='utf-8'),
                      ensure_ascii=False, indent=1)
            report.append(rec)
            continue
        ranked = rank_hits(chosen_hits)
        # 取最多 2 个不同文件
        chosen, seen_files = [], set()
        for h in ranked:
            if h[0] in seen_files:
                continue
            seen_files.add(h[0])
            chosen.append(h)
            if len(chosen) >= 2:
                break
        excerpts = []
        for f, ln, txt in chosen:
            ctx = extract_context(f, ln)
            if not ctx:
                continue
            lines, lo = ctx
            rel = f.replace(clone, '').replace('\\', '/').lstrip('/')
            body = '\n'.join('%4d| %s' % (lo + i + 1, l) for i, l in enumerate(lines))
            excerpts.append({'file': rel, 'line': ln,
                'term_matched': chosen_term,
                'context': body})
        rec['status'] = 'found'
        rec['n_hits'] = len(chosen_hits)
        rec['excerpts'] = excerpts
        json.dump(rec, open(os.path.join(out_dir, did + '.json'), 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        report.append(rec)

    from collections import Counter
    cnt = Counter(r['status'] for r in report)
    print('source excerpts:', dict(cnt), '| total', len(report))
    pending = [r['defect_id'] for r in report if r['status'] == 'clone_pending']
    print('clone_pending (%d):' % len(pending), pending)
    nf = [r['defect_id'] for r in report if r['status'] == 'not_found']
    print('not_found (%d):' % len(nf), nf)


if __name__ == '__main__':
    main()
