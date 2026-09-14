"""Major A: price the implementation source's marginal contribution.

Part 1 answers R1's Q2 second half from data already on disk: how many of the
full stage's 243 case judgments were decided by an explicit by-design
refutation (C = REFUTED), and how the C votes are distributed.

Part 2 aggregates the no-source arm (full stage minus the source clone) and
contrasts it with the full stage.
"""
import glob
import json
import math
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(ROOT, "rerun_v3")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT)
IS_C = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")


def load(paths):
    v = {}
    for f in paths:
        for line in open(f, encoding="utf-8"):
            line = line.strip()
            if line:
                j = json.loads(line)
                v[j["defect_id"]] = j
    return v


def arm(prefix, override=None):
    out = []
    for r in (1, 2, 3):
        p = sorted(glob.glob(os.path.join(V3, f"{prefix}{r}",
                                          "verdicts_batch*.jsonl")))
        if not p:
            return None
        v = load(p)
        if override:
            q = os.path.join(V3, f"{prefix}{r}", override)
            if os.path.exists(q):
                v.update(load([q]))
        out.append(v)
    return out


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0, c - h), 3), round(min(1, c + h), 3))


def mc(b, c):
    n = b + c
    return 1.0 if n == 0 else min(
        1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)


# ---- Part 1: what did the source-anchored perspective actually do? ----------
full = arm("run_full", "verdicts_coganchor_rejudge.jsonl")
cvals = Counter()
c_per_case = []
for r in range(3):
    for c in CASES:
        cv = (full[r][c].get("perspectives") or {}).get("C")
        cvals[cv] += 1
        c_per_case.append((c, r, cv))
print("=== Part 1: perspective C (the source-anchored perspective), full arm ===")
print(f"  243 case judgments: {dict(cvals)}")
refuted = [x for x in c_per_case if str(x[2]).upper().startswith("REFUT")]
weak = [x for x in c_per_case if "WEAK" in str(x[2]).upper()]
print(f"  C=REFUTED (explicit by-design): {len(refuted)}")
print(f"  C=WEAK_REFUTED               : {len(weak)}")
print("  cases with >=1 C=REFUTED:",
      sorted({c for c, _, cv in refuted}))
csrc = [c for c in CASES
        if any("REFUT" in str((full[r][c].get("perspectives") or {})
                              .get("C", "")).upper()
               and "WEAK" not in str((full[r][c].get("perspectives") or {})
                                     .get("C", "")).upper()
               for r in range(3))]
print(f"  of those, majority-confirmed by the full stage: "
      f"{sum(1 for c in csrc if sum(IS_C(full[r][c]['verdict']) for r in range(3)) >= 2)}")

# ---- Part 2: the no-source arm ---------------------------------------------
ns = arm("run_fullnosrc")
if ns is None or any(len(r) != 81 for r in ns):
    print(f"\n=== Part 2: no-source arm incomplete "
          f"{[len(r) for r in ns] if ns else 'no files'} ===")
    raise SystemExit(0)

print("\n=== Part 2: full stage minus the source clone ===")
for r in range(3):
    conf = sum(IS_C(ns[r][c]["verdict"]) for c in CASES)
    hr = sum(ns[r][c]["verdict"] == "HUMAN_REVIEW" for c in CASES)
    print(f"  run{r+1}: confirmed={conf}  HR={hr} ({hr/81:.1%})")
    cv = Counter((ns[r][c].get("perspectives") or {}).get("C") for c in CASES)
    print(f"          C votes: {dict(cv)}")


def mat(runs):
    return {c: sum(IS_C(runs[r][c]["verdict"]) for r in range(3)) >= 2
            for c in CASES}


M_ns, M_full = mat(ns), mat(full)
tp = sum(M_ns[c] and GT[c] == "T" for c in CASES)
fp = sum(M_ns[c] and GT[c] == "F" for c in CASES)
tn = sum((not M_ns[c]) and GT[c] == "F" for c in CASES)
ftp = sum(M_full[c] and GT[c] == "T" for c in CASES)
ffp = sum(M_full[c] and GT[c] == "F" for c in CASES)
ftn = sum((not M_full[c]) and GT[c] == "F" for c in CASES)
print(f"\n  no-source majority: recall {tp/51:.3f} {wilson(tp,51)}  "
      f"supp {tn/30:.3f}  prec {tp/(tp+fp):.3f}")
print(f"  full      majority: recall {ftp/51:.3f} {wilson(ftp,51)}  "
      f"supp {ftn/30:.3f}  prec {ftp/(ftp+ffp):.3f}")

x = sum(1 for c in CASES if M_full[c] and not M_ns[c])
y = sum(1 for c in CASES if M_ns[c] and not M_full[c])
print(f"\n  full vs no-source: discordant {x}/{y}  net {x-y:+d}  "
      f"exact McNemar p={mc(x, y):.4f}")
print(f"  -> the source's marginal contribution to the confirmed set "
      f"is {x-y:+d} cases")
