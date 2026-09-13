"""How far do the served request-body schemas actually reach? Count the
schema-level constraint keywords the paper's bug class needs (numeric bounds,
closed enums) against the type-only declarations, over the tested version's
own OpenAPI artifact. Round-16 fix for the Table 1 claim (R2 3.9)."""
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SPEC = (r".tmp_semantic/qdrant-v1.18.0-forensic/docs/redoc/master/"
        r"openapi.json")
spec = json.load(open(SPEC, encoding="utf-8"))
BOUND = {"minimum", "maximum", "exclusiveMinimum", "exclusiveMaximum",
         "multipleOf", "minLength", "maxLength", "minItems", "maxItems",
         "pattern"}

seen = set()
n_schemas = 0
prop_kinds = Counter()
bound_props = []


def walk(node, where):
    global n_schemas
    if not isinstance(node, dict):
        return
    if node.get("type") == "object" or "properties" in node:
        n_schemas += 1
        for name, prop in (node.get("properties") or {}).items():
            keys = set(prop)
            if keys & BOUND:
                prop_kinds["numeric/structural bound"] += 1
                bound_props.append(f"{name} {' '.join(sorted(keys & BOUND))}")
            elif "enum" in prop:
                prop_kinds["closed enum"] += 1
            elif "type" in prop:
                prop_kinds["type only"] += 1
            else:
                prop_kinds["neither"] += 1
    for v in node.values():
        if isinstance(v, dict):
            walk(v, where)
        elif isinstance(v, list):
            for x in v:
                walk(x, where)


walk(spec, "spec")
print("schema-level property declarations by kind:")
for k, v in prop_kinds.most_common():
    print(f"  {k:26s} {v}")
tot = sum(prop_kinds.values())
print(f"  total {tot}")
print(f"\nobject schemas traversed: {n_schemas}")
print("examples of properties carrying a numeric/structural bound:")
for e in bound_props[:12]:
    print("   ", e)
