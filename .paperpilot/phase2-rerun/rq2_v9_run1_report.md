# RQ2 v9 首轮全量复测报告（2026-08-19）

## 口径

**最新版全量 71 案、无人值守、auditor 新会话判定**——与 v8 增量合并口径（v7.1 判词 + 11 定向重判）不同，
这是含全部 v8 材料变更（7 考古契约断言 + 4 认知锚点 + 最新机械脚本）下的全量复测：

- 15 版本组 auditor 并行判定（原生 testvdb:chain-auditor，≤12 链/批）
- 机械预跑注入（check_chain_grounding + check_physical_constraints，src_dir=源码 clone）
- claim 程序化传递（packet raw_observation 原文，零人工转述）
- leak_scan 15/15 PASS
- 7 NME 案 rework 闭环（builder 重做 + auditor 复审，最多 3 轮）

## 终态指标

| 口径 | recall | precision | f1 | fp_supp | TP/FP/FN/TN |
|------|--------|-----------|-----|---------|-------------|
| v7.x 三轮中位（论文 headline） | 0.705 [0.682,0.727] | 0.775 | — | — | — |
| v7.1 | 0.727 | 0.780 | — | 0.667 | 32/9/12/18 |
| v8 增量合并 | 0.886 | 0.867 | — | 0.778 | 39/6/5/21 |
| **v9 首轮全量+闭环** | **0.909** | **0.889** | **0.899** | **0.815** | **40/5/4/22** |

全量口径下 v8 的增益不仅复现，还更高（recall +0.023、precision +0.022、fp_supp +0.037 vs v8 增量）。

## rework 闭环明细（7 案，全部在 3 轮上限内闭合）

| case | GT | 首轮 | 闭环 | 工单类型 |
|------|----|------|------|---------|
| milvus_007 | FP | NME | NOT_DEFECT ✅ | 活体复现 5 组：声称现象不可复现，Plan.cpp 守卫在 REST v2 路径不可达 |
| milvus_018 | FP | NME | NOT_DEFECT ✅ | rename+create 双成功未复现；锚点 #50192 create 幂等适用 |
| milvus_019 | FP | NME | NOT_DEFECT ✅ | 测量通道校准：get_stats 是 flushed-only（#50193），query 通道 5=5 一致 |
| milvus_021 | FP | NME | NOT_DEFECT ✅ | quick-create 语义（#50319）；第2轮：hs_note 去否定语境裸词校准 |
| milvus_027 | FP | NME | NOT_DEFECT ✅ | 脚本嵌套错误：顶层 shardsNum 被 JSON binding 丢弃，0/-1/65535 未达服务器；第3轮：REQ/RESP 行级分离表述 |
| milvus_029 | TP | NME | DEFECT ✅ | 约束引用错位：limit/dim 值域校验生效（violates=false 正确），真信号=客户端错误以 2xx+业务码返回；契约无错误形态断言 → 去引用走灰区，B=CONFIRMED 定案 |
| qdrant_003 | FP | NME | NOT_DEFECT ✅ | score_threshold 无 range 校验注解，2.0 超出区间被过滤是 by-design FILTER 语义 |

## 与 v8 增量口径的差异归因

v8 0.886/0.867 → v9 全量 0.909/0.889 的构成：

1. **027 闭环成 TN**（v8 是 FP：auditor 误配维持 DEFECT）→ FP 6→5
2. **029 闭环成 TP**（v8 是悬置 FN）→ TP 39→40、FN 5→4
3. **qdrant_010 全量重判 TN**（v8 增量沿用 v7.1 的 FP 判词）
4. **新增 FP ×2（milvus_014/028）**：全量重判时机械 B 规则2（HTTP 语义恒真）在它们上触发——v8 增量口径未重判这两案，未暴露

## 重要发现：机械 B 规则2 的 FP 风险（014/028 vs 029 同族异 GT）

| case | 现象（机械 B 触发依据） | GT |
|------|------------------------|-----|
| milvus_029 | search limit=0 → HTTP 200+code65535 服务器自证 "topk [0] is invalid, should be in range [1,16384]" | CONFIRMED |
| milvus_014 | create dim=32769 → HTTP 200+code65535 服务器自证 "should be in range 2~32768" | FALSE_POSITIVE |
| milvus_028 | create dimension=32769 → HTTP 200+code65535 服务器自证 "should be in range 2~32768" | FALSE_POSITIVE |

三者客观现象完全同族（客户端参数错误以 HTTP 2xx+业务码返回、服务器错误消息自证值非法），
判定层一致判 DEFECT，但 GT 只有 029 认缺陷。两个解释方向：

- **GT 异质性**：014/028 的原 issue resolution 可能将 REST v2 统一 2xx 包装判为 not-a-bug（设计决定），
  029 的 issue 单独被认账——GT 层对同族现象态度不一（注：milvus_011 曾误记 GT 内部矛盾，2026-08-24 复核修正为锚点提取遗漏）
- **B 规则2 触发条件过宽**：规则2 的"契约声称应拒绝/服务器自证"条件无法区分
  "错误形态是缺陷"vs"统一 2xx 包装是设计"——若 REST v2 的 2xx+业务码是统一设计，
  该规则在 MILVUS REST v2 上系统性偏正

处置建议（待拍板，不进本轮）：
1. B 规则2 收紧：服务器自证分支要求"服务器错误消息自证 + 契约 doc_quote 明示 4xx 期望"双条件
2. 或认知锚点补充 REST v2 错误形态 by-design 锚点（若官方文档有统一 2xx 包装的明示）
3. 都不做则接受 precision 0.889（FP5 含 014/028 两案同族错判）

## 残余错误

- **FN 4**：violates 误标族 ×4（001/003/004/024）——与 v7.x/v8 同族，判定层无米之炊
  （链 violates=false 且无独立机械信号，契约缺断言）
- **FP 5**：
  - milvus_011：认知锚点提取遗漏（维护者 MrPresent-Han 2026-06-23 复查否定修复：missing filter≡empty filter 为兼容性设计、revert filter-required PR，2026-08-03 stale 关闭——GT=FP 正确，2026-08-24 复核修正）
  - milvus_014/028：B 规则2 同族错判（见上）
  - qdrant_009 / weaviate_009：无 by-design 明示标签（v8 保守边界维持）

## 执行记录

- 派发词：.paperpilot/phase2-rerun/dispatch_v9/（15 组 auditor + 7 首轮 rework + 3 二轮 + 1 三轮工单）
- 判词：tvdb_sessions/sessions/*/*/debate_logs/chain_verdicts_v9.json（首轮）、
  _v9_r.json（复审）、_v9_r2.json（终审）
- 机械脚本与 SOP：插件 cache 2.3.0（与 mftui/TestVDB 同步确认）

## 下一步

1. **三轮方差复测**（v9 同协议再跑两轮）→ 中位数字才可进论文（v7.x 先例：单轮 0.727，
   三轮中位 0.705 [0.682,0.727] 带宽 0.045）
2. B 规则2 FP 风险三选一决策（收紧/锚点/接受）
3. 论文口径建议不变：headline 用无注入 v7.x 三轮中位，v9 全量作为"文档考古+锚点+闭环"
   ablation 呈现（GT-informed 注入披露）
