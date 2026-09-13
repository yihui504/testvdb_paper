"""A1 step 6 — do the version-mismatched DOC pages differ in content?

Families 1/4/5 cite a documentation page whose version differs from the pack's
declared tested version. This fetches BOTH versions of each cited page and
diffs the readable text, with three guards against over-reading the result:

  1. existence  — a correct-version page that 404s makes the citation
                  unavoidable, so the pair is exempt (like family 6), not a fault;
  2. cosmetic   — changed lines that differ only by the version token are
                  navigation/version chrome, not documentation substance;
  3. relevance  — only changes that touch a term the citing constraints
                  actually assert can affect those constraints.

Qdrant serves a markdown twin at `<url>.md`; milvus.io's `.md` URLs serve HTML
and go through html2text.
"""
import difflib
import json
import os
import re
import urllib.request

import html2text

BASE = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
CACHE = os.path.join(BASE, "doc_pairs")
UA = {"User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                     "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")}
H2T = html2text.HTML2Text()
H2T.ignore_links = True
H2T.ignore_images = True
H2T.body_width = 0

MILVUS = ["Collection%20(v2)/Create.md", "Vector%20(v2)/Search.md",
          "Collection%20(v2)/Drop.md", "Collection%20(v2)/Load.md",
          "Collection%20(v2)/Rename.md", "Vector%20(v2)/Get.md"]
QDRANT = ["api-reference", "api-reference/collections/create-collection",
          "api-reference/search/points", "api-reference/points/upsert-points",
          "api-reference/points/set-payload"]

STOP = set("""the a an and or of to in for on with is are was were be been that this these those
it its as at by from not no if then than so such can may must should would could will shall
value default type range required optional string integer boolean array object""".split())


def fetch(url: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "_", url)[:150]
    path = os.path.join(CACHE, name)
    if os.path.exists(path):
        return open(path, encoding="utf-8", errors="replace").read()
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        raw = r.read().decode("utf-8", errors="replace")
        ctype = r.headers.get("Content-Type", "")
    text = H2T.handle(raw) if "html" in ctype.lower() else raw
    text = re.sub(r"\n{3,}", "\n\n", text)
    os.makedirs(CACHE, exist_ok=True)
    open(path, "w", encoding="utf-8").write(text)
    return text


def norm(text: str):
    out = []
    for line in text.splitlines():
        s = re.sub(r"\s+", " ", line).strip()
        if s and not s.startswith(("!", "[", "> For ")):
            out.append(s)
    return out


def strip_ver(s: str) -> str:
    s = re.sub(r"v-?\d+[-._]\d+([-._]\d+)?", "<VER>", s)
    s = re.sub(r"\bv?\d+\.\d+(\.\d+)?x?\b", "<VER>", s)
    return s


def terms_of(assertion: str, desc: str):
    t = f"{assertion} {desc}".lower()
    return {w for w in re.findall(r"[a-z_]{4,}", t) if w not in STOP}


def analyse(label, url_a, url_b, md, assert_terms):
    ta = fetch(url_a + (".md" if md else ""))
    tb = fetch(url_b + (".md" if md else ""))
    if "Page Not Found" in tb[:400] or len(tb) < 500:
        return {"label": label, "cited": url_a, "tested": url_b,
                "status": "correct-version-page-absent"}
    la, lb = norm(ta), norm(tb)
    diff = [l for l in difflib.unified_diff(la, lb, lineterm="", n=0)
            if l[:1] in "+-" and l[:3] not in ("+++", "---")]
    only_a = [l[1:] for l in diff if l.startswith("-")]
    only_b = [l[1:] for l in diff if l.startswith("+")]
    cosmetic = sum(1 for x in only_a + only_b if strip_ver(x) in
                   {strip_ver(y) for y in only_a + only_b} and True)
    # a changed line is "cosmetic" if some line on the other side matches it
    # once the version token is normalised away
    set_b = {strip_ver(y) for y in only_b}
    set_a = {strip_ver(y) for y in only_a}
    cosmetic = sum(1 for x in only_a if strip_ver(x) in set_b) + \
               sum(1 for x in only_b if strip_ver(x) in set_a)
    subst_a = [x for x in only_a if strip_ver(x) not in set_b]
    subst_b = [x for x in only_b if strip_ver(x) not in set_a]
    relevant = [x for x in subst_a + subst_b
                if any(t in x.lower() for t in assert_terms)]
    return {"label": label, "cited": url_a, "tested": url_b, "status": "compared",
            "lines_cited": len(la), "lines_tested": len(lb),
            "changed": len(only_a) + len(only_b),
            "cosmetic": cosmetic,
            "substantive": len(subst_a) + len(subst_b),
            "relevant_to_assertions": len(relevant),
            "similarity": round(difflib.SequenceMatcher(
                None, "\n".join(la), "\n".join(lb)).ratio(), 4),
            "relevant_lines": relevant[:20], "substantive_lines": (subst_a + subst_b)[:25]}


def main():
    cs = json.load(open(os.path.join(BASE, "constraints.json"), encoding="utf-8"))
    by_url = {}
    for c in cs:
        a = (c["assertions"] or [""])[0]
        d = (c["descriptions"] or [""])[0]
        for u in c["urls"]:
            by_url.setdefault(u, set()).update(terms_of(a, d))

    res = []
    for p in MILVUS:
        ua = f"https://milvus.io/api-reference/restful/v2.6.x/v2/{p}"
        res.append(analyse(f"族1 · milvus {p.split('/')[-1]}", ua,
                           f"https://milvus.io/api-reference/restful/v3.0.x/v2/{p}",
                           False, by_url.get(ua, set())))
    for p in QDRANT:
        ua = f"https://api.qdrant.tech/v-1-18-x/{p}"
        res.append(analyse(f"族4 · qdrant 1.19.0vs1.18 {p.split('/')[-1]}", ua,
                           f"https://api.qdrant.tech/v-1-19-x/{p}", True,
                           by_url.get(ua, set())))
    for p in QDRANT:
        ua = f"https://api.qdrant.tech/v-1-18-x/{p}"
        res.append(analyse(f"族5 · qdrant 1.12.1vs1.18 {p.split('/')[-1]}", ua,
                           f"https://api.qdrant.tech/v-1-12-x/{p}", True,
                           by_url.get(ua, set())))

    json.dump(res, open(os.path.join(BASE, "doc_content_diff.json"), "w",
                        encoding="utf-8"), ensure_ascii=False, indent=1)

    L = ["# A1 · 族 1/4/5 文档页面内容差异（机械）", "",
         "对照：「包实际引用的版本」vs「该受测版本」。",
         "- **cosmetic** = 只差版本号的改动（导航/版本串），非文档实质",
         "- **substantive** = 剔除 cosmetic 后的改动行",
         "- **relevant** = substantive 中命中「引用该页的约束所断言术语」的行数 ← 真正要紧的一列",
         "", "| 页面 | 相似度 | cosmetic | substantive | **relevant** | 状态 |",
         "|---|---|---|---|---|---|"]
    for r in res:
        if r["status"] != "compared":
            L.append(f"| {r['label']} | — | — | — | — | **正确版页面不存在（豁免）** |")
        else:
            L.append(f"| {r['label']} | {r['similarity']} | {r['cosmetic']} | "
                     f"{r['substantive']} | **{r['relevant_to_assertions']}** | 已比对 |")
    L += ["", "## 命中约束断言的改动行（逐页）", ""]
    for r in res:
        if r["status"] != "compared" or not r["relevant_lines"]:
            continue
        L += [f"### {r['label']}", ""]
        for x in r["relevant_lines"]:
            L.append(f"  - {x[:170]}")
        L.append("")
    open(os.path.join(BASE, "doc_content_diff.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("\n".join(L[:len(res) + 9]))


if __name__ == "__main__":
    main()
