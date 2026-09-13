# 候选缺陷 qdrant_024

[vendor=qdrant version=1.19.0 endpoint=recommend]
--- 观察到的行为（observed） ---

重放环境:qdrant v1.19.0 container (port 6338);证据来源:container replay,HTTP interactions captured verbatim。

=== DELETE /collections/main ===
-> 200 {"result":false,"status":"ok","time":0.000107115}
=== DELETE /collections/lookup8 ===
-> 200 {"result":false,"status":"ok","time":0.000073157}
=== PUT /collections/main ===
{"vectors": {"size": 4, "distance": "Euclid"}}
-> 200 {"result":true,"status":"ok","time":0.257165763}
=== PUT /collections/main/points?wait=true ===
{"points": [{"id": 1, "vector": [0.1, 0.2, 0.3, 0.4]}, {"id": 2, "vector": [0.4, 0.3, 0.2, 0.1]}]}
-> 200 {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.003787025}
=== PUT /collections/lookup8 ===
{"vectors": {"size": 8, "distance": "Euclid"}}
-> 200 {"result":true,"status":"ok","time":0.254043806}
=== PUT /collections/lookup8/points?wait=true ===
{"points": [{"id": 100, "vector": [0.9, 0, 0, 0, 0, 0, 0, 0]}]}
-> 200 {"result":{"operation_id":1,"status":"completed"},"status":"ok","time":0.004065926}
=== POST /collections/main/points/recommend ===
{"positive": [100], "limit": 2, "lookup_from": {"collection": "lookup8"}}
-> 400 {"status":{"error":"Wrong input: Vector dimension error: expected dim: 4, got 8"},"time":0.001524875}
=== POST /collections/main/points/recommend ===
{"positive": [[0.1, 0.2, 0.3, 0.4]], "negative": [100], "limit": 3, "lookup_from": {"collection": "lookup8"}}
-> 200 {"result":[{"id":1,"version":1,"score":0.9643651},{"id":2,"version":1,"score":1.3674794}],"status":"ok","time":0.000321475}
--- 契约依据（expected，M3 重建版） ---
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.19.0/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
{"constraint_id": "qdrant_range_recommend_009", "endpoint": "collections+{collection_name}+points+recommend", "description": "strategy must be one of: average_vector, best_score, sum_scores", "assertion": "strategy IN (average_vector, best_score, sum_scores)", "type": "range_constraint", "confidence": 1.0, "evidence_tier": "inferred_from_behavior", "source_url": "https://github.com/qdrant/qdrant/blob/v1.19.0/docs/redoc/master/openapi.json", "source_status": "reachable", "doc_version": "1.18.x", "source_verified": true, "source_type": "structured-spec"}
