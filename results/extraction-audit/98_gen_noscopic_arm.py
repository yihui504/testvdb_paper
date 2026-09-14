"""The missing cell of the 2x2 (R1 3.3 / R2 3.4).

The paper's decomposition has three cells: flat (no perspectives, no
aggregation), flat+aggregation (aggregation, no perspectives), and full
(perspectives + aggregation). The fourth -- perspectives WITHOUT the fixed
aggregation rule -- is missing, which is why "the advantage belongs to the
routing rule rather than to the four perspectives" outruns the design.

This arm supplies it: the full stage with both aggregation blocks excised, so
the judge reads the same four perspectives over the same materials and then
weighs them itself. Everything else -- source clone, cognition, evidence
chain, three-valued verdict space, the five red lines -- is verbatim.

Caveat recorded with the arm: red line 4 still routes insufficient evidence to
Human-Review, so what is removed is the *ordered clause table*, not routing
itself. The contrast against `full` therefore prices the ordered aggregation,
not the routing mandate.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
BATCHES = 6
RUNS = (1, 2, 3)

TASK_OLD = "再按四视角分别评估,最后按保守规则聚合终判。"
TASK_NEW = ("再按四视角分别评估,最后综合四视角自行权衡给出终判"
            "(**本配置不提供固定聚合规则**,见文末说明)。")

NOTE = """## 本配置说明(无固定聚合规则)
本配置**不提供任何固定聚合规则**:上文没有聚合条款表,请你在逐一给出四视角判定后,
**自行权衡**给出终判。以下不变:
1. 终判三值:`CONFIRMED | FALSE_POSITIVE | HUMAN_REVIEW`;HUMAN_REVIEW 计入 CONFIRMED。
2. 判定红线(见下)全部适用——其中红线 4 仍要求证据不足时转人工。
3. 材料、源码 clone、认知材料与纪律条款与本阶段完整形态相同。"""

made = []
for run in RUNS:
    for b in range(1, BATCHES + 1):
        src = os.path.join(V3, f"run_full{run}", f"batch{b}_dispatch.txt")
        t = open(src, encoding="utf-8").read()
        orig = t

        assert TASK_OLD in t, f"{src}: task sentence drift"
        t = t.replace(TASK_OLD, TASK_NEW, 1)

        # excise both aggregation blocks: heading up to the next top-level heading
        for head in (r"## 聚合规则\(保守,与既定口径一致\)",
                     r"## 聚合\(固定,与插件一致\)"):
            pat = head + r"\n.*?(?=\n## )"
            assert re.search(pat, t, re.S), f"{src}: {head} not found"
            t = re.sub(pat, "", t, count=1, flags=re.S)
        assert "## 聚合" not in t, f"{src}: aggregation block survives"

        t = t.rstrip() + "\n\n" + NOTE + "\n"

        t = t.replace(f"run_full{run}\\verdicts_batch{b}.jsonl",
                      f"run_noscopic{run}\\verdicts_batch{b}.jsonl", 1)
        assert f"run_noscopic{run}" in t, f"{src}: output path not retargeted"

        dst_dir = os.path.join(V3, f"run_noscopic{run}")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"batch{b}_dispatch.txt")
        open(dst, "w", encoding="utf-8").write(t)
        made.append(dst)

print(f"wrote {len(made)} dispatches")
print("dirs:", sorted({os.path.basename(os.path.dirname(d)) for d in made}))
