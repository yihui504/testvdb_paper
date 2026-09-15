import json, os, re, sys, glob
from collections import Counter
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ART = r"c:\Users\11428\Desktop\TestVDB_artifact"
P = os.path.join(ART, "rq2", "analyses", "pricing")
ROOT = os.path.join(ART, "rq2", "verdicts")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT); T = [c for c in CASES if GT[c] == "T"]

ws = open(os.path.join(P, "HR17_adjudication_worksheet.md"), encoding="utf-8").read()
blocks = re.split(r"^## ", ws, flags=re.M)[1:]
print("worksheet cases:", len(blocks))
rul = {}
for b in blocks:
    cid = b.split()[0]
    m = re.search(r"裁决: \[([ x])\] CONFIRM\s+\[([ x])\] RETURN\s+\[([ x])\] REJECT", b)
    if not m:
        print("  NO RULING PARSED for", cid); continue
    r = ["CONFIRM","RETURN","REJECT"][[g.replace(" ","") for g in m.groups()].index("x")]
    rul[cid] = r
print("rulings:", dict(Counter(rul.values())))
print("CONFIRM:", sorted(c for c,v in rul.items() if v=="CONFIRM"))
print("RETURN :", sorted(c for c,v in rul.items() if v=="RETURN"))
print("REJECT :", sorted(c for c,v in rul.items() if v=="REJECT"))
print("of the CONFIRMs, true bugs:", sum(1 for c,v in rul.items() if v=="CONFIRM" and GT[c]=="T"))
print("of the RETURNs,  true bugs:", sum(1 for c,v in rul.items() if v=="RETURN" and GT[c]=="T"))

rq = json.load(open(os.path.join(P, "routed_unique.json"), encoding="utf-8"))
print("\nrouted_unique: full", len(rq["full_routed"]), "flat", len(rq["flat_routed"]), "unique", len(rq["unique"]))

def load(pat, ovr):
    runs=[]
    for r in (1,2,3):
        d={}
        for f in sorted(glob.glob(os.path.join(ROOT, pat.format(r), "verdicts_batch*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                if line.strip(): o=json.loads(line); d[o["defect_id"]]=o
        if ovr:
            p=os.path.join(ROOT, pat.format(r), ovr)
            if os.path.exists(p):
                for line in open(p, encoding="utf-8"):
                    if line.strip(): o=json.loads(line); d[o["defect_id"]]=o
        runs.append(d)
    return runs
def hrcount(runs):  return {c: sum(runs[r][c]["verdict"]=="HUMAN_REVIEW" for r in range(3)) for c in CASES}
def conv(runs):
    return {c: sum(runs[r][c]["verdict"] in ("CONFIRMED","HUMAN_REVIEW") for r in range(3)) >= 2 for c in CASES}

for nm, pat, ovr in (("full stage","run_full{}","verdicts_coganchor_rejudge.jsonl"),
                     ("flat + aggregation","run_flatagg{}",None),
                     ("flat judge","run_flat{}","verdicts_rejudge_cog.jsonl")):
    runs=load(pat,ovr); h=hrcount(runs); m=conv(runs)
    q1=[c for c in CASES if h[c]>=1]; q2=[c for c in CASES if h[c]>=2]
    print(f"\n  {nm:20s} >=1HR {len(q1)} ({sum(1 for c in q1 if GT[c]=='T')} TP)   >=2HR(decisive) {len(q2)} ({sum(1 for c in q2 if GT[c]=='T')} TP)")
    print(f"     decisive-routed cases never ruled in the worksheet: {sorted(c for c in q2 if c not in rul)}")
    print(f"     1-of-3-routed only (never decisive): {sorted(c for c in q1 if c not in q2)}")

# joint pricing of the contrast: confirm only if the worksheet CONFIRMs the routed case
def joint(runs, extra_confirm=(), extra_strict=True):
    m = conv(runs)
    out = {}
    for c in CASES:
        if m[c]:
            h = sum(runs[r][c]["verdict"]=="HUMAN_REVIEW" for r in range(3))
            # a case is confirmed under the joint reading only if the routed case was CONFIRMed
            out[c] = True
    return out
print("\n  NOTE: convention_pricing.py prints the full stage's joint 33/51; the contrast prices")
print("  (+3 / +4 / +5) are the unscripted quantities the paper flags.")
