"""A1 step 2b — retry the 5 source_urls that blocked the first fetch.

milvus.io answers curl/urllib-default with 403 (bot filter) and loops on the
`.md` path form. Retry with a browser UA, then fall back to the milvus-docs
source repo (the same repo two working citations already point at).
"""
import json
import os
import urllib.request

OUT = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
PAGES = os.path.join(OUT, "pages")
UA = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                   "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# Explicit fallbacks only where the primary form is known to be blocked.
FALLBACKS = {
    "https://milvus.io/docs/schema.md":
        "https://raw.githubusercontent.com/milvus-io/milvus-docs/master/site/en/userGuide/schema/schema.md",
    "https://milvus.io/docs/index.md":
        "https://raw.githubusercontent.com/milvus-io/milvus-docs/master/site/en/userGuide/index.md",
    "https://milvus.io/docs/single-vector-search.md":
        "https://raw.githubusercontent.com/milvus-io/milvus-docs/master/site/en/userGuide/search-query-get/single-vector-search.md",
    "https://milvus.io/docs/insert-update.md":
        "https://raw.githubusercontent.com/milvus-io/milvus-docs/master/site/en/userGuide/insert-update-delete/insert-update.md",
}


def slug(url: str) -> str:
    import re
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:120]


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8", errors="replace"), r.headers.get("Content-Type", "")


def main():
    report = json.load(open(os.path.join(OUT, "fetch_report.json"), encoding="utf-8"))
    failures = [r for r in report if not r["saved"]]
    print(f"retrying {len(failures)} failures\n")
    for r in failures:
        url = r["source_url"]
        order = [url]
        if url in FALLBACKS:
            order.append(FALLBACKS[url])
        for cand in order:
            try:
                text, ctype = get(cand)
            except Exception as e:  # noqa: BLE001
                print(f"  FAIL {type(e).__name__}: {e}  <- {cand}")
                continue
            name = slug(url) + ".txt"
            with open(os.path.join(PAGES, name), "w", encoding="utf-8") as f:
                f.write(f"# source_url: {url}\n# fetched_from: {cand}\n"
                        f"# content_type: {ctype}\n# bytes: {len(text)}\n"
                        f"{'=' * 70}\n{text}")
            r["saved"] = name
            r["bytes"] = len(text)
            r["fetched_from"] = cand
            r["attempts"].append({"url": cand, "status": "ok-retry",
                                  "bytes": len(text), "content_type": ctype})
            print(f"  OK  {len(text):>7}B  <- {cand}")
            break
    json.dump(report, open(os.path.join(OUT, "fetch_report.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)
    ok = sum(1 for r in report if r["saved"])
    print(f"\ntotal fetched: {ok}/{len(report)}")
    for r in report:
        if not r["saved"]:
            print(f"  STILL MISSING: {r['source_url']}")


if __name__ == "__main__":
    main()
