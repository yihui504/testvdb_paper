#!/usr/bin/env python3
"""
Single-LLM-with-source ablation experiment
Execute compliance probes against Milvus REST API and perform source-anchored judgment
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import time
import os

# Milvus REST API configuration
MILVUS_BASE = "http://localhost:19530/v2/vectordb"

def milvus_request(endpoint, data, method="POST"):
    """Make HTTP request to Milvus REST API"""
    url = f"{MILVUS_BASE}{endpoint}"
    body = json.dumps(data).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            response_data = response.read().decode('utf-8')
            return json.loads(response_data), response.status, None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else None
        return None, e.code, error_body
    except urllib.error.URLError as e:
        return None, 0, str(e)
    except Exception as e:
        return None, 0, str(e)

def setup_test_collection():
    """Create a test collection for insert/query/search operations"""
    # First create dimension-128 collection
    data = {
        "collectionName": "test_dim_128",
        "dimension": 128,
        "consistencyLevel": "Strong"
    }
    result, status, error = milv_request("/collections/create", data)
    return status == 200

def create_collection(params):
    """Create collection with given parameters"""
    data = {
        "collectionName": params.get("collection_name", ""),
        "dimension": params.get("dimension", 128),
        "consistencyLevel": params.get("consistency_level", "Bounded")
    }
    return milv_request("/collections/create", data)

def describe_collection(collection_name):
    """Describe collection to check actual configuration"""
    data = {"collectionName": collection_name}
    return milv_request(f"/collections/{collection_name}/describe", data, method="GET")

def query_collection(params):
    """Query collection"""
    data = {
        "collectionName": params.get("collection_name", ""),
        "limit": params.get("limit", 10),
        "offset": params.get("offset", 0)
    }
    # Add filter if provided
    if "filter" in params:
        data["filter"] = params["filter"]
    return milv_request(f"/collections/{params.get('collection_name')}/query", data)

def search_collection(params):
    """Search collection"""
    data = {
        "collectionName": params.get("collection_name", ""),
        "vectors": params.get("vectors", [[]]),
        "limit": params.get("limit", 10)
    }
    # Add search params if provided
    if "nprobe" in params:
        data["params"] = {"nprobe": params["nprobe"]}
    return milv_request(f"/collections/{params.get('collection_name')}/search", data)

def insert_vectors(params):
    """Insert vectors into collection"""
    data = {
        "collectionName": params.get("collection_name", ""),
        "data": params.get("vectors", [[]])
    }
    return milv_request(f"/collections/{params.get('collection_name')}/insert", data)

def create_index(params):
    """Create index on collection"""
    data = {
        "collectionName": params.get("collection_name", ""),
        "indexName": "test_index"
    }
    if "metric_type" in params:
        data["metricType"] = params["metric_type"]
    if "index_type" in params:
        data["indexType"] = params["index_type"]
    return milv_request(f"/collections/{params.get('collection_name')}/indexes/create", data)

def load_collection(collection_name):
    """Load collection into memory"""
    data = {"collectionName": collection_name}
    return milv_request(f"/collections/{collection_name}/load", data)

def drop_collection(collection_name):
    """Drop collection"""
    data = {"collectionName": collection_name}
    return milv_request(f"/collections/{collection_name}/drop", data)

def milv_request(endpoint, data, method="POST"):
    """Milvus request wrapper - alias for milvus_request"""
    return milvus_request(endpoint, data, method)

def execute_probe(probe):
    """Execute a single probe and return result"""
    operation = probe["operation"]
    params = probe["params"]

    result = None
    status = None
    error = None
    collection_created = False

    try:
        if operation == "create_collection":
            # Skip if missing collection_name (required field)
            if "collection_name" not in params or not params.get("collection_name"):
                result = {"code": 1, "message": "collection_name is required"}
                status = 400
                error = "Missing required field: collection_name"
            else:
                result, status, error = create_collection(params)
                if status == 200:
                    collection_created = True

        elif operation == "describe_collection":
            result, status, error = describe_collection(params.get("collection_name", ""))

        elif operation == "query":
            result, status, error = query_collection(params)

        elif operation == "search":
            result, status, error = search_collection(params)

        elif operation == "insert":
            result, status, error = insert_vectors(params)

        elif operation == "create_index":
            result, status, error = create_index(params)

        elif operation == "load_collection":
            result, status, error = load_collection(params.get("collection_name", ""))

        elif operation == "drop_collection":
            result, status, error = drop_collection(params.get("collection_name", ""))

        else:
            result = {"code": 1, "message": f"Unknown operation: {operation}"}
            status = 400
            error = "Unknown operation"

        # Determine if API accepted the request
        api_accepted = status == 200

        return {
            "probe_id": probe["probe_id"],
            "api_accepted": api_accepted,
            "status_code": status,
            "response": result,
            "error": error,
            "collection_created": collection_created
        }

    except Exception as e:
        return {
            "probe_id": probe["probe_id"],
            "api_accepted": False,
            "status_code": 0,
            "response": None,
            "error": str(e),
            "collection_created": collection_created
        }

def main():
    """Main execution"""
    print("=== Single-LLM-with-source Ablation Experiment ===")
    print(f"Target: {MILVUS_BASE}")
    print()

    # Load probes
    with open('TestVDB/scripts/gen_probes.py', 'r') as f:
        # Extract the probes list from the Python file
        content = f.read()
        # Simple extraction - probes is defined in the file
        exec(content, globals())

    # We'll use the probes that were already generated
    import json
    probes_json = """[
  {"category": "dimension_extreme", "probe_id": "dim_min", "description": "Test minimum dimension boundary (1)", "operation": "create_collection", "params": {"collection_name": "test_dim_min", "dimension": 1, "consistency_level": "Strong"}, "expected": "accept"},
  {"category": "dimension_extreme", "probe_id": "dim_max", "description": "Test maximum dimension boundary (32768)", "operation": "create_collection", "params": {"collection_name": "test_dim_max", "dimension": 32768, "consistency_level": "Strong"}, "expected": "accept"},
  {"category": "dimension_extreme", "probe_id": "dim_below_min", "description": "Test dimension below minimum (0) - should reject", "operation": "create_collection", "params": {"collection_name": "test_dim_bad", "dimension": 0, "consistency_level": "Strong"}, "expected": "reject"},
  {"category": "dimension_extreme", "probe_id": "dim_above_max", "description": "Test dimension above maximum (32769) - should reject", "operation": "create_collection", "params": {"collection_name": "test_dim_bad", "dimension": 32769, "consistency_level": "Strong"}, "expected": "reject"},
  {"category": "consistency_enum", "probe_id": "consistency_invalid_enum", "description": "Test invalid consistencyLevel enum value - should reject", "operation": "create_collection", "params": {"collection_name": "test_consistency_bad", "dimension": 128, "consistency_level": "INVALID_ENUM"}, "expected": "reject"},
  {"category": "consistency_enum", "probe_id": "consistency_empty", "description": "Test empty consistencyLevel - should reject or default", "operation": "create_collection", "params": {"collection_name": "test_consistency_empty", "dimension": 128, "consistency_level": ""}, "expected": "reject_or_default"},
  {"category": "consistency_enum", "probe_id": "consistency_case_sensitivity", "description": "Test different case for consistencyLevel (lowercase strong)", "operation": "create_collection", "params": {"collection_name": "test_consistency_case", "dimension": 128, "consistency_level": "strong"}, "expected": "accept_or_reject"},
  {"category": "metric_enum", "probe_id": "metric_invalid_enum", "description": "Test invalid metricType enum - should reject", "operation": "create_index", "params": {"collection_name": "test_collection", "metric_type": "INVALID_METRIC"}, "expected": "reject"},
  {"category": "metric_enum", "probe_id": "metric_missing", "description": "Test missing metricType - should default to valid value", "operation": "create_index", "params": {"collection_name": "test_collection"}, "expected": "accept_with_default"},
  {"category": "limit_bounds", "probe_id": "limit_negative", "description": "Test negative limit in query - should reject", "operation": "query", "params": {"collection_name": "test_collection", "limit": -1}, "expected": "reject"},
  {"category": "limit_bounds", "probe_id": "limit_zero", "description": "Test zero limit in query - should reject", "operation": "query", "params": {"collection_name": "test_collection", "limit": 0}, "expected": "reject"},
  {"category": "limit_bounds", "probe_id": "limit_above_max", "description": "Test limit > 16383 (should reject limit+offset >= 16384)", "operation": "query", "params": {"collection_name": "test_collection", "limit": 16384}, "expected": "reject"},
  {"category": "limit_bounds", "probe_id": "limit_plus_offset_exceed", "description": "Test limit+offset > 16384 - should reject", "operation": "query", "params": {"collection_name": "test_collection", "limit": 16000, "offset": 400}, "expected": "reject"},
  {"category": "nprobe_bounds", "probe_id": "nprobe_zero", "description": "Test nprobe=0 in search - should reject (must be >=1)", "operation": "search", "params": {"collection_name": "test_collection", "nprobe": 0}, "expected": "reject"},
  {"category": "nprobe_bounds", "probe_id": "nprobe_negative", "description": "Test negative nprobe - should reject", "operation": "search", "params": {"collection_name": "test_collection", "nprobe": -1}, "expected": "reject"},
  {"category": "required_fields", "probe_id": "collection_name_missing", "description": "Test missing collection_name - should reject", "operation": "create_collection", "params": {"dimension": 128, "consistency_level": "Strong"}, "expected": "reject"},
  {"category": "required_fields", "probe_id": "collection_name_empty", "description": "Test empty collection_name - should reject", "operation": "create_collection", "params": {"collection_name": "", "dimension": 128, "consistency_level": "Strong"}, "expected": "reject"},
  {"category": "vector_dimension", "probe_id": "vector_dim_mismatch", "description": "Insert vector with wrong dimension - should reject", "operation": "insert", "params": {"collection_name": "test_dim_128", "vectors": [[0.1] * 64]}, "expected": "reject"},
  {"category": "vector_dimension", "probe_id": "vector_dim_empty", "description": "Insert empty vector - should reject", "operation": "insert", "params": {"collection_name": "test_dim_128", "vectors": [[]]}, "expected": "reject"},
  {"category": "query_validation", "probe_id": "query_with_invalid_filter", "description": "Query with malformed filter expression", "operation": "query", "params": {"collection_name": "test_collection", "filter": "invalid_field == 'value' and"}, "expected": "reject"},
  {"category": "search_validation", "probe_id": "search_with_empty_vector", "description": "Search with empty query vector - should reject", "operation": "search", "params": {"collection_name": "test_collection", "vectors": [[]]}, "expected": "reject"},
  {"category": "search_validation", "probe_id": "search_with_wrong_dim", "description": "Search with vector dimension mismatch", "operation": "search", "params": {"collection_name": "test_dim_128", "vectors": [[0.1] * 256]}, "expected": "reject"},
  {"category": "index_validation", "probe_id": "index_invalid_type", "description": "Create index with invalid index type", "operation": "create_index", "params": {"collection_name": "test_collection", "index_type": "INVALID_INDEX_TYPE"}, "expected": "reject"},
  {"category": "load_drop", "probe_id": "load_nonexistent_collection", "description": "Load non-existent collection - should reject", "operation": "load_collection", "params": {"collection_name": "nonexistent_collection"}, "expected": "reject"},
  {"category": "load_drop", "probe_id": "drop_nonexistent_collection", "description": "Drop non-existent collection - should reject", "operation": "drop_collection", "params": {"collection_name": "nonexistent_collection"}, "expected": "reject"},
  {"category": "describe_validation", "probe_id": "describe_nonexistent", "description": "Describe non-existent collection - should reject", "operation": "describe_collection", "params": {"collection_name": "nonexistent_collection"}, "expected": "reject"}
]"""

    probes = json.loads(probes_json)

    print(f"Loaded {len(probes)} probes")
    print()

    # First, create test collection for insert/query/search operations
    print("Setting up test collection...")
    setup_result = setup_test_collection()
    if setup_result:
        print("OK Test collection 'test_dim_128' created")
    print()

    # Execute all probes
    results = []
    api_accepted_count = 0

    for i, probe in enumerate(probes, 1):
        print(f"[{i}/{len(probes)}] Executing: {probe['probe_id']}")
        result = execute_probe(probe)
        results.append(result)

        if result['api_accepted']:
            api_accepted_count += 1
            print(f"  → API ACCEPTED (status {result['status_code']})")
        else:
            print(f"  → API REJECTED (status {result['status_code']})")

        # Small delay to avoid overwhelming the API
        time.sleep(0.1)

    print()
    print("=" * 60)
    print("PHASE 1 COMPLETE: Probe Execution")
    print("=" * 60)
    print(f"Total probes: {len(probes)}")
    print(f"API accepted: {api_accepted_count}")
    print(f"API rejected: {len(probes) - api_accepted_count}")
    print()

    # Save initial results
    with open('TestVDB/scripts/p1_single_llm_source.json', 'w') as f:
        json.dump({
            "experiment": "single-LLM-with-source ablation",
            "arm": "P1-2 Round 8",
            "phase": "execution_complete",
            "total_probes": len(probes),
            "api_accepted": api_accepted_count,
            "api_rejected": len(probes) - api_accepted_count,
            "probes": probes,
            "results": results
        }, indent=2)

    print("Results saved to TestVDB/scripts/p1_single_llm_source.json")
    print()
    print("NEXT: Perform source-anchored judgment on accepted probes")

    return results, api_accepted_count

if __name__ == "__main__":
    main()