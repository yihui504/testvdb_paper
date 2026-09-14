"""Problem 2 (second pass), step 3: aggregate the blind rulings against the
authors' adjudications (worksheet '## case' blocks + '### case — RULING'
entries + the flat-arm summary), compute agreement on the cases with known
author rulings, and re-run the joint reading under the blind rulings."""
import glob
import json
import math
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
MANIFEST = json.load(open("results/extraction-audit/routed_unique.json",
                          encoding="utf-8"))
UNIQ = MANIFEST["unique"]
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))

# ---- authors' adjudications -------------------------------------------------
ws = open(f"{ROOT}/rerun_v3/HR17_adjudication_worksheet.md",
          encoding="utf-8").read()
authors = {}
cur = None
for line in ws.splitlines():
    m = re.match(r"^##\s+(milvus_\d+|qdrant_\d+|weaviate_\d+)", line)
    if m:
        cur = m.group(1)
        continue
    m3 = re.match(r"^###\s+(milvus_\d+|qdrant_\d+|weaviate_\d+)\s+—\s+"
                  r"(CONFIRM|REJECT|RETURN)", line)
    if m3:
        authors[m3.group(1)] = m3.group(2)
        cur = None
        continue
    if cur:
        if "[x] CONFIRM" in line:
            authors[cur] = "CONFIRM"
        elif "[x] RETURN" in line:
            authors[cur] = "RETURN"
        elif "[x] REJECT" in line:
            authors[cur] = "REJECT"
# flat-arm summary line: upheld 6; the set-level overrides resolved above give
# 010=REJECT, 001=RETURN via the ### entries and the ## blocks respectively.
print(f"authors' rulings parsed: {len(authors)}")
missing = [c for c in UNIQ if c not in authors]
print("routed cases without an author ruling:", missing or "none")

# ---- blind rulings -----------------------------------------------------------
blind = {}
for l in open("results/extraction-audit/blind_pass_verdicts.jsonl",
              encoding="utf-8"):
    l = l.strip()
    if not l:
        continue
    o = json.loads(l)
    blind[o["case"]] = o["ruling"]
print(f"blind rulings: {len(blind)}")

# ---- agreement on cases with both rulings ------------------------------------
MAP = {"CONFIRM_AS_DEFECT": "CONFIRM", "RETURN": "RETURN",
       "REJECT": "REJECT"}
both = [c for c in UNIQ if c in authors and c in blind]
agree = sum(1 for c in both if MAP[blind[c]] == authors[c])
print(f"\n== per-case: blind vs authors ({len(both)} with both) ==")
for c in UNIQ:
    b = MAP.get(blind.get(c, "?"), "?")
    a = authors.get(c, "?")
    mark = "  " if b == a and c in both else "!!" if c in both else "??"
    print(f"  {mark} {c:14s} GT={GT[c]}  blind={b:8s} authors={a}")
print(f"\nagreement {agree}/{len(both)} = {agree / len(both):.3f}")

po = agree / len(both)
marg_b = Counter(MAP[blind[c]] for c in both)
marg_a = Counter(authors[c] for c in both)
pe = sum((marg_b[k] / len(both)) * (marg_a[k] / len(both))
         for k in ("CONFIRM", "RETURN", "REJECT"))
kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
print(f"Cohen's kappa = {kappa:.3f}  (po={po:.3f}, pe={pe:.3f})")

# ---- joint reading under blind rulings ---------------------------------------
def load(base, run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o["verdict"]
    return d


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
for r in range(3):
    p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
    for l in open(p, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        if o.get("defect_id") in CASES_FULL:
            full[r][o["defect_id"]] = o["verdict"]

full_m = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
flat_m = {i: sum(is_c(flat[r][i]) for r in range(3)) >= 2 for i in GT}
full_routed = {i for i in GT if full_m[i]
               and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))}
flat_routed = {i for i in GT if flat_m[i]
               and any(flat[r][i] == "HUMAN_REVIEW" for r in range(3))}
full_forced = {i: sum(full[r][i] == "CONFIRMED" for r in range(3)) >= 2
               for i in GT}
flat_forced = {i: sum(flat[r][i] == "CONFIRMED" for r in range(3)) >= 2
               for i in GT}


def joint(maj, routed, forced, confirm_set):
    out = {}
    for i in GT:
        if not maj[i]:
            out[i] = False
        elif i in routed and not forced[i]:
            out[i] = i in confirm_set
        else:
            out[i] = True
    return out


blind_confirm = {c for c, v in blind.items() if MAP[v] == "CONFIRM"}
AUTH_CONFIRM = {c for c, v in authors.items() if v == "CONFIRM"}
print(f"\nblind CONFIRM: {len(blind_confirm)}; authors CONFIRM: "
      f"{len(AUTH_CONFIRM)}")


def stats(name, conf):
    tp = sum(1 for i in GT if conf[i] and GT[i] == "T")
    fp = sum(1 for i in GT if conf[i] and GT[i] == "F")
    print(f"{name:26s} recall {tp}/51={tp / 51:.3f}  supp {30 - fp}/30="
          f"{(30 - fp) / 30:.3f}  prec {tp / (tp + fp) if tp + fp else 0:.3f}")


print("\n== joint reading: authors' pass vs blind pass ==")
stats("full joint (authors)", joint(full_m, full_routed, full_forced,
                                    AUTH_CONFIRM))
stats("full joint (BLIND)  ", joint(full_m, full_routed, full_forced,
                                    blind_confirm))
stats("flat joint (authors)", joint(flat_m, flat_routed, flat_forced,
                                    AUTH_CONFIRM))
stats("flat joint (BLIND)  ", joint(flat_m, flat_routed, flat_forced,
                                    blind_confirm))
