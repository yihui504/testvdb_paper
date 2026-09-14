"""档3-#1 control arm: the flat judge bound by the full stage's fixed
aggregation rule, holding everything else byte-identical.

Intervention = exactly one variable: the flat dispatch's "no aggregation rule,
judge however you see fit" becomes a fixed aggregation whose DEFAULT is
HUMAN_REVIEW (the full stage's "其余 -> HUMAN_REVIEW(保守)" catch-all),
expressed in the flat judge's own vocabulary (it has no A/B/C/D perspectives).

Everything else -- the 81 packs, the source clones, the discipline clauses, the
v3 three-valued supplement and its red lines -- is copied from the flat arm's
own dispatch verbatim.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
OUT = V3  # sibling of run_flat{1,2,3}, mirroring the other arms' layout
BATCHES = 6
RUNS = (1, 2, 3)

# the authoritative clause, lifted verbatim from the full-stage dispatch
FULL_DISPATCH = os.path.join(V3, "run_full1", "batch1_dispatch.txt")
full = open(FULL_DISPATCH, encoding="utf-8").read()
m = re.search(r"## 聚合\(固定,与插件一致\)\n(.*?)(?=\n## )", full, re.S)
assert m, "aggregation clause not found in the full-stage dispatch"
AGG_SRC = m.group(0).rstrip()
print("--- lifted from the full stage ---")
print(AGG_SRC[:120].replace("\n", " / "), "...")

# the flat judge has no A/B/C/D; restate the same rule in its own vocabulary.
# the mapping is mechanical: A/B -> clauses 1-2, and the full rule's catch-all
# ("其余 -> HUMAN_REVIEW") -> clause 3.
FLAT_AGG = """## 聚合(固定)
给出终判前按顺序自问,先命中者生效:
1. 该观察是否**明确违反**包内契约断言,或落入客观约束类(数值下界/枚举闭集/互斥/类型套套逻辑/同族不一致/接口不对称)?命中 → **CONFIRMED**。
2. 你是否仅因"这是有意设计"而想判非缺陷?源码里必须有**明文注释或文档字符串**支持。没有明文意图证据 → **不得**判 FALSE_POSITIVE;有 → **FALSE_POSITIVE**。
3. 以上都不命中——即证据不足、材料沉默、契约与源码冲突、或需要你看不到的观察才能定论——一律 **HUMAN_REVIEW**(保守)。
**红线**:禁止用 FALSE_POSITIVE 兜底;FALSE_POSITIVE 只能由第 2 条产生。"""

OLD_FREEDOM = ("**没有规定的分析框架**:不要求分视角、不要求四值结果、不要求证据链分节、"
               "不要求任何聚合规则——你按自己认为合理的方式直接判断"
               "\"该观察是否构成一个真实的文档-实现缺陷\"。")
NEW_FREEDOM = ("**没有规定的分析框架**:不要求分视角、不要求证据链分节——你按自己认为合理的"
               "方式判断\"该观察是否构成一个真实的文档-实现缺陷\";**但终判必须按下面的"
               "固定聚合规则给出**。")

assert OLD_FREEDOM in open(os.path.join(V3, "run_flat1",
                                        "batch1_dispatch.txt"),
                           encoding="utf-8").read() \
    or True  # exact string checked per-file below

made = []
for run in RUNS:
    for b in range(1, BATCHES + 1):
        src = os.path.join(V3, f"run_flat{run}", f"batch{b}_dispatch.txt")
        t = open(src, encoding="utf-8").read()
        orig = t

        assert OLD_FREEDOM in t, f"{src}: freedom sentence drift"
        t = t.replace(OLD_FREEDOM, NEW_FREEDOM, 1)

        # the arm's verdict space is three-valued (v3 supplement); make the
        # output schema line agree so the dispatch is self-consistent
        t = t.replace('"verdict": "CONFIRMED|FALSE_POSITIVE"',
                      '"verdict": "CONFIRMED|FALSE_POSITIVE|HUMAN_REVIEW"', 1)

        t = t.rstrip() + "\n\n" + FLAT_AGG + "\n"

        # retarget the output path
        t = t.replace(f"run_flat{run}\\verdicts_batch{b}.jsonl",
                      f"run_flatagg{run}\\verdicts_batch{b}.jsonl", 1)
        assert f"run_flatagg{run}" in t, f"{src}: output path not retargeted"

        dst_dir = os.path.join(OUT, f"run_flatagg{run}")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"batch{b}_dispatch.txt")
        open(dst, "w", encoding="utf-8").write(t)

        # every line except the three edits must be byte-identical; identify
        # the edits by content, not by index (batch6 carries fewer cases)
        a = orig.splitlines()
        c = t.splitlines()
        diff = [i for i in range(min(len(a), len(c))) if a[i] != c[i]]
        kinds = []
        for i in diff:
            if OLD_FREEDOM in a[i]:
                kinds.append("freedom")
            elif "verdicts_batch" in a[i] and "run_flatagg" in c[i]:
                kinds.append("outpath")
            elif '"verdict": "CONFIRMED|FALSE_POSITIVE"' in a[i]:
                kinds.append("enum")
            else:
                raise AssertionError(f"{src}: unexpected diff at line "
                                     f"{i + 1}: {a[i][:80]!r}")
        assert sorted(kinds) == ["enum", "freedom", "outpath"], \
            f"{src}: edits {kinds}"
        made.append((dst, len(t)))

print(f"\nwrote {len(made)} dispatches under {OUT}")
for d, n in made:
    print(f"  {os.path.basename(os.path.dirname(d))}/{os.path.basename(d)}"
          f"  ({n} bytes)")
