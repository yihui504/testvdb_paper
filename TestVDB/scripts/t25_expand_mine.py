#!/usr/bin/env python3
"""t25 expansion MINER (dry-run, no DeepSeek calls).

Mines self-proving over-strict candidates across 5 VDBs:
  numeric default D from raw_knowledge.md violates GLM's asserted bound B
  (e.g., default=0 but GLM asserts ">= 1"  =>  0 < 1  => over-strict, proven by doc alone).

Output: candidate table for human review. After review, t25_expand_run.py will feed
each raw passage to DeepSeek and score reproduction (family-specific vs task-intrinsic).
"""
import sys, re, json, glob, os
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

DBS = {
    "milvus":      ("results/milvus/2.4.0",        "results/milvus/2.4.0"),
    "qdrant":      ("results/qdrant/v1.18.2",      "results/qdrant/v1.18.2"),
    "weaviate":    ("results/weaviate/v1.38.2",    "results/weaviate/v1.38.2"),
    "chroma":      ("results/chroma/v1.5.9",       "results/chroma/v1.5.9"),
    "meilisearch": ("results/meilisearch/v1.48.3", "results/meilisearch/v1.48.3"),
}

# regex: a param bullet line  - `name` (typeinfo): desc
PARAM_LINE = re.compile(r"^\s*-\s+`?([A-Za-z_][\w\.\[\]]*)`?\s*\(([^)]*)\):\s*(.+)$")
DEFAULT_OF = re.compile(r"[Dd]efault[ =:]*([+-]?\d+)")
GE_BOUND  = re.compile(r">=\s*(\d+)|>\s*(\d+)|≥\s*(\d+)|minimum[ =:]*\d*?(\d+)")
REQ_FALSE = re.compile(r"required\s*=\s*false|optional", re.I)
REQ_ASSERTED = re.compile(r"\brequired\b|must be (present|provided|non-empty)|cannot be (null|omitted|empty)", re.I)


def parse_raw(path):
    """Return {param_name: (passage_line, default_val_or_None)}."""
    out = {}
    if not os.path.exists(path):
        return out
    for line in open(path, encoding="utf-8"):
        m = PARAM_LINE.match(line)
        if not m:
            continue
        name, typinfo, desc = m.group(1), m.group(2), m.group(3)
        full = f"`{name}` ({typinfo}): {desc}".strip()
        d = DEFAULT_OF.search(desc) or DEFAULT_OF.search(typinfo)
        dval = int(d.group(1)) if d else None
        req_false = bool(REQ_FALSE.search(typinfo) or REQ_FALSE.search(desc))
        out.setdefault(name, (full, dval, req_false))
    return out


def parse_contract_assertions(path):
    """Return list of (param_hint, assertion_text). Pull strings from constraints + assertions."""
    txts = []
    if not os.path.exists(path):
        return txts
    d = json.load(open(path, encoding="utf-8"))
    cs = d.get("constraints", {})
    items = []
    if isinstance(cs, dict):
        for v in cs.values():
            if isinstance(v, list):
                items += v
    elif isinstance(cs, list):
        items = cs
    for it in items:
        if isinstance(it, dict):
            desc = it.get("description", "")
            asrt = it.get("assertion", "")
            txts.append((desc + " " + asrt, asrt, desc))
    for a in d.get("assertions", []) or []:
        if isinstance(a, dict):
            txts.append((a.get("description", "") + " " + a.get("expected_behavior", "") + " " + a.get("assertion", ""), a.get("assertion", a.get("expected_behavior", "")), a.get("description", "")))
    return txts


def first_ge_bound(s):
    m = GE_BOUND.search(s)
    if not m:
        return None
    for g in m.groups():
        if g is not None:
            return int(g)
    return None


def main():
    candidates = []
    for db, (rawdir, _) in DBS.items():
        raw = parse_raw(f"{rawdir}/raw_knowledge.md")
        # contract: find any structured_contract.json under the dir
        cj = glob.glob(f"{rawdir}/structured_contract.json")
        asserts = parse_contract_assertions(cj[0]) if cj else []
        # index assertions by param name mention
        for name, (passage, dval, req_false) in raw.items():
            if dval is None:
                continue
            # find a contract assertion mentioning this param
            hit = None
            for (full, asrt, desc) in asserts:
                if re.search(r"\b" + re.escape(name) + r"\b", full):
                    hit = (asrt, desc)
                    break
            if not hit:
                continue
            asrt, desc = hit
            # t25 over-strict pattern lives on OPTIONAL params where GLM asserted a
            # strict bound / required / strict enum. Ground truth (is it REALLY
            # over-strict?) needs live special-value testing, done in phase 2.
            kind = None
            if re.search(r">\s*0|>=\s*[1-9]|\bminimum\b", asrt):
                kind = "strict-bound"
            elif REQ_ASSERTED.search(asrt):
                kind = "asserted-required-on-optional"
            elif re.search(r"\bin \[|\bone of\b|\benum\b", asrt, re.I):
                kind = "strict-enum"
            if kind:
                candidates.append({
                    "db": db, "param": name, "default": dval, "kind": kind,
                    "assertion": asrt[:160], "passage": passage[:200],
                })
    # also: optional param asserted required
    print(f"=== NUMERIC-DEFAULT-VIOLATES-BOUND candidates: {len(candidates)} ===\n")
    bydb = {}
    for c in candidates:
        bydb.setdefault(c["db"], []).append(c)
    for db in DBS:
        cs = bydb.get(db, [])
        print(f"--- {db}: {len(cs)} ---")
        for c in cs:
            print(f"  [{c['db']}] {c['param']:22} kind={c['kind']:26} default={c['default']}")
            print(f"       assertion: {c['assertion']}")
            print(f"       passage  : {c['passage']}")
    print(f"\nTOTAL numeric-default-violates candidates: {len(candidates)}")
    json.dump(candidates, open("scripts/t25_expand_candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("[wrote scripts/t25_expand_candidates.json]")


if __name__ == "__main__":
    main()
