"""R1/R3-round-12 sensitivity: evidence-access asymmetry in the full-vs-flat
separation. flat/core/D-only dispatches forbid cognition materials; the full
arm reads them. Question: do the cognition materials drive any of the 17/4
discordant cases? Also: D-only-vs-flat dispatch material parity check."""
import glob
import json
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = (r"c:/Users/11428/Desktop/testvdb_paper/.paperpilot/phase2-rerun/"
        "arms/rq2_3run")
GT = json.load(open(ROOT + "/gt_81.json", encoding="utf-8"))


def load(base, run):
    d = {}
    for f in sorted(glob.glob(f"{ROOT}/{base}/{run}/verdicts_batch*.jsonl")):
        for l in open(f, encoding="utf-8"):
            l = l.strip()
            if not l:
                continue
            o = json.loads(l)
            if o.get("defect_id"):
                d[o["defect_id"]] = o
    return d


full = [load("rerun_v3", f"run_full{k}") for k in (1, 2, 3)]
flat = [load("rerun_v3", f"run_flat{k}") for k in (1, 2, 3)]


def is_c(v):
    return v in ("CONFIRMED", "HUMAN_REVIEW")


fc = {i: sum(is_c(full[k][i]["verdict"]) for k in range(3)) >= 2 for i in GT}
ac = {i: sum(is_c(flat[k][i]["verdict"]) for k in range(3)) >= 2 for i in GT}
win = sorted(i for i in GT if fc[i] and not ac[i])
lose = sorted(i for i in GT if ac[i] and not fc[i])
print(f"discordant: full-only {len(win)}, flat-only {len(lose)}")

print("\n== cognition-material signal (COG key + D key SUPPORTS_*) ==")
n_cog_drive, n_d_drive = 0, 0
for i in win:
    cog = [full[k][i]["perspectives"].get("COG", "") for k in range(3)]
    dv = [full[k][i]["perspectives"].get("D", "") for k in range(3)]
    ncog = sum(1 for x in cog if x == "SUPPORTS_DEFECT")
    nd = sum(1 for x in dv if x == "SUPPORTS_DEFECT")
    if ncog >= 2:
        n_cog_drive += 1
    if nd >= 2:
        n_d_drive += 1
    tag = ""
    if ncog or nd or "SUPPORTS" in "".join(dv):
        tag = f"  COG={cog} D={dv}"
    if tag:
        print(f"  {i} GT={GT[i]}{tag}")
print(f"cognition-driven (COG SUPPORTS_DEFECT >=2 runs): {n_cog_drive}/17")
print(f"D-key SUPPORTS_DEFECT >=2 runs: {n_d_drive}/17 "
      "(weaviate_009 = the disclosed batch-delete leak)")

print("\n== dispatch material parity (flat vs D-only) ==")
a = open(f"{ROOT}/rerun_v3/run_flat1/batch1_dispatch.txt",
         encoding="utf-8").read()
b = open(f"{ROOT}/rerun_v3/run_donly1/batch1_dispatch.txt",
         encoding="utf-8").read()
import re
pa = set(re.findall(r"materials_complete.\w+\.md", a))
pb = set(re.findall(r"materials_complete.\w+\.md", b))
print(f"pack lists identical: {pa == pb} ({len(pa)} packs)")
print(f"flat cites source clones: {a.count('sourcedeps')}, "
      f"D-only: {b.count('sourcedeps')}")
for kw in ("developer_cognition", "禁止", "forbid"):
    print(f"flat mentions {kw!r}: {kw in a}, D-only: {kw in b}")
