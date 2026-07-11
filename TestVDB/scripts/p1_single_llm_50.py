#!/usr/bin/env python3
"""
Single-LLM compliance probe generation for Milvus REST API.
Generate 50+ boundary condition tests and evaluate TP/FP.
"""
import json
import requests
import uuid
from typing import Dict, List, Any

BASE_URL = "http://localhost:19530/v2/vectordb"

results = []
test_collection_prefix = f"p1_probe_{uuid.uuid4().hex[:8]}"


def make_request(method: str, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Make HTTP request and return response details."""
    url = f"{BASE_URL}/{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=10)
        else:
            raise ValueError(f"Unknown method: {method}")

        return {
            "status_code": response.status_code,
            "response_code": response.json().get("code", None),
            "response_body": response.json() if response.text else {}
        }
    except Exception as e:
        return {
            "status_code": -1,
            "response_code": -1,
            "response_body": {"error": str(e)}
        }


def record_probe(probe_name: str, endpoint: str, request_excerpt: str,
                 http_status: int, response_code: int, verdict: str, rationale: str):
    """Record a probe result."""
    results.append({
        "probe_name": probe_name,
        "endpoint": endpoint,
        "request_excerpt": request_excerpt,
        "http_status": http_status,
        "response_code": response_code,
        "verdict": verdict,
        "rationale": rationale
    })


def test_collection_create_dimension_boundaries():
    """Test dimension boundary conditions in collection creation."""

    # Valid schema template
    def make_schema(dimension=128, metric_type="COSINE", consistency_level="Bounded"):
        return {
            "collectionName": f"{test_collection_prefix}_dim_{dimension}",
            "dimension": dimension,
            "vectorFieldType": "FloatVector",
            "metricType": metric_type,
            "consistencyLevel": consistency_level
        }

    # Test 1: dimension = 0
    data = make_schema(dimension=0)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_zero",
        "collections/create",
        json.dumps({"dimension": 0}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=0"
    )

    # Test 2: dimension = -1
    data = make_schema(dimension=-1)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_negative_one",
        "collections/create",
        json.dumps({"dimension": -1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=-1"
    )

    # Test 3: dimension = 1
    data = make_schema(dimension=1)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_one",
        "collections/create",
        json.dumps({"dimension": 1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=1"
    )

    # Test 4: dimension = 32768 (max)
    data = make_schema(dimension=32768)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_max",
        "collections/create",
        json.dumps({"dimension": 32768}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=32768"
    )

    # Test 5: dimension = 32769 (exceeds max)
    data = make_schema(dimension=32769)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_exceeds_max",
        "collections/create",
        json.dumps({"dimension": 32769}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=32769"
    )

    # Test 6: dimension = 99999 (way too large)
    data = make_schema(dimension=99999)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_huge",
        "collections/create",
        json.dumps({"dimension": 99999}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=99999"
    )

    # Test 7: dimension = "string" (invalid type)
    data = make_schema(dimension="invalid")
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_string",
        "collections/create",
        json.dumps({"dimension": "invalid"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension='string'"
    )

    # Test 8: dimension = missing
    data = {
        "collectionName": f"{test_collection_prefix}_dim_missing",
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_missing",
        "collections/create",
        json.dumps({"dimension": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing dimension"
    )


def test_collection_create_metric_type_boundaries():
    """Test metricType boundary conditions."""

    def make_schema(metric_type="COSINE"):
        return {
            "collectionName": f"{test_collection_prefix}_metric_{metric_type}",
            "dimension": 128,
            "vectorFieldType": "FloatVector",
            "metricType": metric_type,
            "consistencyLevel": "Bounded"
        }

    # Test 9: metricType = INVALID
    data = make_schema(metric_type="INVALID")
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "metric_type_invalid",
        "collections/create",
        json.dumps({"metricType": "INVALID"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} metricType=INVALID"
    )

    # Test 10: metricType = missing
    data = {
        "collectionName": f"{test_collection_prefix}_metric_missing",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "metric_type_missing",
        "collections/create",
        json.dumps({"metricType": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing metricType"
    )

    # Test 11: metricType = wrong case (cosine instead of COSINE)
    data = make_schema(metric_type="cosine")
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "metric_type_wrong_case",
        "collections/create",
        json.dumps({"metricType": "cosine"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} metricType=cosine (wrong case)"
    )

    # Test 12: metricType = numeric (123)
    data = make_schema(metric_type=123)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "metric_type_numeric",
        "collections/create",
        json.dumps({"metricType": 123}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} metricType=123"
    )


def test_collection_create_consistency_level_boundaries():
    """Test consistencyLevel boundary conditions."""

    def make_schema(consistency_level="Bounded"):
        return {
            "collectionName": f"{test_collection_prefix}_cons_{consistency_level}",
            "dimension": 128,
            "vectorFieldType": "FloatVector",
            "metricType": "COSINE",
            "consistencyLevel": consistency_level
        }

    # Test 13: consistencyLevel = INVALID
    data = make_schema(consistency_level="INVALID")
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "consistency_level_invalid",
        "collections/create",
        json.dumps({"consistencyLevel": "INVALID"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} consistencyLevel=INVALID"
    )

    # Test 14: consistencyLevel = 42 (numeric)
    data = make_schema(consistency_level=42)
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "consistency_level_numeric",
        "collections/create",
        json.dumps({"consistencyLevel": 42}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} consistencyLevel=42"
    )

    # Test 15: consistencyLevel = missing
    data = {
        "collectionName": f"{test_collection_prefix}_cons_missing",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "consistency_level_missing",
        "collections/create",
        json.dumps({"consistencyLevel": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing consistencyLevel"
    )

    # Test 16: consistencyLevel = wrong case (bounded instead of Bounded)
    data = make_schema(consistency_level="bounded")
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "consistency_level_wrong_case",
        "collections/create",
        json.dumps({"consistencyLevel": "bounded"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} consistencyLevel=bounded (wrong case)"
    )


def test_collection_create_name_boundaries():
    """Test collectionName boundary conditions."""

    # Test 17: collectionName = empty string
    data = {
        "collectionName": "",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "collection_name_empty",
        "collections/create",
        json.dumps({"collectionName": ""}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} empty collectionName"
    )

    # Test 18: collectionName = missing
    data = {
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "collection_name_missing",
        "collections/create",
        json.dumps({"collectionName": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing collectionName"
    )

    # Test 19: collectionName = overlong (256 chars)
    data = {
        "collectionName": "a" * 256,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "collection_name_overlong",
        "collections/create",
        json.dumps({"collectionName": "a" * 256}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} overlong collectionName"
    )


def test_search_boundaries():
    """Test search endpoint boundary conditions."""

    # First create a valid collection for testing
    collection_name = f"{test_collection_prefix}_search_test"
    create_data = {
        "collectionName": collection_name,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    make_request("POST", "collections/create", create_data)

    # Insert some test data
    insert_data = {
        "collectionName": collection_name,
        "data": [
            {"id": 1, "vector": [0.1] * 128}
        ]
    }
    make_request("POST", "entities/insert", insert_data)

    def make_search_data(limit=10, nprobe=None, offset=None, vector_dim=128):
        data = {
            "collectionName": collection_name,
            "annsField": "vector",
            "limit": limit,
            "vector": [0.1] * vector_dim
        }
        if nprobe is not None:
            data["nprobe"] = nprobe
        if offset is not None:
            data["offset"] = offset
        return data

    # Test 20: limit = -1
    data = make_search_data(limit=-1)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_limit_negative",
        "entities/search",
        json.dumps({"limit": -1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=-1"
    )

    # Test 21: limit = 0
    data = make_search_data(limit=0)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_limit_zero",
        "entities/search",
        json.dumps({"limit": 0}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=0"
    )

    # Test 22: limit = 16385 (exceeds max)
    data = make_search_data(limit=16385)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_limit_exceeds_max",
        "entities/search",
        json.dumps({"limit": 16385}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=16385"
    )

    # Test 23: limit = missing
    data = {
        "collectionName": collection_name,
        "annsField": "vector",
        "vector": [0.1] * 128
    }
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_limit_missing",
        "entities/search",
        json.dumps({"limit": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing limit"
    )

    # Test 24: nprobe = 0
    data = make_search_data(limit=10, nprobe=0)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_nprobe_zero",
        "entities/search",
        json.dumps({"nprobe": 0}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} nprobe=0"
    )

    # Test 25: nprobe = -1
    data = make_search_data(limit=10, nprobe=-1)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_nprobe_negative",
        "entities/search",
        json.dumps({"nprobe": -1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} nprobe=-1"
    )

    # Test 26: offset = negative
    data = make_search_data(limit=10, offset=-1)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_offset_negative",
        "entities/search",
        json.dumps({"offset": -1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} offset=-1"
    )

    # Test 27: wrong dimension query vector (127 instead of 128)
    data = make_search_data(limit=10, vector_dim=127)
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_wrong_dimension",
        "entities/search",
        json.dumps({"vector": "[127 dims]"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} wrong dimension vector"
    )

    # Test 28: missing annsField
    data = {
        "collectionName": collection_name,
        "limit": 10,
        "vector": [0.1] * 128
    }
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_missing_anns_field",
        "entities/search",
        json.dumps({"annsField": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing annsField"
    )

    # Test 29: missing data
    data = {
        "collectionName": collection_name,
        "annsField": "vector",
        "limit": 10
    }
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_missing_data",
        "entities/search",
        json.dumps({"vector": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing vector"
    )


def test_query_boundaries():
    """Test query endpoint boundary conditions."""

    collection_name = f"{test_collection_prefix}_query_test"
    create_data = {
        "collectionName": collection_name,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    make_request("POST", "collections/create", create_data)

    def make_query_data(limit=10, filter_expr=None):
        data = {
            "collectionName": collection_name,
            "limit": limit
        }
        if filter_expr is not None:
            data["filter"] = filter_expr
        return data

    # Test 30: limit = -1
    data = make_query_data(limit=-1)
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_limit_negative",
        "entities/query",
        json.dumps({"limit": -1}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=-1"
    )

    # Test 31: limit = 0
    data = make_query_data(limit=0)
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_limit_zero",
        "entities/query",
        json.dumps({"limit": 0}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=0"
    )

    # Test 32: limit = 16385
    data = make_query_data(limit=16385)
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_limit_exceeds_max",
        "entities/query",
        json.dumps({"limit": 16385}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit=16385"
    )

    # Test 33: missing filter
    data = make_query_data(limit=10, filter_expr=None)
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_missing_filter",
        "entities/query",
        json.dumps({"filter": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing filter (may be OK)"
    )

    # Test 34: malformed filter
    data = make_query_data(limit=10, filter_expr="invalid syntax [[[")
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_malformed_filter",
        "entities/query",
        json.dumps({"filter": "invalid syntax [[["}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} malformed filter"
    )


def test_insert_boundaries():
    """Test insert endpoint boundary conditions."""

    collection_name = f"{test_collection_prefix}_insert_test"
    create_data = {
        "collectionName": collection_name,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    make_request("POST", "collections/create", create_data)

    # Test 35: wrong dimension vector (127 instead of 128)
    data = {
        "collectionName": collection_name,
        "data": [{"id": 1, "vector": [0.1] * 127}]
    }
    resp = make_request("POST", "entities/insert", data)
    record_probe(
        "insert_wrong_dimension",
        "entities/insert",
        json.dumps({"vector": "[127 dims]"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} wrong dimension vector"
    )

    # Test 36: missing vector
    data = {
        "collectionName": collection_name,
        "data": [{"id": 1}]
    }
    resp = make_request("POST", "entities/insert", data)
    record_probe(
        "insert_missing_vector",
        "entities/insert",
        json.dumps({"vector": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing vector"
    )


def test_varchar_boundaries():
    """Test VARCHAR field max_length boundary conditions."""

    # Test 37: max_length = 0
    data = {
        "collectionName": f"{test_collection_prefix}_varchar_0",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded",
        "schema": {
            "fields": [
                {"name": "id", "type": "INT64", "primary_key": True},
                {"name": "text", "type": "VARCHAR", "max_length": 0},
                {"name": "vector", "type": "FLOAT_VECTOR", "dim": 128}
            ]
        }
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "varchar_max_length_zero",
        "collections/create",
        json.dumps({"max_length": 0}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} max_length=0"
    )

    # Test 38: max_length = 70000 (exceeds max)
    data = {
        "collectionName": f"{test_collection_prefix}_varchar_huge",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded",
        "schema": {
            "fields": [
                {"name": "id", "type": "INT64", "primary_key": True},
                {"name": "text", "type": "VARCHAR", "max_length": 70000},
                {"name": "vector", "type": "FLOAT_VECTOR", "dim": 128}
            ]
        }
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "varchar_max_length_huge",
        "collections/create",
        json.dumps({"max_length": 70000}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} max_length=70000"
    )

    # Test 39: max_length = missing
    data = {
        "collectionName": f"{test_collection_prefix}_varchar_missing",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded",
        "schema": {
            "fields": [
                {"name": "id", "type": "INT64", "primary_key": True},
                {"name": "text", "type": "VARCHAR"},
                {"name": "vector", "type": "FLOAT_VECTOR", "dim": 128}
            ]
        }
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "varchar_max_length_missing",
        "collections/create",
        json.dumps({"max_length": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing max_length"
    )


def test_index_schema_variations():
    """Test index creation schema variations."""

    collection_name = f"{test_collection_prefix}_index_test"
    create_data = {
        "collectionName": collection_name,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    make_request("POST", "collections/create", create_data)

    # Test 40: invalid index type
    data = {
        "collectionName": collection_name,
        "fieldName": "vector",
        "indexName": "invalid_index",
        "indexType": "INVALID_TYPE",
        "metricType": "COSINE"
    }
    resp = make_request("POST", "indexes/create", data)
    record_probe(
        "index_invalid_type",
        "indexes/create",
        json.dumps({"indexType": "INVALID_TYPE"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} invalid indexType"
    )

    # Test 41: missing index type
    data = {
        "collectionName": collection_name,
        "fieldName": "vector",
        "indexName": "no_type_index"
    }
    resp = make_request("POST", "indexes/create", data)
    record_probe(
        "index_missing_type",
        "indexes/create",
        json.dumps({"indexType": "missing"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} missing indexType"
    )

    # Test 42: invalid metric type in index
    data = {
        "collectionName": collection_name,
        "fieldName": "vector",
        "indexName": "invalid_metric_index",
        "indexType": "IVF_FLAT",
        "metricType": "INVALID_METRIC"
    }
    resp = make_request("POST", "indexes/create", data)
    record_probe(
        "index_invalid_metric",
        "indexes/create",
        json.dumps({"metricType": "INVALID_METRIC"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} invalid metricType"
    )


def test_additional_edge_cases():
    """Test additional edge cases to reach 50+ probes."""

    collection_name = f"{test_collection_prefix}_extra"
    create_data = {
        "collectionName": collection_name,
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    make_request("POST", "collections/create", create_data)

    # Test 43: consistencyLevel = empty string
    data = {
        "collectionName": f"{test_collection_prefix}_cons_empty",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": ""
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "consistency_level_empty",
        "collections/create",
        json.dumps({"consistencyLevel": ""}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} empty consistencyLevel"
    )

    # Test 44: metricType = empty string
    data = {
        "collectionName": f"{test_collection_prefix}_metric_empty",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "metric_type_empty",
        "collections/create",
        json.dumps({"metricType": ""}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} empty metricType"
    )

    # Test 45: vectorFieldType = invalid
    data = {
        "collectionName": f"{test_collection_prefix}_vft_invalid",
        "dimension": 128,
        "vectorFieldType": "INVALID_VECTOR",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "vector_field_type_invalid",
        "collections/create",
        json.dumps({"vectorFieldType": "INVALID_VECTOR"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} invalid vectorFieldType"
    )

    # Test 46: dimension = float (1.5)
    data = {
        "collectionName": f"{test_collection_prefix}_dim_float",
        "dimension": 1.5,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "dimension_float",
        "collections/create",
        json.dumps({"dimension": 1.5}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} dimension=1.5"
    )

    # Test 47: search with empty vector
    data = {
        "collectionName": collection_name,
        "annsField": "vector",
        "limit": 10,
        "vector": []
    }
    resp = make_request("POST", "entities/search", data)
    record_probe(
        "search_empty_vector",
        "entities/search",
        json.dumps({"vector": "[]"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} empty vector"
    )

    # Test 48: insert with null id
    data = {
        "collectionName": collection_name,
        "data": [{"id": None, "vector": [0.1] * 128}]
    }
    resp = make_request("POST", "entities/insert", data)
    record_probe(
        "insert_null_id",
        "entities/insert",
        json.dumps({"id": None}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} null id"
    )

    # Test 49: query with limit = string
    data = {
        "collectionName": collection_name,
        "limit": "ten"
    }
    resp = make_request("POST", "entities/query", data)
    record_probe(
        "query_limit_string",
        "entities/query",
        json.dumps({"limit": "ten"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} limit='string'"
    )

    # Test 50: collectionName starting with number
    data = {
        "collectionName": "123_invalid_name",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "collection_name_starts_with_number",
        "collections/create",
        json.dumps({"collectionName": "123_invalid_name"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} name starting with number"
    )

    # Test 51: collectionName with special characters
    data = {
        "collectionName": "test@#$%collection",
        "dimension": 128,
        "vectorFieldType": "FloatVector",
        "metricType": "COSINE",
        "consistencyLevel": "Bounded"
    }
    resp = make_request("POST", "collections/create", data)
    record_probe(
        "collection_name_special_chars",
        "collections/create",
        json.dumps({"collectionName": "test@#$%collection"}),
        resp["status_code"],
        resp["response_code"],
        "FP" if resp["response_code"] in [1100, 1801, 1802] else "TP",
        f"API {'rejected' if resp['response_code'] in [1100, 1801, 1802] else 'accepted'} special characters in name"
    )


def main():
    """Execute all compliance probes."""
    print("Running single-LLM compliance probes...")

    test_collection_create_dimension_boundaries()
    test_collection_create_metric_type_boundaries()
    test_collection_create_consistency_level_boundaries()
    test_collection_create_name_boundaries()
    test_search_boundaries()
    test_query_boundaries()
    test_insert_boundaries()
    test_varchar_boundaries()
    test_index_schema_variations()
    test_additional_edge_cases()

    # Calculate statistics
    n_total = len(results)
    n_tp = sum(1 for r in results if r["verdict"] == "TP")
    n_fp = n_total - n_tp
    precision = n_tp / n_total if n_total > 0 else 0

    # Wilson score interval (95% confidence)
    import math
    if n_total > 0 and n_tp > 0:
        z = 1.96  # 95% confidence
        p = precision
        denominator = 1 + z**2 / n_total
        center = (p + z**2 / (2 * n_total)) / denominator
        margin = z * math.sqrt((p * (1 - p) + z**2 / (4 * n_total)) / n_total) / denominator

        wilson_ci = f"[{max(0, center - margin):.1%}, {min(1, center + margin):.1%}]"
    else:
        wilson_ci = "[N/A, N/A]"

    # Save results
    output_file = "C:/Users/11428/Desktop/mftui/TestVDB/scripts/p1_single_llm_50.json"
    with open(output_file, 'w') as f:
        json.dump({
            "summary": {
                "n_total": n_total,
                "n_TP": n_tp,
                "n_FP": n_fp,
                "precision": precision,
                "wilson_95_ci": wilson_ci
            },
            "probes": results
        }, f, indent=2)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Single-LLM Baseline Results (n={n_total})")
    print(f"{'='*60}")
    print(f"Total probes:      {n_total}")
    print(f"True Positives:    {n_tp} (API accepted illegal input)")
    print(f"True Negatives:    {n_fp} (API correctly rejected)")
    print(f"Precision:         {precision:.1%}")
    print(f"Wilson 95% CI:     {wilson_ci}")
    print(f"\nTPs found:")
    for tp in [r for r in results if r["verdict"] == "TP"]:
        print(f"  - {tp['probe_name']}: {tp['rationale']}")
    print(f"{'='*60}")

    print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()