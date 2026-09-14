"""Assemble the round-16 review deliverable: the three independent reviews
(reviewer 1, 2, 3 in order) followed by the Meta-Review, in one file."""
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r".paperpilot/review"
IP = os.path.join(ROOT, ".in-progress")
OUT = os.path.join(ROOT, "TestVDB-review-2026-09-14g.md")

parts = []
for n in (1, 2, 3):
    p = os.path.join(IP, f"reviewer-{n}", "draft.md")
    t = open(p, encoding="utf-8").read().strip()
    assert t.startswith(f"## Reviewer {n}:"), f"reviewer-{n} draft header drift"
    parts.append(t)

meta = open(os.path.join(IP, "meta-review.md"), encoding="utf-8").read().strip()
for h in ("### Criterion Consensus", "### Meta Recommendation",
          "### Priority Revisions"):
    assert h in meta, f"meta-review missing {h}"
assert "**ACCEPT**" in meta, "meta-review missing the verdict line"
parts.append(meta)

doc = "\n\n".join(parts) + "\n"
open(OUT, "w", encoding="utf-8").write(doc)

print(f"wrote {OUT}  ({os.path.getsize(OUT)} bytes, "
      f"{len(doc.splitlines())} lines)")
for line in doc.splitlines():
    if line.startswith("## "):
        print("  ", line)
