"""B6: per-template response-class distribution from the RQ3 full-coverage
run logs (205 templates, vdb_fuzzer logging format)."""
import glob
import json
import re
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

LOGS = (r"c:/Users/11428/Desktop/TestVDB_artifact/rq3/runs/full-coverage-v3/"
        "logs")
CODE = re.compile(r"\\u8bf7\\u6c42\\u54cd\\u5e94\\u72b6\\u6001\\u7801[:：\s]*(\d{3})")
TPL = re.compile(r"test_[\w]+ - INFO")


def main() -> None:
    rows = []
    total = Counter()
    for f in sorted(glob.glob(LOGS + "/*.log")):
        name = f.split("\\")[-1].split("/")[-1]
        tpl = name.rsplit("_test_", 1)[0]
        codes = CODE.findall(open(f, encoding="utf-8", errors="replace").read())
        c = Counter(codes)
        total.update(c)
        rows.append({"template": tpl, "n": len(codes),
                     "2xx": sum(v for k, v in c.items() if k.startswith("2")),
                     "4xx": sum(v for k, v in c.items() if k.startswith("4")),
                     "5xx": sum(v for k, v in c.items() if k.startswith("5")),
                     "dist": dict(c)})
    rows.sort(key=lambda r: -r["4xx"])
    out = {
        "total": {"responses": sum(total.values()),
                  "by_class": {k: v for k, v in sorted(total.items())},
                  "templates": len(rows),
                  "templates_with_4xx": sum(1 for r in rows if r["4xx"]),
                  "templates_with_5xx": sum(1 for r in rows if r["5xx"])},
        "per_template": rows,
    }
    p = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit/rq3_pertemplate_dist.json"
    json.dump(out, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("responses:", out["total"]["responses"], dict(total))
    print("templates:", out["total"]["templates"],
          "| with4xx:", out["total"]["templates_with_4xx"],
          "| with5xx:", out["total"]["templates_with_5xx"])
    print("top-4xx templates:")
    for r in rows[:8]:
        print(f"  {r['template'][:60]:62s} n={r['n']:>3} 4xx={r['4xx']:>3} "
              f"5xx={r['5xx']}")


if __name__ == "__main__":
    main()
