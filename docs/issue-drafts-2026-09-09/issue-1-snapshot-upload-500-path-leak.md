# Title
Snapshot upload with a malformed or empty archive returns HTTP 500 (Service internal error) and leaks internal file paths

# Body

## Current Behavior

Uploading a file that is not a valid snapshot archive to
`POST /collections/{collection_name}/snapshots/upload` answers **HTTP 500**
instead of a client error:

- garbage bytes in the `snapshot` form field:

  ```json
  {"status":{"error":"Service internal error: File IO error: Malformed tar archive, reached unknown entry"},"time":0.0074}
  ```

- **empty (0-byte) file** in the `snapshot` form field — additionally discloses the server's internal filesystem layout:

  ```json
  {"status":{"error":"Service internal error: File IO error: failed to open file `/qdrant/./storage/tmp/col-<collection>-recovery-<random>/config.json`: No such file or directory (os error 2)"},"time":0.0081}
  ```

Both responses are deterministic (reproduced 3/3 and 3/3, and again on a
freshly created collection). The node itself is fine — `/healthz` stays 200,
collection state is untouched — so this is an error-classification problem,
not a crash.

For contrast, the *same endpoint* classifies other client mistakes correctly:
wrong form-field name → `400 Required field is missing "snapshot"` (v1.18.0
phrased it `Required field is missing: snapshot` — both 400), missing
Content-Type → `400 "Could not find Content-Type header"`. Only the
archive-decode stage escapes as a 5xx.

## Steps to Reproduce

1. Start a single-node standalone instance (no cluster needed):

   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.19.1
   ```

2. Create a collection and seed one point:

   ```bash
   curl -X PUT http://localhost:6333/collections/test_col \
     -H 'Content-Type: application/json' \
     -d '{"vectors":{"size":4,"distance":"Euclid"}}'

   curl -X PUT 'http://localhost:6333/collections/test_col/points?wait=true' \
     -H 'Content-Type: application/json' \
     -d '{"points":[{"id":1,"vector":[1,0,0,0]}]}'
   ```

3. Upload garbage bytes as the snapshot:

   ```bash
   printf 'GARBAGE-NOT-A-TAR' > bad.snapshot
   curl -i -X POST 'http://localhost:6333/collections/test_col/snapshots/upload?priority=snapshot' \
     -F 'snapshot=@bad.snapshot;type=application/octet-stream'
   ```

   → HTTP 500 with the "Malformed tar archive" body above.

4. Upload an empty file:

   ```bash
   : > empty.snapshot
   curl -i -X POST 'http://localhost:6333/collections/test_col/snapshots/upload?priority=snapshot' \
     -F 'snapshot=@empty.snapshot;type=application/octet-stream'
   ```

   → HTTP 500 with the internal-path-leak body above.

## Expected Behavior

A malformed/empty uploaded archive is a **client** error: the endpoint should
answer 4xx (like every other client mistake on this route) with the standard
`ErrorResponse` shape. The response body must never contain the server's
internal absolute paths (`/qdrant/./storage/tmp/col-...`).

## Possible Solution

The archive-decode path returns bare `std::io::Error`s which are converted by
the blanket `impl From<std::io::Error> for CollectionError`
(`lib/collection/src/operations/types.rs`, `File IO error: {err}`) into
`service_error` → HTTP 500:

- `lib/common/*/src/tar_unpack.rs` — malformed-tar io::Errors (this file
  already *deliberately* strips entry details in release builds to avoid
  leaking contents; the intent is documented in its comments);
- the recovery-config load (`config.rs` via `fs_err`) — the `failed to open
  file ...` message that leaks the path;
- the upload handler (`src/actix/api/snapshot_api.rs`) passes both through
  `error_handler` (`helpers.rs`), which maps `ServiceError` to 500.

Suggested: in the upload/recover boundary, map archive validation/decode
failures to `CollectionError::bad_request` (a 400 `ErrorResponse`), and route
the config-open failure through a message that does not embed the internal
path. The same file (`recover.rs`) already classifies checksum and config
incompatibility as `bad_input` 400s — extending that to decode failures is
consistent.

## Context (Environment)

- qdrant v1.19.1 (commit `6ab21cac`), single-node standalone, Docker, REST API
- Also reproduced on v1.18.0 (commit `db3fca3`); mechanism unchanged between versions
- Impact: clients cannot distinguish "my archive is broken" (retry won't help,
  fix the input) from "server is broken" (retry/alert); the empty-file case
  additionally discloses internal filesystem layout to any unauthenticated
  API caller (in default deployments without API-key)
