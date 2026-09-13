"""Compute RQ2 arm metrics (core / full / D-only / C-only) from the recorded per-case artifacts."""
import json, glob, os, collections

BASE = ".paperpilot/phase2-rerun/arms/rq2_3run"
gt = json.load(open(os.path.join(BASE, "gt_81.json"), encoding="utf-8"))
ids = sorted(gt)
assert len(ids) == 81 and sum(1 for v in gt.values() if v == "T") == 51


def load_jsonl_dir(pattern):
    out = {}
    for f in sorted(glob.glob(os.path.join(BASE, pattern))):
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                r = json.loads(line)
                out[r["defect_id"]] = r
    return out


def confusion(verdicts, label):
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
    print(f"  {label:<26} TP={tp:2d} FP={fp:2d} FN={fn:2d} TN={tn:2d}")
    return dict(TP=tp, FP=fp, FN=fn, TN=tn)


def majority(per_run):
    out = {}
    for i in ids:
        c = sum(1 for r in per_run if per_run[r][i] == "CONFIRMED")
        out[i] = "CONFIRMED" if c * 2 >= len(per_run) else "FALSE_POSITIVE"
    return out


def by_perspective(recs, persp, rule):
    return {k: ("CONFIRMED" if rule(v["perspectives"][persp]) else "FALSE_POSITIVE")
            for k, v in recs.items()}


print("=" * 64)
print("A. PAPER TABLE 4 RECONSTRUCTION  (validates the pipeline)")
print("=" * 64)
core = {r: {k: v["verdict"] for k, v in load_jsonl_dir(f"{r}/verdicts_batch*.jsonl").items()}
        for r in ("run1", "run2", "run3")}
print("core (contract-only):")
for r in core:
    confusion(core[r], f"core {r}")
confusion(majority(core), "core majority")

full_recs = {r: load_jsonl_dir(f"run_full{r[-1]}/verdicts_batch*.jsonl")
             for r in ("full1", "full2", "full3")}
full = {r: {k: v["verdict"] for k, v in recs.items()} for r, recs in full_recs.items()}
print("\nfull (C+D):")
for r in full:
    confusion(full[r], f"full {r}")
confusion(majority(full), "full majority")

cl = json.load(open(os.path.join(BASE, "majority_fullstage_cleaned.json"), encoding="utf-8"))
print("\nfull (cleaned/merged):")
for r in ("1", "2", "3"):
    confusion(cl["merged"][r], f"fullc run{r}")
confusion(cl["majority"], "fullc majority")

print("\n" + "=" * 64)
print("B. PERSPECTIVE DISTRIBUTIONS  (original full runs, 81 cases each)")
print("=" * 64)
for r in ("full1", "full2", "full3"):
    print(f"\n{r}:")
    for p in ("A", "B", "C", "D"):
        c = collections.Counter(v["perspectives"][p] for v in full_recs[r].values())
        print(f"  {p}: " + ", ".join(f"{k}={v}" for k, v in c.most_common()))

print("\n" + "=" * 64)
print("C. SINGLE-PERSPECTIVE RE-AGGREGATIONS")
print("=" * 64)

D_RULE = lambda d: d == "validation_absent"          # only 'validated absent' supports a bug
C_RULE = lambda c: c == "CONFIRMED"

for name, persp, rule in (("D-only", "D", D_RULE), ("C-only", "C", C_RULE)):
    print(f"\n{name} arm (rule: {name.split('-')[0]} alone decides; everything else -> FALSE_POSITIVE):")
    per = {}
    for r in ("full1", "full2", "full3"):
        per[r] = by_perspective(full_recs[r], persp, rule)
        confusion(per[r], f"{name} {r}")
    confusion(majority(per), f"{name} majority")

print("\n" + "=" * 64)
print("D. D-VALUE BREAKDOWN ON GROUND-TRUTH TRUE BUGS vs FALSE POSITIVES")
print("=" * 64)
for r in ("full1", "full2", "full3"):
    print(f"\n{r}:")
    for val in ("validation_absent", "by_design_in_source", "validation_present", "not_found"):
        t = sum(1 for k, v in full[r].items() if gt[k] == "T" and full_recs[r][k]["perspectives"]["D"] == val)
        f = sum(1 for k, v in full[r].items() if gt[k] == "F" and full_recs[r][k]["perspectives"]["D"] == val)
        print(f"  D={val:<20} true-bugs={t:2d}  false-pos={f:2d}")
