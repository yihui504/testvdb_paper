"""A1 step 4 — version alignment between what each pack says it tested and the
version token in the page it cites.

The paper (§3.2) claims a version-alignment gate: documentation version must
match the target's major.minor. This check reports, mechanically, where the
cited page's version token disagrees with the pack's declared tested version.
It does NOT decide whether a disagreement is a violation — a page can be
version-agnostic (an unversioned docs root) by design.
"""
import json
import os
import re
from collections import defaultdict

BASE = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"


def mm(v: str):
    """major.minor, tolerating 2- or 3-part and x-style tokens."""
    if not v:
        return None
    m = re.match(r"(\d+)\.(\d+)", v)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def main():
    packs = {p["pack"]: p for p in json.load(open(os.path.join(BASE, "pack_meta.json"), encoding="utf-8"))}
    constraints = json.load(open(os.path.join(BASE, "constraints.json"), encoding="utf-8"))
    urls = {u["source_url"]: u for u in json.load(open(os.path.join(BASE, "urls.json"), encoding="utf-8"))}

    # Granularity is (pack, constraint, cited page): a constraint shared by two
    # packs of different tested versions must be judged once per pack, otherwise
    # a version-correct pack masks a version-wrong one.
    rows, stats = [], defaultdict(int)
    for c in constraints:
        for pack in sorted(c["packs"]):
            p = packs.get(pack)
            if not p or not p["version"]:
                continue
            tested_mm = mm(p["version"])
            for url in c["urls"]:
                u = urls[url]
                u_mm = mm(u["url_version"]) if u["url_version"] else None
                if u_mm is None:
                    verdict = "page-unversioned"
                elif tested_mm and u_mm == tested_mm:
                    verdict = "aligned"
                else:
                    verdict = "MISMATCH"
                stats[verdict] += 1
                rows.append({"pack": pack,
                             "constraint_id": c["constraint_id"],
                             "vendor": p["vendor"],
                             "tested_version": p["version"],
                             "url_kind": u["kind"],
                             "url_version_token": u["url_version"] or "",
                             "verdict": verdict,
                             "source_url": url})

    order = {"MISMATCH": 0, "aligned": 1, "page-unversioned": 2}
    rows.sort(key=lambda r: (order[r["verdict"]], r["vendor"], r["pack"]))
    import csv
    with open(os.path.join(BASE, "version_check.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    L = ["# A1 · 版本核对（机械，粒度 = 包 × 约束 × 引用页）", "",
         "每个包声明一个受测版本；对每条约束引用的每个页面，比对该 URL 的版本片段。"
         "`page-unversioned` = 该页 URL 不带版本段（如 `github.com/.../constant.go`），无从比对，不等于合格。", "",
         "| 结论 | 行数 |", "|---|---|"]
    for k in ["aligned", "MISMATCH", "page-unversioned"]:
        L.append(f"| {k} | {stats.get(k, 0)} |")
    L += ["", "## MISMATCH 明细", ""]
    mis = [r for r in rows if r["verdict"] == "MISMATCH"]
    if not mis:
        L.append("（无）")
    else:
        L += ["| 包 | 约束 | 库 | 受测版本 | URL 版本 | 引用页 |", "|---|---|---|---|---|---|"]
        for r in mis:
            L.append(f"| {r['pack']} | `{r['constraint_id']}` | {r['vendor']} | {r['tested_version']} | "
                     f"{r['url_version_token']} | `{r['source_url'][:66]}` |")
        bypack = defaultdict(int)
        for r in mis:
            bypack[(r["vendor"], r["tested_version"])] += 1
        L += ["", "按库/版本汇总：" + "；".join(f"{k[0]} {k[1]} ({v}行)" for k, v in sorted(bypack.items()))]
    open(os.path.join(BASE, "version_check.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    print("\n".join(L[:12]))
    print(f"\nMISMATCH 行数: {len(mis)}  -> version_check.md / version_check.csv")


if __name__ == "__main__":
    main()
