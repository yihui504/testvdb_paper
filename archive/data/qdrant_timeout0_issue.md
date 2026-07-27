**Title:** Write operations accept `timeout=0` despite the OpenAPI schema declaring `minimum: 1`

## Current Behavior

Write operations (e.g. `/collections/{collection_name}/points/payload`) accept `timeout=0` as a query parameter and return HTTP 200 with `"status":"ok"`. The OpenAPI specification for the same endpoint declares `timeout` as `{"type": "integer", "minimum": 1}`, so the server accepts a value its own schema forbids.

## Steps to Reproduce

1. Start Qdrus v1.18.2:
   ```
   docker run -p 6333:6333 qdrant/qdrant:v1.18.2
   ```
2. Create a collection and insert a point:
   ```
   curl -X PUT http://localhost:6333/collections/test_timeout \
     -H 'Content-Type: application/json' \
     -d '{"vectors":{"size":4,"distance":"Cosine"}}'

   curl -X PUT http://localhost:6333/collections/test_timeout/points \
     -H 'Content-Type: application/json' \
     -d '{"points":[{"id":1,"vector":[0.1,0.2,0.3,0.4]}]}'
   ```
3. Call a write operation with `timeout=0` (forbidden by the schema):
   ```
   curl -X POST 'http://localhost:6333/collections/test_timeout/points/payload?timeout=0' \
     -H 'Content-Type: application/json' \
     -d '{"payload":{"x":1},"points":[1]}'
   ```
4. Observed: HTTP 200, `{"result":{"operation_id":1,"status":"completed"},"status":"ok",...}`

For comparison, the same call with `timeout=1` (the documented minimum) also returns 200, so `timeout=0` is treated the same as a valid value rather than being rejected.

The same behavior appears on other write endpoints whose OpenAPI parameter is `timeout` with `minimum: 1` (e.g. delete points, create collection, update vectors).

## Expected Behavior

Either:
- The server rejects `timeout=0` with a 422 validation error, matching the OpenAPI schema (`minimum: 1`); **or**
- `timeout=0` is intended to mean "do not wait for commit" / non-blocking, in which case the OpenAPI schema should be updated to `minimum: 0` (or documented as such) so the contract matches the implementation.

## Possible Solution

If `timeout=0` is a valid "no-wait" semantics: update the OpenAPI `timeout` schema from `minimum: 1` to `minimum: 0` and document the `0` semantics in the parameter description.

If `timeout=0` is not intended: add server-side validation for the `timeout` query parameter consistent with the schema (`minimum: 1`), returning 422 for out-of-range values.

## Context (Environment)

- Qdrant version: v1.18.2 (Docker image `qdrant/qdrant:v1.18.2`)
- Deployment: single Docker container on `localhost:6333`
- API: REST, query parameter `timeout` on write operations
- Discovery method: API conformance testing against the OpenAPI specification

## Detailed Description

The OpenAPI specification (v1.18) declares the `timeout` query parameter as `{"type": "integer", "minimum": 1}` on every write endpoint (e.g. set payload, delete points, create collection, update vectors), with descriptions such as "Wait for operation commit timeout in seconds." This is a machine-readable contract that API consumers (and conformance-test tools such as Schemathesis) rely on.

The server does not enforce this constraint: `timeout=0` is accepted on write operations in v1.18.2. This is a doc/code (schema/code) discrepancy — either a validation gap in the server or an inaccuracy in the schema. Either way, the published contract and the runtime behavior disagree, which can mislead clients that trust the schema.

## Possible Implementation

Server-side: validate the `timeout` query parameter against the declared `minimum: 1` and return a 422 for values below it; or relax the schema to `minimum: 0` if `0` carries valid "no-wait" semantics.
