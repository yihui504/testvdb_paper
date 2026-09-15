import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PyPDF2 import PdfReader
PDF = r"c:\Users\11428\Desktop\testvdb_paper\TestVDB-v10.pdf"
r = PdfReader(PDF)
print("pages:", len(r.pages))
for i, p in enumerate(r.pages):
    raw = p.extract_text() or ""
    # strip the leading line-number column: lines that are just an integer
    lines = [l for l in raw.splitlines() if not re.fullmatch(r"\s*\d+\s*", l)]
    t = re.sub(r"\s+", " ", " ".join(lines))
    for name in ("Data Availability", "REFERENCES", "References"):
        for m in re.finditer(re.escape(name), t):
            print(f"p{i+1} '{name}' @{m.start()}: ...{t[max(0,m.start()-140):m.start()+200]}...")
print()
# page 18 / 19 / 20 content
for i in (17, 18, 19):
    raw = r.pages[i].extract_text() or ""
    lines = [l for l in raw.splitlines() if not re.fullmatch(r"\s*\d+\s*", l)]
    t = re.sub(r"\s+", " ", " ".join(lines))
    print(f"\n===== PAGE {i+1} =====\n{t[:2500]}")
