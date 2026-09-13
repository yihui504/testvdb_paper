> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://api.qdrant.tech/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://api.qdrant.tech/_mcp/server.

# Upsert points

PUT http://localhost:6333/collections/{collection_name}/points
Content-Type: application/json

Performs the insert + update action on specified points. Any point with an existing \{id} will be overwritten.

Reference: https://api.qdrant.tech/v-1-12-x/api-reference/points/upsert-points

## Authentication

- `api-key` header (required)

## Servers

- `http://localhost:6333` (http, default)
- `https://localhost:6333` (https)

## Request

### Path parameters

- `collection_name` (string, required) — Name of the collection to update from

### Query parameters

- `wait` (boolean, optional) — If true, wait for changes to actually happen
- `ordering` (enum, optional) — define ordering guarantees for the operation
  - Allowed values: `weak`, `medium`, `strong`

### Body (application/json)

- `object or object`
  - PointsBatch
    - `batch` (object, required)
      - `ids` (list of uint64 or string, required)
      - `vectors` (list of list of double or list of list of list of double or map from string to list of list of double or object or list of list of double or object or list of object, required)
      - `payloads` (list of map from string to any or any, optional, nullable)
    - `shard_key` (string or uint64 or list of string or uint64 or any, optional)
  - PointsList
    - `points` (list of object, required)
      - `id` (uint64 or string, required) — Type, used for specifying point ID in user interface
      - `vector` (list of double or list of list of double or map from string to list of double or object or list of list of double or object or object, required) — Full vector data per point separator with single and multiple vector modes
        - Document
          - `text` (string, required) — Text of the document This field will be used as input for the embedding model
          - `model` (string, optional, nullable) — Name of the model used to generate the vector List of available models depends on a provider
      - `payload` (map from string to any or any, optional) — Payload values (optional)
    - `shard_key` (string or uint64 or list of string or uint64 or any, optional)

## Response

### 200

successful operation

- `time` (double, optional) — Time spent to process this request
- `status` (string, optional)
- `result` (object, optional)
  - `status` (enum, required) — `Acknowledged` - Request is saved to WAL and will be process in a queue. `Completed` - Request is completed, changes are actual.
    - Allowed values: `acknowledged`, `completed`
  - `operation_id` (uint64, optional, nullable) — Sequential number of the operation

## Examples

**Request**

```json
{
  "batch": {
    "ids": [
      42
    ],
    "vectors": {}
  }
}
```

**Response**

```json
{
  "time": 0.002,
  "status": "ok",
  "result": {
    "status": "acknowledged",
    "operation_id": 1
  }
}
```

**SDK Code**

```python
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")

client.upsert(
    collection_name="{collection_name}",
    points=[
        models.PointStruct(
            id=1,
            payload={
                "color": "red",
            },
            vector=[0.9, 0.1, 0.1],
        ),
        models.PointStruct(
            id=2,
            payload={
                "color": "green",
            },
            vector=[0.1, 0.9, 0.1],
        ),
        models.PointStruct(
            id=3,
            payload={
                "color": "blue",
            },
            vector=[0.1, 0.1, 0.9],
        ),
    ],
)

```

```go
package client

import (
	"context"
	"fmt"

	"github.com/qdrant/go-client/qdrant"
)

func upsert() {
	client, err := qdrant.NewClient(&qdrant.Config{
		Host: "localhost",
		Port: 6334,
	})
	if err != nil {
		panic(err)
	}

	response, err := client.Upsert(context.Background(), &qdrant.UpsertPoints{
		CollectionName: "{collection_name}",
		Points: []*qdrant.PointStruct{
			{
				Id:      qdrant.NewIDNum(1),
				Vectors: qdrant.NewVectors(0.9, 0.1, 0.1),
				Payload: qdrant.NewValueMap(map[string]any{
					"color": "red",
				}),
			},
			{
				Id:      qdrant.NewIDNum(2),
				Vectors: qdrant.NewVectors(0.1, 0.9, 0.1),
				Payload: qdrant.NewValueMap(map[string]any{
					"color": "green",
				}),
			},
			{
				Id:      qdrant.NewIDNum(3),
				Vectors: qdrant.NewVectors(0.1, 0.1, 0.9),
				Payload: qdrant.NewValueMap(map[string]any{
					"color": "blue",
				}),
			},
		},
	})
	if err != nil {
		panic(err)
	}
	fmt.Println("Upsert status: ", response.GetStatus())
}

```

```java
import static io.qdrant.client.PointIdFactory.id;
import static io.qdrant.client.VectorFactory.vector;
import static io.qdrant.client.VectorsFactory.namedVectors;

import java.util.List;
import java.util.Map;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;

import io.qdrant.client.grpc.Points.PointStruct;

QdrantClient client = new QdrantClient(
                QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client
    .upsertAsync(
        "{collection_name}",
        List.of(
            PointStruct.newBuilder()
                .setId(id(1))
                .setVectors(
                    namedVectors(
                        Map.of(
                            "image",
                            vector(List.of(0.9f, 0.1f, 0.1f, 0.2f)),
                            "text",
                            vector(List.of(0.4f, 0.7f, 0.1f, 0.8f, 0.1f, 0.1f, 0.9f, 0.2f)))))
                .build(),
            PointStruct.newBuilder()
                .setId(id(2))
                .setVectors(
                    namedVectors(
                        Map.of(
                            "image",
                            List.of(0.2f, 0.1f, 0.3f, 0.9f),
                            "text",
                            List.of(0.5f, 0.2f, 0.7f, 0.4f, 0.7f, 0.2f, 0.3f, 0.9f))))
                .build()))
    .get();

```

```csharp
using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.UpsertAsync(
  collectionName: "{collection_name}",
  points: new List<PointStruct>
  {
    new()
    {
      Id = 1,
      Vectors = new[] { 0.9f, 0.1f, 0.1f },
      Payload = { ["city"] = "red" }
    },
    new()
    {
      Id = 2,
      Vectors = new[] { 0.1f, 0.9f, 0.1f },
      Payload = { ["city"] = "green" }
    },
    new()
    {
      Id = 3,
      Vectors = new[] { 0.1f, 0.1f, 0.9f },
      Payload = { ["city"] = "blue" }
    }
  }
);

```

```typescript
import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.upsert("{collection_name}", {
  points: [
    {
      id: 1,
      payload: { color: "red" },
      vector: [0.9, 0.1, 0.1],
    },
    {
      id: 2,
      payload: { color: "green" },
      vector: [0.1, 0.9, 0.1],
    },
    {
      id: 3,
      payload: { color: "blue" },
      vector: [0.1, 0.1, 0.9],
    },
  ],
});

```

```rust
use qdrant_client::qdrant::{PointStruct, UpsertPointsBuilder};
use qdrant_client::{Qdrant, Payload};
use serde_json::json;

let client = Qdrant::from_url("http://localhost:6334").build()?;

client
    .upsert_points(
        UpsertPointsBuilder::new(
            "{collection_name}",
            vec![
                PointStruct::new(
                    1,
                    vec![0.9, 0.1, 0.1],
                    Payload::try_from(json!(
                        {"color": "red"}
                    ))
                    .unwrap(),
                ),
                PointStruct::new(
                    2,
                    vec![0.1, 0.9, 0.1],
                    Payload::try_from(json!(
                        {"color": "green"}
                    ))
                    .unwrap(),
                ),
                PointStruct::new(
                    3,
                    vec![0.1, 0.1, 0.9],
                    Payload::try_from(json!(
                        {"color": "blue"}
                    ))
                    .unwrap(),
                ),
            ],
        )
        .wait(true),
    )
    .await?;

```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:6333/collections/collection_name/points")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Put.new(url)
request["api-key"] = '<apiKey>'
request["Content-Type"] = 'application/json'
request.body = "{\n  \"batch\": {\n    \"ids\": [\n      42\n    ],\n    \"vectors\": {}\n  }\n}"

response = http.request(request)
puts response.read_body
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('PUT', 'http://localhost:6333/collections/collection_name/points', [
  'body' => '{
  "batch": {
    "ids": [
      42
    ],
    "vectors": {}
  }
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
let parameters = ["batch": [
    "ids": [42],
    "vectors": []
  ]] as [String : Any]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:6333/collections/collection_name/points")! as URL,
                                        cachePolicy: .useProtocolCachePolicy,
                                    timeoutInterval: 10.0)
request.httpMethod = "PUT"
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