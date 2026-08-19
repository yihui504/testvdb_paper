#!/usr/bin/env python3
"""gen_dispatch_v3 — RQ2 新链路派发器（ADR-0008 evidence-builder + chain-auditor，2026-08-17）。

背景：导师 v3.1 反馈要求 RQ2 用 Phase 2 实验集（71 case + GT 44）做载体，被测判定者
从旧 dev-reviewer（单 agent 6 步 SOP）换成新链路（builder 取证 + auditor 收口）。
本脚本生成 v3 派发 prompt——材料包/容器/源码 clone 与 v2 完全同源，仅判定链路不同。

与 v2 的差异（审计要点）：
- SOP 引用 agents/evidence-builder.md + agents/chain-auditor.md（主插件 ADR-0008 版）
- 产出 evidence_chain/{defect_id}.json（builder）→ debate_logs/chain_verdicts.json（auditor）
- 判定者不再读 stage2_aggregation rationale（v2 也禁；v3 仍禁——双盲保留）
- fp_evidence_source（doc/source/both/behavior）+ root_cause 是 RQ2 核心产出字段

用法: python gen_dispatch_v3.py <vendor> <version> <defect_id[,defect_id...]> [--builders|--auditor]
  默认 --builders（fan-out 派发单 case builder prompt × N）
  --auditor 生成收口 prompt（对该 vendor/version 的全部已建链）
"""
import os
import sys

V2 = r'C:/Users/11428/Desktop/tvdb_sessions'
VDB_SRC = r'C:/Users/11428/Desktop/vdb_src'
PLUGIN = r'C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0'
BUILDER_SOP = PLUGIN + r'/agents/evidence-builder.md'
AUDITOR_SOP = PLUGIN + r'/agents/chain-auditor.md'

VENDOR_CFG = {
    'milvus': {
        'live': 'milvus gRPC localhost:19530 (pymilvus) + REST v2 http://localhost:19530/v2/vectordb',
        'env': '',
    },
    'qdrant': {
        'live': 'qdrant REST http://localhost:6333',
        'env': '',
    },
    'weaviate': {
        'live': 'weaviate REST http://localhost:18080/v1',
        'env': '环境变量 WEAVIATE_BASE=http://localhost:18080/v1',
    },
}

BUILDER_TMPL = """你是 TestVDB 的 **evidence-builder（证据链构建 Agent，ADR-0008）**。

## 第一步：读 SOP
Read 并严格按其执行：{SOP}

SOP = step1（文档验证四层 + 执行证据审查 + 证据链追溯）+ step2（源码搜证）。
你不是判定者——只收集并写实证据，不产真伪结论。产出 evidence_chain/{{defect_id}}.json 六节 schema。

## 硬约束
- 禁止读 attack/probe 脚本 .py 源码（双盲核心）。
- step2 源码搜证必须 Grep 本地 clone（.srcdir 路径），source_excerpt 非空（not_found_in_source 除外）。
- 禁止使用 Agent 工具派发子 agent；所有工作用 Read/Bash/Grep/Glob/WebFetch/Write 直接完成。
- 每条证据含 evidence_source 标注（doc / source / behavior）。

## 材料定位
- SESSION_DIR: {sess}（含 output_*.log、debate_logs/stage2_aggregation.json 只取候选清单字段、.srcdir）
- 契约: {contract}（该版本 structured_contract.json）
- 源码 clone: {clone}

## 你的候选
defect_id={did}

Write {sess}/evidence_chain/{did}.json 后 Bash touch {sess}/evidence_chain/{did}.json.done。
完成后一行汇报：{did} doc=<VERIFIED/PARTIAL/MISMATCH> grade=<A-D> chain=<断点或null> src=<outcome>。"""

AUDITOR_TMPL = """你是 TestVDB 的 **chain-auditor（证据链审计 Agent，ADR-0008）**。

## 第一步：读 SOP
Read 并严格按其执行：{SOP}

SOP = 三查（完备性/一致性/自洽性）+ 三视角聚合（契约/物理压倒行为优雅，固定规则）。
你只读证据链文件与契约（引证核对），不做取证，禁读 attack 脚本源码。
启动先做 #9255 回归自检。

## 材料定位
- SESSION_DIR 前缀: {sess_root}（各 case 子目录 evidence_chain/）
- 契约: {contract}
- 候选清单（本次审计对象）:
{did_lines}

## 产出
Write {out}（verdicts[] + summary 含 fp_evidence_source_distribution + root_cause_distribution）
后 Bash touch {out}.done。verdict ∈ {{DEFECT, NOT_DEFECT, NEEDS_MORE_EVIDENCE}}；
NOT_DEFECT 必填 fp_evidence_source（doc/source/both/behavior）与 root_cause（词表见 SOP）。
完成后一行/case 汇报：<defect_id> verdict=… fp_src=… root_cause=…。"""


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    mode = 'builders' if '--auditor' not in sys.argv else 'auditor'
    vendor, version, dids_s = args[0], args[1], args[2]
    dids = dids_s.split(',')
    cfg = VENDOR_CFG[vendor]
    sess_root = '%s/sessions/%s/%s' % (V2, vendor, version)
    contract = '%s/structured_contract.json' % sess_root
    clone = '%s/%s/%s' % (VDB_SRC, vendor, tag_for(vendor, version))

    if mode == 'builders':
        for did in dids:
            sess = '%s/%s' % (sess_root, did)
            print(BUILDER_TMPL.format(SOP=BUILDER_SOP, sess=sess, contract=contract,
                                      clone=clone, did=did))
            print('\n' + '═' * 60 + '\n')
    else:
        did_lines = '\n'.join('  - %s (%s/%s/evidence_chain/)' % (d, sess_root, d) for d in dids)
        out = '%s/debate_logs/chain_verdicts.json' % sess_root
        print(AUDITOR_TMPL.format(SOP=AUDITOR_SOP, sess_root=sess_root, contract=contract,
                                  did_lines=did_lines, out=out))
        print('\n【目标 DB 容器已运行】\n  ' + cfg['live'])
        if cfg['env']:
            print('  ' + cfg['env'])


if __name__ == '__main__':
    main()
