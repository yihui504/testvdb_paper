"""Prepare rerun_v3 (corrected): dispatch files aligned with the REAL plugin
2.5.0 chain-auditor protocol (agents/chain-auditor.md), not a reconstruction.

Key alignments:
  - four perspectives as implemented: A contract / B physical (objective
    constraint classes, no contract endorsement needed) / C behavioral
    elegance (explicit by-design ONLY) / D maintainer cognition
  - A=CONFIRMED is not overturnable by source arguments
  - bare structural inference is WEAK_REFUTED -> human channel
  - human channel (NEEDS_MORE_EVIDENCE) counts as CONFIRMED in the study
    aggregation (user decision 2026-09-12:宁可误报不错杀)
core arm stays on rerun_v2 (contract-only, protocol-invariant).
"""
import glob
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/arms/rq2_3run"
V2 = ROOT + "/rerun_v2"
V3 = ROOT + "/rerun_v3"
ARMS = ["run_full1", "run_full2", "run_full3",
        "run_flat1", "run_flat2", "run_flat3",
        "run_donly1", "run_donly2", "run_donly3",
        "run_donlyq1", "run_donlyq2", "run_donlyq3"]

# ---------------- shared red lines (verbatim-aligned with chain-auditor.md)
REDLINES = """
## 判定红线(v3 协议,2026-09-12,与插件 2.5.0 chain-auditor 对齐)
1. **A=CONFIRMED 不可被推翻**:一旦包内契约断言被观察明确违反,终判即为 CONFIRMED——即使你认为源码表明该行为有意、或契约已过时(实测中 LLM 以源码理由推翻 A=CONFIRMED 曾致 5 个真缺陷丢失,此为违规)。对源码与契约冲突的正确处理是:在 rationale 记录怀疑,交给 C/D 视角标准裁决,不改变终判。
2. **"实现与观察一致"不构成非缺陷证据**:documentation-implementation 缺陷的参照系是文档 vs 实现,不是实现 vs 观察。仅凭"源码里就是这样写的"判 FALSE_POSITIVE 是违规。
3. **by-design 仅认明文**:只有当源码摘录包含意图证据(代码注释/文档字符串,如 `// intentionally` / `by design` / `we don't guarantee` 类)或维护者认知材料中的 developer_quote 明确声明同类现象非缺陷时,才可判 by-design。**裸的"它就这样行为/没看到校验/无注释的静默行为"不构成 by-design**——这种判定记为 WEAK_REFUTED。
4. **WEAK_REFUTED/证据不足 → 转人工(HUMAN_REVIEW),禁止静默过滤**(这是实测中真缺陷被误筛的主通道)。
5. **verdict 三值**:`CONFIRMED | FALSE_POSITIVE | HUMAN_REVIEW`。HUMAN_REVIEW 在本研究口径下**计入 CONFIRMED**(宁可误报、不可错过真缺陷;人工审核为该判定的默认后续动作)。
"""

# ---------------- full arm: real four-perspective structure
FULL_PROTOCOL = """
## 四视角(与插件 2.5.0 chain-auditor 同构;每案逐一评估)

**A 契约**:包内契约断言是否被观察明确违反?逐字比对断言文本与观察行为面(机械包含性检查)。判定依据只能来自包内契约行;源码意见不得进入 A 的判定。

**B 物理(客观约束,优先级最高;以下七类Violation 不需要包内契约背书)**:
- 数值下界:count/size/parallelism/limit 类参数接受负数或 0(客观违反;注意 ef/nprobe 类 HNSW 参数的 by-design 负哨兵先例——若源码有明文注释说明 -1/-0 为哨兵值则不触发)
- 枚举闭集:参数值域为有限集合(metricType/consistencyLevel 类),接受集合外值
- 互斥参数:文档/语义上互斥的参数被一起接受
- 类型套套逻辑:数值字段接受非数值,向量字段接受标量
- 同族不一致:同一端点同类违反值,一族被拒绝另一族静默替换默认值返回成功
- 接口不对称:同一参数同一违反值在 REST/gRPC/SDK 面上一个拒绝另一个接受(契约明示的面差异除外)
- HTTP 语义(强限定,须同时满足):①错误是请求侧可判定的(参数校验类)②契约/文档对该错误响应形态有承诺(示例为 4xx 或断言明说 invalid → reject),而实测为 2xx+业务错误码
执行记录显示 API 接受违反值 → B=CONFIRMED;参数不属于任何客观约束类 → B=NEUTRAL(rationale 须说明为何不属于)。**禁止因契约链断裂而连带判 B=NEUTRAL——视角独立;A 缺材料躺平时,B 是最后一道客观防线。**

**C 行为优雅性(权重 LOW;不能单独推翻 A/B)**:仅**明文 by-design** 可 REFUTE——"明文"指源码摘录含意图证据(代码注释/文档字符串),或认知材料 developer_quote 明确声明同类现象非缺陷。裸"它就这样行为/无注释的静默行为"→ **WEAK_REFUTED**(转人工,禁止静默过滤);优雅但无源码证据 → WEAK_REFUTED;行为不优雅 → CONFIRMED。

**D 维护者认知**:Read 认知材料(milvus/qdrant/weaviate 三库各一,路径见材料清单)。认知是维护者态度的陈述,不是证据——禁止用认知填补链上缺失的执行观察;禁止跨库引用;命中必须是现象级匹配(参数类/行为类同构),不是字面词重叠。
- `blindspot_indicators` 命中 → SUPPORTS_DEFECT(维护者已知盲区——同类现象曾被修复)
- `by_design_patterns`/`rejection_patterns` 命中 → SUPPORTS_NOT_DEFECT(必须引用 developer_quote 与 pattern_id)
- 无命中 → NO_SIGNAL

## 聚合(固定,与插件一致)
- A=CONFIRMED → **CONFIRMED**(不可推翻)
- A=REFUTED → **FALSE_POSITIVE**(fp 依据记 doc)
- A=REFUTED 但 B=CONFIRMED(信号冲突)→ **HUMAN_REVIEW**(契约引用可能错位)
- A=NEUTRAL(GREY_ZONE)时:
  - B=CONFIRMED → **CONFIRMED**
  - D=SUPPORTS_DEFECT → **CONFIRMED**(链上须有实质违反观察)
  - D=SUPPORTS_NOT_DEFECT → **FALSE_POSITIVE**
  - B=NEUTRAL 且 D=NO_SIGNAL:
    - C=REFUTED(满足明文标准)→ **FALSE_POSITIVE**
    - C=WEAK_REFUTED → **HUMAN_REVIEW**
    - 其余 → **HUMAN_REVIEW**(保守)
""" + REDLINES

# ---------------- donly/donlyq: perspective-C forensics standalone
DONLY_PROTOCOL = """
## 源码取证判定规则(v3 协议,与插件 2.5.0 C 视角+客观约束标准对齐)
你做的是独立的源码取证单视角。对每案:
1. 先在包内契约段找是否断言覆盖观察面——覆盖且观察违反断言 → 判 CONFIRMED(引用断言+观察);
2. 未覆盖/含糊时,在**该案版本的源码 clone**中定位相关逻辑(grep 参数名/错误消息/端点路由),按以下标准判:
   - **客观约束违反**(数值下界/枚举闭集/互斥/类型套套逻辑/同族不一致/接口不对称)→ CONFIRMED(此类不需要契约背书;注意 ef/nprobe 类负哨兵先例——源码明文注释说明哨兵语义的除外)
   - **明文 by-design**(源码注释/文档字符串说明该行为有意;d_evidence 必须引用注释原文)→ FALSE_POSITIVE
   - 裸结构推断("没有校验"/"静默行为"/默认分支)→ **WEAK_REFUTED → HUMAN_REVIEW**(禁止判 FALSE_POSITIVE)
   - 定位不到(not_found)→ **HUMAN_REVIEW**(禁止判 FALSE_POSITIVE)
""" + REDLINES

# ---------------- flat arm: no framework, but red lines + three values
FLAT_PROTOCOL = """
## 终判规则补充(v3 协议,2026-09-12,与插件 2.5.0 判定红线对齐)
- 终判三值:`CONFIRMED | FALSE_POSITIVE | HUMAN_REVIEW`;HUMAN_REVIEW 计入 CONFIRMED(宁可误报、不可错过真缺陷)。
- 你引用源码时:以"该行为是有意设计"为由判 FALSE_POSITIVE,**必须引用源码明文注释/文档字符串原文**;裸结构推断不算数。
- "源码里就是这样写的"不构成 FALSE_POSITIVE 理由——文档 vs 实现才是参照系。
- 数值下界/枚举闭集/互斥/类型套套逻辑类违反(如 count/limit 类参数接受 0 或负数、枚举参数接受集合外值)即使包内无契约行也可判 CONFIRMED。
- 无法确证时给 HUMAN_REVIEW,禁止用 FALSE_POSITIVE 兜底。
"""


def main() -> None:
    os.makedirs(V3, exist_ok=True)
    n = 0
    for arm in ARMS:
        src_dir = os.path.join(V2, arm)
        dst_dir = os.path.join(V3, arm)
        os.makedirs(dst_dir, exist_ok=True)
        if arm.startswith("run_full"):
            proto = FULL_PROTOCOL
        elif arm.startswith("run_flat"):
            proto = FLAT_PROTOCOL
        else:
            proto = DONLY_PROTOCOL
        for f in sorted(glob.glob(src_dir + "/batch*_dispatch.txt")):
            t = open(f, encoding="utf-8").read()
            t = t.replace("rq2_3run\\rerun_v2\\" + arm,
                          "rq2_3run\\rerun_v3\\" + arm)
            t = t.replace("rq2_3run/rerun_v2/" + arm,
                          "rq2_3run/rerun_v3/" + arm)
            t = t.rstrip() + "\n" + proto
            open(os.path.join(dst_dir, os.path.basename(f)), "w",
                 encoding="utf-8").write(t)
            n += 1
    print("rerun_v3 dispatch files:", n)
    bad = 0
    for f in glob.glob(V3 + "/*/batch*_dispatch.txt"):
        t = open(f, encoding="utf-8").read()
        arm_name = os.path.basename(os.path.dirname(f))
        problems = []
        if "rerun_v2" in t or "HUMAN_REVIEW" not in t:
            problems.append("path/protocol")
        if arm_name.startswith("run_full") and "客观约束" not in t:
            problems.append("missing objective classes")
        if problems:
            bad += 1
            print("BAD:", f, problems)
    print("checks:", "OK" if bad == 0 else f"{bad} BAD")


if __name__ == "__main__":
    main()
