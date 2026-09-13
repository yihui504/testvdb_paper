# fix-PR 性质分析(A 类已修 bug)

日期:2026-09-05。数据:`results/fix_pr_analysis/fix_pr_details.json`(issue→PR 映射 + 每 PR files 分类);运行日志 `run.log`。
用途:论文 RQ1 "Fix nature" 段——回应"fixed 就一定是真 bug 吗";方法论与 9149 证伪交叉验证。

## 2026-09-05 晚间改判(用户拍板,触发本分析)

原 A 类 29 中的 6 个为**错账**(修复 PR 未 merge / 未修复),已改判 A→B(xlsx 备份 backup7):
- milvus#47763(未修复,PR #47782 closed-unmerged,labels 含 stale)→ TP_ACK_CLOSED_NOFIX
- weaviate#11399/11401/11730/11732/11741(修复未 merge)→ TP_ACK_OPEN
- weaviate#11400 例外:修复 PR **#11824 已 merged**(与 11729 同 PR 双修),保持 A

**改判后终态:A(=fixed)23 / B 28;submitted 81 / confirmed 51 / FP 30 不变。**

## 结论(终态)

| 性质 | issue 数 | 说明 |
|---|---|---|
| **真代码修复(可定位 merged PR)** | **23**(全部 fixed) | 全部改动实现代码;15 个 PR 同时带回归测试 |
| 文档-only 修复 | **0** | — |
| 测试-only 修复 | **0**(A 类内) | 见下"方法论验证" |

**代码+测试混合**(15 个):milvus 49890/49843/51084(×2)/52307/52309,qdrant 10120/9039/9045/9017/9421/9522/9942,weaviate 11729/12041/**11400(#11824)**。
**9942 澄清**:fix-PR #10324 标题是 `docs(schema):` 前缀,但实际 3 文件 = `lib/collection/src/operations/types.rs`(代码补校验)+ openapi.json + tests/openapi/test_limits.py——**真代码修复带文档同步**,非文档-only。

## 方法论验证(9149 交叉复现)

分类器对 qdrant#9178(issue **9149**,已被 phase3 证伪剔出 A 类)判 **test_only**:唯一文件 `tests/openapi/test_validation.py`,标题 "Add test to validate shard number and replication factor is positive"。与 phase3 七版本复验结论(fix-PR 实为补测试,非修复)**独立吻合**——该方法可直接作为 9149 处置的证据链一环。

## 已定位明细(23 issue → merged fix-PR)

milvus: 49843→#50731(code2+test1) · 49890→#50195(1+1) · 50355→(pr-evidence) · 51084→#51088+#51168 · 51085→(pr-evidence) · 52307→#52261 · 52309→#52346 · 52311/52313/52315/52325→(pr-evidence)
qdrant: 9017→#9320 · 9039→#9058 · 9045→#9070 · 9421→#9431 · 9522→#9531 · 9524→#9847(lib/segment/src/types.rs 单文件;注意 #9374 为 31-file 无关 feat 型干扰 PR,勿计入) · 9942→#10324(code+test+doc) · 10120→#10141 · 10373→#10382
weaviate: 11729→#11824 · **11400→#11824(同 PR 双修)** · 12041→#12049

(pr-evidence = 映射与分类来自 phase3 pr-evidence.json + 本次 files 拉取;明细见 JSON)

## 方法与坑(复跑必读)

1. **title 前缀不可靠**:9942 的修复 PR 前缀是 `docs(schema):` 但实为代码修复;9524 的关联 PR #9374 前缀 `feat:` 且 31 文件,是无关大 PR(干扰)。判定必须看 files。
2. **XREF + merged 双条件**:REST timeline 的 cross-referenced PR 须再查 merged(closed≠merged:47782/11429/11439/11543 均 closed-unmerged)。
3. **7 个未定位 issue** 的深挖路径(如需):GraphQL connectedEvent / 按文件 blame 溯源;本次收口不展开。
4. 9149(9178)是全数据集唯一 test_only——恰为已剔除案,佐证 A 类 29 内无"假修复"。
