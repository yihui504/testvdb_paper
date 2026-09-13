# -*- coding: utf-8 -*-
"""FULL re-verification of every entry in TestVDB.bib (xept:check-references).

Primary: direct arXiv abs fetch (arXiv IDs) / Crossref API (DOIs).
Fallback: DBLP search + OpenAlex search (title-only entries).
Each check records authoritative fields for automated comparison.
"""
import json, re, time, io, html, sys
import urllib3
import requests

urllib3.disable_warnings()
UA = {"User-Agent": "RefCheck/2.0 (mailto:test@example.org)"}
BIB = r"C:\Users\11428\Desktop\testvdb_paper\files\TestVDB.bib"
OUT = r"C:\Users\11428\Desktop\testvdb_paper\resources\working_memory\verify_all_out.json"

def sess():
    s = requests.Session()
    s.trust_env = False
    return s
S = sess()

def get(url, params=None, timeout=45, allow_404=False):
    r = S.get(url, params=params, timeout=timeout, verify=False, headers=UA)
    if r.status_code == 404 and allow_404:
        return None
    r.raise_for_status()
    return r

# ---------------- bib parser ----------------
def parse_bib(path):
    with io.open(path, encoding="utf-8-sig") as f:
        txt = f.read()
    txt = re.sub(r"(?m)^\s*%.*$", "", txt)
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([A-Za-z0-9_.\-]+)\s*,", txt):
        etype = m.group(1).lower()
        key = m.group(2)
        start = m.end()
        # regex already consumed the entry's opening '{' -> start depth at 1
        depth = 1
        i = start
        body_start = start
        while i < len(txt):
            c = txt[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    break
            i += 1
        body = txt[body_start:i]
        fields = {}
        for fm in re.finditer(r"([A-Za-z\-]+)\s*=\s*", body):
            fname = fm.group(1).lower()
            vstart = fm.end()
            v = ""
            if vstart < len(body) and body[vstart] == "{":
                d = 0
                j = vstart
                while j < len(body):
                    if body[j] == "{":
                        d += 1
                    elif body[j] == "}":
                        d -= 1
                        if d == 0:
                            break
                    j += 1
                v = body[vstart+1:j]
            else:
                j = vstart
                while j < len(body) and body[j] not in ",}":
                    j += 1
                v = body[vstart:j].strip()
            fields[fname] = v.strip()
        entries.append({"ID": key, "ENTRYTYPE": etype, **fields})
    return entries

def extract_arxiv(e):
    for f in ("howpublished", "note", "eprint", "url"):
        v = e.get(f, "") or ""
        m = re.search(r"arXiv[:\s]*(\d{4}\.\d{4,5})", v, re.I)
        if m:
            return m.group(1)
    return None

def split_authors(s):
    out = []
    depth = 0
    cur = ""
    i = 0
    while i < len(s):
        c = s[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        if depth == 0 and s[i:i+5].lower() == " and ":
            out.append(cur.strip())
            cur = ""
            i += 5
            continue
        cur += c
        i += 1
    if cur.strip():
        out.append(cur.strip())
    return out

def fam_of(chunk):
    chunk = chunk.strip()
    if not chunk:
        return ""
    if chunk.startswith("{") and chunk.endswith("}"):
        return chunk.strip("{}")
    s = re.sub(r"\{\\[`'\"^~=.]?[a-zA-Z]+\}", lambda m: m.group(0)[1:-1].lstrip("\\").lstrip("`'\"^~=."), chunk)
    s = re.sub(r"[{}]", "", s)
    if "," in s:
        return s.split(",")[0].strip()
    parts = s.split()
    return parts[-1].strip().rstrip(".")

def normalize(s):
    if not s:
        return ""
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def title_sim(a, b):
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    wa, wb = set(a.split()), set(b.split())
    inter = len(wa & wb)
    return inter / max(len(wa), len(wb), 1)

# ---------------- fetch helpers ----------------
def crossref_doi(doi):
    m = get("https://api.crossref.org/works/" + doi).json()["message"]
    title = (m.get("title") or [""])[0]
    authors = []
    for a in m.get("author", []):
        g = a.get("given", ""); f = a.get("family", "")
        authors.append((g + " " + f).strip() if g else f)
    year = None
    for k in ("published-print", "published", "issued"):
        dp = m.get(k, {}).get("date-parts", [[None]])
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]; break
    return {"title": title, "authors": authors, "year": year,
            "venue": (m.get("container-title") or [""])[0], "doi": m.get("DOI")}

def arxiv_abs(arxiv_id):
    """Direct fetch of the arXiv abs page; parse title + authors from HTML."""
    r = get("https://arxiv.org/abs/" + arxiv_id, allow_404=True)
    if r is None:
        return {"error": "404_not_found"}
    mtitle = re.search(r'<meta name="citation_title" content="([^"]*)"', r.text)
    authors = re.findall(r'<meta name="citation_author" content="([^"]*)"', r.text)
    mdate = re.search(r'<meta name="citation_date" content="([^"]*)"', r.text)
    return {"title": mtitle.group(1) if mtitle else "",
            "authors": authors,
            "date": mdate.group(1) if mdate else ""}

def semantic_arxiv(arxiv_id, retries=3):
    url = "https://api.semanticscholar.org/graph/v1/paper/arXiv:" + arxiv_id
    for i in range(retries):
        try:
            r = S.get(url, params={"fields": "title,authors,year,venue,externalIds"},
                      timeout=45, verify=False, headers=UA)
            if r.status_code == 429:
                time.sleep(5 * (i + 1)); continue
            if r.status_code == 404:
                return {"error": "not_found_404"}
            r.raise_for_status()
            d = r.json()
            return {"title": d.get("title") or "",
                    "authors": [a["name"] for a in d.get("authors", [])],
                    "year": d.get("year"), "venue": d.get("venue"),
                    "ext": d.get("externalIds", {})}
        except requests.RequestException:
            time.sleep(3)
    return {"error": "429/network"}

def dblp_search(query, h=5):
    r = get("https://dblp.org/search/publ/api",
            params={"q": query, "format": "json", "h": str(h)})
    d = r.json()["result"]["hits"]
    total = int(d.get("@total", 0))
    out = []
    for x in d.get("hit", []):
        info = x.get("info", {})
        authors = []
        au = info.get("authors", {})
        if isinstance(au, dict):
            alist = au.get("author", [])
            if isinstance(alist, dict):
                alist = [alist]
            for a in alist:
                authors.append(a.get("text", ""))
        out.append({"title": info.get("title", ""), "authors": authors,
                    "year": info.get("year"), "venue": info.get("venue", ""),
                    "url": info.get("url", "")})
    return {"total": total, "hits": out}

def openalex_search(title, per_page=4):
    r = get("https://api.openalex.org/works",
            params={"filter": "title.search:" + title[:120], "per-page": per_page})
    out = []
    for w in r.json().get("results", []):
        authors = [a["author"]["display_name"] for a in w.get("authorships", [])]
        src = (w.get("primary_location") or {}).get("source") or {}
        out.append({"title": w.get("title") or "", "authors": authors,
                    "year": w.get("publication_year"),
                    "venue": src.get("display_name")})
    return out

def check_url(url):
    """@misc/@online with URL: does the URL load?"""
    try:
        r = get(url, timeout=45)
        return {"status": r.status_code, "final": r.url, "ok": True}
    except Exception as ex:
        return {"status": "error", "err": str(ex)[:120], "ok": False}

# ---------------- main ----------------
entries = parse_bib(BIB)
results = []
for e in entries:
    key = e["ID"]; etype = e["ENTRYTYPE"]
    title = e.get("title", ""); year = e.get("year", "")
    doi = e.get("doi", ""); arxiv = extract_arxiv(e)
    bib_authors = e.get("author", "")
    fams = [fam_of(c) for c in split_authors(bib_authors)]
    rec = {"key": key, "type": etype, "bib_title": title, "bib_year": year,
           "bib_doi": doi, "bib_arxiv": arxiv, "bib_surnames": fams, "checks": []}

    if doi:
        try:
            m = crossref_doi(doi); m["src"] = "crossref_doi"; rec["checks"].append(m)
        except Exception as ex:
            rec["checks"].append({"src": "crossref_doi", "error": str(ex)[:150]})

    if arxiv:
        try:
            m = arxiv_abs(arxiv); m["src"] = "arxiv_abs"; rec["checks"].append(m)
        except Exception as ex:
            rec["checks"].append({"src": "arxiv_abs", "error": str(ex)[:150]})
        if not doi:
            time.sleep(1)
            try:
                m = semantic_arxiv(arxiv); m["src"] = "semantic_arxiv"; rec["checks"].append(m)
            except Exception as ex:
                rec["checks"].append({"src": "semantic_arxiv", "error": str(ex)[:150]})

    if not doi and not arxiv:
        q = re.sub(r"[^A-Za-z0-9 ]+", " ", title).strip()
        try:
            rec["dblp"] = dblp_search(q[:80], h=5)
        except Exception as ex:
            rec["dblp"] = {"error": str(ex)[:150]}
        time.sleep(0.5)
        try:
            rec["openalex"] = openalex_search(q[:100], 4)
        except Exception as ex:
            rec["openalex"] = {"error": str(ex)[:150]}

    # @misc with a URL (schemathesis) -> direct URL check
    if etype in ("misc", "online", "software") and not arxiv:
        url = e.get("url", "") or e.get("howpublished", "")
        m = re.search(r"https?://[^\s}]+", url)
        if m:
            rec["url_check"] = check_url(m.group(0).rstrip("}"))

    results.append(rec)
    print(key, "| doi=", doi, "| arxiv=", arxiv, "| fams=", fams, flush=True)

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)
print("\nWROTE", OUT, "entries=", len(results))
