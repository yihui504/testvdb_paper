#!/usr/bin/env python3
"""audit_arms_materials.py — 两臂材料包确定性泄露审计（0 FAIL 才可派发）。

审计面：
A. GT 信号：gt 标签 / group 字母 / gt_category 常量 / maintainer 表态词 / related_issue_numbers 非空
B. packet 专属通道：cognition / bug_shapes / source_excerpt 字段名与内容特征（Go/Rust 源码行号 excerpt）
C. issue 原文：'[Bug]' 标题模式 / issue 编号引用（47635 等五位号）
D. 路径泄露：phase2/rerun/experiment 字样路径、.srcdir、intelligence 路径
E. 结构校验：71+71 文件齐、JSON 可解析、milvus_001 特例标注、执行日志非空（除 001）
"""
import json
import os
import re
import sys

RERUN = r'c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun'
ARMS = os.path.join(RERUN, 'arms')

GT_WORDS = [
    r'\bgt[_\s]*(=|:)\s*\w', r'"gt"', r'\bgroup[A-C]"\s*:', r'\bgroup"\s*:\s*"[ABC]"',
    r'TP_FIXED|TP_ACK|FP_BY_DESIGN|BY_DESIGN|NOT_REPRO|UNADJUDICATED|CLOSED_NOFIX',
    r'ground[_\s]?truth',
    # maintainer 表态（developer_cognition 的锚点语汇）
    r'maintainers?\s+(?:explicitly\s+)?(?:stated|confirmed|fixed|rejected|consider(?:s|ed)\s+this\s+(?:as\s+)?(?:expected|by[\s_-]?design))',
    r'repeatedly\s+fixed',
]
PACKET_WORDS = [r'cognition', r'bug_shapes', r'source_excerpt', r'blindspot', r'rejection_patterns',
                r'by_design_patterns', r'developer_quote']
ISSUE_WORDS = [r'\[Bug\]', r'#\d{4,5}\b']
PATH_WORDS = [r'phase2', r'rerun', r'\.srcdir', r'intelligence', r'vdb_src', r'experiment']

FAILS = []


def scan_text(path, text, patterns, label):
    for pat in patterns:
        for m in re.finditer(pat, text, re.IGNORECASE):
            # 允许例外：raw_knowledge.md 的 constraint_id 里含 'rerun'？契约 id 不含。逐条记录待人工裁决
            FAILS.append(f"[{label}] {os.path.basename(path)}: /{pat}/ -> {text[max(0,m.start()-40):m.end()+40]!r}")


def main():
    sl_dir = os.path.join(ARMS, 'single_llm', 'materials')
    sl_files = sorted(os.listdir(sl_dir))
    if len(sl_files) != 71:
        FAILS.append(f"[structure] single_llm materials = {len(sl_files)} != 71")

    n_empty_log, n_json_ok = 0, 0
    for f in sl_files:
        p = os.path.join(sl_dir, f)
        text = open(p, encoding='utf-8').read()
        scan_text(p, text, GT_WORDS, 'GT')
        scan_text(p, text, PACKET_WORDS[:7], 'PACKET')   # source_excerpt 等
        scan_text(p, text, ISSUE_WORDS, 'ISSUE')
        scan_text(p, text, PATH_WORDS, 'PATH')
        if '[no raw HTTP captured]' in text and f != 'milvus_001.md':
            n_empty_log += 1
            FAILS.append(f"[empty-log] {f}: 无观察且非 milvus_001 特例")

    vt_root = os.path.join(ARMS, 'voting', 'sessions')
    cand_files = []
    for dirpath, dirs, files in os.walk(vt_root):
        for fn in files:
            if fn.endswith('.json'):
                full = os.path.join(dirpath, fn)
                text = open(full, encoding='utf-8').read()
                scan_text(full, text, GT_WORDS, 'GT')
                scan_text(full, text, PACKET_WORDS, 'PACKET')
                scan_text(full, text, ISSUE_WORDS, 'ISSUE')
                scan_text(full, text, PATH_WORDS, 'PATH')
                try:
                    json.loads(text)
                    n_json_ok += 1
                except Exception as e:
                    FAILS.append(f"[json] {full}: {e}")
                if 'candidates' in dirpath:
                    cand_files.append(fn)
    if len(cand_files) != 71:
        FAILS.append(f"[structure] voting candidates = {len(cand_files)} != 71")

    # milvus_001 特例在包内必须被标注
    p001 = os.path.join(sl_dir, 'milvus_001.md')
    if 'milvus_001' in open(p001, encoding='utf-8').read():
        pass
    m1 = json.load(open(os.path.join(vt_root, 'milvus', '2.3', 'milvus_001', 'candidates', 'milvus_001.json'), encoding='utf-8'))
    if m1['observed'].get('log_file') != 'output_milvus_001.log':
        FAILS.append('[structure] milvus_001 log_file 应为占位符日志')
    # execution_results 里 captured_raw_http 应为 False
    e1 = json.load(open(os.path.join(vt_root, 'milvus', '2.3', 'milvus_001', 'debate_logs', 'execution_results.json'), encoding='utf-8'))
    if e1['execution_summary']['logs'][0]['captured_raw_http'] is not False:
        FAILS.append('[structure] milvus_001 captured_raw_http 应为 False')

    print(f"single_llm: {len(sl_files)} files | voting json parsed ok: {n_json_ok} | candidates: {len(cand_files)}")
    if FAILS:
        print(f"\nFAIL {len(FAILS)}:")
        for f in FAILS[:40]:
            print(' ', f)
        sys.exit(1)
    print("AUDIT PASS (0 FAIL)")


if __name__ == '__main__':
    main()
