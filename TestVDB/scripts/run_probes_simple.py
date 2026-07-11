#!/usr/bin/env python3
"""
Single-LLM-with-source ablation experiment
Direct probe execution with no intermediate JSON
"""

import json
import urllib.request
import urllib.error
import time

# Milvus REST API configuration
MILVUS_BASE = "http://localhost:19530/v2/vectordb"

def milv_request(endpoint, data, method="POST"):
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

def main():
    """Main execution"""
    print("=== Single-LLM-with-source Ablation Experiment ===")
    print(f"Target: {MILVUS_BASE}")
    print()

    # Define probes directly
    probes = [
        # 1. Dimension extremes
        {"id": "dim_min", "op": "create", "name": "test_dim_min", "dim": 1, "consistency": "Strong", "expected": "accept"},
        {"id": "dim_max", "op": "create", "name": "test_dim_max", "dim": 32768, "consistency": "Strong", "expected": "accept"},
        {"id": "dim_below_min", "op": "create", "name": "test_dim_bad", "dim": 0, "consistency": "Strong", "expected": "reject"},
        {"id": "dim_above_max", "op": "create", "name": "test_dim_bad2", "dim": 32769, "consistency": "Strong", "expected": "reject"},

        # 2. ConsistencyLevel enum
        {"id": "consistency_invalid", "op": "create", "name": "test_cons_bad", "dim": 128, "consistency": "INVALID_ENUM", "expected": "reject"},
        {"id": "consistency_empty", "op": "create", "name": "test_cons_empty", "dim": 128, "consistency": "", "expected": "reject_or_default"},
        {"id": "consistency_lower", "op": "create", "name": "test_cons_lower", "dim": 128, "consistency": "strong", "expected": "accept_or_reject"},

        # 3. MetricType enum (need to test against actual collection)
        # Skipping for now - would require creating a test collection first

        # 4. Limit bounds (query operations)
        # Skipping for now - would require actual data

        # 5. Nprobe bounds (search operations)
        # Skipping for now - would require actual data and vectors

        # 6. Required fields
        {"id": "missing_name", "op": "create", "name": "", "dim": 128, "consistency": "Strong", "expected": "reject"},
        {"id": "empty_name", "op": "create", "name": "", "dim": 128, "consistency": "Strong", "expected": "reject"},

        # 7. Load/drop non-existent collections
        {"id": "load_nonexist", "op": "load", "name": "nonexistent_collection", "expected": "reject"},
        {"id": "drop_nonexist", "op": "drop", "name": "nonexistent_collection2", "expected": "reject"},

        # 8. Describe non-existent collection
        {"id": "describe_nonexist", "op": "describe", "name": "nonexistent_collection3", "expected": "reject"},
    ]

    print(f"Loaded {len(probes)} probes")
    print()

    # Execute probes
    results = []
    api_accepted = 0

    for i, probe in enumerate(probes, 1):
        print(f"[{i}/{len(probes)}] Executing: {probe['id']}")

        result = {
            "probe_id": probe["id"],
            "api_accepted": False,
            "status_code": None,
            "error": None,
            "response": None
        }

        try:
            if probe["op"] == "create":
                data = {
                    "collectionName": probe["name"],
                    "dimension": probe["dim"],
                    "consistencyLevel": probe["consistency"]
                }
                response, status, error = milv_request("/collections/create", data)
                result["status_code"] = status
                result["response"] = response
                result["error"] = error
                result["api_accepted"] = status == 200

            elif probe["op"] == "load":
                data = {"collectionName": probe["name"]}
                response, status, error = milv_request(f"/collections/{probe['name']}/load", data)
                result["status_code"] = status
                result["response"] = response
                result["error"] = error
                result["api_accepted"] = status == 200

            elif probe["op"] == "drop":
                data = {"collectionName": probe["name"]}
                response, status, error = milv_request(f"/collections/{probe['name']}/drop", data)
                result["status_code"] = status
                result["response"] = response
                result["error"] = error
                result["api_accepted"] = status == 200

            elif probe["op"] == "describe":
                response, status, error = milv_request(f"/collections/{probe['name']}/describe", {}, method="GET")
                result["status_code"] = status
                result["response"] = response
                result["error"] = error
                result["api_accepted"] = status == 200

            if result["api_accepted"]:
                api_accepted += 1
                print(f"  -> API ACCEPTED (status {result['status_code']})")
            else:
                print(f"  -> API REJECTED (status {result['status_code']})")

        except Exception as e:
            result["error"] = str(e)
            print(f"  -> ERROR: {result['error']}")

        results.append(result)
        time.sleep(0.1)

    print()
    print("=" * 60)
    print("PHASE 1 COMPLETE: Probe Execution")
    print("=" * 60)
    print(f"Total probes: {len(probes)}")
    print(f"API accepted: {api_accepted}")
    print(f"API rejected: {len(probes) - api_accepted}")
    print()

    # Save results
    output = {
        "experiment": "single-LLM-with-source ablation",
        "arm": "P1-2 Round 8",
        "phase": "execution_complete",
        "total_probes": len(probes),
        "api_accepted": api_accepted,
        "api_rejected": len(probes) - api_accepted,
        "results": results
    }

    with open('TestVDB/scripts/p1_single_llm_source.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("Results saved to TestVDB/scripts/p1_single_llm_source.json")
    print()
    print("NEXT: Perform source-anchored judgment on accepted probes")

    return results, api_accepted

if __name__ == "__main__":
    main()