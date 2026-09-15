"""Reviewer-2 independent recomputation, from raw JSONL only.

Does NOT import the artifact's analysis scripts. Re-derives every quantity the
paper prints, from rq2/verdicts/*/verdicts_batch*.jsonl + the re-judge overrides,
using the conventions the paper states in text.

Run:  python indep_recompute.py <artifact_root>
"""
import glob, json, math, os, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ART = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/11428/Desktop/TestVDB_artifact"
ROOT = os.path.join(ART, "rq2", "verdicts")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT)
NB = sum(1 for c in CASES if GT[c] == "T")
NF = sum(1 for c in CASES if GT[c] == "F")
print(f"pool: {NB} T + {NF} F = {len(CASES)}   (paper says 51 + 30 = 81)")

ARMS = [
    ("contract core",        "run{}",            "verdicts_rejudge_cog.jsonl"),
    ("full stage",           "run_full{}",       "verdicts_coganchor_rejudge.jsonl"),
    ("source-only",          "run_donly{}",      "verdicts_rejudge_cog.jsonl"),
    ("flat judge",           "run_flat{}",       "verdicts_rejudge_cog.jsonl"),
    ("flat + schema fix",    "run_flatschema{}", None),
    ("flat + aggregation",   "run_flatagg{}",    None),
    ("full, no source",      "run_fullnosrc{}",  "verdicts_coganchor_rejudge.jsonl"),
    ("full, no aggregation", "run_noscopic{}",   "verdicts_coganchor_rejudge.jsonl"),
    ("source-only-Qwen",     "run_donlyq{}",     "verdicts_rejudge_cog.jsonl"),
    ("full-Qwen",            "run_fullq{}",      "verdicts_coganchor_rejudge.jsonl"),
    ("flat-Qwen",            "run_flatq{}",      "verdicts_rejudge_cog.jsonl"),
    ("flat + aggregation-Qwen", "run_flataggq{}", None),
]

def load(pattern, override):
    runs = []
    for r in (1, 2, 3):
        d = {}
        for f in sorted(glob.glob(os.path.join(ROOT, pattern.format(r), "verdicts_batch*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                line = line.strip()
                if line:
                    o = json.loads(line)
                    if o["defect_id"] in d:
                        raise SystemExit(f"DUPLICATE {o['defect_id']} in {f}")
                    d[o["defect_id"]] = o
        if override:
            p = os.path.join(ROOT, pattern.format(r), override)
            if os.path.exists(p):
                for line in open(p, encoding="utf-8"):
                    line = line.strip()
                    if line:
                        o = json.loads(line)
                        d[o["defect_id"]] = o   # override wins
        if len(d) != len(CASES):
            print(f"   !! {pattern.format(r)}: {len(d)} cases, expected {len(CASES)}")
        runs.append(d)
    return runs

def maj(runs, convention=True):
    ok = (lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")) if convention else (lambda v: v == "CONFIRMED")
    return {c: sum(ok(runs[r][c]["verdict"]) for r in range(3)) >= 2 for c in CASES}

def mcnemar(b, c):
    n = b + c
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(0, min(b, c) + 1)) / 2 ** n)

loaded = {}
print("\n" + "=" * 96)
print("A. PER-ARM MAJORITY MATRICES  (convention: HR counts confirmed)")
print("=" * 96)
print(f"{'arm':24s} {'recall':>8s} {'supp':>7s} {'prec':>6s} {'forced':>7s} {'conf set':>9s}  HR/243")
for name, pat, ovr in ARMS:
    runs = load(pat, ovr)
    if any(len(r) != len(CASES) for r in runs):
        print(f"{name:24s} LOAD FAILED"); continue
    loaded[name] = runs
    m = maj(runs); mf = maj(runs, convention=False)
    tp = sum(m[c] and GT[c] == "T" for c in CASES); fp = sum(m[c] and GT[c] == "F" for c in CASES)
    tn = sum((not m[c]) and GT[c] == "F" for c in CASES)
    ftp = sum(mf[c] and GT[c] == "T" for c in CASES)
    hr = sum(runs[r][c]["verdict"] == "HUMAN_REVIEW" for r in range(3) for c in CASES)
    print(f"{name:24s} {tp:3d}/{NB} {tn:3d}/{NF} {tp/(tp+fp):6.3f} {ftp:3d}/{NB}  {tp:3d}+{fp:<4d} {hr:4d} {hr/243:6.1%}")

print("\n" + "=" * 96)
print("B. PAIRED EXACT McNEMAR -- confirmed set (n=81) and recall level (n=51)")
print("=" * 96)
M = {n: maj(loaded[n]) for n in loaded}
T = [c for c in CASES if GT[c] == "T"]
PAIRS = [("full stage","flat judge"),("flat + aggregation","flat judge"),
         ("flat judge","contract core"),("flat + aggregation","full stage"),
         ("full, no source","full stage"),("full, no aggregation","full stage"),
         ("full, no aggregation","flat + aggregation"),("flat + schema fix","flat judge"),
         ("flat + aggregation","flat + schema fix"),("full, no aggregation","flat judge"),
         ("full, no aggregation","flat + schema fix"),("flat + aggregation-Qwen","flat-Qwen"),
         ("full-Qwen","flat + aggregation-Qwen"),("full-Qwen","flat-Qwen"),
         ("full stage","flat + schema fix")]
for a, b in PAIRS:
    x8 = sum(1 for c in CASES if M[a][c] and not M[b][c]); y8 = sum(1 for c in CASES if M[b][c] and not M[a][c])
    x5 = sum(1 for c in T if M[a][c] and not M[b][c]); y5 = sum(1 for c in T if M[b][c] and not M[a][c])
    ta = sum(1 for c in T if M[a][c]); tb = sum(1 for c in T if M[b][c])
    se = math.sqrt(max(0.0, x5 + y5 - (x5 - y5) ** 2 / len(T))) / len(T)
    print(f"{a:24s} vs {b:24s} | 81set {x8:2d}/{y8:2d} p={mcnemar(x8,y8):.4f} | 51recall {ta}/{tb} {x5:2d}/{y5:2d} p={mcnemar(x5,y5):.4f} +/-{1.96*se:.2f}")

print("\n" + "=" * 96)
print("C. FORCED TRUE-BUG SET INTERSECTIONS (paper: 22 of 27 and 23 of 26)")
print("=" * 96)
sf = {c for c in T if maj(loaded["full stage"], False)[c]}
qf = {c for c in T if maj(loaded["full-Qwen"], False)[c]}
af = {c for c in T if maj(loaded["flat + aggregation-Qwen"], False)[c]}
ff = {c for c in T if maj(loaded["flat-Qwen"], False)[c]}
print(f"  full stage forced TPs {len(sf)}; flat+agg-Qwen forced TPs {len(af)}; intersection {len(sf & af)}")
print(f"  full-Qwen  forced TPs {len(qf)}; flat-Qwen    forced TPs {len(ff)}; intersection {len(qf & ff)}")

print("\n" + "=" * 96)
print("D. CLAUSE CENSUS (primary: run_full1..3, candidate-anchor rejudge applied)")
print("=" * 96)
SRC_VOCAB = {"validation_present","validation_absent","by_design_in_source","not_found"}
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
for bb, pat in (("primary","run_full{}"),("second","run_fullq{}")):
    runs = loaded["full stage"] if bb=="primary" else loaded["full-Qwen"]
    t = defaultdict(lambda: [0,0])
    for r in range(3):
        for c in CASES:
            k = clause(runs[r][c])
            t[k][0 if GT[c]=="T" else 1] += 1
    print(f"\n  --- {bb} backbone ---")
    tot_t = tot_f = 0
    for k in ["B=Confirmed","A=Confirmed","D=Supports-Defect","A=Refuted","C=Refuted",
              "D=Supports-Not-Defect","A=Refuted+B=Confirmed","catch-all"]:
        if k not in t: continue
        nt, nf = t[k]; tot_t += nt; tot_f += nf
        print(f"    {k:24s} n={nt+nf:3d}  onBugs={nt:3d}  onFPs={nf:3d}")
    print(f"    {'TOTAL':24s} n={tot_t+tot_f:3d}  onBugs={tot_t:3d}  onFPs={tot_f:3d}")
    nsrc = sum(1 for r in range(3) for c in CASES if str((runs[r][c].get("perspectives") or {}).get("D","")).lower() in SRC_VOCAB)
    print(f"    D-cell source vocabulary: {nsrc} of 243")
    wrong_fp = t["A=Refuted"][0] + t["C=Refuted"][0] + t["D=Supports-Not-Defect"][0]
    print(f"    incorrect closures to FP total = {wrong_fp};  A=Refuted share = {t['A=Refuted'][0]}/{wrong_fp} = {t['A=Refuted'][0]/wrong_fp:.3f}")

print("\n" + "=" * 96)
print("E. CATCH-ALL COMPOSITION (primary)")
print("=" * 96)
runs = loaded["full stage"]
ca = [(r, c) for r in range(3) for c in CASES if clause(runs[r][c]) == "catch-all"]
print(f"  catch-all judgments: {len(ca)}")
srcv = [(r,c) for r,c in ca if str((runs[r][c].get("perspectives") or {}).get("D","")).lower() in SRC_VOCAB]
cogv = [(r,c) for r,c in ca if (r,c) not in srcv]
print(f"  carrying source vocabulary in D: {len(srcv)} ({len(srcv)/len(ca):.1%})  rest on true bugs: {sum(1 for r,c in srcv if GT[c]=='T')}")
print(f"  carrying cognition vocabulary  : {len(cogv)}  rest on true bugs: {sum(1 for r,c in cogv if GT[c]=='T')} = {sum(1 for r,c in cogv if GT[c]=='T')/len(cogv):.3f}")
print(f"  pool base rate: {NB*3}/243 = {NB*3/243:.3f}")

print("\n" + "=" * 96)
print("F. RULE COMPLIANCE / REPLAYS (primary)")
print("=" * 96)
mand = [(r,c) for r in range(3) for c in CASES if clause(runs[r][c]) == "catch-all"]
rec  = [(r,c) for r in range(3) for c in CASES if runs[r][c]["verdict"] == "HUMAN_REVIEW"]
print(f"  rule mandates HR: {len(mand)};  judge recorded HR: {len(rec)}")
print(f"  deviations: {Counter(runs[r][c]['verdict'] for r,c in mand if runs[r][c]['verdict']!='HUMAN_REVIEW')}")
print(f"  reverse deviations (judge HR, rule not catch-all): {sum(1 for r,c in rec if clause(runs[r][c])!='catch-all')}")
def replay(mut, convention):
    ok = (lambda v: v in ("CONFIRMED","HUMAN_REVIEW")) if convention else (lambda v: v=="CONFIRMED")
    per = [{c: mut(runs[r][c]) for c in CASES} for r in range(3)]
    m = {c: sum(ok(per[r][c]) for r in range(3)) >= 2 for c in CASES}
    tp = sum(m[c] and GT[c]=="T" for c in CASES); tn = sum((not m[c]) and GT[c]=="F" for c in CASES)
    fp = sum(m[c] and GT[c]=="F" for c in CASES)
    return tp, tn, fp
for lbl, mut in (("measured", lambda o: o["verdict"]),
                 ("A=Refuted routed", lambda o: "HUMAN_REVIEW" if clause(o)=="A=Refuted" else o["verdict"]),
                 ("strict compliance", lambda o: "HUMAN_REVIEW" if o["verdict"]=="FALSE_POSITIVE" and clause(o)=="catch-all" else o["verdict"])):
    for conv in (True, False):
        tp, tn, fp = replay(mut, conv)
        print(f"  {lbl:20s} [{'convention' if conv else 'forced':10s}] recall {tp}/51 supp {tn}/30 conf set {tp}+{fp}")

print("\n" + "=" * 96)
print("G. OF THE 24 A=REFUTED TRUE-BUG CLOSURES: case-level span")
print("=" * 96)
cases_ar = [c for c in CASES if sum(1 for r in range(3) if clause(runs[r][c])=="A=Refuted") >= 2]
print(f"  cases closed by A=Refuted in >=2 of 3 runs: {len(cases_ar)}; of them true bugs: {sum(1 for c in cases_ar if GT[c]=='T')}")
mm = M["full stage"]
print(f"  of those true bugs, confirmed by the measured majority: {sum(1 for c in cases_ar if GT[c]=='T' and mm[c])}")
