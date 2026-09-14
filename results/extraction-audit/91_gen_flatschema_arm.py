"""Confound control for the flat+agg arm: change ONLY the output-schema enum,
add NO aggregation rule.

The flat dispatch carried a self-contradiction -- its "## 产出" line declared a
binary verdict field while the appended v3 supplement mandates three-valued
verdicts. The flat+agg arm fixed that line *and* appended the aggregation, so
two variables moved together. This arm isolates the field fix.

If this arm lands near the flat arm (~0.588) the field fix is inert and the
flat+agg attribution is clean. If it lands near 0.765 the flat+agg result is a
confound and must be withdrawn.
"""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
BATCHES = 6
RUNS = (1, 2, 3)

OLD_ENUM = '"verdict": "CONFIRMED|FALSE_POSITIVE"'
NEW_ENUM = '"verdict": "CONFIRMED|FALSE_POSITIVE|HUMAN_REVIEW"'

made = []
for run in RUNS:
    for b in range(1, BATCHES + 1):
        src = os.path.join(V3, f"run_flat{run}", f"batch{b}_dispatch.txt")
        t = open(src, encoding="utf-8").read()
        orig = t

        assert OLD_ENUM in t, f"{src}: enum line drift"
        assert "## 聚合(固定)" not in t, f"{src}: source already has aggregation"
        assert "不要求任何聚合规则" in t, f"{src}: freedom sentence drift"

        t = t.replace(OLD_ENUM, NEW_ENUM, 1)
        t = t.replace(f"run_flat{run}\\verdicts_batch{b}.jsonl",
                      f"run_flatschema{run}\\verdicts_batch{b}.jsonl", 1)
        assert f"run_flatschema{run}" in t, f"{src}: output path not retargeted"

        dst_dir = os.path.join(V3, f"run_flatschema{run}")
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, f"batch{b}_dispatch.txt")
        open(dst, "w", encoding="utf-8").write(t)

        a, c = orig.splitlines(), t.splitlines()
        diff = [i for i in range(min(len(a), len(c))) if a[i] != c[i]]
        kinds = []
        for i in diff:
            if OLD_ENUM in a[i]:
                kinds.append("enum")
            elif "verdicts_batch" in a[i] and "run_flatschema" in c[i]:
                kinds.append("outpath")
            else:
                raise AssertionError(f"{src}: unexpected diff line {i+1}: "
                                     f"{a[i][:90]!r}")
        assert sorted(kinds) == ["enum", "outpath"], f"{src}: edits {kinds}"
        made.append(dst)

print(f"wrote {len(made)} dispatches")
print("dirs:", sorted({os.path.basename(os.path.dirname(d)) for d in made}))
