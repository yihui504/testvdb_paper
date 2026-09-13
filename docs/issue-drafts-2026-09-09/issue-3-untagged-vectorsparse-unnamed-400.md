# Title
Malformed sparse vector gets a generic "untagged enum VectorStruct" 400 that names neither the field nor the point (unlike validation-layer 422s)

# Body

## Current Behavior

On `PUT /collections/{c}/points`, several malformed **sparse vector** shapes
are rejected with a 400 whose message contains no actionable location
information:

```json
{"status":{"error":"Format error in JSON body: data did not match any variant of untagged enum VectorStruct"}}
```

Legs that produce it (each its own request):

| request vector | problem | response |
|---|---|---|
| `{"sparse":{"indices":[1,2]}}` | missing required `values` | 400, no field named |
| `{"sparse":{"values":[0.5]}}` | missing required `indices` | 400, no field named |
| `{"sparse":{"indices":[-1],"values":[0.5]}}` | negative index (uint32 min 0) | 400, no field named |
| `{"sparse":{"indices":[1.5],"values":[0.5]}}` | float index | 400, no field named |
| `{"sparse":{"indices":[18446744073709551616],"values":[0.5]}}` | out of u64 range | 400, no field named |

On a batch with many points, nothing indicates **which point** or **which
sub-field** failed — the client has to bisect its own payload to find out.

The same endpoint *does* produce precise messages once a request survives
deserialization, e.g. duplicate indices and length mismatch:

```json
{"status":{"error":"Validation error in JSON body: [points[0].vector.?.indices: Validation error: must be unique [{}]]"}}
{"status":{"error":"Validation error in JSON body: [points[0].vector.?.values: Validation error: must be the same length as indices [{}]]"}}
```

So the split is structural: the serde (untagged-enum) layer gives a generic
fallthrough message that discards every per-variant failure reason, while the
validation layer names point index, field and rule. (The `?.` placeholder in
the 422 path is a separate small quirk: the named-vector slot renders as `?`
instead of the actual vector name.)

## Steps to Reproduce

1. Start standalone:

   ```bash
   docker run -p 6333:6333 qdrant/qdrant:v1.19.1
   ```

2. Create a collection and send a sparse vector missing `values`:

   ```bash
   curl -X PUT http://localhost:6333/collections/test_col \
     -H 'Content-Type: application/json' \
     -d '{"vectors":{"size":4,"distance":"Euclid"}}'

   curl -i -X PUT 'http://localhost:6333/collections/test_col/points?wait=true' \
     -H 'Content-Type: application/json' \
     -d '{"points":[{"id":1,"vector":{"sparse":{"indices":[1,2]}}}]}'
   ```

   → 400 `data did not match any variant of untagged enum VectorStruct`.

3. Contrast — duplicate indices (validation layer, names everything):

   ```bash
   curl -i -X PUT 'http://localhost:6333/collections/test_col/points?wait=true' \
     -H 'Content-Type: application/json' \
     -d '{"points":[{"id":1,"vector":{"sparse":{"indices":[1,1],"values":[0.5,0.5]}}}]}'
   ```

   → 422 `points[0].vector.?.indices: must be unique`.

## Expected Behavior

A 400 for a malformed vector should say at least which field is missing or
wrong (e.g. `points[0].vector: missing field 'values'` style), consistent with
the precision the validation layer already provides. Serde rejection quality is
the only diagnostic a client gets for shape mistakes.

## Possible Solution

`VectorStruct` (`lib/api/src/rest/schema.rs`) is `#[serde(untagged)]`, and
serde's untagged fallthrough replaces all per-variant errors with one generic
message (`serde_derive/src/de.rs`, untagged-enum branch). Improvements that
keep the wire format:

- `#[serde(expecting = "expected a dense array, {name: array}, {name: {indices, values}}, ...")]`
  on the enum (static, but far better than the current message), or
- a custom `Deserialize` (or deserialize-into-`serde_json::Value` then convert)
  that accumulates per-variant reasons and reports the closest match's failure.

## Context (Environment)

- qdrant v1.19.1 (commit `6ab21cac`) and v1.18.0 (commit `db3fca3`), Docker
  standalone, REST API
- Related: other `#[serde(untagged)]` enums in the API surface show the same
  pattern (e.g. the `with_lookup` style fallthrough messages) — this issue
  documents it specifically for the sparse-vector domain, where the
  required-field mistakes are the most likely user errors. SparseVector's own
  schema (`indices` unique, `values` same length, uint32) is documented; these
  legs violate it and get zero guidance from the response.
