# 答辩话术 / Rebuttal Snippets

> 遇到质疑时怎么答。每条：**触发问题 → 核心策略 → 可直接说的话**。
> 持续补充；组会 / 审稿 rebuttal 直接取用。

---

## 1. "加 threat-model 并集不是更好吗？"（组会老师已问 ✅）

**核心策略**：先认对（数据上 union 确实更好）→ 重框 claim（不是"source 最优"，是"必须有独立 truth 信号"）→ 解释 threat 不成熟 + 列 future work。**不嘴硬。**

**可说的话**：
> 老师说得对，并集 11/12 确实比 source 单独 9/12 好。但这恰恰是我们框架预期的——核心不是"source 最好"，而是"LLM 的合规判断必须有独立于它的 truth 信号来证伪"。threat-model 是另一个 truth 信号，和 source 各抓一类 FP（source 抓 state/concurrency，threat 抓 boundary-default），互补说得通。
> 但 threat 现在不成熟：state/concurrency 上过火、run 间不稳定、n=12 太小（11/12 vs 9/12 统计上分不开）。所以诚实标成 exploratory。把 threat 做稳定是明确 future work——做稳了多 anchor union 确实更强，但那是改进方向，不是现在的贡献。

---

## 2. "CTS 不就是查源码的 agent？/ 这词造得不明觉厉"（组会老师已反馈 ✅）

**核心策略**：**例子先行，不先抛大词**；把"分离"当 design observation 讲，不当专有招牌。命名按 B1 第三条路（方法描述性 + framing 讲分离原则）。

**可说的话**（待 B1 拍板后定稿）：
> [先用 constant.go 故事] 我们的 formalizer 从 `constant.go`「提取」了一条复杂度要求当契约，judge 随即确认了好几个「违规 bug」。查源码发现那常量是防一次历史性能回退的 guard，根本不是行为约束。
> [让听众顿悟] 造契约的和判合规的是**同一个 LLM 家族**，造错了，判的时候不会发现自己的错——自我包庇。我们叫这个 contract hallucination propagation。
> [方法朴实] 怎么治？加一个独立的、只信源码的审稿去推翻它。就这一步，误报压制 31% → 81%。

---

## 3. "凭什么 LLM 是唯一 oracle？排除法太草率"（预判审稿人会问）

**核心策略**：用 **oracle taxonomy（Barr 2015）逐类排除**，不靠"排除法"四个字蒙混。弹药见 [glossary.md](glossary.md)「oracle taxonomy」节。

**可说的话**：
> oracle 分四类。合规缺陷：specified（文档契约）可能错（contract hallucination）；derivable（数学不变量）只覆盖 cos>1 这种子集；implicit（differential / metamorphic）不适用——differential 要 reference impl 而 VDB API 跨厂商无统一语义，metamorphic 要可变换的等价查询形式而合规是 accept/reject 是非判断。所以剩下只能靠 LLM 做语义判断。

---

## 4. "独创性在哪？多 agent debate / 查源码降假阳性都不是你首创"

**核心策略**：**换尺子**。你是"实证系统 + 洞察"型，不是"方法创新"型。别在机制维度比。

**可说的话**：
> 机制上多 agent debate、查源码确实不新，我们也没 claim 首创（都 cite 了）。我们的贡献是：识别出 **contract hallucination propagation** 这个失败模式（在 testing 场景无先例形式化），给了一个有原则的应对（assertion/truth 分离 + source-grounded falsification），加上 5 库 111 缺陷 / 36 维护者承认的实证。卖点是 real-world impact + insight，不是新机制。

---

## 5. reproduction anchor 实验结果（2026-07-15 跑完，C3）

**结果**（干净 setup，N=5，milvus v2.6.19，`TestVDB/scripts/reproduction_anchor_results.json`）：
- tooling_artifact: reproduction **KILL 12/12**（重审后；原 12/14——C15/C27 重审移到 by-design）
- by_design: reproduction **误判 11/13**（含重审移入的 C15/C27；reproduction 对 code=0 接受行为失效）
- unstable: 0

**达标表述**（可写进论文，dev-reviewer 升级为多 anchor 按 FP 成因分工）：
> dev-reviewer 的多 anchor 按 FP 成因分工：source-grounding 反 contract hallucination / by-design（validated，31%→81%），reproduction 反 tooling artifact（脚本误读响应，独立 kill 12/14），threat-model 补 boundary-default 残余（exploratory）。reproduction 的独立价值是不查源码、纯 live 复现 + 补全参数（outputFields）抓脚本误读，作 source 的独立兜底。

**必须诚实报告的边界**（否则审稿人抓）：
1. **reproduction 对「live 返回 code=0 的接受行为」统一失效**——不论 by-design（upsert/idempotent/dynamic，9/11 误判）还是 tooling（C15 metric invalid / C27 not-loaded，live 均 code=0 → MISS）。**reproduction 不能替代 source**（source 才能判 by-design）。
2. **C15/C27 已重审为 by-design silent fallback**（非 CORRECT_REJECT，2026-07-15 live 验证）：milvus v2.6.19 **完全忽略 search 的 metricType 参数**（L2/INVALID/IP/COSINE/空 全返回相同距离 [0,8,8]）且**允许 not-loaded search 返回数据**——与 q3/q37 同类（contract hallucination）。仍是 FP（27 killed ground-truth 不变，论文 45.6%/69.2% 不受影响），但归类从 tooling 移到 by-design。**副产品**：milvus 忽略 search metricType 是独立 by-design 行为（search 用 collection metric，不 override）。
3. **D20-23 的 kill 依赖「补全 outputFields」判据**（dev-reviewer.md 第1步「补全必要参数」）——合理，但要写清楚。

**副产品确认**：诊断证实 `get_stats` rowCount 在 insert 成功后仍滞后（search 能查到但 rowCount=0）——**验证 q12/state_001 类 FP 根因是 milvus 异步聚合，不是 oracle 脚本 bug**。论文该 case 站得住。
