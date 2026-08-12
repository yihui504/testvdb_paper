#!/usr/bin/env python3
"""Phase 1 收集: yihui504 在三个 VDBMS repo 的所有 issue.

需 gh CLI 装且已认证 (gh auth login).
运行:  py docs/phase1-collect.py
输出:  yihui504-vdbms-issues.json  +  yihui504-vdbms-issues.csv  (当前目录)

爬完后把 .json 放到 mftui/data/, 下轮基于真实 label 精化分类.
"""
import subprocess, json, csv, sys
from collections import Counter

REPOS = ["milvus-io/milvus", "qdrant/qdrant", "weaviate/weaviate"]
FIELDS = "number,title,state,stateReason,labels,createdAt,closedAt,url"

all_issues = []
for repo in REPOS:
    r = subprocess.run(
        ["gh", "issue", "list", "--repo", repo, "--author", "yihui504",
         "--state", "all", "--limit", "300", "--json", FIELDS],
        capture_output=True, text=True)
    if r.returncode != 0:
        print(f"FAIL {repo}: {r.stderr.strip()}", file=sys.stderr)
        continue
    items = json.loads(r.stdout)
    for it in items:
        it["repo"] = repo
    all_issues.extend(items)
    print(f"  {repo}: {len(items)}", file=sys.stderr)

# 去重(同 repo+number)
seen, dedup = set(), []
for it in all_issues:
    k = (it["repo"], it["number"])
    if k in seen:
        continue
    seen.add(k)
    dedup.append(it)
print(f"total: {len(all_issues)} | dedup: {len(dedup)}", file=sys.stderr)

json.dump(dedup, open("yihui504-vdbms-issues.json", "w", encoding="utf-8"), indent=2, ensure_ascii=False)


def label_str(it):
    return " ".join(l.get("name", "") for l in it.get("labels", [])).lower()


# 初步分类(state + stateReason + label 关键词; 每 repo label 体系不同, 需后续校准)
def categorize(it):
    s, r = it.get("state", ""), it.get("stateReason", "") or ""
    lbl = label_str(it)
    if s == "closed" and r == "completed":
        return "FIXED" if "bug" in lbl else "CLOSED_OTHER"
    if s == "closed" and r == "not_planned":
        return "BY_DESIGN_OR_REJECTED"
    if s == "open" and ("bug" in lbl or "type/bug" in lbl):
        return "BUG_OPEN"
    if s == "open":
        return "OPEN_NO_LABEL"
    return "CLOSED_OTHER"


cat = Counter(categorize(it) for it in dedup)
print("categories:", dict(cat), file=sys.stderr)
by_repo = Counter(it["repo"] for it in dedup)
print("by_repo:", dict(by_repo), file=sys.stderr)

with open("yihui504-vdbms-issues.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["repo", "number", "state", "stateReason", "category",
                "title", "url", "labels"])
    for it in sorted(dedup, key=lambda x: (x["repo"], x["number"])):
        w.writerow([
            it["repo"], it["number"], it.get("state", ""), it.get("stateReason", ""),
            categorize(it), it.get("title", ""), it.get("url", ""),
            "|".join(l.get("name", "") for l in it.get("labels", [])),
        ])
print("wrote yihui504-vdbms-issues.json + .csv", file=sys.stderr)
