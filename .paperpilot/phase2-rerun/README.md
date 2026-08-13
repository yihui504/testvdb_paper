# Phase 2 rerun 实验材料（复用指南）

> 本目录是 dev-reviewer 级 1:1 重做实验的全部材料。实验报告见 `docs/phase2-rerun-results.md`，终结果 `FINAL_RESULTS.json`。

## 目录结构

```
.paperpilot/phase2-rerun/
├── cases_index.json          # 71 scored case 索引(num/vendor/version/group/gt_label/title)，A28+B17+C26
├── contracts/                # 契约基
│   ├── {milvus,qdrant,weaviate}/{ver}.json   # 版本契约(7 现成 mftui 搬 + 9 派生 version_map)
│   ├── version_map.json      # 9 缺失版本→最近版本派生映射
│   └── segments/{vendor}_{num}.json  # 每 case 匹配的契约段(54 matched+17 gap)+_coverage.json
├── intel/{vendor}/{developer_cognition,bug_shapes}.json  # 维护者认知+根因(从 mftui 搬)
├── source_excerpts/          # (已废弃,主动模式下 dev-reviewer 自行 Grep) 70 found+1 not_found
├── packets/, judge_prompt.md # (已废弃,改用真 dev-reviewer)
├── run/                      # ★ dev-reviewer 实际读的文件布局(还原后的真实 pipeline 布局)
│   ├── results/{vendor}/{version}/structured_contract.json + api_templates.md  # 版本级
│   ├── intelligence/{vendor}/{developer_cognition,bug_shapes}.json
│   └── results/{vendor}/{version}/{num}/   # 每 case 一个 session
│       ├── .srcdir                          # 一行: 该版本 clone 路径
│       ├── output_{vendor}_{num}.log        # raw HTTP(E4 实验):探针执行输出
│       └── debate_logs/stage2_aggregation.json  # 候选清单(单样本,defect_id/endpoint/defect_type,无GT)
├── *.py                      # 脚本(见下)
├── FINAL_RESULTS.json        # ★ 终 metrics + FN/FP 清单
├── analysis_rows.json        # 逐 case verdict/conf/root/source(分析中间产物)
└── clone_all.sh              # 16 (vendor,tag) shallow clone→~/Desktop/vdb_src
```

## 关键脚本

| 脚本 | 作用 | 复用场景 |
|------|------|----------|
| `clone_all.sh` | shallow clone 16 版本源码到 `~/Desktop/vdb_src/{vendor}/{tag}` | 换机器重跑前先跑 |
| `layout_inputs.py` | 把现有产物摆进 `run/` 下 dev-reviewer 真实布局(契约/intel/.srcdir/stage2_aggregation) | 重建 run/ |
| `fill_endpoints.py` | 从探针脚本抽 endpoint 补 stage2_aggregation | layout 后跑(endpoint 对齐) |
| `run_probes.py <vendor> <version>` | 起对应版本容器+跑该版本 probe+生成 output_*.log(留容器供 dev-reviewer) | E1 实验期,逐版本 |
| `build_contract_segments.py` | 抽每 case 相关契约段(已用过,产物在 contracts/segments/) | 契约更新时重跑 |
| `source_excerpts.py` | (废弃)静态抽源码片段 |
| `audit_src_version.py` | 审 source 版本对不对得上 case 版本 | 质量审计 |
| `audit_inputs.py` | 审 endpoint 是否与实际流量对齐 + setup 健康 | 质量审计 |
| `extract_flip_cards.py` | 抽 flips 的复核卡(三视角/源码/rationale) | 定性复核 |
| `analyze_rerun.py` | 汇总 71 dev_review vs GT,算 recall/precision/FP-supp + flips | 每次 verdict 更新后重跑 |
| `find_dups.py` | 查重复 dev_review(清理用) | 排错 |

## 复现 dev-reviewer 判定（单 case）

1. 起 case 对应版本容器：`py run_probes.py <vendor> <version>`（留容器）
2. 派 dev-reviewer agent：
   ```
   Agent(subagent_type="general-purpose",
     prompt="Read C:/.../testvdb4exp/agents/dev-reviewer.md 作 SOP。
       SESSION_DIR=C:/.../phase2-rerun/run/results/<vendor>/<ver>/<num>,
       target/version, DB LIVE=http://localhost:<port>,
       TESTVDB_SRC_DIR=<clone路径>(读 .srcdir)。
       候选在 stage2_aggregation.json, 事实源 output_*.log。
       Write debate_logs/dev_review.json + touch .done。")
   ```
3. `py analyze_rerun.py` 重算 metrics。

## 端口/版本约定

- milvus 19530(REST /v2/vectordb, 需 etcd+minio infra, `run_probes.py` 自动起; 2.3→v2.3.22 镜像 fallback 已内置)
- qdrant 6333（简单 `docker run`）
- weaviate 18080(8080 被 dify 占,映射 18080,env WEAVIATE_BASE=http://localhost:18080/v1)

## 复用要点 / 已知坑

- **endpoint 抽取**：`fill_endpoints.py` 对 milvus REST 探针有偏差(常抽到 setup 操作)，复用前跑 `audit_inputs.py` 核 endpoint↔流量对齐。
- **SDK 探针无 raw**：milvus pymilvus 探针 `output_*.log` 可能为空(reqs=0)，dev-reviewer 靠 Step1 自己复现——派发时提示用 pymilvus 或 REST 等价复现。
- **测全路径**：dev-reviewer 可能只测一条路径(sync/REST)漏另一条(async/gRPC)，对"跨协议/跨模式"类缺陷需在 prompt 明确指定。
- **reported_version 来源**：`cases_index.json` 的 version_source 多为 None，A 组(已修)case 可能是 post-fix 版本(bug 已修不复现)——复用时注意。
- **源码 clone 路径**：`.srcdir` 指 `C:/Users/11428/Desktop/vdb_src/{vendor}/{tag}`，换机器需改 layout_inputs.py 的 VDB_SRC + 重跑 clone_all.sh。
