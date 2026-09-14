"""Audit every C=REFUTED vote the full stage cast on an adjudicated TRUE BUG.

Two questions, both raised by the design owner:
  (1) was the refutation backed by verbatim intent evidence (a source comment or
      docstring), as red line 3 requires -- or is it bare structural inference,
      which the rule says must be recorded as WEAK_REFUTED and routed, never
      used to close a case as FALSE_POSITIVE?
  (2) did C actually decide the verdict, or was the case driven by another
      perspective and C merely recorded alongside?
"""
import glob
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

V3 = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
GT = json.load(open(r".paperpilot/phase2-rerun/arms/rq2_3run/gt_81.json",
                    encoding="utf-8"))
CASES7 = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
          "milvus_021", "milvus_027", "qdrant_017"}
IS_C = lambda v: v in ("CONFIRMED", "HUMAN_REVIEW")


def load(r):
    d = {}
    for f in sorted(glob.glob(f"{V3}/run_full{r}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if l:
                o = json.loads(l)
                d[o["defect_id"]] = o
    for l in open(f"{V3}/run_full{r}/verdicts_coganchor_rejudge.jsonl",
                  encoding="utf-8"):
        l = l.strip()
        if l:
            o = json.loads(l)
            if o["defect_id"] in CASES7:
                d[o["defect_id"]] = o
    return d


runs = [load(r) for r in (1, 2, 3)]


def driver(o):
    """Which clause of the fixed aggregation actually decided this judgment."""
    p = o.get("perspectives") or {}
    A = str(p.get("A", "")).upper()
    B = str(p.get("B", "")).upper()
    C = str(p.get("C", "")).upper()
    D = str(p.get("D", "")).upper()
    if A.startswith("CONF"):
        return "A=CONFIRMED"
    if A.startswith("REFUT"):
        return "A=REFUTED"
    if B.startswith("CONF"):
        return "B=CONFIRMED"
    if "SUPPORTS_DEFECT" in D:
        return "D=SUPPORTS_DEFECT"
    if "SUPPORTS_NOT_DEFECT" in D:
        return "D=SUPPORTS_NOT_DEFECT"
    if C.startswith("REFUT") and "WEAK" not in C:
        return "C=REFUTED"
    if "WEAK" in C:
        return "C=WEAK_REFUTED"
    return "catch-all"


# verbatim intent evidence = a quoted comment/docstring, or a cognition quote
VERBATIM = re.compile(r"[‘’'\"“”]|//|/\*|docstring|注释|文档字符串|developer_quote"
                      r"|quote|原话|明文注释", re.I)
BARE = re.compile(r"by_design_in_source|回退|常量|无校验|结构|直传|硬编码|静默丢弃",
                  re.I)

print("=== every C=REFUTED vote on an adjudicated TRUE BUG ===")
n_vote = n_decided = n_bare = n_cog = 0
for i in sorted(GT):
    if GT[i] != "T":
        continue
    for r in range(3):
        o = runs[r][i]
        C = str((o.get("perspectives") or {}).get("C", "")).upper()
        if not ("REFUT" in C and "WEAK" not in C):
            continue
        n_vote += 1
        d = driver(o)
        ev = o.get("d_evidence", "")
        rat = o.get("rationale", "")
        verb = bool(VERBATIM.search(ev + " " + rat))
        bare = bool(BARE.search(ev)) and not re.search(r"[‘’'\"“”]", ev)
        tag = []
        if d == "C=REFUTED":
            n_decided += 1
            tag.append("DECIDED-BY-C")
        if bare:
            n_bare += 1
            tag.append("BARE-STRUCTURE")
        if "D=SUPPORTS_NOT_DEFECT" in d or "认知" in rat:
            n_cog += 1
            tag.append("COGNITION")
        if not verb:
            tag.append("no-verbatim-quote")
        print(f"  {i:14s} r{r+1}  verdict={o['verdict']:14s} "
              f"actual-driver={d:22s} {' '.join(tag)}")

print(f"\n  C=REFUTED votes on true bugs      : {n_vote}")
print(f"  ...where C actually decided the FP: {n_decided}")
print(f"  ...carrying bare structural infer.: {n_bare}")
print(f"  ...routed through cognition       : {n_cog}")
