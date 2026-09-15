import io

t = io.open(r"C:\Users\11428\Desktop\TestVDB_artifact\rq2\verdicts\run_flat1\batch1_dispatch.txt",
            encoding="utf-8", errors="ignore").read()
for k in ["\u7f51\u7edc", "\u72ec\u7acb", "pack", "clone", "source=", "Human-Review", "False-Positive"]:
    print(ascii(k), t.count(k))
