#!/usr/bin/env python3
"""为 run-2/run-3 复制独立 session 树（仅输入，剥除任何历史 verdict），保证双盲独立性。

从 run/ 复制到 run2/ 和 run3/：
  保留: .srcdir, output_*.log, raw_*.log, stage2_aggregation.json,
        版本级 structured_contract.json / api_templates.md, intelligence/
  剥除: debate_logs/dev_review.json, *.done   （agent 自己重新产出）
两个 run 树完全独立、互不可见对方/首跑的 verdict。
"""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'run')


def ignore_verdicts(directory, names):
    drop = []
    for n in names:
        full = os.path.join(directory, n)
        # 剥除任何已有 verdict 及 done 标记（输入树里不应有结论）
        if os.path.isfile(full) and (n == 'dev_review.json' or n.endswith('.done')
                                     or n.startswith('dev_review') and n.endswith('.json')):
            drop.append(n)
    return drop


def main():
    for run in ('run2', 'run3'):
        dst = os.path.join(ROOT, run)
        if os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(SRC, dst, ignore=ignore_verdicts)
        # 统计
        n_sess = 0
        n_input_log = 0
        n_leftover_verdict = 0
        for v in ('milvus', 'qdrant', 'weaviate'):
            base = os.path.join(dst, 'results', v)
            if not os.path.isdir(base):
                continue
            for ver in os.listdir(base):
                nd = os.path.join(base, ver)
                if not os.path.isdir(nd):
                    continue
                for num in os.listdir(nd):
                    sess = os.path.join(nd, num)
                    if not os.path.isdir(sess):
                        continue
                    n_sess += 1
                    if any(f.startswith('output_') and f.endswith('.log') for f in os.listdir(sess)):
                        n_input_log += 1
                    db = os.path.join(sess, 'debate_logs')
                    if os.path.isdir(db):
                        for f in os.listdir(db):
                            if f == 'dev_review.json' or f.endswith('.done'):
                                n_leftover_verdict += 1
        print('%s: %d sessions | %d with input log | leftover verdicts: %d'
              % (run, n_sess, n_input_log, n_leftover_verdict))


if __name__ == '__main__':
    main()
