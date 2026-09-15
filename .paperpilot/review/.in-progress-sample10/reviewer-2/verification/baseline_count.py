import glob, os, re, sys, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
os.chdir(r"c:\Users\11428\Desktop\TestVDB_artifact\rq3\runs\full-coverage-v3")
files = sorted(glob.glob("logs/*.log"))
ESC = re.compile("\\\\u([0-9a-fA-F]{4})")
def deesc(t):
    return ESC.sub(lambda m: chr(int(m.group(1), 16)), t)
STA = "\u8bf7\u6c42\u54cd\u5e94\u72b6\u6001\u7801: "        # request response status code:
STG = "Randomized mutation testing completed"
ANM = "\u4e2a\u5bfc\u81f4\u5f02\u5e38\u7684\u53d8\u5f02"       # N mutation sequences causing anomalies
master = [f for f in files if os.path.getsize(f) > 3_000_000]
print("log files:", len(files), " master:", master)
for label, sel in (("ALL files", files),
                   ("EXCLUDING master", [f for f in files if f not in master])):
    statuses = stages = anom = afiles = nonzero = 0
    codes = collections.Counter()
    for f in sel:
        t = deesc(open(f, encoding="utf-8", errors="replace").read())
        ss = re.findall(STA + r"(\d+)", t); statuses += len(ss); codes.update(ss)
        stages += t.count(STG)
        for m in re.finditer(r"\u53d1\u73b0 (\d+) " + ANM, t):
            anom += 1; nonzero += (int(m.group(1)) > 0)
        if ANM in t: afiles += 1
    print(f"  {label:18s} files={len(sel):4d} status-lines={statuses:6d} stages={stages:5d} "
          f"anomaly-lines={anom:4d} in {afiles} files (nonzero={nonzero})")
    print(f"      codes={dict(codes.most_common()[:8])}  5xx={sum(v for k,v in codes.items() if k.startswith('5'))}")
