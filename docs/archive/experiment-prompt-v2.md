# RQ2 实验集完整复测启动提示词（E6 插件版，71 case，2026-08-18）

将下面整段作为新会话开场。这是在 Phase 2 实验集上用 E6 版插件链路跑完整复测（v7 轮）。

---

在 Phase 2 实验集上跑 TestVDB E6 判定链路的完整复测（71 case，15 组）。

## 实验材料位置（全部已在盘）
- 实验集根: C:/Users/11428/Desktop/tvdb_sessions
- case 清单: C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/defect_id_map.json（71 case → vendor/version 映射）
- 真实 claim 锚: C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/packets/{orig_issue}.json 的 raw_observation 字段（packet claim 为空时用 cases_index.json 中该 issue 的 title）
- GT（仅主进程结束后对照用，过程禁读）: 同目录 cases_index.json 的 gt_label
- 旧轮判词（对照参考）: rq2_e6_verdicts.json 及各版本组 debate_logs/chain_verdicts_e*.json

## 执行流程（按版本组，共 15 组）
每组依次：
1. 容器: 在 C:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun 下 `python start_container.py {vendor} {version}` 等就绪
2. **builder 重建链**: 派 `testvdb:evidence-builder`（原生 agent，可用 gen_dispatch_v4.py 生成派发词或按其模板手写），每组 ≤6 case 一批
   - 材料: sessions/{vendor}/{version}/{did}/（output log + .srcdir）；契约同版本目录 structured_contract.json；源码 clone C:/Users/11428/Desktop/vdb_src/{vendor}/v{version}
   - **claim 锚程序化注入**：从 packets/{orig}.json 直读 raw_observation 原文放进派发词，禁止转述改写；packet 为空用 issue title
   - 产出: {SESSION_DIR}/evidence_chain/{did}.json 覆盖 + .done
3. **auditor 收口**: 派 `testvdb:chain-auditor`（原生），≤12 链/批
   - 会跑 check_chain_grounding.py（implied 四态）与 check_physical_constraints.py——采信不干预
   - 产出: {前缀}/debate_logs/chain_verdicts_v7.json + .done
4. **rework 闭环**: NME 带 rework_order 的 case → 重派 builder（携带工单原文）→ auditor 复审；同 did 最多 3 轮（计数 rq2_v7_rework_state.json），超限保守 NOT_DEFECT；CONFLICT case 必须走闭环不许跳过

## 铁律
- 全程派 testvdb 原生 agent（evidence-builder/chain-auditor），禁止普通 agent 代跑
- 派发词禁 GT/预期结论语言
- auditor 超批会被 SOP 拒（BATCH_LIMIT_EXCEEDED）——15 组天然分组，勿合并
- 判词 JSON 写完才 touch .done

## 完成后
71 case 全部出 verdict 后，主进程读 cases_index.json 的 gt_label 做对照，
算 TP/FP/FN/TN/NME + recall/precision/fp_supp，与 E6（0.793/0.852）和 fixF（0.621/0.818）
对比，落盘 rq2_v7_report.md + rq2_v7_verdicts.json。逐 case diff E6→v7 的翻转清单。

---
