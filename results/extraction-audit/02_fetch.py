"""A1 step 2 — fetch every distinct source_url cited by the 81 frozen packs.

Read-only w.r.t. the paper. Saves each cited page verbatim under pages/ so the
human adjudication in step 3 works from captured text, not from a live fetch.
For github.com/.../blob/... URLs it retries the raw.githubusercontent.com form,
which is what the extractor would actually have read.
"""
import json
import os
import re
import urllib.request
import urllib.error

OUT = r"c:/Users/11428/Desktop/testvdb_paper/results/extraction-audit"
PAGES = os.path.join(OUT, "pages")
UA = {"User-Agent": "Mozilla/5.0 (compatible; TestVDB-extraction-audit/1.0)"}


def candidates(url: str):
    """Fetch order: raw form first where a blob page would hide the text."""
    m = re.match(r"https://github\.com/([^/]+)/([^/]+)/blob/(.+)", url)
    if m:
        owner, repo, rest = m.groups()
        head = f"https://raw.githubusercontent.com/{owner}/{repo}/{rest}"
        return [head, url]
    return [url]


def slug(url: str) -> str:
    s = re.sub(r"^https?://", "", url)
    s = re.sub(r"[^A-Za-z0-9._-]+", "_", s)
    return s[:120]


def fetch(url: str):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=45) as r:
        raw = r.read()
        ctype = r.headers.get("Content-Type", "")
    return raw, ctype


def main():
    os.makedirs(PAGES, exist_ok=True)
    urls = json.load(open(os.path.join(OUT, "urls.json"), encoding="utf-8"))
    report = []
    for u in urls:
        url = u["source_url"]
        got = None
        attempts = []
        for cand in candidates(url):
            try:
                raw, ctype = fetch(cand)
                text = raw.decode("utf-8", errors="replace")
                attempts.append({"url": cand, "status": "ok",
                                 "bytes": len(raw), "content_type": ctype})
                if got is None:
                    got = (cand, text, ctype, len(raw))
            except Exception as e:  # noqa: BLE001 - record any failure verbatim
                attempts.append({"url": cand, "status": f"FAIL {type(e).__name__}: {e}"})
        name = slug(url) + ".txt"
        if got:
            cand, text, ctype, nbytes = got
            with open(os.path.join(PAGES, name), "w", encoding="utf-8") as f:
                f.write(f"# source_url: {url}\n# fetched_from: {cand}\n"
                        f"# content_type: {ctype}\n# bytes: {nbytes}\n"
                        f"{'=' * 70}\n{text}")
            report.append({"source_url": url, "kind": u["kind"],
                           "instances": u["instances"],
                           "n_constraints": u["n_constraints"],
                           "saved": name, "bytes": nbytes,
                           "fetched_from": cand, "attempts": attempts})
        else:
            report.append({"source_url": url, "kind": u["kind"],
                           "instances": u["instances"],
                           "n_constraints": u["n_constraints"],
                           "saved": None, "bytes": 0,
                           "fetched_from": None, "attempts": attempts})
    json.dump(report, open(os.path.join(OUT, "fetch_report.json"), "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)

    ok = sum(1 for r in report if r["saved"])
    print(f"fetched {ok}/{len(report)} distinct source_urls\n")
    for r in report:
        flag = "OK " if r["saved"] else "FAIL"
        print(f"[{flag}] {r['instances']:>4}x {r['n_constraints']:>3}c "
              f"{r['kind']:<22} {r['bytes']:>8}B  {r['source_url']}")
        if not r["saved"]:
            for a in r["attempts"]:
                print(f"         {a['status']}  {a['url']}")


if __name__ == "__main__":
    main()
