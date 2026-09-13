> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://api.qdrant.tech/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://api.qdrant.tech/_mcp/server.

# Search points

POST http://localhost:6333/collections/{collection_name}/points/search
Content-Type: application/json

Retrieves the closest points based on vector similarity and given filtering conditions.

Reference: https://api.qdrant.tech/v-1-12-x/api-reference/search/points

## Authentication

- `api-key` header (required)

## Servers

- `http://localhost:6333` (http, default)
- `https://localhost:6333` (https)

## Request

### Path parameters

- `collection_name` (string, required) — Name of the collection to search in

### Query parameters

- `consistency` (integer or enum, optional) — Define read consistency guarantees for the operation
- `timeout` (integer, optional) — If set, overrides global timeout for this request. Unit is seconds.

### Body (application/json)

- `vector` (list of double or object or object, required) — Vector data separator for named and unnamed modes Unnamed mode: \{ "vector": \[1.0, 2.0, 3.0] } or named mode: \{ "vector": \{ "vector": \[1.0, 2.0, 3.0], "name": "image-embeddings" } }
  - NamedVector
    - `name` (string, required) — Name of vector data
    - `vector` (list of double, required) — Vector data
  - NamedSparseVector
    - `name` (string, required) — Name of vector data
    - `vector` (object, required) — Sparse vector structure
      - `indices` (list of uint, required) — Indices must be unique
      - `values` (list of double, required) — Values and indices must be the same length
- `limit` (integer, required) — Max number of result to return
- `shard_key` (string or uint64 or list of string or uint64 or any, optional) — Specify in which shards to look for the points, if not specified - look in all shards
- `filter` (object or any, optional) — Look only for points which satisfies this conditions
  - Filter
    - `should` (object or object or object or object or object or object or list of object or object or object or object or object or object or any, optional) — At least one of those conditions should match
    - `min_should` (object or any, optional) — At least minimum amount of given conditions should match
      - MinShould
        - `conditions` (list of object or object or object or object or object or object, required)
          - FieldCondition
            - `key` (string, required) — Payload key
            - `match` (object or object or object or object or any, optional) — Check if point has field with a given value
            - `range` (object or object or any, optional) — Check if points value lies in a given range
            - `geo_bounding_box` (object or any, optional) — Check if points geo location lies in a given area
            - `geo_radius` (object or any, optional) — Check if geo point is within a given radius
            - `geo_polygon` (object or any, optional) — Check if geo point is within a given polygon
            - `values_count` (object or any, optional) — Check number of values of the field
          - IsEmptyCondition
            - `is_empty` (object, required) — Payload field
          - IsNullCondition
            - `is_null` (object, required) — Payload field
          - HasIdCondition
            - `has_id` (list of uint64 or string, required)
          - NestedCondition
            - `nested` (object, required) — Select points with payload for a specified nested field
        - `min_count` (integer, required)
    - `must` (object or object or object or object or object or object or list of object or object or object or object or object or object or any, optional) — All conditions must match
    - `must_not` (object or object or object or object or object or object or list of object or object or object or object or object or object or any, optional) — All conditions must NOT match
- `params` (object or any, optional) — Additional search params
  - SearchParams
    - `hnsw_ef` (integer, optional, nullable) — Params relevant to HNSW index Size of the beam in a beam-search. Larger the value - more accurate the result, more time required for search.
    - `exact` (boolean, optional, default: false) — Search without approximation. If set to true, search may run long but with exact results.
    - `quantization` (object or any, optional) — Quantization params
      - QuantizationSearchParams
        - `ignore` (boolean, optional, default: false) — If true, quantized vectors are ignored. Default is false.
        - `rescore` (boolean, optional, nullable) — If true, use original vectors to re-score top-k results. Might require more time in case if original vectors are stored on disk. If not set, qdrant decides automatically apply rescoring or not.
        - `oversampling` (double, optional, nullable) — Oversampling factor for quantization. Default is 1.0. Defines how many extra vectors should be pre-selected using quantized index, and then re-scored using original vectors. For example, if `oversampling` is 2.4 and `limit` is 100, then 240 vectors will be pre-selected using quantized index, and then top-100 will be returned after re-scoring.
    - `indexed_only` (boolean, optional, default: false) — If enabled, the engine will only perform search among indexed or small segments. Using this option prevents slow searches in case of delayed index, but does not guarantee that all uploaded vectors will be included in search results
- `offset` (integer, optional, nullable) — Offset of the first result to return. May be used to paginate results. Note: large offset values may cause performance issues.
- `with_payload` (boolean or list of string or object or object or any, optional) — Select which payload to return with the response. Default is false.
- `with_vector` (boolean or list of string or any, optional) — Options for specifying which vectors to include into response. Default is false.
- `score_threshold` (double, optional, nullable) — Define a minimal score threshold for the result. If defined, less similar results will not be returned. Score of the returned result might be higher or smaller than the threshold depending on the Distance function used. E.g. for cosine similarity only higher scores will be returned.

## Response

### 200

successful operation

- `time` (double, optional) — Time spent to process this request
- `status` (string, optional)
- `result` (list of object, optional)
  - `id` (uint64 or string, required) — Type, used for specifying point ID in user interface
  - `version` (uint64, required) — Point version
  - `score` (double, required) — Points vector distance to the query vector
  - `payload` (map from string to any or any, optional) — Payload - values assigned to the point
  - `vector` (list of double or list of list of double or map from string to list of double or object or list of list of double or object or object or any, optional) — Vector of the point
  - `shard_key` (string or uint64 or any, optional) — Shard Key
  - `order_value` (long or double or any, optional) — Order-by value

## Examples

**Request**

```json
{
  "vector": [
    1.1
  ],
  "limit": 1
}
```

**Response**

```json
{
  "time": 0.002,
  "status": "ok",
  "result": [
    {
      "id": 42,
      "version": 3,
      "score": 0.75,
      "payload": {},
      "vector": {},
      "shard_key": "region_1",
      "order_value": 42
    }
  ]
}
```

**SDK Code**

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.search(
    collection_name="{collection_name}",
    query_filter=models.Filter(
        must=[
            models.FieldCondition(
                key="city",
                match=models.MatchValue(
                    value="London",
                ),
            )
        ]
    ),
    query_vector=[0.2, 0.1, 0.9, 0.7],
    limit=3,
)

```

```go
package client

import (
	"context"
	"fmt"

	"github.com/qdrant/go-client/qdrant"
)

func search() {
	client, err := qdrant.NewClient(&qdrant.Config{
		Host: "localhost",
		Port: 6334,
	})
	if err != nil {
		panic(err)
	}

	limit := uint64(3)
	results, err := client.Query(context.Background(), &qdrant.QueryPoints{
		CollectionName: "{collection_name}",
		Query:          qdrant.NewQuery(0.2, 0.1, 0.9, 0.7),
		Filter: &qdrant.Filter{
			Must: []*qdrant.Condition{
				qdrant.NewMatch("city", "London"),
			},
		},
		Limit: &limit,
	})
	if err != nil {
		panic(err)
	}
	fmt.Println("Results: ", results)
}

```

```java
import static io.qdrant.client.ConditionFactory.matchKeyword;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;

import io.qdrant.client.grpc.Points.Filter;
import io.qdrant.client.grpc.Points.SearchPoints;

QdrantClient client = new QdrantClient(
                QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client
    .searchAsync(
        SearchPoints.newBuilder()
            .setCollectionName("{collection_name}")
            .setFilter(Filter.newBuilder().addMust(matchKeyword("city", "London")).build())
            .addAllVector(List.of(0.2f, 0.1f, 0.9f, 0.7f))
            .setLimit(3)
            .build())
    .get();

```

```csharp
using Qdrant.Client;
using static Qdrant.Client.Grpc.Conditions;

var client = new QdrantClient("localhost", 6334);

await client.SearchAsync(
  collectionName: "{collection_name}",
  vector: new float[] { 0.2f, 0.1f, 0.9f, 0.7f },
  filter: MatchKeyword("city", "London"),
  limit: 3
);

```

```typescript
import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.search("{collection_name}", {
    filter: {
        must: [
            {
                key: "city",
                match: {
                    value: "London",
                },
            },
        ],
    },
    vector: [0.2, 0.1, 0.9, 0.7],
    limit: 3,
});

```

```rust
use qdrant_client::qdrant::{Condition, Filter, SearchParamsBuilder, SearchPointsBuilder};
use qdrant_client::Qdrant;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
    .search_points(
        SearchPointsBuilder::new("{collection_name}", vec![0.2, 0.1, 0.9, 0.7], 3)
            .filter(Filter::must([Condition::matches(
                "city",
                "London".to_string(),
            )]))
            .params(SearchParamsBuilder::default().hnsw_ef(128).exact(false)),
    )
    .await?;

```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:6333/collections/collection_name/points/search")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Post.new(url)
request["api-key"] = '<apiKey>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"vector\": [\n    1.1\n  ],\n  \"limit\": 1\n}"

response = http.request(request)
puts response.read_body
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'http://localhost:6333/collections/collection_name/points/search', [
  'body' => '{
  "vector": [
    1.1
  ],
  "limit": 1
}',
  'headers' => [
    'Content-Type' => 'application/json',
    'api-key' => '<apiKey>',
  ],
]);

echo $response->getBody();
```

```swift
import Foundation

let headers = [
  "api-key": "<apiKey>",
  "Content-Type": "application/json"
]
let parameters = [
  "vector": [1.1],
  "limit": 1
] as [String : Any]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:6333/collections/collection_name/points/search")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "POST"
request.allHTTPHeaderFields = headers
request.httpBody = postData as Data

let session = URLSession.shared
let dataTask = session.dataTask(with: request as URLRequest, completionHandler: { (data, response, error) -> Void in
  if (error != nil) {
    print(error as Any)
  } else {
    let httpResponse = response as? HTTPURLResponse
    print(httpResponse)
  }
})

dataTask.resume()
```