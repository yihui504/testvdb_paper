"""Problem 2 (second pass), step 2: generate the blind second-pass dispatch.
25 unique routed cases, shuffled order, pack materials only, no arm / GT /
prior-adjudication information. Output: one dispatch file + a per-case order
manifest for later aggregation."""
import json
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms"
# the packs the actual runs read are arms/materials_complete/ (cognition
# stripped); arms/rq2_3run/materials_complete/ is the pre-cleanup v9 copies
PACK_DIR = f"{ROOT}/materials_complete"
MANIFEST = json.load(open("results/extraction-audit/routed_unique.json",
                          encoding="utf-8"))
uniq = MANIFEST["unique"]

# deterministic shuffle (seeded) so the order is reproducible but not sorted
random.Random(20260914).shuffle(uniq)

RULES = """\
你是一名独立的缺陷裁决员。对下列每个候选缺陷，仅依据其证据包材料裁决。
裁决规则（与部署的 pack-materials 规则一致）：
1. 只使用证据包内的材料：观察记录（原始 HTTP 交换）、契约行（文档约束）、
   行为摘要。不得查询 issue tracker、不得联网、不得使用任何外部知识补充材料。
2. 三选一裁决：
   - CONFIRM_AS_DEFECT：包内证据足以确认这是文档-实现不一致缺陷
     （观察到的行为与包内文档约束矛盾，或构成包内材料支持的客观违反）。
   - RETURN：材料不足以裁决（缺执行记录、缺可核查的契约锚点、前提失真、
     观察不能隔离所声称的行为）。
   - REJECT：包内材料表明这不是缺陷（描述性而非规范性的文档语句、
     行为在文档允许范围内、或包内明示的 by-design 证据）。
3. 裁决只看包内材料能否支撑，不猜测维护者会怎么判。
输出格式（每案一个 JSON 行）：
{"case": "<案号>", "ruling": "CONFIRM_AS_DEFECT|RETURN|REJECT",
 "rationale": "<一两句中文理由，引用包内具体证据>"}
"""

out = ["# Blind second-pass adjudication dispatch",
       "",
       "对以下 25 个候选缺陷逐案裁决。所有案子的裁决规则相同。",
       "逐案输出一个 JSON 行，最后把全部 25 行写入结果文件。",
       "",
       RULES,
       ""]
for n, case in enumerate(uniq, 1):
    pack = open(f"{PACK_DIR}/{case}.md",
                encoding="utf-8").read()
    assert "developer_cognition" not in pack, f"{case} still has cognition!"
    out.append(f"\n\n--------\n\n## 案 {n}: {case}\n\n{pack}")

open("results/extraction-audit/blind_pass_dispatch.md", "w",
     encoding="utf-8").write("\n".join(out))
json.dump(uniq, open("results/extraction-audit/blind_pass_order.json", "w"),
          indent=1)
print(f"dispatch written: 25 cases, shuffled order")
print("order:", uniq)
