"""Find file paths / artifact names that the anchor run produced or consumed."""
import json
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PATH = (r"C:\Users\11428\.claude\projects"
        r"\c--Users-11428-Desktop-testvdb-paper"
        r"\97277b57-c1ce-460f-b536-cfc43e375f52.jsonl")

# path-like tokens mentioning anchor / 32 / seed / unsubmitted
TOK = re.compile(
    r"[\w./\\-]*(?:anchor|unsubmitted|never_submitted|seed|non_submitted)"
    r"[\w./\\-]*", re.I)

counts = Counter()
with open(PATH, encoding="utf-8", errors="replace") as f:
    for line in f:
        if not re.search(r"anchor|unsubmitted|never.submitted|seed", line,
                         re.I):
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue

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
            for m in TOK.findall(t):
                m = m.strip()
                if len(m) > 4 and ("." in m or "/" in m or "\\" in m):
                    counts[m] += 1

print("top path-like anchor tokens:")
for tok, n in counts.most_common(40):
    print(f"  {n:4d}  {tok}")
