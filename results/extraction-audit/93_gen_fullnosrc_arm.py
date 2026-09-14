"""Major A control arm: the full stage with the implementation source withheld.

R1 (3.4) and R2 (2.5) both note that no arm removes the source clone while
holding everything else fixed, so the paper's "the implementation source above
all" is never priced. This arm is the full stage exactly as dispatched --
four perspectives, chain sections, cognition as perspective D, the same fixed
aggregation -- with the per-case source path removed from the materials list
and the source channel explicitly closed.

Intervention = two edits only:
  1. strip ` | source=<path>` from every case line in the materials list
  2. append a short configuration note closing the source channel
Every rule sentence -- the four perspectives, the aggregation, the five red
lines -- is copied verbatim.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
BATCHES = 6
RUNS = (1, 2, 3)

NOTE = """## 本配置说明(无源码臂)
本配置**不提供实现源码 clone**:材料清单中每案的源码路径已一并移除。
1. 不得联网、不得访问任何源码 clone 或仓库副本;只读上述材料包与认知材料。
2. 凡规则中要求"源码摘录含意图证据"的 by-design 判定(C 视角、判定红线 3),本配置下
   该证据不可得:仅当**认知材料的 developer_quote 明确声明同类现象非缺陷**时才可判
   REFUTED,否则按 **WEAK_REFUTED → HUMAN_REVIEW** 处理。
3. B 视角的 `ef`/`nprobe` 类负哨兵豁免同样无源码可查,故该豁免在本配置下不适用。
4. 判定红线 1、2、4、5 的其他要求不变;聚合规则不变。"""

CASE_LINE = re.compile(r"^(?P<pre>- \w+_\d+: pack=[^|\n]+?)\s*\|\s*source=[^\n]+$",
                       re.M)

made = []
for run in RUNS:
    for b in range(1, BATCHES + 1):
        src = os.path.join(V3, f"run_full{run}", f"batch{b}_dispatch.txt")
        t = open(src, encoding="utf-8").read()
        orig = t

        n_cases = len(CASE_LINE.findall(t))
        assert n_cases in (11, 14), f"{src}: {n_cases} case lines"
        assert "| source=" in t, f"{src}: no source paths"

        t, n_sub = CASE_LINE.subn(lambda m: m.group("pre").rstrip(), t)
        assert n_sub == n_cases, f"{src}: substituted {n_sub}/{n_cases}"
        assert "| source=" not in t, f"{src}: source paths remain"

        t = t.rstrip() + "\n\n" + NOTE + "\n"

        t = t.replace(f"run_full{run}\\verdicts_batch{b}.jsonl",
                      f"run_fullnosrc{run}\\verdicts_batch{b}.jsonl", 1)
        assert f"run_fullnosrc{run}" in t, f"{src}: output path not retargeted"

        dst_dir = os.path.join(V3, f"run_fullnosrc{run}")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"batch{b}_dispatch.txt")
        open(dst, "w", encoding="utf-8").write(t)

        # only the case lines and the output path may differ
        a, c = orig.splitlines(), t.splitlines()
        for i in range(min(len(a), len(c))):
            if a[i] == c[i]:
                continue
            if re.match(r"^- \w+_\d+: pack=", a[i]) and "source=" in a[i]:
                continue
            if "verdicts_batch" in a[i] and "run_fullnosrc" in c[i]:
                continue
            raise AssertionError(f"{src}: unexpected diff line {i+1}: "
                                 f"{a[i][:90]!r}")
        made.append((dst, n_cases))

print(f"wrote {len(made)} dispatches, "
      f"{sum(n for _, n in made)} case lines de-sourced")
print("dirs:", sorted({os.path.basename(os.path.dirname(d)) for d, _ in made}))
