"""A1 step 3 — build the human-adjudication materials.

Produces, from the step-1 inventory and the step-2 captured pages:
  pages_text/<slug>.txt   readable text of each cited page (HTML stripped)
  evidence.md             per source_url: what it is, which constraints cite it
  worksheet.csv           one row per (constraint, cited page) — verdict columns BLANK
  triage.csv              mechanical term-presence signal (an AID, not a verdict)

No judgement is made here. The mechanical signal in triage.csv is deliberately
labelled as an aid: a term appearing on a page does not mean the page supports
the assertion, and that decision stays with the human reader.
"""
import csv
import html as html_mod
import json
import os
import re

BASE = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
PAGES = os.path.join(BASE, "pages")
TEXT = os.path.join(BASE, "pages_text")

STOP = set("""the a an and or of to in for on with is are was were be been being that this these those
it its as at by from not no if then than so such can may must should would could will shall do does
did not only also more most other others any all each both same between within into over under above
below when where which who whom whose how what why has have had having value values return returns
returned data type types field fields name names case true false null none default specified provide
provides provided support supports supported using used use one two three first second""".split())


def clean(path: str) -> str:
    raw = open(path, encoding="utf-8", errors="replace").read()
    header, _, body = raw.partition("=" * 70)
    head = header.lower()
    if "text/html" in head:
        import html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.body_width = 0
        body = h.handle(body)
    elif "json" in head:
        try:
            obj = json.loads(body)
            body = json.dumps(obj, ensure_ascii=False, indent=1)
        except json.JSONDecodeError:
            pass
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def tokens(text: str):
    return {t for t in re.findall(r"[a-zA-Z_]{5,}", text.lower()) if t not in STOP}


def main():
    os.makedirs(TEXT, exist_ok=True)
    report = {r["source_url"]: r for r in
              json.load(open(os.path.join(BASE, "fetch_report.json"), encoding="utf-8"))}
    constraints = json.load(open(os.path.join(BASE, "constraints.json"), encoding="utf-8"))
    urls = json.load(open(os.path.join(BASE, "urls.json"), encoding="utf-8"))

    page_text, page_tokens = {}, {}
    for url, r in report.items():
        if not r.get("saved"):
            continue
        txt = clean(os.path.join(PAGES, r["saved"]))
        out = os.path.join(TEXT, r["saved"])
        open(out, "w", encoding="utf-8").write(txt)
        page_text[url] = txt
        page_tokens[url] = tokens(txt)

    # ---- worksheet: one row per (constraint, cited page)
    rows, triage = [], []
    for c in constraints:
        assertion = (c["assertions"] or [""])[0]
        desc = (c["descriptions"] or [""])[0]
        for url in c["urls"]:
            r = report.get(url, {})
            rows.append({
                "constraint_id": c["constraint_id"],
                "vendor": ";".join(c["vendors"]),
                "endpoint": ";".join(x for x in c["endpoints"] if x),
                "type": ";".join(x for x in c["types"] if x),
                "assertion": assertion,
                "description": desc,
                "source_url": url,
                "url_kind": next((u["kind"] for u in urls if u["source_url"] == url), ""),
                "page_captured": "yes" if r.get("saved") else "NO",
                "verdict_page_supports": "",
                "verdict_is_documentation": "",
                "note": "",
            })
            want = tokens(f"{assertion} {desc}")
            have = page_tokens.get(url)
            if have is None:
                triage.append({"constraint_id": c["constraint_id"], "source_url": url,
                               "terms": len(want), "found": "", "missing_terms": "PAGE NOT CAPTURED"})
            else:
                found = sorted(want & have)
                missing = sorted(want - have)
                triage.append({"constraint_id": c["constraint_id"], "source_url": url,
                               "terms": len(want), "found": len(found),
                               "missing_terms": " ".join(missing[:12])})

    with open(os.path.join(BASE, "worksheet.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    with open(os.path.join(BASE, "triage.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["constraint_id", "source_url", "terms",
                                          "found", "missing_terms"])
        w.writeheader()
        w.writerows(triage)

    # ---- evidence.md
    by_url = {}
    for c in constraints:
        for url in c["urls"]:
            by_url.setdefault(url, []).append(c)

    L = ["# A1 · 抽取阶段审计 — 证据汇编", "",
         f"约束 {len(constraints)} 条；引用页 {len(urls)} 个（捕获成功 {len(page_text)}）。",
         "判定列在 `worksheet.csv` 中留空，由人填写。`triage.csv` 的术语命中数只是检索线索，不是判定。",
         ""]
    for u in urls:
        url = u["source_url"]
        r = report.get(url, {})
        L += [f"## `{url}`", "",
              f"- 性质：**{u['kind']}**｜URL 版本片段：{u['url_version'] or '—'}"
              f"｜实例 {u['instances']}｜引用该页的约束 {u['n_constraints']} 条",
              f"- 捕获：{'`pages_text/' + r['saved'] + '`' if r.get('saved') else '**未捕获**'}"
              + (f"（实际取自 `{r['fetched_from']}`）" if r.get("fetched_from") and r["fetched_from"] != url else ""),
              ""]
        for c in sorted(by_url.get(url, []), key=lambda c: c["constraint_id"]):
            L.append(f"- **{c['constraint_id']}** 〔{';'.join(c['vendors'])} / {c['endpoint'] if False else ';'.join(x for x in c['endpoints'] if x)}〕")
            if c["assertions"]:
                L.append(f"  - assertion: `{c['assertions'][0]}`")
            if c["descriptions"]:
                L.append(f"  - description: {c['descriptions'][0]}")
        L.append("")
    open(os.path.join(BASE, "evidence.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")

    print(f"constraints      : {len(constraints)}")
    print(f"worksheet rows   : {len(rows)}  -> worksheet.csv")
    print(f"triage rows      : {len(triage)} -> triage.csv")
    print(f"pages captured   : {len(page_text)}/{len(urls)} -> pages_text/")
    print(f"evidence sections: {len(urls)} -> evidence.md")


if __name__ == "__main__":
    main()
