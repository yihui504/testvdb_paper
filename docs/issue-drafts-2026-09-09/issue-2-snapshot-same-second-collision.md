# Title
Two snapshots created within the same second share one name and the first is silently lost — both requests still return 200

# Body

## Current Behavior

Collection snapshot names carry only **second-resolution timestamps**
(`<collection>-<peer_id>-<YYYY-MM-DD-HH-MM-SS>.snapshot`). If two snapshots of
the same collection are created within the same second — easily done with
concurrent requests or a fast loop — both requests answer **HTTP 200 with an
identical `name`**, but only **one** archive exists: the second `store_file`
silently replaces the first (temp path `persist()` = rename-overwrite, no
existence check). The first snapshot the client was *told* exists is gone.

Measured on v1.19.1 and v1.18.0:

- concurrent pair: 5/5 trials produced the same name on both 200 responses,
  and `GET /collections/{c}/snapshots` listed 1 entry;
- sequential fast (no sleep, ~10 ms apart): 3 requests → 1 distinct name;
  when collection data differs between creates, the two 200 bodies carry
  **different checksums under the same name**, and the listing entry matches
  only the last one;
- spacing the creates >1.1 s apart yields distinct names (control) — so the
  second-resolution window is exactly the trigger.

The delete side behaves consistently (one delete of the shared name clears the
listing with no phantom), which confirms the loss happens at create time.

## Steps to Reproduce

1. Start standalone:

   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.19.1
   ```

2. Create a collection with a point:

   ```bash
   curl -X PUT http://localhost:6333/collections/test_col \
     -H 'Content-Type: application/json' \
     -d '{"vectors":{"size":4,"distance":"Euclid"}}'
   curl -X PUT 'http://localhost:6333/collections/test_col/points?wait=true' \
     -H 'Content-Type: application/json' \
     -d '{"points":[{"id":1,"vector":[1,0,0,0]}]}'
   ```

3. Fire two snapshot creates within one second:

   ```bash
   curl -s -X POST http://localhost:6333/collections/test_col/snapshots & \
   curl -s -X POST http://localhost:6333/collections/test_col/snapshots & wait
   ```

   Both responses: `"status":"ok"`, identical `"name"` values.

4. List snapshots:

   ```bash
   curl -s http://localhost:6333/collections/test_col/snapshots
   ```

   Only **one** entry — the other accepted snapshot no longer exists.

## Expected Behavior

Either:

1. every accepted creation is observable — e.g. make the final name unique the
   way the *temporary* archive file already is (`-arc-XXXX` suffix in the same
   function: sub-second timestamp, random suffix, or counter), or
2. a collision is refused with a 4xx/409 instead of silently overwriting an
   existing snapshot.

Returning 200 twice for one stored snapshot means the client's snapshot
inventory (and any backup pipeline built on it) silently loses a file it was
told was created.

## Possible Solution

In `lib/collection/src/collection/snapshots.rs` (`create_snapshot`), the name
is `format!("{}-{this_peer_id}-{}.snapshot", self.name(),
chrono::Utc::now().format("%Y-%m-%d-%H-%M-%S"))`. The temp file created right
below it already carries a unique `-arc-XXXX` suffix that is dropped at
persist time. Options: keep uniqueness in the final name (append a short
random suffix or microsecond precision), or add an existence check +
collision error before `store_file`. The same second-resolution format string
also appears in `shard_holder` and `content_manager` snapshot paths — worth
auditing together.

## Context (Environment)

- qdrant v1.19.1 (commit `6ab21cac`) and v1.18.0 (commit `db3fca3`),
  single-node standalone, Docker, REST API
- Impact: backup automation that takes multiple snapshots per second (or
  retries without backoff) silently loses snapshots while receiving 200 for
  all of them; the checksum mismatch under one name also makes the two faces
  of the API (create response vs listing) disagree about what exists
