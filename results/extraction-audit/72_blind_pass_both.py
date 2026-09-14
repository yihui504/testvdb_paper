"""Problem 2 final: compare both blind passes (pack-only = source-access
ablation; pack+source = protocol-faithful replication) against the authors'
adjudications, and recompute the joint reading under each."""
import glob
import json
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run"
CASES_FULL = {"milvus_004", "milvus_006", "milvus_018", "milvus_019",
              "milvus_021", "milvus_027", "qdrant_017"}
UNIQ = json.load(open("results/extraction-audit/routed_unique.json",
                      encoding="utf-8"))["unique"]
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))
MAP = {"CONFIRM_AS_DEFECT": "CONFIRM", "RETURN": "RETURN",
       "REJECT": "REJECT"}

# ---- authors' rulings -------------------------------------------------------
ws = open(f"{ROOT}/rerun_v3/HR17_adjudication_worksheet.md",
          encoding="utf-8").read()
authors = {}
cur = None
for line in ws.splitlines():
    m = re.match(r"^##\s+([a-z]+_\d+)", line)
    if m:
        cur = m.group(1)
        continue
    m3 = re.match(r"^###\s+([a-z]+_\d+)\s+—\s+(CONFIRM|REJECT|RETURN)", line)
    if m3:
        authors[m3.group(1)] = m3.group(2)
        cur = None
        continue
    if cur:
        for tag, val in (("[x] CONFIRM", "CONFIRM"), ("[x] RETURN", "RETURN"),
                         ("[x] REJECT", "REJECT")):
            if tag in line:
                authors[cur] = val


def load_verdicts(path):
    d = {}
    for l in open(path, encoding="utf-8"):
        l = l.strip()
        if not l:
            continue
        o = json.loads(l)
        d[o["case"]] = MAP[o["ruling"]]
    return d


passes = {
    "pack-only     (68)": load_verdicts(
        "results/extraction-audit/blind_pass_verdicts.jsonl"),
    "pack+source   (71)": load_verdicts(
        "results/extraction-audit/blind_pass_source_verdicts.jsonl"),
    "full protocol (73)": load_verdicts(
        "results/extraction-audit/blind_pass_protocol_verdicts.jsonl"),
}

print(f"authors' rulings: {len(authors)}; routed cases with no author ruling: "
      f"{[c for c in UNIQ if c not in authors]}\n")

for name, blind in passes.items():
    both = [c for c in UNIQ if c in authors and c in blind]
    agree = sum(1 for c in both if blind[c] == authors[c])
    po = agree / len(both)
    mb = Counter(blind[c] for c in both)
    ma = Counter(authors[c] for c in both)
    pe = sum((mb[k] / len(both)) * (ma[k] / len(both))
             for k in ("CONFIRM", "RETURN", "REJECT"))
    kappa = (po - pe) / (1 - pe) if pe < 1 else float("nan")
    print(f"== {name} ==")
    print(f"   rulings: {dict(Counter(blind.values()))}")
    print(f"   agreement {agree}/{len(both)} = {po:.3f}   kappa = {kappa:.3f}")
    print(f"   CONFIRM cases: {sorted(c for c in blind if blind[c] == 'CONFIRM')}")
    print()

# ---- joint reading under each pass -----------------------------------------
def load_run(base, run):
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


full = [load_run("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat = [load_run("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]
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


def joint(maj, routed, forced, confirms):
    out = {}
    for i in GT:
        if not maj[i]:
            out[i] = False
        elif i in routed and not forced[i]:
            out[i] = i in confirms
        else:
            out[i] = True
    return out


def stats(name, conf):
    tp = sum(1 for i in GT if conf[i] and GT[i] == "T")
    fp = sum(1 for i in GT if conf[i] and GT[i] == "F")
    print(f"   {name:24s} recall {tp}/51={tp / 51:.3f}  supp {30 - fp}/30="
          f"{(30 - fp) / 30:.3f}  prec "
          f"{tp / (tp + fp) if tp + fp else 0:.3f}")


print("== joint reading (full arm) ==")
stats("authors' pass",
      joint(full_m, full_routed, full_forced,
            {c for c, v in authors.items() if v == "CONFIRM"}))
for name, blind in passes.items():
    stats(name.split()[0], joint(full_m, full_routed, full_forced,
                                 {c for c, v in blind.items()
                                  if v == "CONFIRM"}))
print("\n== joint reading (flat arm) ==")
stats("authors' pass",
      joint(flat_m, flat_routed, flat_forced,
            {c for c, v in authors.items() if v == "CONFIRM"}))
for name, blind in passes.items():
    stats(name.split()[0], joint(flat_m, flat_routed, flat_forced,
                                 {c for c, v in blind.items()
                                  if v == "CONFIRM"}))
