# single-LLM 臂预注册（跑前定稿）

日期：2026-08-16 | Run 标识：**arm-sl-{runN}**（run1 起）| 用户拍板：可并行跑，先跑本臂

## 1. 定义

single-LLM = 相同材料（71 case 冻结包）+ **无任何工具**，一次纯调用出 CONFIRMED / FALSE_POSITIVE。
对照臂：voting（4 judge + 代码聚合，待跑）、dev-reviewer（fixF 三轮，已有）。
材料面 = voting 阶段 judge 的本地可见面（头部 + observed[摘要+log 全文+VERDICT:UNKNOWN 行] + expected[契约超集]）。

## 2. 运行纪律（对齐 fixF 系列）

- 模型 GLM-5.2 标准档；每 case 独立调用（新会话语义）
- **禁工具**：不 Bash/不 Read 文件/不联网——材料全文内联进 prompt，一次调用即判
- 材料顺序：materials/{did}.md 原文逐字内联，不增删
- 3 轮（run1/run2/run3），每轮全量 71 case；落 `arms/single_llm/run{N}/verdicts/{did}.json`
- milvus_001：log 为占位符——照常判（材料面如实呈现"无原始 HTTP"），与另两臂同口径

## 3. 判定 prompt 模板（冻结）

```
你是数据库缺陷判定审查员。以下是一个候选缺陷的完整材料（观察到的行为 + 契约依据）。
基于且仅基于材料判断：该候选描述的是否为真实缺陷（CONFIRMED）或误报（FALSE_POSITIVE）。

规则：
- 只依据材料内容判断，不假设材料之外的信息
- 契约依据是 expected 的参考；若契约条目与候选 endpoint 无关，忽略之
- 材料中 VERDICT: UNKNOWN 行表示重放捕获无上游断言输出，非判定线索
- 无契约依据时按观察行为本身评估

输出 JSON：{"defect_id": "...", "verdict": "CONFIRMED|FALSE_POSITIVE", "confidence": 0.0-1.0, "rationale": "一句话理由"}
只输出 JSON。

【材料开始】
{materials/{did}.md 全文}
【材料结束】
```

## 4. 预注册判据（描述性，跑前写死）

1. **三指标三轮带**（分母 44 真 / C 组 27）：recall / fp_supp / precision 区间 + 中位数；
   预期带：recall 0.45-0.75（无工具无源码，锚点缺失 → 预期低于 fixF 中位 0.659），
   fp_supp 0.40-0.80（C 组判 FP 靠契约对照，无工具下不确定度大）
2. **vs dev-reviewer**：paired per-case 比较（McNemar），重点看 tool 使用（源码接地+实跑）的增量
3. **vs voting**（voting 臂跑后补）：同输入不同架构的差分
4. **轮间 κ**：与 fixF 轮间 κ(0.187-0.486) 对比——纯调用是否比方差更稳
5. **超集稀释分层**：按 case 抽到约束条数分桶（0-4 / 5-11 / 12+）看 fp_supp 差异
6. **无 expected 依据 case**（qdrant_014/018）：单独报告落点
7. **锚点不可达类**：顽固 FN 5（001/009/012/q002/q014）预期仍漏（无态度通道）；结构性取证类
   （008/017/009/q002 在 fixF 系翻正过的）看无源码下是否回落 F

## 5. 产物

- run{N}/verdicts/{did}.json ×71 ×3 轮
- 汇总：arm-sl-RESULTS.json + ARM_SL_REPORT.md（三轮后）
