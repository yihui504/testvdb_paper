"""Count the abstract's paragraphs and words (for the round-15 presentation
fix and to settle the reviewers' divergent counts)."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

src = open(".paperpilot/review/.in-progress/paper/TestVDB.tex",
           encoding="utf-8").read()
m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", src, re.S)
abstract = m.group(1)
paras = [p.strip() for p in abstract.split("\n\n") if p.strip()]
print("paragraphs:", len(paras))
total = 0
for i, p in enumerate(paras, 1):
    w = len(p.split())
    total += w
    print(f"  para{i}: {w} words")
print("total (raw tokens):", total)

clean = re.sub(r"\\[a-zA-Z]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", abstract)
clean = re.sub(r"[{}$\\]", " ", clean)
print("total (latex-stripped):", len(clean.split()))
