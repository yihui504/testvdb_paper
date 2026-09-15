import re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"c:\Users\11428\Desktop\TestVDB_artifact\rq2\analyses\pricing\HR17_adjudication_worksheet.md"
for i, line in enumerate(open(p, encoding="utf-8"), 1):
    s = line.rstrip("\n")
    if s.startswith("## "):
        print(f"{i:5d} HDR  {s[3:60]}")
    elif s.startswith("# "):
        print(f"{i:5d} TITLE {s[2:80]}")
    elif "裁决" in s and "CONFIRM" in s:
        print(f"{i:5d} RUL  {re.sub(r'备注.*','',s)[:110]}")
    elif s.startswith("- 裁决"):
        print(f"{i:5d} other {s[:110]}")
