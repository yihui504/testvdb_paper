"""Red line 3 compliance across the whole full arm.

The rule: a by-design refutation (C = REFUTED) is legal only when the source
excerpt carries intent evidence -- a code comment or docstring -- or the
maintainer-cognition material carries a developer quote declaring the same
phenomenon intended. Bare structural inference ("no validation is seen") is
WEAK_REFUTED and must route, never close a case as FALSE_POSITIVE.

Mechanical first pass: does the judgment's evidence carry BOTH a source
location (file:line) AND a quoted fragment? Then a reverse check on
WEAK_REFUTED: does it in fact carry verbatim evidence, i.e. should it have been
REFUTED? Borderline rows are printed for hand adjudication.
"""
import glob
import json
import os
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
V3 = os.path.join(ROOT, "rerun_v3")
CASES7 = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
          "milvus_021", "milvus_027", "qdrant_017"}

SRC_LOC = re.compile(r"[\w./-]+\.(?:go|rs|py|java|cpp|cc|h)\b[^\n]{0,12}?:"
                     r"\s?\d+")
QUOTE = re.compile(r"['\"‘’“”「」]([^'\"‘’“”「」]{6,})['\"‘’“”「」]")
COG_QUOTE = re.compile(r"(?:认知|developer_quote|quote|原话|维护者)[^\n]{0,60}"
                       r"['\"‘’“”「」][^'\"‘’“”「」]{8,}['\"‘’“”「」]")


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

ref_rows, weak_rows = [], []
for r in range(3):
    for i in sorted(runs[r]):
        o = runs[r][i]
        C = str((o.get("perspectives") or {}).get("C", "")).upper()
        if "REFUT" not in C:
            continue
        blob = (o.get("d_evidence", "") or "") + " " + \
               (o.get("rationale", "") or "")
        has_loc = bool(SRC_LOC.search(blob))
        has_quote = bool(QUOTE.search(blob))
        has_cog = bool(COG_QUOTE.search(blob))
        row = (i, r + 1, o["verdict"], has_loc, has_quote, has_cog,
               o.get("d_evidence", "")[:120])
        (weak_rows if "WEAK" in C else ref_rows).append(row)

print(f"=== C = REFUTED ({len(ref_rows)} judgments) ===")
print("  A refutation is rule-compliant if it carries a source location AND a")
print("  quoted fragment, or a maintainer quote from cognition.\n")
ok = bad = 0
for i, r, v, loc, q, cog, ev in ref_rows:
    good = (loc and q) or cog
    ok += good
    bad += not good
    if not good:
        print(f"  [NEEDS REVIEW] {i} r{r} verdict={v} loc={loc} quote={q} cog={cog}")
        print(f"      {ev}")
print(f"\n  compliant (mechanical): {ok}/{len(ref_rows)}")
print(f"  needs hand review     : {bad}/{len(ref_rows)}")

print(f"\n=== C = WEAK_REFUTED ({len(weak_rows)} judgments) — reverse check ===")
print("  A weak refutation carrying verbatim evidence should have been REFUTED.")
susp = 0
for i, r, v, loc, q, cog, ev in weak_rows:
    if (loc and q) or cog:
        susp += 1
        if susp <= 8:
            print(f"  [CHECK] {i} r{r} verdict={v} loc={loc} quote={q} cog={cog}")
            print(f"      {ev}")
print(f"\n  weak refutations carrying verbatim evidence: {susp}/{len(weak_rows)}")
