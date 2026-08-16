# voting 臂预注册（跑前定稿）

日期：2026-08-16 | Run 标识：**arm-vt-{runN}**（run1 起）| 用户拍板：首轮后检查，无超预期问题续跑满 3 轮

## 1. 定义

voting 臂 = TestVDB as-shipped 判定架构（pre-devreviewer 阶段）：4 专责 judge
（doc → evidence / severity / novelty）+ `aggregate_votes.py` 代码化级联聚合。
**不是多数投票**——是级联闸门（聚合器规则 0-6，机制快照见 §6）。

对照臂：single-LLM（同材料纯调用，已完成）、dev-reviewer（fixF，已有）。

材料面 = 与 single-LLM 臂严格同源（audit 0 FAIL 冻结包），分槽到 judge 输入位：
- judge-doc：candidates/{did}.json + 版本目录 structured_contract.json + raw_knowledge.md
- judge-evidence：stage2_doc.json + debate_logs/execution_results.json + output_{did}.log
- judge-severity：stage2_doc.json + stage2_evidence.json + output_{did}.log
- judge-novelty：stage2_doc.json

## 2. 运行纪律

- 模型 GLM-5.2 标准档；**novelty / doc judge 关网**（GT 泄露防护，走 SOP 自带降级路径）；
  evidence/severity 只读本地（无网无容器）
- **doc/novelty 关网 = 代码直出确定降级产出**（SOP L221 / L176-178 规则确定，无 LLM 自由度：
  doc 全部 DOC_PARTIAL；novelty 全部 novelty_rating=unknown + vote=is_defect）。
  LLM 判定面 = evidence + severity 两 judge ×71。让 LLM 复读确定规约只会引入采样噪声，
  代码直出是 SOP 降级路径的最严格执行（记录为设计决策，非 deviation）
- 每 case 一个 session 目录（`voting/sessions/{vendor}/{version}/{did}/`），4 judge
  按 as-shipped 依赖顺序执行：doc → evidence → severity → novelty，各自独立输入面
- 每 judge 产出按 SOP schema 写 `debate_logs/stage2_{doc,evidence,severity,novelty}.json`
- 聚合 = 原版 `aggregate_votes.py`（逐 case 调用，target=vendor；无 intelligence 目录
  → by_design 白名单仅硬编码项，与预扫描口径一致）
- 3 轮；判定 = stage2_aggregation.json 的 confirmed/rejected 映射
  （confirmed→CONFIRMED，rejected→FALSE_POSITIVE）

## 3. 确定性路径（跑前预判，违反=执行缺陷而非实验结果）

1. **规则 0 崩溃旁路**：预扫描 71 log，恰 2 case 命中（qdrant_014/weaviate_010
   均 'status: 500'）→ 聚合必 confirmed（crash_auto_confirmed，不经 LLM）
2. **doc 关网降级**（SOP L221）：全部 unverifiable → 综合降 **DOC_PARTIAL ×71**（代码直出）。
   跑前实测查表：验证 1-3/5 全依赖网络（降级 unverifiable）；验证 4 查表 59/71 命中
   （12 未中 = qdrant 'points' 短名 6 + weaviate REST 路径形态 6，联网补充也关网 →
   unverifiable）→ 全 case 至少一项 PARTIAL/ unverifiable，综合表 PARTIAL 行成立；
   **DOC_MISMATCH 不应出现**（表 L147-151 各 MISMATCH 行均需某验证 FAIL，
   关网下唯一 FAIL 通道是"无 source_url"，而 candidates 均带契约 source_url → 不触发）
3. **novelty 关网**（SOP L176-178）：全 unknown → 全 vote=is_defect → 无否决、无 already_reported
4. **severity 覆盖口径**：SOP 字面"全部 DOC_VERIFIED" vs 实测（mftui round3 真实产出：
   severity 覆盖 VERIFIED+PARTIAL 全部）——**取实测口径**：评 doc 产出全部非 MISMATCH 候选
5. **evidence 单脚本门槛**（SOP L89-102）：仅 1 脚本触发 + Type2/低成功率组合 → 强制
   not_defect；replay 证据形态（无 FAILED 标记，见 VERDICT: UNKNOWN 行）下
   "PASSED 且无 FAILED → not_defect" 与 "日志为空→not_defect" 规则可能大规模触发，
   这属 as-shipped 行为，如实记录

## 4. 预注册判据（跑前写死）

1. **三指标三轮带**（分母 44 真 / C 组 27）：recall 预期 **0.25-0.65**
   （崩溃旁路保底 2/44≈0.045 + evidence 语义匹配翻正；evidence 闸门保守 → 低于 single-LLM 0.422 中位也可能），
   fp_supp 预期 **0.30-0.85**（级联闸门方向不确定：severity trivial 拒 + evidence not_defect 拒会压 FP，
   但 DOC_PARTIAL -1 级会放大 trivial 化），precision 区间报告。
   **级联放大效应预判**：doc 全 DOC_PARTIAL → severity 全 -1 级 → 聚合再 -1（规则 6）
   = 双重降级；基线 Medium 以下（Type2/元数据面/单脚本）全部降到 trivial → 拒。
   预期 recall 下压、fp_supp 上抬——若实测反之（recall 高/fp_supp 低），定性为超预期发现
2. **vs single-LLM**（McNemar paired）：同材料不同架构差分——级联 vs 纯调用的保守度差异
3. **vs dev-reviewer**（fixF）：三臂收口对比
4. **轮间 κ**：预期与 fixF/sl 同量级（0.19-0.49）；若显著更高 → 假说：
   确定性成分（崩溃旁路+代码聚合）压缩了采样方差
5. **崩溃旁路 2 case 单列**：qdrant_014/weaviate_010 应全轮 confirmed（GT=真缺陷）→
   recall 保底贡献；weaviate_010 与 sl 臂 FFF 锁死的三臂对照
6. **无 expected 依据 case**（qdrant_014/018）：014 走崩溃旁路（与契约无关），
   018 无契约无崩溃信号 → evidence/severity 纯行为判定，单独报告
7. **确定性路径核查**（§3 全 5 项）：run1 后逐项核对，违反项定性为执行缺陷

## 5. 产物

- run{N}/ 下：judge 产出快照 + stage2_aggregation.json ×71 + dispatch_log
- 汇总：ARM_VT_REPORT.md（三轮后）+ 跨臂合成表（RQ2）

## 6. 机制快照（2026-08-16 冻结）

- `testvdb4exp/scripts/aggregate_votes.py`
  SHA-256: f1d0a519ce9ea28cf672f115e7251e49d58ce8c01d74db4ab8d99ebf9e4c11a9
- 级联顺序：规则 0 崩溃自动确认（纯子串匹配，含 by_design 白名单短路）→
  规则 4 novelty not_defect 否决 → 规则 1 evidence 闸门 → 规则 6 doc 降级
  （MISMATCH -2 / PARTIAL -1，ladder trivial→critical）→ 规则 2 severity 缺失拒 →
  规则 3 trivial 拒 → confirmed
- 已知偏差（记 deviations）：judge SOP 原配 model=sonnet → 统一 GLM-5.2；
  doc/novelty 关网（原设计联网）；SOP 版本 = 仓库当前 HEAD
