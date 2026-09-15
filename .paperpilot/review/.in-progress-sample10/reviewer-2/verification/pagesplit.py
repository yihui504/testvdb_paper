import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pypdf import PdfReader
r = PdfReader(r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.pdf")
print("total pages:", len(r.pages))
targets = ["ABSTRACT", "1 Introduction", "2 Preliminaries", "3 Approach", "4 Evaluation",
           "5 Discussion", "6 Threats to Validity", "7 Related Work", "8 Conclusion",
           "References", "Data Availability", "A ", "Appendix"]
for i, p in enumerate(r.pages):
    t = p.extract_text() or ""
    flat = re.sub(r"\s+", " ", t)
    hits = [w for w in targets if w.lower() in flat.lower()]
    print(f"--- page {i+1}: {hits}")
# locate exact markers
for i, p in enumerate(r.pages):
    t = re.sub(r"\s+", " ", p.extract_text() or "")
    for m in re.finditer(r"(References|Data Availability|Conclusion|RELATED WORK|REFERENCES)", t):
        print(f"page {i+1}: marker '{m.group(1)}' at char {m.start()}  ctx: ...{t[max(0,m.start()-80):m.start()+120]}...")
