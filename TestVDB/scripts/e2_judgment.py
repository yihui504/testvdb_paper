#!/usr/bin/env python3
"""E2-judgment: cross-model judging vs source/behavior on GLM over-strict clauses.

Tests C3 directly: on the SAME set of GLM over-strict contract clauses, does a
second LLM family (DeepSeek) judging the clause catch the error, especially on
the task-intrinsic subset (where DeepSeek's own generation also over-formalized)?

Ground truth: all clauses are over-strict (GLM wrong); the VDB accepts the special
value the clause rejects (established via by-design bugs / t25 real semantics).
Source/behavior therefore contradicts every over-strict clause (recall = 100% by
construction). The empirical question is cross-model JUDGING recall, split by the
task-intrinsic flag (from t25 generation: DeepSeek also over-strict).

Inputs: 9 GLM over-strict clauses from t25 (3 with real glm_assertion, 6 reconstructed
from the t25 over_strict descriptions). N=9 pilot, Milvus-only.
"""
import json, os, sys, requests, time, re
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

_key_paths = ["deepseek_apikey.txt", "../deepseek_apikey.txt", "../../deepseek_apikey.txt"]
API_KEY = next(open(p).read().strip() for p in _key_paths if os.path.exists(p))
URL = "https://api.deepseek.com/chat/completions"
S = requests.Session(); S.trust_env = False

# (id, raw passage, glm_clause, real_semantics, task_intrinsic)
CASES = [
 ("shardsNum", "`shardsNum` (integer, optional): Number of shards (default: 1).",
  "shardsNum >= 1", "0 means use the default shard number", True),
 ("metricType", "`metricType` (string, optional): Supports L2, IP, COSINE.",
  "metricType in ['L2','IP','COSINE']", "omitted or invalid falls back to a default metric", False),
 ("consistencyLevel", "`consistencyLevel` (string, optional): Allowed: Strong, Session, Bounded, Eventually. Default: Bounded.",
  "consistencyLevel in ['Strong','Session','Bounded','Eventually'] (required)", "missing or invalid falls back to Bounded", False),
 ("data_search", "`data` (array[array[float]], required): Query vector embeddings.",
  "data must be a non-empty array of non-empty float arrays", "an empty data array is tolerated (returns empty)", True),
 ("outputFields", "`outputFields` (array of strings, optional): Fields to include in results. If omitted, all fields are returned.",
  "outputFields is required and must be non-empty", "omitted means return all fields", False),
 ("limit", "`limit` (integer, optional): Maximum number of results to return. Default: 0 (returns all matches).",
  "limit >= 1", "0 means no limit (return all matches)", False),
 ("roundDecimal", "`roundDecimal` (integer, optional): Decimal places to round distances to. Default: -1 (no rounding).",
  "roundDecimal >= 0", "-1 means no rounding", False),
 ("offset", "`offset` (integer, optional): Number of results to skip. Default: 0.",
  "offset >= 1", "0 means skip none", False),
 ("dbName", "`dbName` (string, optional): Target database name. Default: 'default'.",
  "dbName is required (non-empty)", "omitted uses the default database", False),
]

PROMPT = ("You are reviewing a formal constraint that another engineer derived from an "
          "API documentation passage. Judge whether the constraint correctly and completely "
          "captures the DOCUMENTED behavior, or whether it is over-strict (rejects values the "
          "documentation actually allows) or under-strict (allows values the documentation rejects). "
          "Base your judgment ONLY on the documentation passage, not on any implementation.\n\n"
          "Documentation passage:\n{raw}\n\nConstraint under review:\n{clause}\n\n"
          "Respond with STRICT JSON only, no prose: "
          '{{"judgment": "correct" | "over-strict" | "under-strict", "rationale": "..."}}')

def judge(raw, clause):
    payload = {"model": "deepseek-chat", "temperature": 0.0,
               "messages": [{"role": "user", "content": PROMPT.format(raw=raw, clause=clause)}],
               "max_tokens": 200}
    hdr = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last = None
    for attempt in range(5):
        try:
            r = S.post(URL, headers=hdr, timeout=60, json=payload)
            txt = r.json()["choices"][0]["message"]["content"].strip()
            break
        except Exception as e:
            last = e; time.sleep(2 * (attempt + 1))
    else:
        return ("call-error", repr(last)[:120])
    m = re.search(r'\{[^{}]*\}', txt, re.S)
    if not m: return ("parse-error", txt[:120])
    try: j = json.loads(m.group(0))
    except Exception: return ("parse-error", txt[:120])
    return (j.get("judgment","?").lower().strip(), j.get("rationale","")[:100])

rows = []
for cid, raw, clause, real, ti in CASES:
    verdict, rat = judge(raw, clause)
    flagged = verdict.startswith("over")  # cross-model catches over-strict
    rows.append({"id": cid, "task_intrinsic": ti, "ground_truth": "over-strict",
                 "source_contradicts": True, "crossmodel_judgment": verdict,
                 "crossmodel_flagged": flagged, "rationale": rat})
    print(f"{cid:18} TI={ti!s:5} deepseek={verdict:14} flagged={flagged}  | {rat}")
    time.sleep(0.5)

ti = [r for r in rows if r["task_intrinsic"]]
fs = [r for r in rows if not r["task_intrinsic"]]
print("\n=== SUMMARY (N=%d, Milvus pilot) ===" % len(rows))
print(f"task-intrinsic   n={len(ti)}  cross-model catches {sum(r['crossmodel_flagged'] for r in ti)}/{len(ti)}  source catches {sum(r['source_contradicts'] for r in ti)}/{len(ti)}")
print(f"family-specific  n={len(fs)}  cross-model catches {sum(r['crossmodel_flagged'] for r in fs)}/{len(fs)}  source catches {sum(r['source_contradicts'] for r in fs)}/{len(fs)}")
print(f"ALL over-strict  n={len(rows)} cross-model catches {sum(r['crossmodel_flagged'] for r in rows)}/{len(rows)}")
json.dump(rows, open("scripts/e2_judgment_results.json","w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("[wrote scripts/e2_judgment_results.json]")
