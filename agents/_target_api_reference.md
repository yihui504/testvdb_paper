# Target API Reference

## safe_request() Wrapper Definition

All HTTP calls must use the `safe_request()` wrapper. It returns a three-tuple `(status_code, body, raw_text)`.

```python
import os
import requests
import json

BASE_URL = os.environ.get("TESTVDB_DB_URL")
if not BASE_URL:
    print("VERDICT: SCRIPT_ERROR — TESTVDB_DB_URL not set")
    sys.exit(2)

def safe_request(method, endpoint, json=None, timeout=10):
    """
    Safe HTTP request wrapper with unified error handling.
    Returns: (status_code, body, raw_text)
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.request(
            method=method,
            url=url,
            json=json,
            headers=headers,
            timeout=timeout
        )
        status_code = response.status_code
        raw_text = response.text

        try:
            body = response.json()
        except:
            body = raw_text

        return status_code, body, raw_text
    except Exception as e:
        return -1, str(e), str(e)
```

## DB-Specific API Selection Guide

### chroma
- **SDK**: `chromadb.HttpClient` (SDK-first)
- **REST**: REST v1 is deprecated
- **Preferred**: chromadb.HttpClient with HTTP mode

### milvus
- **REST API**: v2 (`/v2/vectordb/`)
- **SDK**: pymilvus only for dynamic schema operations
- **Preferred**: REST API for standard operations

### qdrant / weaviate / meilisearch
- **Preferred**: REST API via `requests` library

### pgvector
- **Preferred**: psycopg2 SQL

## Script Cleanup Requirements

All teardown operations must be wrapped in try/except:

```python
try:
    client.delete_collection("test_collection")
except Exception:
    pass  # cleanup failures are non-fatal
```

## Response Key Patterns

Each DB has different response structures. Extract results dynamically:

- **chroma**: body.get("results") or body.get("ids")
- **milvus**: body.get("data") or body.get("results")
- **qdrant**: body.get("result") or body.get("results")
- **weaviate**: body.get("data", {}).get("Get")
- **meilisearch**: body.get("hits")
