"""A1 M2 — fetch the pages the empty-pack archaeology needs.

qdrant sub-pages come from the links embedded in the already-fetched api-reference
root page; milvus pages come from the milvus-docs *version branches* (v2.6.x /
v3.0.x), which is also the G1-correct anchor pattern for every milvus row.
"""
import json
import re
import sys
import urllib.request
from html2text import HTML2Text

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUTDIR = "pages_text"

TARGETS = [
    # (label, url)
    ("qdrant_014.recover", "https://api.qdrant.tech/v-1-18-x/api-reference/distributed/recover-current-peer"),
    ("qdrant_018.count", "https://api.qdrant.tech/v-1-18-x/api-reference/points/count-points"),
    ("qdrant_023.snapshot_recover", "https://api.qdrant.tech/v-1-18-x/api-reference/snapshots/recover-from-snapshot"),
    ("qdrant_023.v119.probe", "https://api.qdrant.tech/v-1-19-x/api-reference/snapshots/recover-from-snapshot"),
    ("milvus_012.list_v26", "https://milvus.io/api-reference/restful/v2.6.x/v2/Collection%20(v2)/List.md"),
    ("milvus_017.alias_list_v26", "https://milvus.io/api-reference/restful/v2.6.x/v2/Alias%20(v2)/List.md"),
    ("milvus_008.metric_v26", "https://raw.githubusercontent.com/milvus-io/milvus-docs/v2.6.x/site/en/userGuide/search-query-get/metric.md"),
    ("milvus_034_039_041.upsert_v30", "https://milvus.io/api-reference/restful/v3.0.x/v2/Entity%20(v2)/Upsert.md"),
    ("milvus_034.insert_v30", "https://milvus.io/api-reference/restful/v3.0.x/v2/Entity%20(v2)/Insert.md"),
]


def fetch(url: str) -> tuple[int, str]:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception as e:  # noqa: BLE001 - report and continue
        return -1, str(e)


def main() -> None:
    report = []
    for label, url in TARGETS:
        status, body = fetch(url)
        saved = None
        if status == 200 and body:
            if url.startswith("https://api.qdrant.tech") or url.startswith("https://milvus.io"):
                h = HTML2HText()
                text = h.handle(body)
            else:
                text = body
            saved = re.sub(r"[^A-Za-z0-9._-]+", "_", label) + ".txt"
            open(f"{OUTDIR}/{saved}", "w", encoding="utf-8").write(text)
        report.append({"label": label, "url": url, "status": status,
                       "saved": saved, "bytes": len(body)})
        print(f"{status:>4}  {label:32s} {len(body):>8}B  {url[:90]}")
    json.dump(report, open(f"{OUTDIR}/../archaeology_fetch_report.json", "w",
                           encoding="utf-8"), ensure_ascii=False, indent=1)


class HTML2HText(HTML2Text):
    def __init__(self) -> None:
        super().__init__()
        self.ignore_links = False
        self.body_width = 0


if __name__ == "__main__":
    main()
