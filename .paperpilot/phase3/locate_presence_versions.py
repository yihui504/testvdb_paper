#!/usr/bin/env python3
"""档1: 存在版本定位 (phase3-plan §2)。

A 组 28 (TP_FIXED_PR): fix-PR merged_at -> 修复前最近发布的 release tag = 存在版本。
B 组 17 (确认未修复): 报告版本即存在版本。

数据源:
- manifest.json (人工核对后的分类 + reported_version)
- verify-c3/ 已抓的 17 条 timeline (cross-referenced PR 证据), 缺的 11 条现场拉
- GitHub API (GITHUB_TOKEN 认证): timeline / PR 详情 / releases

产物 (全部落盘, 可增量重跑):
- timeline-cache/{repo}-{num}.json   增量缓存, 已存在则复用
- pr-evidence.json                   每 bug 的 cross-ref PR 列表 + merged_at
- releases-cache/{repo}.json         全量 release (tag, published_at), 过滤 prerelease/draft
- presence-versions.csv              主产出
"""
import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).parent
RAW = HERE.parent / "phase1-raw"
TL_CACHE = HERE / "timeline-cache"
REL_CACHE = HERE / "releases-cache"
for d in (TL_CACHE, REL_CACHE):
    d.mkdir(parents=True, exist_ok=True)

TOKEN = os.environ.get("GITHUB_TOKEN", "")
HDRS = {
    "User-Agent": "testvdb-phase3",
    "Accept": "application/vnd.github.mockingbird-preview+json",
}
if TOKEN:
    HDRS["Authorization"] = f"Bearer {TOKEN}"

REPOS = ["milvus-io/milvus", "qdrant/qdrant", "weaviate/weaviate"]
GROUP_B_CATS = {"TP_ACK_OPEN", "TP_ACK_CLOSED_NOFIX", "TP_DUP_TRACKED"}


def get(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def api_get_all(url):
    """Follow pagination."""
    out, page = [], 1
    while True:
        sep = "&" if "?" in url else "?"
        out.extend(get(f"{url}{sep}per_page=100&page={page}"))
        if len(out) < page * 100:
            return out
        page += 1


def ver_key(tag):
    """'v2.6.10' -> (2,6,10) for ordering."""
    nums = tag.lstrip("vV").split(".")
    return tuple(int(n) for n in nums[:3])


SERVER_TAG = __import__("re").compile(r"^v\d+\.\d+(\.\d+)?$")


def is_server_tag(tag):
    """排除 client/ 等 SDK release tag（与 server 时间线交错会污染定位）。"""
    return bool(SERVER_TAG.match(tag))


# ---------------------------------------------------------------- 数据准备
manifest = json.load(open(RAW / "manifest.json", encoding="utf-8"))
group_a = [r for r in manifest if r["gt_category"] == "TP_FIXED_PR"]
group_b = [r for r in manifest if r["gt_category"] in GROUP_B_CATS]
assert len(group_a) == 28 and len(group_b) == 17, (len(group_a), len(group_b))

# ---------------------------------------------------------------- releases
for repo in REPOS:
    fn = REL_CACHE / f"{repo.replace('/', '-')}.json"
    if fn.exists():
        continue
    print(f"[releases] {repo} ...", flush=True)
    rels = api_get_all(f"https://api.github.com/repos/{repo}/releases")
    keep = [
        {"tag": r["tag_name"], "published_at": r["published_at"]}
        for r in rels
        if not r["draft"] and not r["prerelease"]
    ]
    json.dump(keep, open(fn, "w", encoding="utf-8"), indent=1)
    print(f"  {len(keep)} stable releases", flush=True)

releases = {
    repo: json.load(open(REL_CACHE / f"{repo.replace('/', '-')}.json", encoding="utf-8"))
    for repo in REPOS
}


def tag_before(repo, iso_time):
    """最新的 published_at < iso_time 的 stable server release; None 若无。"""
    prior = [r for r in releases[repo]
             if r["published_at"] < iso_time and is_server_tag(r["tag"])]
    return max(prior, key=lambda r: r["published_at"]) if prior else None


# ---------------------------------------------------------------- timeline / PR 证据
# verify-c3 已有 17 条人工升级的 timeline; 先复用, 缺的现拉。
c3 = RAW / "verify-c3"

pr_evidence = {}
for bug in group_a:
    repo, num = bug["repo"], bug["number"]
    key = f"{repo}-{num}"
    fn = TL_CACHE / f"{repo.replace('/', '-')}-{num}.json"
    if not fn.exists() and (c3 / fn.name).exists():
        fn = c3 / fn.name  # 复用 verify-c3
    if not fn.exists():
        print(f"[timeline] {key} ...", flush=True)
        evs = api_get_all(f"https://api.github.com/repos/{repo}/issues/{num}/timeline")
        json.dump(evs, open(TL_CACHE / f"{repo.replace('/', '-')}-{num}.json", "w", encoding="utf-8"), indent=1)
        time.sleep(0.3)

    evs = json.load(open(fn, encoding="utf-8"))
    seen, prs = set(), []
    for e in evs:
        src = e.get("source", {}).get("issue", {}) or {}
        if e.get("event") == "cross-referenced" and src.get("pull_request"):
            pr_repo = src.get("repository_url", "").replace("https://api.github.com/repos/", "")
            pid = (pr_repo, src["number"])
            if pid in seen:
                continue
            seen.add(pid)
            prs.append({"repo": pr_repo, "number": src["number"],
                        "title": src.get("title", ""), "state": src.get("state", "")})
    pr_evidence[key] = prs

# PR merged_at: 认证额度充足, 对所有 cross-ref PR 逐个补详情
detail_fn = HERE / "pr-details.json"
details = json.load(open(detail_fn, encoding="utf-8")) if detail_fn.exists() else {}
for key, prs in pr_evidence.items():
    for pr in prs:
        dkey = f'{pr["repo"]}#{pr["number"]}'
        if dkey in details:
            continue
        print(f"[pr] {dkey} ...", flush=True)
        d = get(f'https://api.github.com/repos/{pr["repo"]}/pulls/{pr["number"]}')
        details[dkey] = {"merged": d.get("merged", False),
                         "merged_at": d.get("merged_at"),
                         "changed_files": d.get("changed_files")}
        time.sleep(0.3)
json.dump(details, open(detail_fn, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

json.dump(pr_evidence, open(HERE / "pr-evidence.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)

# ---------------------------------------------------------------- 定位 + 输出
MILVUS_23_FALLBACK = "v2.3.22"  # phase2 约定: 报告版本 "2.3" 具体化到 2.3 系列末尾 tag


def pick_fix_pr(bug):
    """从 cross-ref PR 中选 merged 的 fix-PR, merged_at 最早者为主修复。"""
    key = f'{bug["repo"]}-{bug["number"]}'
    prs = pr_evidence.get(key, [])
    merged = []
    for pr in prs:
        d = details.get(f'{pr["repo"]}#{pr["number"]}', {})
        if d.get("merged") and d.get("merged_at"):
            merged.append({**pr, **d})
    merged.sort(key=lambda p: p["merged_at"])
    return prs, merged


def normalize_reported(bug):
    r = bug.get("reported_version") or ""
    if bug["repo"] == "milvus-io/milvus" and r == "2.3":
        return MILVUS_23_FALLBACK
    return "v" + r if r else ""


rows = []
for bug in group_a + group_b:
    repo, num = bug["repo"], bug["number"]
    reported = normalize_reported(bug)
    group = "A" if bug["gt_category"] == "TP_FIXED_PR" else "B"

    if group == "B":
        presence, fix_pr, merged_at, note = reported, "", "", "B组:报告版本即存在版本"
    else:
        prs, merged = pick_fix_pr(bug)
        if not merged:
            # 修复 PR 未 merge 或不可追溯 → 修复未进任何 release → 报告版本必含 bug
            presence, fix_pr, merged_at = reported, "", ""
            note = f"无 merged fix-PR({len(prs)}候选) → 保守取报告版本"
        else:
            fp = merged[0]
            tag = tag_before(repo, fp["merged_at"])
            cand = tag["tag"] if tag else ""
            # 并行维护线: 修复前最后 release 可能落在旧线(如2.6.x)而报告在新线(3.0.0);
            # 两个版本都含 bug, 取版本序较大者(=报告版本所在线, 且有报告人实证)。
            if cand and reported:
                try:
                    cand = max((cand, reported), key=ver_key)
                except ValueError:
                    pass
            presence = cand
            fix_pr = f'{fp["repo"]}#{fp["number"]}'
            merged_at = fp["merged_at"]
            kind = "doc" if "docs" in fp["repo"] else "code"
            note = f"fix-PR({kind}) merged_at 前最近 server release"
        if group == "A" and len(prs) > len(merged):
            note += f"; {len(prs)-len(merged)} 个未merge PR 见 pr-evidence.json"

    warn = ""
    tags = {r["tag"] for r in releases[repo] if is_server_tag(r["tag"])}
    if presence and presence not in tags:
        warn = f"存在版本 {presence} 无对应 release tag,需人工"

    rows.append({
        "repo": repo.split("/")[1], "issue": num, "group": group,
        "category": bug["gt_category"], "title": bug["title"][:80],
        "reported_version": reported, "fix_pr": fix_pr, "merged_at": merged_at,
        "presence_version": presence, "warning": warn, "note": note,
    })

cols = list(rows[0].keys())
with open(HERE / "presence-versions.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)

n_ok = sum(1 for r in rows if r["presence_version"] and not r["warning"])
n_warn = sum(1 for r in rows if r["warning"])
n_missing = sum(1 for r in rows if not r["presence_version"])
print(f"\n完成: {len(rows)} 条 | 定位成功 {n_ok} | 警告 {n_warn} | 未定位 {n_missing}")
print(f"输出: {HERE / 'presence-versions.csv'}")
for r in rows:
    if r["warning"] or not r["presence_version"]:
        print(f"  !! {r['repo']}/{r['issue']} [{r['group']}] {r['warning'] or '未定位'}")
