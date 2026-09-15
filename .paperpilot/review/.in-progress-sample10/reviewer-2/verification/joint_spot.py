import json, os, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"c:\Users\11428\Desktop\TestVDB_artifact\rq2\verdicts"
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
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
UPHELD = ["milvus_005","milvus_013","milvus_036","milvus_038","milvus_043",
          "qdrant_014","qdrant_015","qdrant_016","qdrant_027"]
FLAT_UPHELD = ["milvus_036","milvus_038","milvus_043","qdrant_014","milvus_033","weaviate_003"]
print("GT of the worksheet's CONFIRM list:")
for c in UPHELD: print(f"   {c:14s} {GT[c]}")
print("GT of the flat section's upheld list:")
for c in FLAT_UPHELD: print(f"   {c:14s} {GT[c]}")
print()
for nm, pat, ovr, target in (("full stage","run_full{}","verdicts_coganchor_rejudge.jsonl",33),
                             ("flat + aggregation","run_flatagg{}",None,32),
                             ("flat judge","run_flat{}","verdicts_rejudge_cog.jsonl",29)):
    runs = load(pat, ovr)
    forced = {c: sum(runs[r][c]["verdict"]=="CONFIRMED" for r in range(3)) >= 2 for c in GT}
    conv   = {c: sum(runs[r][c]["verdict"] in ("CONFIRMED","HUMAN_REVIEW") for r in range(3)) >= 2 for c in GT}
    ftp = sum(1 for c in GT if forced[c] and GT[c]=="T")
    upheld_tp = sum(1 for c in UPHELD if GT[c]=="T" and not forced[c])
    upheld_tp_flat = sum(1 for c in FLAT_UPHELD if GT[c]=="T" and not forced[c])
    print(f"{nm:20s} forced recall {ftp};  joint(UPHELD set) = {ftp}+{upheld_tp} = {ftp+upheld_tp}"
          f"   (flat-upheld variant {ftp}+{upheld_tp_flat} = {ftp+upheld_tp_flat})   paper joint {target}")
