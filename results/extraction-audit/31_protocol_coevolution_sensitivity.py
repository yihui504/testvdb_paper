"""R2-round-12 sensitivity: protocol-pool co-evolution.
(1) ef/nprobe carve-out: which cases touch the parameter family, and does the
    carve-out flip any verdict; (2) B-driven confirmations (perspective B
    CONFIRMED in >=2 runs, A taking precedence) and recall with them excluded;
    (3) evidence-absent stratum three-reading structure per case."""
import glob
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/rerun_v3/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


full = [load(f"run_full{k}") for k in (1, 2, 3)]
tp41 = sorted(i for i in GT if GT[i] == "T"
              and sum(is_c(full[k][i]["verdict"]) for k in range(3)) >= 2)

print("== 1. nprobe/ef carve-out footprint ==")
fam = []
for i in sorted(GT):
    txt = open(rf".paperpilot/phase2-rerun/arms/materials_complete/{i}.md",
               encoding="utf-8").read()
    if re.search(r"nprobe|ef=|search_params", txt):
        fam.append(i)
fam_t = [i for i in fam if GT[i] == "T"]
fam_f = [i for i in fam if GT[i] == "F"]
print(f"parameter-family cases: {len(fam)} (T {len(fam_t)}, F {len(fam_f)})")
for i in fam:
    vs = [full[k][i]["verdict"] for k in range(3)]
    print(f"  {i} GT={GT[i]} {vs}")

print("\n== 2. B-driven exclusion (A precedence, CONFIRMED>=2 runs) ==")
def driven(i, p, val="CONFIRMED"):
    return sum(1 for k in range(3)
               if full[k][i]["perspectives"].get(p) == val) >= 2
a = [i for i in tp41 if driven(i, "A")]
b = [i for i in tp41 if i not in a and driven(i, "B")]
cog = [i for i in tp41 if i not in a and i not in b
       and (driven(i, "COG", "SUPPORTS_DEFECT")
            or driven(i, "D", "SUPPORTS_DEFECT"))]
rest = [i for i in tp41 if i not in a and i not in b and i not in cog]
print(f"A {len(a)} / B {len(b)} / COG {len(cog)} / none {len(rest)} "
      f"= {len(tp41)}  (paper: 7/16/2/16)")
print(f"recall excluding B-driven: {len(tp41)-len(b)}/51 = "
      f"{(len(tp41)-len(b))/51:.3f}")
print("B-driven nprobe/ef overlap:", sorted(set(b) & set(fam_t)))

print("\n== 3. evidence-absent stratum per case ==")
mainv = [json.loads(l) for l in open(
    r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/"
    "rebuild_v1/verify_verdicts_main.jsonl", encoding="utf-8")]
LAYER = {x["case"]: x["layer"] for x in mainv if x.get("layer")}
AUD = json.load(open(r"c:/Users/11428/Desktop/testvdb_paper/results/"
                     "extraction-audit/rebuild_final/assembly_audit.json",
                     encoding="utf-8"))
for r in AUD:
    if r["case"] not in LAYER:
        LAYER[r["case"]] = ("evidence_absent" if r["rows_kept"] == 0
                            and r["arch"] == 0 else "evidence_present")
LAYER["milvus_038"] = "weak_evidence"
ADJ = {"milvus_005", "milvus_013", "milvus_036", "milvus_038", "milvus_043",
       "qdrant_014", "qdrant_015", "qdrant_016", "qdrant_027"}
ea = [i for i in tp41 if LAYER.get(i) == "evidence_absent"]
pool = sorted(i for i in GT if GT[i] == "T" and LAYER.get(i) == "evidence_absent")
for i in pool:
    vs = [full[k][i]["verdict"] for k in range(3)]
    conv = sum(is_c(v) for v in vs) >= 2
    forc = sum(v == "CONFIRMED" for v in vs) >= 2
    hr = any(v == "HUMAN_REVIEW" for v in vs)
    joint = conv and (not hr or i in ADJ)
    print(f"  {i} {vs} conv={conv} forced={forc} routed={hr} joint={joint}")
n_forced = sum(1 for i in pool
               if sum(full[k][i]['verdict'] == 'CONFIRMED' for k in range(3)) >= 2)
n_joint = sum(1 for i in ea
              if not any(full[k][i]['verdict'] == 'HUMAN_REVIEW' for k in range(3))
              or i in ADJ)
print(f"layer TP: conv {len(ea)}/11, forced {n_forced}/11, joint {n_joint}/11")
