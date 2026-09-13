"""Collect and analyze D-only arm run 1 against gt and the post-hoc re-aggregation."""
import json, glob, os, math, collections

BASE = ".paperpilot/phase2-rerun/arms/rq2_3run"
gt = json.load(open(os.path.join(BASE, "gt_81.json"), encoding="utf-8"))
ids = sorted(gt)


def load_run(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(BASE, pattern))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                r = json.loads(line)
                if r["defect_id"] in out:
                    raise SystemExit(f"DUPLICATE {r['defect_id']} in {f}")
                out[r["defect_id"]] = r
    return out


def wilson(k, n, z=1.959964):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def report(verdicts, label):
    tp = fp = fn = tn = 0
    for i in ids:
        v = verdicts.get(i)
        if v is None:
            raise SystemExit(f"MISSING {i} in {label}")
        pos = (v == "CONFIRMED")
        if gt[i] == "T":
            tp += pos; fn += (not pos)
        else:
            fp += pos; tn += (not pos)
    sup = tn / 30
    lo, hi = wilson(tn, 30)
    print(f"  {label:<24} TP={tp:2d} FP={fp} FN={fn:2d} TN={tn:2d} | recall={tp/51:.3f} suppression={sup:.3f} [{lo:.3f},{hi:.3f}]")
    return tp, fp, fn, tn


run1 = load_run("run_donly1/verdicts_batch*.jsonl")
print(f"run_donly1 cases: {len(run1)}/81")
print("\n== D-only arm, run 1 (independent end-to-end) ==")
report({k: v["verdict"] for k, v in run1.items()}, "donly1")
print("\n  d_outcome distribution:", dict(collections.Counter(v["d_outcome"] for v in run1.values())))

print("\n== references ==")
fullR = {r: {} for r in ("full1", "full2", "full3")}
for r in fullR:
    for f in sorted(glob.glob(os.path.join(BASE, f"run_full{r[-1]}/verdicts_batch*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                rec = json.loads(line)
                fullR[r][rec["defect_id"]] = rec
def maj(per):
    return {i: ("CONFIRMED" if sum(1 for r in per if per[r][i] == "CONFIRMED") * 2 >= 3 else "FALSE_POSITIVE") for i in ids}
post = maj({r: {k: ("CONFIRMED" if v["perspectives"]["D"] == "validation_absent" else "FALSE_POSITIVE") for k, v in recs.items()} for r, recs in fullR.items()})
report(post, "post-hoc D-only maj")
report(maj({r: {k: v["verdict"] for k, v in recs.items()} for r, recs in fullR.items()}), "full maj (ref)")

print("\n== run1 vs post-hoc, per case ==")
diff = [(i, gt[i], run1[i]["verdict"], post[i], run1[i]["d_outcome"]) for i in ids if run1[i]["verdict"] != post[i]]
agree = 81 - len(diff)
print(f"case-level agreement: {agree}/81 ({agree/81:.1%}); disagreeing: {len(diff)}")
for i, g, a, b, do in diff:
    dvals = [fullR[r][i]["perspectives"]["D"] for r in ("full1", "full2", "full3")]
    print(f"  {i}: gt={g} run1={a} posthoc={b} run1_D={do} full_D_fields={dvals}")

print("\n== run1 d_outcome vs full-run D fields (same case) ==")
same = sum(1 for i in ids if run1[i]["d_outcome"] in [fullR[r][i]["perspectives"]["D"] for r in ("full1", "full2", "full3")])
print(f"run1 d_outcome matches at least one full-run D field: {same}/81")
