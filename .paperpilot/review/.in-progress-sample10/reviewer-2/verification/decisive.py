"""Which operationalisation gives the paper's '22 decisive routed cases' (control)
and '8' (flat judge)?"""
import glob, json, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ART = r"c:\Users\11428\Desktop\TestVDB_artifact"
ROOT = os.path.join(ART, "rq2", "verdicts")
GT = json.load(open(os.path.join(ROOT, "gt_81.json"), encoding="utf-8"))
CASES = sorted(GT); T = [c for c in CASES if GT[c] == "T"]

def load(pat, ovr):
    runs = []
    for r in (1, 2, 3):
        d = {}
        for f in sorted(glob.glob(os.path.join(ROOT, pat.format(r), "verdicts_batch*.jsonl"))):
            for line in open(f, encoding="utf-8"):
                if line.strip():
                    o = json.loads(line); d[o["defect_id"]] = o
        if ovr:
            p = os.path.join(ROOT, pat.format(r), ovr)
            if os.path.exists(p):
                for line in open(p, encoding="utf-8"):
                    if line.strip():
                        o = json.loads(line); d[o["defect_id"]] = o
        runs.append(d)
    return runs

for nm, pat, ovr, paper_q, paper_never in (("flat + aggregation (control)", "run_flatagg{}", None, 22, 9),
                                           ("flat judge", "run_flat{}", "verdicts_rejudge_cog.jsonl", 8, 2)):
    runs = load(pat, ovr)
    hr = {c: sum(runs[r][c]["verdict"] == "HUMAN_REVIEW" for r in range(3)) for c in CASES}
    forced = {c: sum(runs[r][c]["verdict"] == "CONFIRMED" for r in range(3)) >= 2 for c in CASES}
    q1 = [c for c in CASES if hr[c] >= 1]
    # the convention confirmation of a case with >=1 HR run hinges on the routing:
    # it is confirmed by convention but NOT under forced verdicts
    decisive = [c for c in q1 if not forced[c]]
    print(f"{nm}: >=1HR {len(q1)};  not-forced-confirmed among them {len(decisive)}   [paper {paper_q}]")
    print(f"    of the decisive, true bugs {sum(1 for c in decisive if GT[c]=='T')}")
    ruled = {
        "milvus_005","milvus_013","milvus_036","milvus_038","milvus_043","qdrant_014","qdrant_015",
        "qdrant_016","qdrant_027","milvus_001","milvus_031","milvus_004","milvus_006","milvus_012",
        "milvus_030","qdrant_026","weaviate_007","milvus_019","milvus_021","milvus_010","milvus_033",
        "weaviate_003"}
    unruled = sorted(c for c in decisive if c not in ruled)
    print(f"    decisive cases not in the worksheet: {len(unruled)} {unruled}   [paper {paper_never}]")
    print(f"    of those, true bugs: {[c for c in unruled if GT[c]=='T']}")
    q2 = [c for c in CASES if hr[c] >= 2]
    print(f"    alt (>=2HR) decisive {len(q2)}; unruled {len([c for c in q2 if c not in ruled])} {sorted(c for c in q2 if c not in ruled)}")
    print()
