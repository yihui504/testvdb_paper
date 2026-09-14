"""Stream the big session transcript and pull out everything around the
32-candidate anchor: its dispatch, its case list, and its verdicts."""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = (r"C:\Users\11428\.claude\projects"
        r"\c--Users-11428-Desktop-testvdb-paper"
        r"\97277b57-c1ce-460f-b536-cfc43e375f52.jsonl")

HITS = re.compile(r"(32 案|19/32|19 of 32|anchor)")
CASEID = re.compile(r"\b((?:milvus|qdrant|weaviate)_\d+)\b")

n_lines = 0
n_hit = 0
case_ids = set()
samples = []
with open(PATH, encoding="utf-8", errors="replace") as f:
    for line in f:
        n_lines += 1
        if not HITS.search(line):
            continue
        n_hit += 1
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        # walk the record for text
        def texts(x):
            if isinstance(x, str):
                yield x
            elif isinstance(x, dict):
                for v in x.values():
                    yield from texts(v)
            elif isinstance(x, list):
                for v in x:
                    yield from texts(v)
        for t in texts(o):
            if HITS.search(t):
                found = set(CASEID.findall(t))
                if found:
                    case_ids |= found
                if len(samples) < 6 and len(t) > 200:
                    samples.append(t[:900])

print(f"lines scanned: {n_lines}; hit lines: {n_hit}")
print(f"distinct case ids mentioned in anchor context: {len(case_ids)}")
print(sorted(case_ids)[:60])
print("\n=== samples ===")
for s in samples:
    print("---")
    print(s)
