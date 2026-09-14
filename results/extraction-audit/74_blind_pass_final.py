"""Problem 2 final numbers, restricted to the cases where the authors' pass has
a recorded ruling (the comparable subset), plus the substitution effect on the
joint reading."""
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

ws = open(f"{ROOT}/rerun_v3/HR17_adjudication_worksheet.md",
          encoding="utf-8").read()
authors, cur = {}, None
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

PASSES = [
    ("pack-only", "blind_pass_verdicts.jsonl"),
    ("pack+source", "blind_pass_source_verdicts.jsonl"),
    ("full protocol", "blind_pass_protocol_verdicts.jsonl"),
]
loaded = {}
for name, fn in PASSES:
    d = {}
    for l in open(f"results/extraction-audit/{fn}", encoding="utf-8"):
        l = l.strip()
        if l:
            o = json.loads(l)
            d[o["case"]] = MAP[o["ruling"]]
    loaded[name] = d

comparable = [c for c in UNIQ if c in authors]
auth_conf = {c for c in comparable if authors[c] == "CONFIRM"}
print(f"unique routed cases: {len(UNIQ)}; comparable (authors ruled): "
      f"{len(comparable)}")
print(f"authors' CONFIRM on the comparable subset: {len(auth_conf)} -> "
      f"{sorted(auth_conf)}\n")

for name, _ in PASSES:
    b = loaded[name]
    agree = sum(1 for c in comparable if b[c] == authors[c])
    mb = Counter(b[c] for c in comparable)
    ma = Counter(authors[c] for c in comparable)
    pe = sum((mb[k] / len(comparable)) * (ma[k] / len(comparable))
             for k in ("CONFIRM", "RETURN", "REJECT"))
    po = agree / len(comparable)
    kappa = (po - pe) / (1 - pe)
    bc = {c for c in comparable if b[c] == "CONFIRM"}
    print(f"== {name} ==")
    print(f"   CONFIRM {len(bc)} (overlap with authors "
          f"{len(bc & auth_conf)}): {sorted(bc)}")
    print(f"   agreement {agree}/{len(comparable)} = {po:.2f}  "
          f"kappa {kappa:.2f}")
    print(f"   joint recall under this pass: ", end="")

    # joint substitution
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
    for r in range(3):
        p = f"{ROOT}/rerun_v3/run_full{r + 1}/verdicts_coganchor_rejudge.jsonl"
        for l in open(p, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id") in CASES_FULL:
                full[r][o["defect_id"]] = o["verdict"]
    fm = {i: sum(is_c(full[r][i]) for r in range(3)) >= 2 for i in GT}
    ff = {i: sum(full[r][i] == "CONFIRMED" for r in range(3)) >= 2 for i in GT}
    fr = {i for i in GT if fm[i]
          and any(full[r][i] == "HUMAN_REVIEW" for r in range(3))}
    conf = {}
    for i in GT:
        if not fm[i]:
            conf[i] = False
        elif i in fr and not ff[i]:
            conf[i] = i in bc
        else:
            conf[i] = True
    tp = sum(1 for i in GT if conf[i] and GT[i] == "T")
    fp = sum(1 for i in GT if conf[i] and GT[i] == "F")
    print(f"{tp}/51 = {tp / 51:.3f}  (supp {30 - fp}/30 = "
          f"{(30 - fp) / 30:.3f})\n")
