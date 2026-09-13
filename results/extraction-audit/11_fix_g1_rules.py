"""Fix the G1 verdict rule: a versioned doc *segment* (v2.6.x, 1.18.x) covers
every patch release of that major.minor, so 'url 2.6.x vs tested 2.6.16' is
aligned, not a mismatch. Recompute the verdict for every pair and re-score
the audit statistics (the 299-row figure used the strict string compare).

Also fetch the qdrant v-1-12-x segment root page for the qdrant_001 rebuild.
"""
import glob
import json
import re
import sys
import urllib.request
from collections import Counter
from html2text import HTML2Text

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def version_token(url: str) -> str | None:
    m = re.search(r"/v[-]?(\d+\.\d+(?:\.\d+)?|x)[./-]", url)
    if m:
        return m.group(1)
    m = re.search(r"/v-(\d+)-(\d+)(?:-|/)", url)
    return f"{m.group(1)}.{m.group(2)}" if m else None


def aligned(url_ver: str | None, tested: str) -> str:
    if url_ver is None:
        return "page-unversioned"
    u, t = url_ver.split("."), tested.split(".")
    if u == t:
        return "aligned"
    # segment: 2.6.x / 1.18.x (or its truncated form '2.6') covers 2.6.* / 1.18.*
    if len(u) == 3 and u[2] == "x" and u[:2] == t[:2]:
        return "aligned-segment"
    if len(u) == 2 and len(t) >= 2 and u == t[:2]:
        return "aligned-segment"
    return "MISMATCH"


def main() -> None:
    # 1. rescore every pair from lines_to_verify (pair grain)
    rows = [json.loads(l) for l in open("rebuild_v1/lines_to_verify.jsonl",
                                        encoding="utf-8")]
    pairs: dict[tuple, dict] = {}
    for r in rows:
        k = (r["cid"], r["source_url"])
        if k not in pairs:
            pairs[k] = r
    new = Counter()
    true_mis = []
    for r in pairs.values():
        uv = version_token(r["source_url"])
        v = aligned(uv, r["version"]) if uv is not None or True else None
        new[v] += 1
        if v == "MISMATCH":
            true_mis.append((r["case"], r["cid"][:40], uv, r["version"],
                             r["source_url"][:60]))
    print("对级 G1（修正后）:", dict(new.most_common()))
    print(f"\n真 MISMATCH 对 {len(true_mis)}:")
    for t in true_mis[:30]:
        print("  ", t)

    # 2. row-grain rescore for the audit statistics
    row_new = Counter()
    for r in rows:
        uv = version_token(r["source_url"])
        row_new[aligned(uv, r["version"])] += 1
    print("\n行级 G1（修正后）:", dict(row_new.most_common()))

    # 3. fetch qdrant v-1-12-x root for qdrant_001
    url = "https://api.qdrant.tech/v-1-12-x/api-reference"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    h = HTML2Text()
    h.ignore_links = False
    h.body_width = 0
    open("pages_text/qdrant_v-1-12-x_root.txt", "w", encoding="utf-8").write(
        h.handle(body))
    links = sorted(set(re.findall(r'href="([^"]*api-reference[^"]*)"', body)))
    print(f"\nv-1-12-x root: {len(body)}B, {len(links)} subpage links")


if __name__ == "__main__":
    main()
