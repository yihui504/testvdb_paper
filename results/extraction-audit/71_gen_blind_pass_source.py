"""Problem 2 (second pass), fair replication: the authors' adjudication
protocol in practice included source forensics (their rationales cite
file:line). This dispatch adds the per-case pinned source clone so the blind
pass matches that protocol; the pack-only version (script 68) becomes the
source-access ablation."""
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

# case -> source clone, parsed from the dispatch the actual runs used
src = {}
for f in glob.glob(f"{RUNS}/run_flat1/batch*.txt"):
    for line in open(f, encoding="utf-8"):
        m = re.match(r"^\s*-?\s*([a-z]+_\d+): pack=(.+?) \| source=(.+?)\s*$",
                     line)
        if m:
            src[m.group(1)] = m.group(3)
print(f"source paths resolved: {len(src)}")

missing_src, missing_pack, contaminated = [], [], []
for c in UNIQ:
    if c not in src:
        missing_src.append(c)
    elif not Path(src[c]).exists():
        missing_src.append(c)
    if not Path(f"{PACK_DIR}/{c}.md").exists():
        missing_pack.append(c)
    elif "developer_cognition" in open(f"{PACK_DIR}/{c}.md",
                                       encoding="utf-8").read():
        contaminated.append(c)
print("missing sources:", missing_src or "none")
print("missing packs  :", missing_pack or "none")
print("contaminated   :", contaminated or "none")
assert not (missing_src or missing_pack or contaminated)

order = list(UNIQ)
random.Random(20260914).shuffle(order)

RULES = """\
你是一名独立的缺陷裁决员，执行部署通道人工裁决者的角色。对下列每个候选缺陷
给出裁决：该案路由到人工审查后应判往何处。

## 裁决规则（与部署的 pack-materials 规则一致）

1. **材料范围**：每案的材料包（观察记录 + 契约行）+ 该案对应版本的源码 clone。
   你可以 grep/Read 源码中任意文件来查证行为与意图。**不得**查询 issue
   tracker、不得联网、不得读取任何认知/情报（developer_cognition /
   intelligence）材料。
2. **三选一裁决**：
   - `CONFIRM_AS_DEFECT`：证据足以确认这是文档-实现不一致缺陷
     （观察行为与包内文档约束矛盾，或构成包内材料支持的客观违反，
     且源码中无明文 by-design 意图证据）。
   - `RETURN`：证据不足（缺执行记录、缺可核查契约锚点、前提失真、
     观察未隔离所声称行为、材料自相矛盾）。
   - `REJECT`：材料表明这不是缺陷（文档语句为描述性而非规范性、
     行为在文档允许范围内、或源码含明文 by-design 意图证据）。
3. 源码的作用有二：为 by-design 抗辩找明文意图证据（注释/文档串）；定位
   "契约预测缺失校验"处的实现，以判断行为是否属实、是否被隔离。
4. 唯一裁决只看证据，不猜测维护者会怎么判。

输出格式（每案一个 JSON 行）：
{"case": "<案号>", "ruling": "CONFIRM_AS_DEFECT|RETURN|REJECT",
 "rationale": "<一两句中文理由，引用包内或源码的具体证据>"}
"""

out = ["# Blind second-pass adjudication (pack + pinned source)",
       "",
       "对以下 %d 个候选缺陷逐案裁决。每案的源码 clone 路径已给出，"
       "可在其中 grep/Read 查证。" % len(order),
       "逐案输出一个 JSON 行。",
       "",
       RULES,
       ""]
for n, case in enumerate(order, 1):
    pack = open(f"{PACK_DIR}/{case}.md", encoding="utf-8").read()
    out.append(f"\n\n--------\n\n## 案 {n}: {case}\n\n"
               f"**源码 clone**：`{src[case]}`\n\n{pack}")

open("results/extraction-audit/blind_pass_source_dispatch.md", "w",
     encoding="utf-8").write("\n".join(out))
json.dump({"order": order, "source": {c: src[c] for c in order}},
          open("results/extraction-audit/blind_pass_source_order.json", "w"),
          indent=1)
print(f"dispatch written: {len(order)} cases with source paths")
