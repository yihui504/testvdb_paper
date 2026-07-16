#!/usr/bin/env python3
"""E2 expansion: mine over-strict candidate clauses across Milvus/Qdrant/Weaviate.

For each bound/enum-style GLM assertion on an optional param, extract the param,
its raw_knowledge passage + default, and auto-flag over-strict (default violates
the asserted bound, or the doc passage states a special value the bound excludes).
Output: candidate set for human curation -> then DeepSeek judging.
"""
import sys, re, json, glob, os
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

DBS = {
    "milvus":   ("TestVDB/results/milvus/2.4.0",   "Milvus"),
    "qdrant":   ("TestVDB/results/qdrant/v1.18.2", "Qdrant"),
    "weaviate": ("TestVDB/results/weaviate/v1.38.2","Weaviate"),
}

# bound/enum/required assertion patterns + param extractor
ASSERT_RE = [
    (re.compile(r"^([A-Za-z_][\w\.]*)\s*(>=|>|<=|<)\s*\d"), "bound"),
    (re.compile(r"^([A-Za-z_][\w\.]*)\s+in\s*[\(\[]"), "enum"),
    (re.compile(r"^([A-Za-z_][\w\.]*)\s+(must be|required|is required)"), "required"),
]
PARAM_LINE = re.compile(r"^\s*-\s+`?([A-Za-z_][\w\.\[\]]*)`?\s*\(([^)]*)\):\s*(.+)$")
DEFAULT_OF = re.compile(r"[Dd]efault[ =:]*([+-]?\d+)")
GE_BOUND = re.compile(r">=\s*(\d+)|>\s*(\d+)")

def parse_raw(path):
    out = {}
    if not os.path.exists(path): return out
    for line in open(path, encoding="utf-8"):
        m = PARAM_LINE.match(line)
        if not m: continue
        name, typinfo, desc = m.group(1), m.group(2), m.group(3)
        d = DEFAULT_OF.search(desc) or DEFAULT_OF.search(typinfo)
        out[name] = (f"`{name}` ({typinfo}): {desc}".strip(), int(d.group(1)) if d else None,
                     bool(re.search(r"required\s*=\s*false|optional", typinfo+desc, re.I)))
    return out

def contract_assertions(path):
    d = json.load(open(path, encoding="utf-8"))
    items = []
    cs = d.get("constraints", {})
    if isinstance(cs, dict):
        for v in cs.values(): items += v if isinstance(v, list) else []
    elif isinstance(cs, list): items = cs
    items += d.get("assertions", []) or []
    out = []
    for it in items:
        if not isinstance(it, dict): continue
        for key in ("assertion", "expected_behavior"):
            t = it.get(key, "")
            if t and t.strip(): out.append(t.strip())
    return out

def first_bound(s):
    m = GE_BOUND.search(s)
    if not m: return None
    for g in m.groups():
        if g is not None: return int(g)
    return None

def main():
    cands = []
    for db, (rawdir, label) in DBS.items():
        raw = parse_raw(f"{rawdir}/raw_knowledge.md")
        cj = glob.glob(f"{rawdir}/structured_contract.json")
        asserts = contract_assertions(cj[0]) if cj else []
        for a in asserts:
            kind = None; param = None
            for pat, k in ASSERT_RE:
                m = pat.match(a)
                if m: kind, param = k, m.group(1); break
            if not param: continue
            base = param.split(".")[-1]  # replicationConfig.factor -> factor
            info = raw.get(param) or raw.get(base)
            if not info: continue
            passage, dval, opt = info
            b = first_bound(a)
            auto = ""
            if kind == "bound" and dval is not None and b is not None and dval < b:
                auto = f"OVER-STRICT(default={dval}<{b})"
            elif kind == "bound" and dval is not None and b is not None and dval == b and re.search(r"0|empty|null|optional", passage, re.I):
                auto = "maybe(0/special?)"
            elif kind == "enum" and opt:
                auto = "maybe(strict-enum on optional)"
            elif kind == "required" and opt:
                auto = "maybe(required on optional)"
            cands.append({"db": db, "param": param, "kind": kind, "assertion": a[:90],
                          "default": dval, "optional": opt, "auto": auto, "passage": passage[:140]})
    print(f"=== {len(cands)} candidates ===")
    from collections import Counter
    print("per DB:", dict(Counter(c["db"] for c in cands)))
    print("auto OVER-STRICT:", sum(1 for c in cands if c["auto"].startswith("OVER")), "| maybe:", sum(1 for c in cands if c["auto"].startswith("maybe")))
    for c in cands:
        flag = "★" if c["auto"].startswith("OVER") else ("?" if c["auto"].startswith("maybe") else " ")
        print(f" {flag} [{c['db']:8}] {c['param']:22} {c['kind']:8} d={str(c['default']):4} {c['assertion'][:55]}")
        if flag != " ": print(f"           passage: {c['passage']}")
    json.dump(cands, open("TestVDB/scripts/e2_expand_candidates.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n[wrote TestVDB/scripts/e2_expand_candidates.json]")

if __name__ == "__main__":
    main()
