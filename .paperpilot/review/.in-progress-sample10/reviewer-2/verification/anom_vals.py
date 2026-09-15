import glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(r"c:\Users\11428\Desktop\TestVDB_artifact\rq3\runs\full-coverage-v3")
ESC = re.compile(r"\\u([0-9a-fA-F]{4})")
PAT = re.compile("\u53d1\u73b0 (\\d+) \u4e2a\u5bfc\u81f4\u5f02\u5e38\u7684\u53d8\u5f02")
files = sorted(glob.glob("logs/*.log"))
per = [f for f in files if os.path.getsize(f) < 3_000_000]
vals = collections.Counter()
for f in per:
    t = ESC.sub(lambda m: chr(int(m.group(1), 16)), open(f, encoding="utf-8", errors="replace").read())
    for m in PAT.finditer(t):
        vals[m.group(1)] += 1
print("anomaly report values:", dict(vals))
