#!/usr/bin/env python3
"""生成 dev-reviewer 派发 prompt（run2/run3 多 run 复用，保证每次 prompt 一致）。

用法: python gen_dispatch.py <run> <vendor> <version> <num,num,...>
例:   python gen_dispatch.py run2 milvus 2.6.16 49823,49843,49844,49889,49890,49928
打印可直接粘进 Agent(general-purpose) 的 prompt。
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.dirname(os.path.dirname(ROOT))
SOP = r'C:/Users/11428/Desktop/testvdb4exp/agents/dev-reviewer.md'
VDB_SRC = r'C:/Users/11428/Desktop/vdb_src'

VENDOR_CFG = {
    'milvus': {
        'live': 'milvus gRPC localhost:19530 (pymilvus) + REST v2 http://localhost:19530/v2/vectordb',
        'probe_hint': '用 pymilvus (python `from pymilvus import MilvusClient`) 或 REST v2；创建唯一 collection 名如 repro_<num>',
        'env': '',
    },
    'qdrant': {
        'live': 'qdrant REST http://localhost:6333',
        'probe_hint': '用 curl 或 python requests 打 http://localhost:6333；创建唯一 collection 名如 repro_<num>',
        'env': '',
    },
    'weaviate': {
        'live': 'weaviate REST http://localhost:18080/v1',
        'probe_hint': '用 curl 或 python requests 打 http://localhost:18080/v1；创建唯一 class 名如 repro_<num>',
        'env': '环境变量 WEAVIATE_BASE=http://localhost:18080/v1',
    },
}


def tag_for(vendor, version):
    if vendor == 'milvus':
        return 'v2.3.22' if version == '2.3' else 'v' + version
    return 'v' + version


def main():
    run, vendor, version, nums_s = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    nums = [int(x) for x in nums_s.split(',')]
    cfg = VENDOR_CFG[vendor]
    tag = tag_for(vendor, version)
    clone = '%s/%s/%s' % (VDB_SRC, vendor, tag)
    run_root = '%s/.paperpilot/phase2-rerun/%s' % (PAPER.replace('\\', '/'), run)

    sessions = []
    for n in nums:
        sd = '%s/results/%s/%s/%d' % (run_root, vendor, version, n)
        sessions.append((n, sd))

    lines = []
    lines.append('你是 TestVDB 的 dev-reviewer（开发者视角终审 Agent）。第一步必须 Read SOP 并严格按其执行：')
    lines.append('  ' + SOP)
    lines.append('SOP 定义双盲 + 6 步审查（干净复现→前提审计→契约对照→源码接地→反向证伪→平凡排除→三视角聚合）与输出格式。务必逐条遵守：第1/4步必须 Bash 实际发请求；第3.5步必须 Grep 本地 clone 源码接地（无 source_excerpt=审查无效）；第6步三视角聚合按固定规则。')
    lines.append('')
    lines.append('本轮你审 %d 个候选（目标=%s，版本=%s），逐个独立审查。' % (len(nums), vendor, version))
    lines.append('')
    lines.append('【目标 DB 容器已 LIVE 运行】')
    lines.append('  ' + cfg['live'])
    if cfg['env']:
        lines.append('  ' + cfg['env'])
    lines.append('  复现/证伪：' + cfg['probe_hint'])
    lines.append('【源码 clone】%s （也写在每个 session 的 .srcdir 里）' % clone)
    lines.append('【版本契约】SESSION_DIR 上级目录的 structured_contract.json + api_templates.md')
    lines.append('【维护者认知】intelligence/%s/{developer_cognition,bug_shapes}.json（相对 %s 根）' % (vendor, run))
    lines.append('')
    lines.append('【候选 SESSION_DIR】（每个含 output_*.log=raw HTTP 事实源、debate_logs/stage2_aggregation.json=候选清单、.srcdir）')
    for n, sd in sessions:
        lines.append('  - %d : %s' % (n, sd))
    lines.append('')
    lines.append('【对每个 case】')
    lines.append('  Turn1 Read：stage2_aggregation.json（只取候选清单 defect_id/endpoint/defect_type，禁看 rationale）、developer_cognition.json、bug_shapes.json、structured_contract.json、api_templates.md、.srcdir')
    lines.append('  第1步复现+第4步证伪：Bash 实际对 LIVE 容器发请求（用唯一 collection/class 名 repro_<num> 避免冲突）；从 output_*.log 提取 raw 请求重建语义等价最小请求')
    lines.append('  第3.5步：Grep 源码 clone 做接地，深层源码片段(文件+行号)写入 source_grounding.source_excerpt')
    lines.append('  第6步三视角聚合 → final verdict')
    lines.append('  Write {SESSION_DIR}/debate_logs/dev_review.json（judge="dev-review"，格式见 SOP）+ Bash touch {SESSION_DIR}/debate_logs/dev_review.json.done')
    lines.append('')
    lines.append('【铁律】双盲：绝不读任何已存在的 dev_review*.json；绝不看 attack/probe 脚本 .py 源码。怀疑优先，举证责任在"证明真 bug"。各 case 独立，各写一份 dev_review.json。')
    lines.append('')
    lines.append('完成后仅用一行/case 汇报：<num> verdict=X conf=Y src=有/无。')
    print('\n'.join(lines))


if __name__ == '__main__':
    main()
