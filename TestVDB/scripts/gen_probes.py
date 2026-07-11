#!/usr/bin/env python3
import json

# Probe generation: ~30 compliance probes for Milvus REST API
probes = []

# 1. Dimension extreme values
probes.append({
    "category": "dimension_extreme",
    "probe_id": "dim_min",
    "description": "Test minimum dimension boundary (1)",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_dim_min",
        "dimension": 1,
        "consistency_level": "Strong"
    },
    "expected": "accept"
})

probes.append({
    "category": "dimension_extreme",
    "probe_id": "dim_max",
    "description": "Test maximum dimension boundary (32768)",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_dim_max",
        "dimension": 32768,
        "consistency_level": "Strong"
    },
    "expected": "accept"
})

probes.append({
    "category": "dimension_extreme",
    "probe_id": "dim_below_min",
    "description": "Test dimension below minimum (0) - should reject",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_dim_bad",
        "dimension": 0,
        "consistency_level": "Strong"
    },
    "expected": "reject"
})

probes.append({
    "category": "dimension_extreme",
    "probe_id": "dim_above_max",
    "description": "Test dimension above maximum (32769) - should reject",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_dim_bad",
        "dimension": 32769,
        "consistency_level": "Strong"
    },
    "expected": "reject"
})

# 2. ConsistencyLevel enum validation
probes.append({
    "category": "consistency_enum",
    "probe_id": "consistency_invalid_enum",
    "description": "Test invalid consistencyLevel enum value - should reject",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_consistency_bad",
        "dimension": 128,
        "consistency_level": "INVALID_ENUM"
    },
    "expected": "reject"
})

probes.append({
    "category": "consistency_enum",
    "probe_id": "consistency_empty",
    "description": "Test empty consistencyLevel - should reject or default",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_consistency_empty",
        "dimension": 128,
        "consistency_level": ""
    },
    "expected": "reject_or_default"
})

probes.append({
    "category": "consistency_enum",
    "probe_id": "consistency_case_sensitivity",
    "description": "Test different case for consistencyLevel (lowercase strong)",
    "operation": "create_collection",
    "params": {
        "collection_name": "test_consistency_case",
        "dimension": 128,
        "consistency_level": "strong"
    },
    "expected": "accept_or_reject"
})

# 3. MetricType enum validation
probes.append({
    "category": "metric_enum",
    "probe_id": "metric_invalid_enum",
    "description": "Test invalid metricType enum - should reject",
    "operation": "create_index",
    "params": {
        "collection_name": "test_collection",
        "metric_type": "INVALID_METRIC"
    },
    "expected": "reject"
})

probes.append({
    "category": "metric_enum",
    "probe_id": "metric_missing",
    "description": "Test missing metricType - should default to valid value",
    "operation": "create_index",
    "params": {
        "collection_name": "test_collection"
    },
    "expected": "accept_with_default"
})

# 4. Limit bounds
probes.append({
    "category": "limit_bounds",
    "probe_id": "limit_negative",
    "description": "Test negative limit in query - should reject",
    "operation": "query",
    "params": {
        "collection_name": "test_collection",
        "limit": -1
    },
    "expected": "reject"
})

probes.append({
    "category": "limit_bounds",
    "probe_id": "limit_zero",
    "description": "Test zero limit in query - should reject",
    "operation": "query",
    "params": {
        "collection_name": "test_collection",
        "limit": 0
    },
    "expected": "reject"
})

probes.append({
    "category": "limit_bounds",
    "probe_id": "limit_above_max",
    "description": "Test limit > 16383 (should reject limit+offset >= 16384)",
    "operation": "query",
    "params": {
        "collection_name": "test_collection",
        "limit": 16384
    },
    "expected": "reject"
})

probes.append({
    "category": "limit_bounds",
    "probe_id": "limit_plus_offset_exceed",
    "description": "Test limit+offset > 16384 - should reject",
    "operation": "query",
    "params": {
        "collection_name": "test_collection",
        "limit": 16000,
        "offset": 400
    },
    "expected": "reject"
})

# 5. Nprobe bounds
probes.append({
    "category": "nprobe_bounds",
    "probe_id": "nprobe_zero",
    "description": "Test nprobe=0 in search - should reject (must be >=1)",
    "operation": "search",
    "params": {
        "collection_name": "test_collection",
        "nprobe": 0
    },
    "expected": "reject"
})

probes.append({
    "category": "nprobe_bounds",
    "probe_id": "nprobe_negative",
    "description": "Test negative nprobe - should reject",
    "operation": "search",
    "params": {
        "collection_name": "test_collection",
        "nprobe": -1
    },
    "expected": "reject"
})

# 6. CollectionName required
probes.append({
    "category": "required_fields",
    "probe_id": "collection_name_missing",
    "description": "Test missing collection_name - should reject",
    "operation": "create_collection",
    "params": {
        "dimension": 128,
        "consistency_level": "Strong"
    },
    "expected": "reject"
})

probes.append({
    "category": "required_fields",
    "probe_id": "collection_name_empty",
    "description": "Test empty collection_name - should reject",
    "operation": "create_collection",
    "params": {
        "collection_name": "",
        "dimension": 128,
        "consistency_level": "Strong"
    },
    "expected": "reject"
})

# 7. Wrong dimension vectors
probes.append({
    "category": "vector_dimension",
    "probe_id": "vector_dim_mismatch",
    "description": "Insert vector with wrong dimension - should reject",
    "operation": "insert",
    "params": {
        "collection_name": "test_dim_128",
        "vectors": [[0.1] * 64]
    },
    "expected": "reject"
})

probes.append({
    "category": "vector_dimension",
    "probe_id": "vector_dim_empty",
    "description": "Insert empty vector - should reject",
    "operation": "insert",
    "params": {
        "collection_name": "test_dim_128",
        "vectors": [[]]
    },
    "expected": "reject"
})

# 8. Query with invalid params
probes.append({
    "category": "query_validation",
    "probe_id": "query_with_invalid_filter",
    "description": "Query with malformed filter expression",
    "operation": "query",
    "params": {
        "collection_name": "test_collection",
        "filter": "invalid_field == 'value' and"
    },
    "expected": "reject"
})

# 9. Search with invalid params
probes.append({
    "category": "search_validation",
    "probe_id": "search_with_empty_vector",
    "description": "Search with empty query vector - should reject",
    "operation": "search",
    "params": {
        "collection_name": "test_collection",
        "vectors": [[]]
    },
    "expected": "reject"
})

probes.append({
    "category": "search_validation",
    "probe_id": "search_with_wrong_dim",
    "description": "Search with vector dimension mismatch",
    "operation": "search",
    "params": {
        "collection_name": "test_dim_128",
        "vectors": [[0.1] * 256]
    },
    "expected": "reject"
})

# 10. Index edge cases
probes.append({
    "category": "index_validation",
    "probe_id": "index_invalid_type",
    "description": "Create index with invalid index type",
    "operation": "create_index",
    "params": {
        "collection_name": "test_collection",
        "index_type": "INVALID_INDEX_TYPE"
    },
    "expected": "reject"
})

# 11. Load/drop edge cases
probes.append({
    "category": "load_drop",
    "probe_id": "load_nonexistent_collection",
    "description": "Load non-existent collection - should reject",
    "operation": "load_collection",
    "params": {
        "collection_name": "nonexistent_collection"
    },
    "expected": "reject"
})

probes.append({
    "category": "load_drop",
    "probe_id": "drop_nonexistent_collection",
    "description": "Drop non-existent collection - should reject",
    "operation": "drop_collection",
    "params": {
        "collection_name": "nonexistent_collection"
    },
    "expected": "reject"
})

# 12. Describe collection edge cases
probes.append({
    "category": "describe_validation",
    "probe_id": "describe_nonexistent",
    "description": "Describe non-existent collection - should reject",
    "operation": "describe_collection",
    "params": {
        "collection_name": "nonexistent_collection"
    },
    "expected": "reject"
})

print(f"Generated {len(probes)} probes")
print(json.dumps(probes, indent=2))