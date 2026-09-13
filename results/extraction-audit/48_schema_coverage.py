"""Measure the Table 1 claim "several endpoints serve no schema" against the
tested version's own OpenAPI artifact (round-16 fix; R2 3.9)."""
import json
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

SPEC = (r".tmp_semantic/qdrant-v1.18.0-forensic/docs/redoc/master/"
        r"openapi.json")
spec = json.load(open(SPEC, encoding="utf-8"))
paths = spec.get("paths", {})

total = 0
with_schema = 0
no_body = 0
body_no_schema = 0
examples = []
for path, ops in paths.items():
    for method, op in ops.items():
        if method not in ("get", "post", "put", "patch", "delete"):
            continue
        total += 1
        rb = op.get("requestBody")
        if not rb:
            no_body += 1
            continue
        content = rb.get("content", {})
        has = any("schema" in media for media in content.values())
        if has:
            with_schema += 1
        else:
            body_no_schema += 1
            examples.append(f"{method.upper()} {path}")

print(f"openapi version: {spec.get('openapi') or spec.get('swagger')}")
print(f"operations: {total}")
print(f"  with a request-body schema : {with_schema}")
print(f"  no request body declared   : {no_body}")
print(f"  request body without schema: {body_no_schema}")
for e in examples[:10]:
    print("    ", e)
