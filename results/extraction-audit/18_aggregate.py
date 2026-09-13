"""Aggregate the rerun_v2 verdicts: per-arm majority over 3 runs, then the
five-arm metric table, layered recall (Q1a), and the old-vs-new comparison.

Majority rule follows v9: CONFIRMED if >=2 of 3 runs confirm.
Metrics: TP/FP/FN/TN against gt_81.json; Wilson 95% CIs; suppression =
TN/(TN+FP) per arm (majority grain); recall = TP/51.
"""
import glob
import json
import math
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/arms/rq2_3run"
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
GTD = GT if isinstance(GT, dict) else {
    (d.get("defect_id") or d.get("case")): (d.get("gt") or d.get("label"))
    for d in GT}
LAYER = {}
mainv = [json.loads(l) for l in open(
    r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/rebuild_v1/"
    "verify_verdicts_main.jsonl", encoding="utf-8")]
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

ARMS = {"core": ["run1", "run2", "run3"],
        "full": ["run_full1", "run_full2", "run_full3"],
        "flat": ["run_flat1", "run_flat2", "run_flat3"],
        "donly": ["run_donly1", "run_donly2", "run_donly3"],
        "donlyq": ["run_donlyq1", "run_donlyq2", "run_donlyq3"]}
# v3 protocol rerun: core stays on rerun_v2 (contract-only, protocol-
# invariant); the four source-consuming arms move to rerun_v3. HUMAN_REVIEW
# counts as CONFIRMED (user decision 2026-09-12).
RUN_BASE = {"core": "rerun_v2",
            "full": "rerun_v3", "flat": "rerun_v3",
            "donly": "rerun_v3", "donlyq": "rerun_v3"}
VERDICT_MAP = {"CONFIRMED": "CONFIRMED", "FALSE_POSITIVE": "FALSE_POSITIVE",
               "HUMAN_REVIEW": "CONFIRMED"}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def load_run(run: str, base: str = "rerun_v2") -> dict[str, str]:
    out: dict[str, str] = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            did = o.get("defect_id")
            v = VERDICT_MAP.get(o.get("verdict"), o.get("verdict"))
            if did and v:
                out[did] = v
    return out


def main() -> None:
    report = ["# RQ2 rerun_v2 聚合", ""]
    arm_stats = {}
    for arm, runs in ARMS.items():
        per_run = {r: load_run(r, RUN_BASE[arm]) for r in runs}
        # agreement over common ids
        ids = [i for i in GTD if all(i in per_run[r] for r in runs)]
        maj: dict[str, str] = {}
        run_flips = Counter()
        for i in ids:
            vs = [per_run[r][i] for r in runs]
            m = "CONFIRMED" if vs.count("CONFIRMED") >= 2 else "FALSE_POSITIVE"
            maj[i] = m
            if len(set(vs)) > 1:
                run_flips[i] = vs
        tp = sum(1 for i in ids if maj[i] == "CONFIRMED" and GTD[i] == "T")
        fp = sum(1 for i in ids if maj[i] == "CONFIRMED" and GTD[i] == "F")
        fn = sum(1 for i in ids if maj[i] == "FALSE_POSITIVE" and GTD[i] == "T")
        tn = sum(1 for i in ids if maj[i] == "FALSE_POSITIVE" and GTD[i] == "F")
        n = len(ids)
        rec = tp / max(1, tp + fn)
        prec = tp / max(1, tp + fp)
        sup = tn / max(1, tn + fp)
        arm_stats[arm] = dict(n=n, tp=tp, fp=fp, fn=fn, tn=tn, rec=rec,
                              prec=prec, sup=sup, flips=len(run_flips),
                              ids=ids, maj=maj, per_run=per_run)
        rlo, rhi = wilson(tp, tp + fn)
        slo, shi = wilson(tn, tn + fp)
        report += [
            f"## {arm}（覆盖 {n}/81；三轮翻转 {len(run_flips)} 案）",
            "",
            f"- TP {tp} / FP {fp} / FN {fn} / TN {tn}",
            f"- recall {rec:.3f} [{rlo:.3f}, {rhi:.3f}]；"
            f"precision {prec:.3f}；suppression {sup:.3f} [{slo:.3f}, {shi:.3f}]",
            "",
        ]
        # layered recall
        lay_rows = []
        for lay in ("evidence_present", "weak_evidence", "evidence_absent"):
            t_l = [i for i in ids if GTD[i] == "T" and LAYER.get(i) == lay]
            c_l = [i for i in t_l if maj[i] == "CONFIRMED"]
            if t_l:
                lay_rows.append(f"    {lay}: {len(c_l)}/{len(t_l)}"
                                f" = {len(c_l)/len(t_l):.3f}")
        report += ["  分层 recall（GT=T 子集）："] + [f"  {r}" for r in lay_rows] + [""]

    # old-vs-new comparison (v9 archive majority files)
    old = {}
    for arm, fn in (("core", "majority_verdicts.json"),
                    ("full", "majority_fullstage.json")):
        for base in (ROOT + "/_v9_archive", ROOT):
            try:
                old[arm] = json.load(open(f"{base}/{fn}", encoding="utf-8"))
                break
            except Exception:
                old[arm] = {}
    report += ["## 新旧对照（majority 口径）", "",
               "| 臂 | 旧 recall | 新 recall | 旧 suppression | 新 suppression |",
               "|---|---|---|---|---|"]
    for arm in ("core", "full"):
        if arm not in old or not old[arm]:
            continue
        ov = old[arm]
        # v9 files store per-case verdicts; recompute quickly
        tps = sum(1 for i, v in ov.items()
                  if str(v).upper().startswith("CONF") and GTD.get(i) == "T")
        fps = sum(1 for i, v in ov.items()
                  if str(v).upper().startswith("CONF") and GTD.get(i) == "F")
        fns = sum(1 for i, v in ov.items()
                  if str(v).upper().startswith("FALSE") and GTD.get(i) == "T")
        tns = sum(1 for i, v in ov.items()
                  if str(v).upper().startswith("FALSE") and GTD.get(i) == "F")
        s = arm_stats[arm]
        report.append(
            f"| {arm} | {tps/max(1,tps+fns):.3f} | {s['rec']:.3f} | "
            f"{tns/max(1,tns+fps):.3f} | {s['sup']:.3f} |")

    # leaked-pack tracking
    report += ["", "## 泄漏 4 包（剥除 _provenance 后）", ""]
    for arm, s in arm_stats.items():
        vs = {c: s["maj"].get(c) for c in
              ("milvus_008", "milvus_013", "milvus_038", "qdrant_016")}
        report.append(f"- {arm}: {vs}")

    out = ROOT + "/rerun_v2/AGGREGATE_REPORT.md"
    open(out, "w", encoding="utf-8").write("\n".join(report) + "\n")
    print("\n".join(report))
    json.dump({a: {k: v for k, v in s.items() if k not in ("per_run", "maj")}
               for a, s in arm_stats.items()},
              open(ROOT + "/rerun_v2/arm_stats.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
