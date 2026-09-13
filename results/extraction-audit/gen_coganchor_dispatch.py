"""Generate per-run rejudge dispatches for the 7 cognition-anchored cases.

Each output dispatch is byte-identical to the original batch1 v3 protocol text
except: (a) the material list carries only the 7 affected cases (material lines
collected from whichever original batch file contained them); (b) the
cognition-material line points at the candidate-anchored *cleaned* variants;
(c) the output path is <run>/verdicts_coganchor_rejudge.jsonl."""
import glob
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/phase2-rerun/arms/rq2_3run/rerun_v3"
CASES = ["milvus_004", "milvus_006", "milvus_018", "milvus_019",
         "milvus_021", "milvus_027", "qdrant_017"]
RUNS = ["run_full1", "run_full2", "run_full3",
        "run_fullq1", "run_fullq2", "run_fullq3"]
BASE = "C:/Users/11428/Desktop/tvdb_sessions/intelligence"

case_set = set(CASES)
src = open(ROOT + r"/run_full1/batch1_dispatch.txt", encoding="utf-8").read()

mat = {}
for f in glob.glob(ROOT + r"/run_full1/batch*_dispatch.txt"):
    for ln in open(f, encoding="utf-8"):
        m = re.match(r"- (milvus_\d+|qdrant_\d+|weaviate_\d+): pack=", ln)
        if m and m.group(1) in case_set:
            mat[m.group(1)] = ln.rstrip("\n")
missing = [c for c in CASES if c not in mat]
assert not missing, f"missing material lines: {missing}"

proto = []
for ln in src.split("\n"):
    if re.match(r"- (milvus_\d+|qdrant_\d+|weaviate_\d+): pack=", ln):
        continue
    if "维护者认知" in ln:
        continue
    proto.append(ln)
body = "\n".join(proto)
materials = "\n".join(mat[c] for c in CASES)
cog = ("- 维护者认知(三库各一,全文 Read 一次即可;**本次为候选锚定清理版**):"
       f"{BASE}/milvus/developer_cognition_cleaned.json | "
       f"{BASE}/qdrant/developer_cognition_cleaned.json | "
       f"{BASE}/weaviate/developer_cognition.json")
header = ("# RQ2 全臂认知锚定重判(7 案;唯一改动=认知文件换候选锚定清理版,"
          "协议与红线逐字同原 batch dispatch v3;判前 verdicts 已备份至各 run "
          "目录 _pre_coganchor.jsonl)\n\n")
anchor = "## 每案材料"
assert anchor in body
body2 = body.replace(anchor, anchor + "\n" + materials + "\n" + cog + "\n", 1)

for run in RUNS:
    outp = body2.replace("verdicts_batch1.jsonl",
                         "verdicts_coganchor_rejudge.jsonl")
    outp = outp.replace(
        "rerun_v3" + "\\" + "run_full1" + "\\",
        "rerun_v3" + "\\" + run + "\\")
    outp = outp.replace("rerun_v3/run_full1/", f"rerun_v3/{run}/")
    p = ROOT + "\\" + run + "\\" + "coganchor_rejudge_dispatch.txt"
    open(p, "w", encoding="utf-8").write(header + outp)
    n_mat = len(re.findall(r"- (?:milvus|qdrant|weaviate)_\d+: pack=", outp))
    ok = (f"rerun_v3" + "\\" + run + "\\" + "verdicts_coganchor_rejudge.jsonl"
          in outp)
    print(run, "| materials:", n_mat, "| out ok:", ok,
          "| cleaned refs:", outp.count("developer_cognition_cleaned.json"))
