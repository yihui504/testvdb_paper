"""Problem 2, pass 3: the protocol-faithful blind dispatch. Passes 1-2 (scripts
68/71) under-specified the full-stage protocol: they omitted the seven
objective-constraint classes (which confirm WITHOUT contract endorsement) and
the verbatim-intent red line for by-design refutation. Most of their RETURN
rulings were 'no contract anchor' -- a rule the deployed protocol does not
require for class-B confirmations. This dispatch states the deployed protocol
in full."""
import glob
import json
import random
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms"
PACK_DIR = f"{ROOT}/materials_complete"
RUNS = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
UNIQ = json.load(open("results/extraction-audit/routed_unique.json",
                      encoding="utf-8"))["unique"]

src = {}
for f in glob.glob(f"{RUNS}/run_flat1/batch*.txt"):
    for line in open(f, encoding="utf-8"):
        m = re.match(r"^\s*-?\s*([a-z]+_\d+): pack=(.+?) \| source=(.+?)\s*$",
                     line)
        if m:
            src[m.group(1)] = m.group(3)
order = list(UNIQ)
random.Random(20260914).shuffle(order)

RULES = r"""\
你是部署通道的人工裁决者。下面是全阶段协议的完整规则。对每个路由来的候选
缺陷，按这套规则给出人工裁决（该案经人工审查后的去向）。

## 材料

每案给出：材料包（观察记录 + 契约行）+ 该案版本钉定的源码 clone。
可以在 clone 中 grep/Read 任意文件。
**不得**查询 issue tracker、不得联网、不得读取任何认知/情报材料。

## 判据（三层，按此顺序）

### 第一层：契约（perspective A）
若包内某条契约行的规范内容被观察直接违反 → 确认缺陷。

### 第二层：客观约束（perspective B）——不需要契约行背书
以下七类客观违反**在无契约行时也可确认**：
1. 计数/大小/上限类参数的**数值下界**违反（例如 limit 类参数接受 0 或负数）
2. **闭合枚举集**：传入集合外的值被接受
3. **互斥参数**同时被接受
4. **类型套套逻辑**：数值语义的参数（如超时头）接受非数值并静默回落
5. **同族不一致**：同一端点/同族中，一族显式拒绝而另一族静默接受同一违反值
6. **接口不对称**：REST / gRPC / SDK 三面对同一违反值处置不一致
7. **HTTP 响应语义**（强限定）：仅在明显错配时使用
判据要旨：**"文档没有写"不等于"不是缺陷"**。一个 limit 参数接受 0 就是客观
违反，即使没有任何契约行写了边界。

### 第三层：by-design 抗辩（perspective C）——只有明文意图证据才能驳回
若源码中出现**逐字意图证据**（注释或文档串，如 `// intentionally`、
`we don't guarantee`），可判非缺陷。
**裸结构性推断不算**——"这里没有校验"、"这是个未注释的默认分支"、
"代码里有归一化赋值"都只是**弱反驳**，不构成 by-design，应转人工而非判非缺陷。
（例外：若源码注释明写该默认/归一行为是有意为之，则算明文证据。）

## 三选一裁决

- `CONFIRM_AS_DEFECT`：第一层或第二层成立，且第三层无明文 by-design 证据。
- `RETURN`：证据不足——缺执行记录、观察未隔离所声称行为（探针参数未生效、
  对照臂被无关错误污染）、材料自相矛盾、或只有弱反驳而无足够确认依据。
- `REJECT`：**仅当**文档语句为纯描述性（无规范承诺可违反）**或**源码含明文
  by-design 意图证据。

## 纪律
只看证据，不猜测维护者会怎么判。独立裁决，不受其他案影响。

## 输出格式（每案一个 JSON 行）
{"case": "<案号>", "ruling": "CONFIRM_AS_DEFECT|RETURN|REJECT",
 "rationale": "<一两句中文理由，指明是哪一层判据 + 具体证据（包内契约行 id 或源码 file:line）>"}
"""

out = ["# Blind adjudication, pass 3 (deployed protocol stated in full)", "",
       f"对以下 {len(order)} 个路由案逐案裁决。", "",
       RULES, ""]
for n, case in enumerate(order, 1):
    pack = open(f"{PACK_DIR}/{case}.md", encoding="utf-8").read()
    assert "developer_cognition" not in pack
    out.append(f"\n\n--------\n\n## 案 {n}: {case}\n\n"
               f"**源码 clone**：`{src[case]}`\n\n{pack}")

open("results/extraction-audit/blind_pass_protocol_dispatch.md", "w",
     encoding="utf-8").write("\n".join(out))
json.dump({"order": order}, open(
    "results/extraction-audit/blind_pass_protocol_order.json", "w"), indent=1)
print(f"dispatch written: {len(order)} cases, deployed protocol stated in full")
