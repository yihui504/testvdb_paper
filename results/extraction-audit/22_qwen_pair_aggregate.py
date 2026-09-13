"""Aggregate the Qwen-backbone full/flat pair (single run each) and run the
leak sensitivity on both the Qwen pair and the GLM flagship pair.

Conventions follow 18_aggregate.py: HR counts toward CONFIRMED (study
convention); forced-verdict-only sensitivity treats HR as not-confirmed;
GLM arms use 3-run majority (>=2 of 3).

Leak set: 10 packs embedding a developer_cognition section (carried over
from the v9 originals), which the flat/donly/donlyq dispatches forbid
reading. The full arm legitimately reads cognition (perspective D), so the
sensitivity only removes those cases from BOTH arms of a pair.
"""
import glob
import json
import math
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
LEAK = {"milvus_010", "milvus_014", "milvus_018", "milvus_019", "milvus_022",
        "milvus_026", "milvus_027", "milvus_028", "milvus_032", "milvus_033"}


def load(run: str) -> dict:
    out = {}
    for f in sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                assert o["defect_id"] not in out, f"dup {o['defect_id']} in {run}"
                out[o["defect_id"]] = o.get("verdict")
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0, c - h), min(1, c + h))


def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)
    p = sum(math.comb(n, k) for k in range(0, m + 1)) / 2 ** n
    return min(1.0, 2 * p)


def majority(runs):
    """runs: list of dicts; returns case -> verdict under HR=CONFIRMED."""
    ids = sorted(set.intersection(*(set(r) for r in runs)))
    maj = {}
    for i in ids:
        vs = [("CONFIRMED" if r[i] in ("CONFIRMED", "HUMAN_REVIEW")
               else "FALSE_POSITIVE") for r in runs]
        maj[i] = "CONFIRMED" if vs.count("CONFIRMED") >= 2 else "FALSE_POSITIVE"
    return maj


def conf(v, hr_confirmed=True):
    return v == "CONFIRMED" or (hr_confirmed and v == "HUMAN_REVIEW")


def pair(label, fullv, flatv, hr_confirmed, drop=None):
    ids = sorted(set(fullv) & set(flatv) & set(GT))
    if drop:
        ids = [i for i in ids if i not in drop]
    rows = []
    for name, d in (("full", fullv), ("flat", flatv)):
        tp = sum(1 for i in ids if conf(d[i], hr_confirmed) and GT[i] == "T")
        fp = sum(1 for i in ids if conf(d[i], hr_confirmed) and GT[i] == "F")
        fn = sum(1 for i in ids if not conf(d[i], hr_confirmed) and GT[i] == "T")
        tn = sum(1 for i in ids if not conf(d[i], hr_confirmed) and GT[i] == "F")
        rec = tp / (tp + fn) if tp + fn else 0.0
        rlo, rhi = wilson(tp, tp + fn)
        rows.append((name, tp, fp, fn, tn, rec, rlo, rhi))
    b = sum(1 for i in ids if conf(fullv[i], hr_confirmed)
            and not conf(flatv[i], hr_confirmed))
    c = sum(1 for i in ids if not conf(fullv[i], hr_confirmed)
            and conf(flatv[i], hr_confirmed))
    p = mcnemar(b, c)
    tag = "HR=CONFIRMED" if hr_confirmed else "forced-only"
    n = len(ids)
    print(f"[{label}] {tag}  (n={n})")
    for name, tp, fp, fn, tn, rec, rlo, rhi in rows:
        print(f"  {name:5s} TP {tp} FP {fp} FN {fn} TN {tn}"
              f"  recall {rec:.3f} [{rlo:.3f},{rhi:.3f}]")
    print(f"  discordant full-only {b} / flat-only {c}"
          f"  exact McNemar p = {p:.4f}")
    return p


def hr_rate(run_dict):
    hr = sum(1 for v in run_dict.values() if v == "HUMAN_REVIEW")
    return hr, len(run_dict)


def main():
    qf = load("run_fullq1")
    qa = load("run_flatq1")
    print(f"Qwen runs loaded: full {len(qf)} cases, flat {len(qa)} cases")
    for name, d in (("qwen-full", qf), ("qwen-flat", qa)):
        hr, n = hr_rate(d)
        print(f"  {name}: HR-routed {hr}/{n} = {hr/n:.3f}")

    print()
    pair("Qwen pair", qf, qa, True)
    pair("Qwen pair", qf, qa, False)
    pair("Qwen pair, drop 10 leak packs", qf, qa, True, drop=LEAK)
    pair("Qwen pair, drop 10 leak packs", qf, qa, False, drop=LEAK)

    print()
    gf = [load(f"run_full{i}") for i in (1, 2, 3)]
    ga = [load(f"run_flat{i}") for i in (1, 2, 3)]
    gfm = majority(gf)
    gam = majority(ga)
    pair("GLM flagship (majority)", gfm, gam, True)
    pair("GLM flagship (majority), drop 10 leak packs", gfm, gam, True,
         drop=LEAK)

    print()
    print("== tight cognition-citation check in cognition-forbidden arms ==")
    pat = re.compile(r"维护者|认知|developer_cognition|50192|50193|50319|50351",
                     re.I)
    for run in ("run_flat1", "run_flat2", "run_flat3", "run_flatq1",
                "run_donly1", "run_donly2", "run_donly3",
                "run_donlyq1", "run_donlyq2", "run_donlyq3"):
        d = load(run) if run != "run_flatq1" else qa
        # reload full record for rationale
        hits = []
        for f in sorted(glob.glob(
                f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
            for l in open(f, encoding="utf-8"):
                l = l.strip()
                if not l:
                    continue
                o = json.loads(l)
                if o.get("defect_id") in LEAK and pat.search(
                        o.get("rationale") or ""):
                    hits.append(o["defect_id"])
        print(f"  {run}: {sorted(set(hits))}")


if __name__ == "__main__":
    main()
