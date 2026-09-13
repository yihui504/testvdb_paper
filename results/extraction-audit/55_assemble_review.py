"""Assemble a delivered review: Reviewer 1, 2, 3, then the Meta-Review, in one
file under .paperpilot/review/, and structurally validate it."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE = ".paperpilot/review/.in-progress"
OUT = sys.argv[1] if len(sys.argv) > 1 \
    else ".paperpilot/review/TestVDB-review-cycle2.md"

parts = []
for i in (1, 2, 3):
    parts.append(open(f"{BASE}/reviewer-{i}/draft.md",
                      encoding="utf-8").read().strip())
parts.append(open(f"{BASE}/meta-review.md", encoding="utf-8").read().strip())

doc = "\n\n---\n\n".join(parts) + "\n"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

required = ["## Reviewer 1:", "## Reviewer 2:", "## Reviewer 3:",
            "## Meta-Review", "### Criterion Consensus",
            "### Meta Recommendation", "### Priority Revisions"]
for h in required:
    n = doc.count(h)
    print(f"{'OK ' if n == 1 else 'FAIL'} {n}x  {h!r}")
m = re.search(r"### Meta Recommendation\n\*\*(ACCEPT|REVISION|REJECT)\*\*", doc)
print("meta verdict:", m.group(1) if m else "NOT FOUND")
print("lines:", doc.count("\n"))
print("written:", OUT)
