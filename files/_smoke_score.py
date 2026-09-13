# -*- coding: utf-8 -*-
"""EN formalizer 全文件行为冒烟评分:与 CN 时代 v1.18.0 契约基准对比。"""
import json
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = "C:/Users/11428/.claude/plugins/cache/testvdb/testvdb/2.3.0/results/qdrant/v1.18.0/structured_contract.json"
SMOKE = "c:/Users/11428/Desktop/testvdb_paper/files/_smoke_contract_en.json"

base = json.load(open(BASE, encoding="utf-8"))
smoke = json.load(open(SMOKE, encoding="utf-8"))

FORM = re.compile(r"^[a-z0-9]+(\+[a-z0-9]+)*$")

def keyset(c):
    return {(e.get("path"), e.get("method")) for e in c.get("api_endpoints", [])}

def constraint_items(c):
    out = []
    for g, arr in c.get("constraints", {}).items():
        for it in arr or []:
            out.append((g, it))
    return out

bk, sk = keyset(base), keyset(smoke)
inter = bk & sk
print(f"endpoints: base={len(bk)} smoke={len(sk)} intersect={len(inter)}")
if sk:
    print(f"keyspace alignment (smoke keys present in base): {len(inter)}/{len(sk)} = {len(inter)/len(sk):.1%}")
only_smoke = sorted(p for p, m in sk - bk)
if only_smoke:
    print("smoke-only keys:", only_smoke[:10])

# 形式合规(规则 2.10)
viol = [e for e in smoke.get("api_endpoints", []) if not FORM.match(str(e.get("path", "")))]
print("form violations (rule 2.10):", len(viol), [e.get("path") for e in viol[:5]])

# 约束结构
bc, sc = constraint_items(base), constraint_items(smoke)
print(f"constraints: base={len(bc)} smoke={len(sc)}")
bep = {e.get("path") for e in base.get("api_endpoints", [])}
sep = {e.get("path") for e in smoke.get("api_endpoints", [])}
bad_ref = [it.get("constraint_id") for g, it in sc if it.get("endpoint") not in sep]
print("constraints referencing nonexistent smoke endpoints:", len(bad_ref), bad_ref[:5])

# 约束组覆盖
sg = {g for g, _ in sc}
print("smoke constraint groups:", sorted(sg))

# 关键字段完备性抽查
n_no_tier = sum(1 for g, it in sc if it.get("evidence_tier") not in ("explicit", "inferred"))
n_no_level = sum(1 for g, it in sc if it.get("level") not in ("endpoint", "system"))
n_no_src = sum(1 for g, it in sc if not it.get("source_url"))
print(f"missing evidence_tier: {n_no_tier}; missing level: {n_no_level}; missing source_url: {n_no_src}")

# 语义抽样:同参数约束比对(以 assertion 含相同参数名的为近似对)
import collections
def params(items):
    c = collections.Counter()
    for g, it in items:
        a = str(it.get("assertion", ""))
        for m in re.findall(r"[a-z_][a-z0-9_]{2,}", a):
            c[m] += 1
    return c
bp, sp = params(bc), params(sc)
common = set(bp) & set(sp)
print("top assertion-token overlap sample:", sorted(common)[:15])
