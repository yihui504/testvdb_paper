# -*- coding: utf-8 -*-
"""R46 six-gate (v5: DELETE scan starts after docstring) checker (v4 pattern, _sc_ prefix). Usage: py -3.12 .tmp_r41_gate.py"""
import json
import os
import py_compile
import re
import sys

DL = r"C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.5.0/results/qdrant/v1.18.0/2026-09-04T12-14-11Z/debate_logs"

def module_docstring(src: str) -> str:
    # v4: find first/next triple-quote, skipping shebang/coding lines naturally
    i = src.find('"""')
    if i < 0:
        i = src.find("'''")
        if i < 0:
            return ""
        j = src.find("'''", i + 3)
        return src[i + 3 : j] if j > 0 else ""
    j = src.find('"""', i + 3)
    return src[i + 3 : j] if j > 0 else ""

def delete_calls_unwrapped(src: str) -> list:
    # v5: scan only the CODE region (after module docstring) — docstring lines mentioning
    # DELETE + request are description text, not calls (R36 lesson 3 extension)
    bad = []
    i = src.find('"""')
    if i >= 0:
        j = src.find('"""', i + 3)
        if j > 0:
            src = src[j+3:]
    lines = src.splitlines()
    in_try = 0
    func_try_wrapped = False
    for idx, ln in enumerate(lines):
        s = ln.strip()
        if s.startswith("def ") or s.startswith("class "):
            # lookahead: function body fully try-wrapped?
            body = "\n".join(lines[idx + 1 : idx + 40])
            func_try_wrapped = bool(re.search(r"^\s{4}try:", body, re.M))
        if ("DELETE" in ln or '"DELETE"' in ln or "'DELETE'" in ln) and (
            "request" in ln or "urlreq" in ln or "urlopen" in ln or "Request(" in ln
        ):
            if in_try <= 0 and not func_try_wrapped:
                bad.append(f"L{idx+1}: {s[:90]}")
        if re.match(r"^\s*try:", ln):
            in_try += 1
        elif re.match(r"^\s*(finally:|except)", ln):
            pass
    return bad

def main():
    prefixes = ("state_snu_",)
    scripts = sorted(f for f in os.listdir(DL) if f.endswith(".py") and f.startswith(prefixes))
    if not scripts:
        print("NO SCRIPTS FOUND"); sys.exit(2)
    fails = []
    for name in scripts:
        path = os.path.join(DL, name)
        issues = []
        # G1 compile
        try:
            py_compile.compile(path, doraise=True)
        except Exception as e:
            issues.append(f"G1 compile: {e}")
        src = open(path, encoding="utf-8", errors="replace").read()
        ds = module_docstring(src)
        # G2 Attack + Oracle single line each
        atk = [l for l in ds.splitlines() if l.strip().startswith("Attack:")]
        ora = [l for l in ds.splitlines() if l.strip().startswith("Oracle:")]
        if len(atk) != 1:
            issues.append(f"G2 Attack lines={len(atk)}")
        if len(ora) != 1:
            issues.append(f"G2 Oracle lines={len(ora)}")
        # G3 path marker: docstring + meta consistency
        m = re.search(r"path:\s*([AB])\b", ds)
        doc_path = m.group(1) if m else None
        mp = path.replace(".py", ".meta.json")
        meta = {}
        if os.path.exists(mp):
            try:
                meta = json.load(open(mp, encoding="utf-8"))
            except Exception as e:
                issues.append(f"G3 meta parse: {e}")
        else:
            issues.append("G3 meta missing")
        meta_path = meta.get("path")
        if doc_path is None:
            issues.append("G3 docstring path marker missing")
        elif meta_path != doc_path:
            issues.append(f"G3 path mismatch doc={doc_path} meta={meta_path}")
        # G4 DELETE try-wrap
        bad = delete_calls_unwrapped(src)
        if bad:
            issues.append("G4 DELETE untry: " + " | ".join(bad[:3]))
        # G5 requests ban
        if re.search(r"^\s*(import requests|from requests)", src, re.M):
            issues.append("G5 requests import banned")
        # G6 meta required fields
        for k in ("defect_id", "endpoint", "path", "constraint_ids", "strategy"):
            if k not in meta:
                issues.append(f"G6 meta.{k} missing")
        if meta.get("defect_id") and meta["defect_id"] != name[:-3]:
            issues.append(f"G6 defect_id != stem: {meta.get('defect_id')}")
        tag = "PASS" if not issues else "FAIL"
        print(f"[{tag}] {name}  (path={doc_path})")
        for it in issues:
            print(f"    - {it}")
            fails.append(f"{name}: {it}")
    print(f"\n=== {len(scripts)} scripts, {len(fails)} issues ===")
    sys.exit(1 if fails else 0)

if __name__ == "__main__":
    main()
