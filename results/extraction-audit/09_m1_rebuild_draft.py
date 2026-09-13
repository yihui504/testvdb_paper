"""A1 M1 — mechanical rebuild draft for all 81 packs.

Applies, per pack:
  G4  endpoint filter   (drop contract rows whose endpoint does not match the
                         pack's candidate endpoint; the 4 doc-archaeology
                         main-assertion rows are exempt — they are the case's
                         own assertion)
  G6  leak strip        (drop the _provenance field; flag issue numbers)
  G1  version anchor    (join with version_check.csv verdict)
  G2  url status        (dead / landing / unresolved from fetch_report.json)
  page-text keyword hit (pages_text/*.txt, for the human verify stage)

Outputs:
  rebuild_v1/packs/<case>.md     draft pack (observed & maintainer sections kept
                                 verbatim; contract rows carry an _audit block)
  rebuild_v1/lines_to_verify.jsonl  every surviving row, priority-ordered
  rebuild_v1/m1_report.md        statistics

No judgement calls in here: rows are dropped or kept mechanically; everything
else is flagged for the human verify pass.
"""
import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = r"c:/Users/11428/Desktop/testvdb_paper"
MAT = ROOT + r"/.paperpilot/phase2-rerun/arms/materials_complete"
AUDIT = ROOT + r"/results/extraction-audit"
OUT = AUDIT + r"/rebuild_v1"

HEADER = re.compile(
    r"\[vendor=(\S+)\s+version=(\S+)\s+(?:defect_type=(\S+)\s+)?endpoint=([^\]]+)\]"
)
ISSUE_NO = re.compile(r"#\d{4,6}")

SEG_RE = re.compile(r"^---\s*(.+?)\s*---\s*$", re.M)
JSON_LINE = re.compile(r"^\{.*\"source_url\".*\}$")


def norm_path(endpoint: str) -> list[str]:
    """Ordered endpoint path tokens, placeholder- and method-insensitive.

    'collections+{collection_name}+points+query' -> ['collections','points','query']
    'POST /schema' -> ['schema']
    """
    e = endpoint.strip()
    e = re.sub(r"\{[^}]*\}", " ", e)
    e = re.sub(r"\b(get|post|put|patch|delete)\b", " ", e, flags=re.I)
    return [t.lower() for t in re.split(r"[+/ \-]+", e) if t.lower()]


def _stem(t: str) -> str:
    return t.rstrip("s") if len(t) > 3 else t


def g4_match(pack_ep: str, row_ep: str | None) -> bool:
    """Row relates to the pack's candidate endpoint iff (a) one path is a
    prefix of the other (row is a sub-operation of the pack's resource face),
    or (b) the pack declares a single bare resource token and the row touches
    that resource (covers qdrant packs written as 'points' / 'collection')."""
    if not row_ep:
        return False
    p, r = norm_path(pack_ep), norm_path(row_ep)
    if not p or not r:
        return False
    shorter = min(len(p), len(r))
    if p[:shorter] == r[:shorter]:
        return True
    if len(p) == 1 and any(_stem(p[0]) == _stem(t) for t in r):
        return True
    return False


def load_version_check() -> dict[tuple[str, str], dict]:
    """(pack, constraint_id) -> row from version_check.csv (1,645-row grain)."""
    idx: dict[tuple[str, str], dict] = {}
    with open(AUDIT + r"/version_check.csv", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            idx[(row["pack"], row["constraint_id"])] = row
    return idx


def load_url_status() -> dict[str, dict]:
    """source_url -> {status, saved} from fetch_report.json."""
    fr = json.load(open(AUDIT + r"/fetch_report.json", encoding="utf-8"))
    out: dict[str, dict] = {}
    for rec in fr:
        out[rec["source_url"]] = rec
    return out


def url_status(url: str) -> str:
    """G2 mechanical classification."""
    u = url.rstrip("/")
    if u.endswith("/api-reference") or u.endswith("/docs"):
        return "LANDING_PAGE"
    if url == "https://milvus.io/docs/index.md":
        return "UNRESOLVABLE"
    return "OK"


def page_text(saved: str | None) -> str | None:
    if not saved:
        return None
    p = os.path.join(AUDIT, "pages_text", saved)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else None


def keyword_hits(row: dict, text: str | None) -> list[str]:
    """Which row keywords appear in the page text (evidence for the verify pass)."""
    if not text:
        return []
    blob = " ".join(str(row.get(k) or "") for k in
                    ("assertion", "description", "expected_behavior"))
    words = {w.strip(".,:()[]{}") for w in re.findall(r"[A-Za-z_][A-Za-z_0-9]{2,}", blob)}
    words -= {"must", "the", "and", "with", "for", "non", "empty", "string",
              "integer", "returns", "response", "success", "data", "field",
              "collection", "vector", "vectors", "type", "value", "values"}
    hits = [w for w in sorted(words) if w.lower() in text.lower()]
    return hits[:12]


def split_pack(txt: str) -> dict[str, str]:
    """Split a pack into named segments (header line, segments, trailing lines)."""
    marks = [(m.start(), m.group(1)) for m in SEG_RE.finditer(txt)]
    segs: dict[str, str] = {"_head": txt[: marks[0][0]] if marks else txt}
    for i, (pos, name) in enumerate(marks):
        end = marks[i + 1][0] if i + 1 < len(marks) else len(txt)
        segs[name] = txt[pos:end]
    return segs


def seg_kind(name: str) -> str:
    n = name.split("（")[0].split("(")[0]
    if "观察" in name:
        return "observed"
    if "补充契约依据" in name:
        return "archaeology"      # main assertion — G4-exempt
    if "补充契约行" in name:
        return "bulk"
    if "维护者态度" in name:
        return "maintainer"       # kept verbatim, paper-sanctioned
    if "契约依据" in name:
        return "core"
    return "other"


def strip_provenance(obj: dict) -> tuple[dict, bool]:
    """G6: remove _provenance wholesale; flag residual issue numbers."""
    leaked = "_provenance" in obj
    obj = {k: v for k, v in obj.items() if k != "_provenance"}
    if ISSUE_NO.search(json.dumps(obj, ensure_ascii=False)):
        return obj, True
    return obj, leaked


def main() -> None:
    os.makedirs(OUT + "/packs", exist_ok=True)
    vc = load_version_check()
    fr = load_url_status()

    lines_out: list[dict] = []
    stats = {
        "packs": 0, "rows_total": 0, "rows_dropped_g4": 0,
        "rows_kept": 0, "provenance_stripped": 0, "issue_flagged": 0,
        "empty_contract_packs": [], "seg_counts": Counter(),
    }
    g1_counter: Counter = Counter()
    g2_counter: Counter = Counter()

    for path in sorted(glob.glob(MAT + "/*.md")):
        case = os.path.basename(path)[:-3]
        txt = open(path, encoding="utf-8").read()
        segs = split_pack(txt)
        stats["packs"] += 1

        h = HEADER.search(segs.get("_head", ""))
        vendor, version, dtype, pack_ep = h.groups() if h else (None,) * 4

        kept: dict[str, list[str]] = defaultdict(list)   # kind -> rendered rows
        for name, body in segs.items():
            if name == "_head":
                continue
            kind = seg_kind(name)
            stats["seg_counts"][kind] += 1
            if kind in ("observed", "maintainer", "other"):
                kept[kind].append(body.rstrip() + "\n")
                continue
            # contract-bearing segments: rebuild row by row
            for line in body.splitlines():
                line = line.strip()
                if not JSON_LINE.match(line):
                    if line and not line.startswith("---"):
                        kept[kind].append(line)   # prose intros kept for context
                    continue
                stats["rows_total"] += 1
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    kept[kind].append(line)
                    continue
                row_ep = obj.get("endpoint")
                if kind != "archaeology" and not g4_match(pack_ep or "", row_ep):
                    stats["rows_dropped_g4"] += 1
                    continue
                cid = obj.get("constraint_id") or obj.get("assertion_id") or "<noid>"
                obj, leaked = strip_provenance(obj)
                if leaked:
                    stats["provenance_stripped"] += 1
                issue_hit = bool(ISSUE_NO.search(json.dumps(obj, ensure_ascii=False)))
                if issue_hit:
                    stats["issue_flagged"] += 1
                vrow = vc.get((case, cid))
                g1 = vrow["verdict"] if vrow else "NO_VC_ROW"
                g1_counter[g1] += 1
                url = obj.get("source_url", "")
                frec = fr.get(url)
                g2 = url_status(url)
                if g2 == "OK" and frec and not frec.get("saved"):
                    g2 = "DEAD_LINK"
                g2_counter[g2] += 1
                ptext = page_text(frec.get("saved")) if frec else None
                hits = keyword_hits(obj, ptext)
                audit = {
                    "g1": g1, "g2": g2, "issue_no": issue_hit,
                    "page": "text" if ptext is not None else "none",
                    "kw_hits": hits, "priority": "main" if kind == "archaeology" else "bulk",
                }
                obj["_audit"] = audit
                kept[kind].append(json.dumps(obj, ensure_ascii=False))
                stats["rows_kept"] += 1
                lines_out.append({
                    "case": case, "vendor": vendor, "version": version,
                    "pack_endpoint": pack_ep, "segment": kind, "cid": cid,
                    "row_endpoint": row_ep, "g1": g1, "g2": g2,
                    "issue_no": issue_hit, "page": audit["page"],
                    "kw_hits": hits, "priority": audit["priority"],
                    "source_url": url,
                    "assertion": obj.get("assertion") or obj.get("expected_behavior") or "",
                    "description": obj.get("description") or "",
                })

        # assemble draft pack
        n_contract = len(kept.get("core", [])) + len(kept.get("bulk", [])) \
            + len(kept.get("archaeology", []))
        out = [segs["_head"].rstrip()]
        order = ["observed", "core", "archaeology", "bulk", "maintainer"]
        labels = {"core": "契约依据（expected，M1 过滤后初稿）",
                  "archaeology": "契约依据·主断言（M1，_provenance 已剥）",
                  "bulk": "补充契约行（M1 端点过滤后）"}
        for k in order:
            if k not in kept:
                continue
            if k in labels:
                out.append(f"--- {labels[k]} ---")
                if not kept[k] or all(not l.startswith("{") for l in kept[k]):
                    out.append(f"[经端点过滤后无相关契约行；需人工考古 endpoint={pack_ep}]")
                    stats["empty_contract_packs"].append(case)
            out.extend(kept[k])
        open(f"{OUT}/packs/{case}.md", "w", encoding="utf-8").write(
            "\n".join(out) + "\n")

    prio = {"main": 0, "bulk": 1}
    lines_out.sort(key=lambda r: (prio[r["priority"]], r["case"]))
    with open(OUT + "/lines_to_verify.jsonl", "w", encoding="utf-8") as f:
        for r in lines_out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    rep = [
        "# M1 机械初稿报告", "",
        f"- 包数 {stats['packs']}；契约行总数 {stats['rows_total']}",
        f"- G4 端点过滤删除 {stats['rows_dropped_g4']}（{stats['rows_dropped_g4']/max(stats['rows_total'],1):.1%}）",
        f"- 保留 {stats['rows_kept']}（其中主断言 {sum(1 for r in lines_out if r['priority']=='main')}）",
        f"- _provenance 剥除 {stats['provenance_stripped']} 行；issue 号残留标记 {stats['issue_flagged']} 行",
        f"- 端点过滤后契约段为空、需人工考古的包 {len(stats['empty_contract_packs'])}：",
        f"  {', '.join(stats['empty_contract_packs'])}", "",
        "## G1 版本核对（保留行）", "",
    ] + [f"- {k}: {v}" for k, v in g1_counter.most_common()] + [
        "", "## G2 URL 状态（保留行）", "",
    ] + [f"- {k}: {v}" for k, v in g2_counter.most_common()] + [
        "", "## 待人工核查行（lines_to_verify.jsonl）", "",
        f"- main（主断言）: {sum(1 for r in lines_out if r['priority']=='main')}",
        f"- bulk: {sum(1 for r in lines_out if r['priority']=='bulk')}",
        f"- 其中页面文本缺（需补抓）: {sum(1 for r in lines_out if r['page']=='none')}",
    ]
    open(OUT + "/m1_report.md", "w", encoding="utf-8").write("\n".join(rep) + "\n")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
