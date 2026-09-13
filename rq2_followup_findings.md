# 两追问的查证结论（2026-08-18）

## 追问 1：upsert-autoID 文档被修复了，能找修复前版本吗？——找到了，且时间线完全咬合

**时间线**：
- 契约生成（cached_at）：2026-06-06
- issue #50355 创建：2026-06-07
- 文档修复 commit `12acf1cb` "Clarify upsert behavior with autoID"：**2026-06-08（issue 次日）**
- 契约抓的正是**修复前版本**（99af7351，2026-05-14 现行版）——版本没错位

**修复前原文**（issue 时期现行版，即契约生成时应提取的声称）：
> "If the target collection has `autoid` enabled on its primary field, Milvus will
> generate a new primary key for the data carried in the request payload before
> inserting it."

**修复后**（12acf1cb，改口）：
> "If the target collection has `autoID` enabled on its primary field, the `upsert`
> request **must still include the primary key** of the target entity..."

——维护者没有修代码，而是**改文档**使其符合实现（upsert 仍需 PK）。GT 判 TP 的依据
正是修复前的声称被违反。

**结论**：031 归因修正——不是"契约缺断言"这么简单，是 **contract-formalizer 提取遗漏**
（修复前文档明确有此声称，cached_at 在修复前一天，材料在位但没提进契约）。
这是 RQ1 管线的 Step 1 缺陷（概念文档必抓清单里 upsert-entities.md 的关键声称漏提），
也再次呼应了 milvus v3.0.0 的历史教训（83 个 api-ref 0 概念文档 → 幻觉约束）。

**可修**：契约补此断言（引修复前文档原文 + source_url 锚到 99af7351 版本快照）后，
031 链 violates=True → 机械 A=CONFIRMED → implied DEFECT。属"契约补提取"族的实证首例。

## 追问 2：被机械层锁死（004/006）能否改进机械层？——部分能，但这两案不行

**机械层可改进点（已识别）**：
1. **信号冲突降级**：violates=False（REFUTED）但机械 B=CONFIRMED → 降 GREY_ZONE
   交 LLM 仲裁，而非锁死（A 与 B 独立证据源冲突时机械层不该单方定案）——架构上可行，
   但需回测确认不引入翻错
2. **violates 双通道复核**：violates 是 builder 声明的语义事实，机械层无条件信任。
   可加机械复核——log 观测"值被接受"（200+code:0/accepted）+ quote 含数值/类型
   约束 → violates 应为 True 的模式检查，不符 → 打回 builder（rework 已有通道）

**004/006 为什么救不了**（逐案验证）：
- 机械 B 均 NOT_TRIGGERED（无服务器自证：静默接受 200+code:0；无 null/负值/挂起模式）
- 006 链审错现象（审了字段名合法性，GT 认的是类型强转）= claim 漂移，证据本身错位
- 004 的降序区间 [10,5] 是语义灰区（语法合法的空集表达式）
- 两案的违规信号都不在机械可识别模式内——**改进机械层的正确路径是先修链（claim 对准）
  再谈判定**，否则机械层是在错误证据上加速

## 综合建议

1. 031：走契约补提取（实证首例：文档修复前声称 + 版本快照锚定）→ 修链 → 预期 +1 TP
2. 机械层两项改进（信号冲突降级 / violates 复核）值得做但先小实验回测——建议排在
   契约补提取之后（031 案验证"上游修对后机械层自然吃进"的路径优先）
