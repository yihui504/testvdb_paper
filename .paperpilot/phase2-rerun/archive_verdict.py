#!/usr/bin/env python3
"""归档单 case 判词：校验合格后 mv 到 {run_dir}/verdicts/{did}.json(+.done)。

用法: python archive_verdict.py <run_dir> <did>
run_dir 例: clean_run_fixes/fixA_run2；did 例: milvus_002
校验（纪律 §7.2）: JSON 合法 + verdicts[0].verdict 二值 + source_excerpt>=50 + files_examined 非空 + .done 存在。
不合格或判词缺失 → exit 1（编排者决定重派）。
"""
import json
import os
import shutil
import sys

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
MAP = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'defect_id_map.json'), encoding='utf-8'))


def main():
    run_dir, did = sys.argv[1], sys.argv[2]
    r = MAP[did]
    src = os.path.join(V2, 'sessions', r['vendor'], r['version'], did, 'debate_logs', 'dev_review.json')
    dst = os.path.join(run_dir, 'verdicts', did + '.json')
    if not os.path.isfile(src) or not os.path.isfile(src + '.done'):
        print('MISSING: %s' % src)
        sys.exit(1)
    d = json.load(open(src, encoding='utf-8'))
    vs = d.get('verdicts')
    if not isinstance(vs, list) or not vs:
        print('FAIL: no verdicts array')
        sys.exit(1)
    v0 = vs[0]
    verdict = v0.get('verdict')
    sg = v0.get('steps', {}).get('source_grounding', {}) if isinstance(v0.get('steps'), dict) else {}
    excerpt = sg.get('source_excerpt') or v0.get('source_excerpt') or ''
    files = sg.get('files_examined') or v0.get('files_examined') or []
    problems = []
    if verdict not in ('CONFIRMED', 'FALSE_POSITIVE'):
        problems.append('verdict=%r' % verdict)
    if len(excerpt) < 50:
        problems.append('excerpt_len=%d' % len(excerpt))
    if not files:
        problems.append('files_examined empty')
    if problems:
        print('FAIL: ' + ', '.join(problems))
        sys.exit(1)
    shutil.move(src, dst)
    shutil.move(src + '.done', dst + '.done')
    print('ARCHIVED %s verdict=%s conf=%s' % (did, verdict, v0.get('confidence')))


if __name__ == '__main__':
    main()
