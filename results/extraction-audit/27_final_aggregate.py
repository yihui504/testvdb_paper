"""Final clean-pool aggregation after the cognition-strip re-judge (all 13
runs merged). Emits every number the paper needs: per-arm confusion + rates
+ Wilson, three-run agreement, HR rates, stratified recall, all seven paired
McNemar tests with Holm ordering, and the Qwen full-vs-flat probe pair."""
import glob
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
LAYERS = {
    "evidence_present": None,  # filled from the same source 18_aggregate uses
    "weak_evidence": {"milvus_038"},
    "evidence_absent": set(),
}
# layer per case, recomputed the same way as 18_aggregate.py
mainv = [json.loads(l) for l in open(
    r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/"
    "rebuild_v1/verify_verdicts_main.jsonl", encoding="utf-8")]
LAYER = {}
for x in mainv:
    if x.get("layer"):
        LAYER[x["case"]] = x["layer"]
AUD = json.load(open(r"c:/Users/11428/Desktop/testvdb_paper/results/"
                     "extraction-audit/rebuild_final/assembly_audit.json",
                     encoding="utf-8"))
for r in AUD:
    c = r["case"]
    if c not in LAYER:
        LAYER[c] = ("evidence_absent" if r["rows_kept"] == 0 and r["arch"] == 0
                    else "evidence_present")
LAYER["milvus_038"] = "weak_evidence"


def load(run, base):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o.get("verdict")
    return d


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def mc(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1))
               / 2 ** n)


def conf(v, forced=False):
    if forced:
        return v == "CONFIRMED"
    return v in ("CONFIRMED", "HUMAN_REVIEW")


def majority(runs, forced=False):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    return {i: ("CONFIRMED" if sum(conf(r[i], forced) for r in runs) >= 2
                else "FALSE_POSITIVE") for i in ids}


def arm_line(name, d):
    tp = sum(1 for i in d if d[i] == "CONFIRMED" and GT[i] == "T")
    fp = sum(1 for i in d if d[i] == "CONFIRMED" and GT[i] == "F")
    fn, tn = 51 - tp, 30 - fp
    rlo, rhi = wilson(tp, 51)
    slo, shi = wilson(tn, 30)
    print(f"{name:11s} TP {tp:2d} FP {fp:2d} FN {fn:2d} TN {tn:2d}  "
          f"recall {tp/51:.3f} [{rlo:.3f},{rhi:.3f}]  "
          f"prec {tp/(tp+fp):.3f}  supp {tn/30:.3f} [{slo:.3f},{shi:.3f}]")
    return d


def agreement(runs):
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    same = sum(1 for i in ids if len({runs[k][i] for k in range(len(runs))}) == 1)
    return same, len(ids)


def layered(name, d):
    out = []
    for lay in ("evidence_present", "weak_evidence", "evidence_absent"):
        t = [i for i in d if GT[i] == "T" and LAYER.get(i) == lay]
        c = [i for i in t if d[i] == "CONFIRMED"]
        if t:
            out.append(f"{lay} {len(c)}/{len(t)}={len(c)/len(t):.3f}")
    print(f"  {name} strata: " + "; ".join(out))


def main():
    core_m = arm_line("core", majority([load(f"run{i}", "rerun_v2")
                                        for i in (1, 2, 3)]))
    full_runs = [load(f"run_full{i}", "rerun_v3") for i in (1, 2, 3)]
    flat_runs = [load(f"run_flat{i}", "rerun_v3") for i in (1, 2, 3)]
    don_runs = [load(f"run_donly{i}", "rerun_v3") for i in (1, 2, 3)]
    donq_runs = [load(f"run_donlyq{i}", "rerun_v3") for i in (1, 2, 3)]
    full_m = arm_line("full", majority(full_runs))
    flat_m = arm_line("flat", majority(flat_runs))
    don_m = arm_line("donly", majority(don_runs))
    donq_m = arm_line("donly-Qwen", majority(donq_runs))
    print("  forced-only: core",
          sum(1 for v in majority([load(f"run{i}", "rerun_v2")
                                   for i in (1, 2, 3)], True).values()
              if v == "CONFIRMED"),
          " full",
          sum(1 for v in majority(full_runs, True).values() if v == "CONFIRMED"),
          " flat",
          sum(1 for v in majority(flat_runs, True).values() if v == "CONFIRMED"))
    for nm, rs in (("core", [load(f"run{i}", "rerun_v2") for i in (1, 2, 3)]),
                   ("full", full_runs), ("flat", flat_runs),
                   ("donly", don_runs), ("donly-Qwen", donq_runs)):
        s, n = agreement(rs)
        print(f"  {nm} 3-run agreement {s}/{n} = {s/n:.3f}")
    hr = sum(1 for r in full_runs for v in r.values() if v == "HUMAN_REVIEW")
    print(f"  full HR routed verdicts {hr}/243 = {hr/243:.3f}")
    conf_hr = [i for i in full_m if full_m[i] == "CONFIRMED"]
    ncomp = sum(1 for i in conf_hr
                if any(full_runs[k][i] == "HUMAN_REVIEW" for k in range(3)))
    print(f"  full confirmations with HR component: {ncomp}")
    print()
    layered("full", full_m)
    layered("flat", flat_m)
    layered("core", core_m)
    layered("donly", don_m)
    layered("donly-Qwen", donq_m)
    print()
    qf = load("run_fullq1", "rerun_v3")
    qa = load("run_flatq1", "rerun_v3")
    b = sum(1 for i in qf if conf(qf[i]) and not conf(qa[i]))
    c = sum(1 for i in qf if not conf(qf[i]) and conf(qa[i]))
    qtp = sum(1 for i in qf if conf(qf[i]) and GT[i] == "T")
    aqp = sum(1 for i in qa if conf(qa[i]) and GT[i] == "T")
    qhr = sum(1 for v in qf.values() if v == "HUMAN_REVIEW")
    ahr = sum(1 for v in qa.values() if v == "HUMAN_REVIEW")
    print(f"Qwen pair (single run): full {qtp}/51 recall, flat {aqp}/51; "
          f"HR {qhr}/81 vs {ahr}/81; discordant {b}/{c}; p={mc(b,c):.4f}")
    print()
    def pair(n1, d1, n2, d2):
        b = sum(1 for i in d1 if d1[i] == "CONFIRMED"
                and d2[i] != "CONFIRMED")
        c = sum(1 for i in d1 if d1[i] != "CONFIRMED"
                and d2[i] == "CONFIRMED")
        return n1 + "-vs-" + n2, b, c, mc(b, c)
    tests = [pair("core", core_m, "full", full_m),
             pair("core", core_m, "flat", flat_m),
             pair("core", core_m, "D-only", don_m),
             pair("full", full_m, "flat", flat_m),
             pair("full", full_m, "D-only", don_m),
             pair("D-only", don_m, "flat", flat_m),
             pair("D-only-Qwen", donq_m, "flat", flat_m)]
    tests_sorted = sorted(tests, key=lambda t: t[3])
    print("Holm family (rank, raw p, multiplier, corrected):")
    prev = 0.0
    for k, (nm, b, c, p) in enumerate(tests_sorted):
        mult = len(tests_sorted) - k
        corr = min(1.0, max(prev, p * mult))
        prev = corr
        print(f"  {k+1} {nm:20s} {b:2d}/{c:2d} raw {p:.5f} x{mult} -> {corr:.4f}")
    print()
    # forced-only full-vs-flat (sensitivity reported in the paper)
    fm = majority(full_runs, True)
    am = majority(flat_runs, True)
    b = sum(1 for i in fm if fm[i] == "CONFIRMED" and am[i] != "CONFIRMED")
    c = sum(1 for i in fm if fm[i] != "CONFIRMED" and am[i] == "CONFIRMED")
    ftp = sum(1 for i in fm if fm[i] == "CONFIRMED" and GT[i] == "T")
    atp = sum(1 for i in am if am[i] == "CONFIRMED" and GT[i] == "T")
    print(f"forced-only: full {ftp}/51={ftp/51:.3f} flat {atp}/51={atp/51:.3f}"
          f" discordant {b}/{c} p={mc(b,c):.4f}")


if __name__ == "__main__":
    main()
