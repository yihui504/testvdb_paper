#!/usr/bin/env python3
"""Enumerate the harvestable space for RQ3 scaling.

Scan Milvus + Qdrant raw_knowledge.md for parameters that are:
  - optional / required=false
  - have a stated default OR are explicitly optional
  - have NO explicit bound (no "minimum", "must be", "range", ">=", "<=", "max")
These are the ambiguous optional-default params where GLM can over-formalize.
Exclude the 12 params already in Table 4 (tab:e2).

Output: candidate pool size per DB + the list. Answers: can n grow from 12 to ~30?
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parents[1]
DBS = {
    "milvus": ROOT / "results/milvus/2.4.0/raw_knowledge.md",
    "qdrant": ROOT / "results/qdrant/v1.18.2/raw_knowledge.md",
}

# already in Table 4 (tab:e2) — exclude (match by lowercase name)
ALREADY = {
    "shardsnum", "metrictype", "consistencylevel", "data", "data_search",
    "outputfields", "limit", "rounddecimal", "offset", "dbname",
    "timeout", "group_size", "groupsize", "score_threshold", "scorethreshold",
}

PARAM_LINE = re.compile(r"^\s*- `?([A-Za-z_][\w\.\[\]]*)`?\s*\(([^)]*)\):\s*(.+)$")
BOUND_MARK = re.compile(
    r"\b(minimum|must be|range|maximum|in \[|in \(|>=|<=|>= |max\b|valid range|"
    r"between \d|from \d)",
    re.I,
)
OPT_MARK = re.compile(r"required\s*=\s*false|optional", re.I)
DEFAULT_MARK = re.compile(r"default", re.I)
REQUIRED_TRUE = re.compile(r"required\s*=\s*true", re.I)


def parse(path: Path) -> list[dict]:
    out: list[dict] = []
    if not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        m = PARAM_LINE.match(line)
        if not m:
            continue
        name, info, desc = m.group(1), m.group(2), m.group(3)
        blob = f"{info} {desc}"
        if REQUIRED_TRUE.search(blob):
            continue
        if not OPT_MARK.search(blob):
            continue
        if BOUND_MARK.search(blob):
            continue
        key = name.lower().replace("-", "_")
        if key in ALREADY:
            continue
        has_default = bool(DEFAULT_MARK.search(blob))
        out.append({"param": name, "info": info, "desc": desc[:110], "default": has_default})
    return out


def main() -> None:
    for db, path in DBS.items():
        cands = parse(path)
        # dedupe by param name (keep first)
        seen: set[str] = set()
        uniq: list[dict] = []
        for c in cands:
            if c["param"].lower() in seen:
                continue
            seen.add(c["param"].lower())
            uniq.append(c)
        with_default = [c for c in uniq if c["default"]]
        print(f"\n=== {db}: {len(uniq)} optional-no-bound candidates "
              f"({len(with_default)} with explicit 'default') ===")
        for c in uniq[:40]:
            star = "*" if c["default"] else " "
            print(f"  {star} {c['param']:32} ({c['info'][:28]})  {c['desc'][:70]}")


if __name__ == "__main__":
    main()
