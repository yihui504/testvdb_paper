"""Reviewer-2 independent verification, part 2: the paper's secondary claims."""
import glob, json, math, os, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ART = sys.argv[1] if len(sys.argv) > 1 else "c:/Users/11428/Desktop/TestVDB_artifact"
ROOT = os.path.join(ART, "rq2", "verdicts")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT)
T = [c for c in CASES if GT[c] == "T"]

def load(pattern, override):
    runs = []
    for r in (1, 2, 3):
        d = {}
        for f in sorted(glob.glob(os.path.join(ROOT, pattern.format(r), "verdicts_batch*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                if line.strip():
                    o = json.loads(line); d[o["defect_id"]] = o
        if override:
            p = os.path.join(ROOT, pattern.format(r), override)
            if os.path.exists(p):
                for line in open(p, encoding="utf-8"):
                    if line.strip():
                        o = json.loads(line); d[o["defect_id"]] = o
        runs.append(d)
    return runs

def maj(runs, convention=True):
    ok = (lambda v: v in ("CONFIRMED","HUMAN_REVIEW")) if convention else (lambda v: v == "CONFIRMED")
    return {c: sum(ok(runs[r][c]["verdict"]) for r in range(3)) >= 2 for c in CASES}

print("="*96); print("C-FIX. FORCED TRUE-BUG SET INTERSECTIONS, correct arm pairs"); print("="*96)
full = load("run_full{}", "verdicts_coganchor_rejudge.jsonl")
fagg = load("run_flatagg{}", None)
fullq = load("run_fullq{}", "verdicts_coganchor_rejudge.jsonl")
faggq = load("run_flataggq{}", None)
def tpset(runs):
    m = maj(runs, convention=False); return {c for c in T if m[c]}
a, b = tpset(full), tpset(fagg)
print(f"  PRIMARY  full stage forced TPs {len(a)} vs flat+aggregation forced TPs {len(b)}"
      f"  -> intersection {len(a & b)} of {len(a)}   [paper: 22 of 27]")
c, d = tpset(fullq), tpset(faggq)
print(f"  SECOND   full-Qwen forced TPs {len(c)} vs flat+agg-Qwen forced TPs {len(d)}"
      f"  -> intersection {len(c & d)} of {len(c)}   [paper: 23 of 26]")

print("\n"+"="*96); print("H. THE SECOND LEAK REPAIR: pre/post coganchor rejudge"); print("="*96)
for nm, pat, ovr in (("full stage","run_full{}","verdicts_coganchor_rejudge.jsonl"),
                     ("full, no source","run_fullnosrc{}","verdicts_coganchor_rejudge.jsonl"),
                     ("full, no aggregation","run_noscopic{}","verdicts_coganchor_rejudge.jsonl"),
                     ("full-Qwen","run_fullq{}","verdicts_coganchor_rejudge.jsonl")):
    post = load(pat, ovr)
    pre  = load(pat, None)   # no override == pre-repair state
    moved = 0; toward = 0; between = 0; away = 0
    was = []
    for r in range(3):
        p = os.path.join(ROOT, pat.format(r), ovr) if ovr else None
        if not p or not os.path.exists(p): continue
        for line in open(p, encoding="utf-8"):
            if not line.strip(): continue
            o = json.loads(line); cid = o["defect_id"]
            old = pre[r][cid]["verdict"]; new = o["verdict"]
            if old != new:
                moved += 1
                rank = {"FALSE_POSITIVE":0,"HUMAN_REVIEW":1,"CONFIRMED":2}
                was.append((cid, r, old, new))
                if rank[new] > rank[old]: toward += 1
                elif rank[new] < rank[old]: away += 1
                else: between += 1
    mp_post = maj(post); mp_pre = maj(pre)
    conv = lambda m: (sum(m[c] and GT[c]=="T" for c in CASES), sum(m[c] and GT[c]=="F" for c in CASES))
    print(f"  {nm:22s} overridden verdicts changed: {moved}  toward-confirm {toward}  cross-HR/FP {between}  away {away}")
    print(f"      convention  pre {conv(mp_pre)}  post {conv(mp_post)}   (tp+fp)")
    print(f"      forced recall pre {sum(1 for c in T if maj(pre,False)[c])}  post {sum(1 for c in T if maj(post,False)[c])}")
    if nm in ("full stage",):
        print(f"      suppressed FPs: pre {sum(1 for c in CASES if GT[c]=='F' and not mp_pre[c])}/30  post {sum(1 for c in CASES if GT[c]=='F' and not mp_post[c])}/30")

print("\n"+"="*96); print("I. milvus_001: routed by how many of the 12 configurations?"); print("="*96)
ARMS = [("contract core","run{}","verdicts_rejudge_cog.jsonl"),("full stage","run_full{}","verdicts_coganchor_rejudge.jsonl"),
        ("source-only","run_donly{}","verdicts_rejudge_cog.jsonl"),("flat judge","run_flat{}","verdicts_rejudge_cog.jsonl"),
        ("flat + schema fix","run_flatschema{}",None),("flat + aggregation","run_flatagg{}",None),
        ("full, no source","run_fullnosrc{}","verdicts_coganchor_rejudge.jsonl"),
        ("full, no aggregation","run_noscopic{}","verdicts_coganchor_rejudge.jsonl"),
        ("source-only-Qwen","run_donlyq{}","verdicts_rejudge_cog.jsonl"),("full-Qwen","run_fullq{}","verdicts_coganchor_rejudge.jsonl"),
        ("flat-Qwen","run_flatq{}","verdicts_rejudge_cog.jsonl"),("flat + aggregation-Qwen","run_flataggq{}",None)]
routed = 0
for nm, pat, ovr in ARMS:
    runs = load(pat, ovr)
    n = sum(1 for r in range(3) if runs[r]["milvus_001"]["verdict"] == "HUMAN_REVIEW")
    ok = n >= 2
    routed += ok
    print(f"  {nm:24s} milvus_001 HR in {n} of 3 runs -> {'credited' if ok else 'NOT credited'}")

print("\n"+"="*96); print("J. THREE-WAY SPLITS and the 'two identical verdicts' rule (full stage)"); print("="*96)
three = [c for c in CASES if len({full[r][c]["verdict"] for r in range(3)}) == 3]
print(f"  cases with three distinct verdicts: {len(three)} {three}   [paper: three of the 81]")
strict = {c: sum(1 for r in range(3) if full[r][c]["verdict"] == "HUMAN_REVIEW") +
             sum(1 for r in range(3) if full[r][c]["verdict"] == "CONFIRMED") for c in CASES}
# rule: two identical verdicts required (identical literal verdict strings)
ident = {c: max(Counter(full[r][c]["verdict"] for r in range(3)).values()) >= 2 for c in CASES}
print(f"  under 'two identical verdicts' the deployed recall would be "
      f"{sum(1 for c in T if ident[c])}/51   [paper: 37/51]")

print("\n"+"="*96); print("K. C=REFUTED RATIONALE AUDIT (primary, 19 judgments)"); print("="*96)
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
cr = [(c, r) for r in range(3) for c in CASES if clause(full[r][c]) == "C=Refuted"]
print(f"  C=Refuted judgments: {len(cr)}")
print(f"  by case: {Counter(c for c,r in cr)}")
for c, r in sorted(cr):
    o = full[r][c]
    print(f"\n  --- {c} run{r+1}  GT={GT[c]}  C={o.get('perspectives',{}).get('C')}")
    print(f"      d_evidence: {str(o.get('d_evidence'))[:120]}")
    print(f"      rationale : {str(o.get('rationale'))[:600]}")

print("\n"+"="*96); print("L. WEAK-REFUTED runs of milvus_011 / milvus_012"); print("="*96)
for cid in ("milvus_011","milvus_012","milvus_026"):
    print(f"\n  ### {cid}  GT={GT[cid]}")
    for r in range(3):
        o = full[r][cid]
        print(f"    run{r+1}: verdict={o['verdict']}  C={o.get('perspectives',{}).get('C')}")
        print(f"        rationale: {str(o.get('rationale'))[:500]}")

print("\n"+"="*96); print("M. CATCH-ALL D-VALUE COMPOSITION (primary)"); print("="*96)
ca = [(r,c) for r in range(3) for c in CASES if clause(full[r][c]) == "catch-all"]
print(f"  {Counter(str((full[r][c].get('perspectives') or {}).get('D')) for r,c in ca)}")

print("\n"+"="*96); print("N. WILSON INTERVALS for the headline arms"); print("="*96)
def wilson(k,n,z=1.959964):
    p=k/n; d=1+z*z/n; cen=(p+z*z/(2*n))/d
    h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/d
    return (max(0.0,cen-h), min(1.0,cen+h))
for nm, pat, ovr in (("full stage","run_full{}","verdicts_coganchor_rejudge.jsonl"),
                     ("flat judge","run_flat{}","verdicts_rejudge_cog.jsonl")):
    m = maj(load(pat, ovr)); k = sum(1 for c in T if m[c])
    print(f"  {nm:14s} recall {k}/51 = {k/51:.3f}  Wilson {tuple(round(x,3) for x in wilson(k,51))}")
