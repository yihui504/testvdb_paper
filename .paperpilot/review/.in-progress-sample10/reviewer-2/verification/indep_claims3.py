"""Reviewer-2 verification part 3: the re-judge ledger, the 37/51 rule, pre-repair census."""
import glob, json, os, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ART = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/11428/Desktop/TestVDB_artifact"
ROOT = os.path.join(ART, "rq2", "verdicts")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT); T = [c for c in CASES if GT[c] == "T"]

def batch(pattern, r):
    d = {}
    for f in sorted(glob.glob(os.path.join(ROOT, pattern.format(r), "verdicts_batch*.jsonl"))):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                o = json.loads(line); d[o["defect_id"]] = o
    return d

def override_lines(pattern, r, ovr):
    p = os.path.join(ROOT, pattern.format(r), ovr)
    if not p or not os.path.exists(p): return []
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]

print("="*98)
print("H2. THE SIX RE-JUDGE FILES OF THE TWO FULL-FAMILY CONTROLS, verdict by verdict")
print("="*98)
tot_lines = tot_changed = tot_toward = tot_between = tot_away = 0
for nm, pat, ovr in (("full, no source","run_fullnosrc{}","verdicts_coganchor_rejudge.jsonl"),
                     ("full, no aggregation","run_noscopic{}","verdicts_coganchor_rejudge.jsonl")):
    for r in (1,2,3):
        pre = batch(pat, r)
        for o in override_lines(pat, r, ovr):
            cid = o["defect_id"]; old = pre[cid]["verdict"]; new = o["verdict"]
            tot_lines += 1
            if old == new: continue
            tot_changed += 1
            if old == "FALSE_POSITIVE" and new != "FALSE_POSITIVE": tot_toward += 1; k = "TOWARD "
            elif old != "FALSE_POSITIVE" and new == "FALSE_POSITIVE": tot_away += 1; k = "AWAY   "
            else: tot_between += 1; k = "BETWEEN"
            print(f"  {nm:22s} {cid:14s} run{r}: {old:15s} -> {new:15s}  [{k}] GT={GT[cid]}")
print(f"\n  re-judge lines total: {tot_lines}; verdict CHANGED: {tot_changed}"
      f"  (toward {tot_toward}, between HR/CONF {tot_between}, away {tot_away})")
print(f"  paper says 'of the nineteen verdicts the six re-judge files rewrite, fifteen move a case")
print(f"  toward confirmation under the convention, four move between Confirmed and Human-Review,")
print(f"  which the convention counts alike, and none moves away'")

print("\n"+"="*98)
print("H3. THE SAME LEDGER INCLUDING THE DEPLOYED STAGE (run_full*, 3 re-judge files, 7 cases)")
print("="*98)
tot2 = Counter()
for nm, pat in (("full stage","run_full{}"), "andQwen") if False else (("full stage","run_full{}"),):
    for r in (1,2,3):
        pre = batch(pat, r)
        for o in override_lines(pat, r, "verdicts_coganchor_rejudge.jsonl"):
            old = pre[o["defect_id"]]["verdict"]; new = o["verdict"]
            if old != new: tot2[(old,new)] += 1
print("  full stage pre->post transitions:", dict(tot2))

print("\n"+"="*98)
print("J2. 'two identical verdicts' readings of the deployed stage's recall")
print("="*98)
full = []
for r in (1,2,3):
    d = batch("run_full{}", r)
    for o in override_lines("run_full{}", r, "verdicts_coganchor_rejudge.jsonl"):
        d[o["defect_id"]] = o
    full.append(d)
conv = lambda v: v in ("CONFIRMED","HUMAN_REVIEW")
a = sum(1 for c in T if sum(conv(full[r][c]["verdict"]) for r in range(3)) >= 2)
b = sum(1 for c in T if sum(full[r][c]["verdict"] == "CONFIRMED" for r in range(3)) >= 2)
c_ = sum(1 for c in T if sum(full[r][c]["verdict"] == "HUMAN_REVIEW" for r in range(3)) >= 2)
d_ = sum(1 for c in T if (sum(full[r][c]["verdict"]=="CONFIRMED" for r in range(3)) >= 2
                          or sum(full[r][c]["verdict"]=="HUMAN_REVIEW" for r in range(3)) >= 2))
print(f"  >=2 runs say {{CONF,HR}}              : {a}/51   <- the paper's reported rule (39)")
print(f"  >=2 runs literally CONFIRMED          : {b}/51")
print(f"  >=2 runs literally HUMAN_REVIEW      : {c_}/51")
print(f"  >=2 runs agree on a confirming verdict: {d_}/51")
print(f"  dominant verdict >=2 AND confirming  : "
      f"{sum(1 for c in T if (lambda cc: cc.most_common(1)[0][1] >= 2 and conv(cc.most_common(1)[0][0]))(Counter(full[r][c]['verdict'] for r in range(3))))}/51")
print(f"  three-way split cases: {[c for c in CASES if len({full[r][c]['verdict'] for r in range(3)})==3]}")

print("\n"+"="*98)
print("O. PRE-REPAIR CLAUSE CENSUS (full stage with the coganchor override NOT applied)")
print("="*98)
def clause(o):
    p = o.get("perspectives") or {}
    A,B = str(p.get("A","")).upper(), str(p.get("B","")).upper()
    C,D = str(p.get("C","")).upper(), str(p.get("D","")).upper()
    if A.startswith("CONF"): return "A=Confirmed"
    if A.startswith("REFUT") and B.startswith("CONF"): return "A=Refuted+B=Confirmed"
    if A.startswith("REFUT"): return "A=Refuted"
    if B.startswith("CONF"): return "B=Confirmed"
    if "SUPPORTS_DEFECT" in D and "NOT" not in D: return "D=Supports-Defect"
    if "SUPPORTS_NOT_DEFECT" in D: return "D=Supports-Not-Defect"
    if C.startswith("REFUT") and "WEAK" not in C: return "C=Refuted"
    return "catch-all"
for label, useovr in (("post-repair (paper)", True), ("pre-repair (archived)", False)):
    runs = []
    for r in (1,2,3):
        d = batch("run_full{}", r)
        if useovr:
            for o in override_lines("run_full{}", r, "verdicts_coganchor_rejudge.jsonl"):
                d[o["defect_id"]] = o
        runs.append(d)
    t = Counter(); wrong = Counter()
    for r in range(3):
        for c in CASES:
            k = clause(runs[r][c]); t[k] += 1
            if k in ("A=Refuted","C=Refuted","D=Supports-Not-Defect") and GT[c] == "T": wrong[k] += 1
    print(f"  {label}: A=Refuted {t['A=Refuted']}, C=Refuted {t['C=Refuted']}, "
          f"catch-all {t['catch-all']}, total {sum(t.values())}")
print("  paper §4.5: 'the archived pre-repair cells would give contract refutation 47 closures")
print("  and by-design 20'  and the post-repair table is 50 / 19")

print("\n"+"="*98)
print("P. THE PRE-REPAIR COUNTERFACTUALS the paper prints for the second repair")
print("="*98)
for nm, pat in (("full, no source","run_fullnosrc{}"),("full, no aggregation","run_noscopic{}")):
    pre = [batch(pat, r) for r in (1,2,3)]
    post = []
    for r in (1,2,3):
        d = batch(pat, r)
        for o in override_lines(pat, r, "verdicts_coganchor_rejudge.jsonl"): d[o["defect_id"]] = o
        post.append(d)
    def arms(runs, conv=True):
        ok = (lambda v: v in ("CONFIRMED","HUMAN_REVIEW")) if conv else (lambda v: v=="CONFIRMED")
        m = {c: sum(ok(runs[r][c]["verdict"]) for r in range(3)) >= 2 for c in CASES}
        tp = sum(m[c] and GT[c]=="T" for c in CASES); fp = sum(m[c] and GT[c]=="F" for c in CASES)
        tn = sum((not m[c]) and GT[c]=="F" for c in CASES)
        return tp, fp, tn
    for lbl, runs in (("pre ", pre), ("post", post)):
        tp, fp, tn = arms(runs); ftp = arms(runs, False)[0]
        print(f"  {nm:22s} {lbl}  conv {tp}+{fp}  supp {tn}/30 = {tn/30:.3f}  forced recall {ftp}/51")
