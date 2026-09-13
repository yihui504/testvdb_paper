> For clean Markdown of any page, append .md to the page URL.
> For a complete documentation index, see https://api.qdrant.tech/llms.txt.
> For AI client integration (Claude Code, Cursor, etc.), connect to the MCP server at https://api.qdrant.tech/_mcp/server.

# Set payload

POST http://localhost:6333/collections/{collection_name}/points/payload
Content-Type: application/json

Sets payload values for specified points.

Reference: https://api.qdrant.tech/v-1-18-x/api-reference/points/set-payload

## Authentication

- `api-key` header (required)

## Servers

- `http://localhost:6333` (http, default)
- `https://localhost:6333` (https)

## Request

### Path parameters

- `collection_name` (string, required) — Name of the collection to set from

### Query parameters

- `wait` (boolean, optional) — If true, wait for changes to actually happen
- `ordering` (enum, optional) — define ordering guarantees for the operation
  - Allowed values: `weak`, `medium`, `strong`
- `timeout` (integer, optional) — Timeout for the operation

### Body (application/json)

- `payload` (map from string to any, required)
- `points` (list of uint64 or string, optional, nullable) — Assigns payload to each point in this list
- `filter` (object or any, optional) — Assigns payload to each point that satisfy this filter condition
  - Filter
    - `should` (object or object or object or object or object or object or object or list of object or object or object or object or object or object or object or any, optional) — At least one of those conditions should match
    - `min_should` (object or any, optional) — At least minimum amount of given conditions should match
      - MinShould
        - `conditions` (list of object or object or object or object or object or object or object, required)
          - FieldCondition
            - `key` (string, required) — Payload key
            - `match` (object or object or object or object or object or object or any, optional) — Check if point has field with a given value
            - `range` (object or object or any, optional) — Check if points value lies in a given range
            - `geo_bounding_box` (object or any, optional) — Check if points geolocation lies in a given area
            - `geo_radius` (object or any, optional) — Check if geo point is within a given radius
            - `geo_polygon` (object or any, optional) — Check if geo point is within a given polygon
            - `values_count` (object or any, optional) — Check number of values of the field
            - `is_empty` (boolean, optional, nullable) — Check that the field is empty, alternative syntax for `is_empty: "field_name"`
            - `is_null` (boolean, optional, nullable) — Check that the field is null, alternative syntax for `is_null: "field_name"`
          - IsEmptyCondition
            - `is_empty` (object, required) — Payload field
          - IsNullCondition
            - `is_null` (object, required) — Payload field
          - HasIdCondition
            - `has_id` (list of uint64 or string, required)
          - HasVectorCondition
            - `has_vector` (string, required)
          - NestedCondition
            - `nested` (object, required) — Select points with payload for a specified nested field
        - `min_count` (integer, required)
    - `must` (object or object or object or object or object or object or object or list of object or object or object or object or object or object or object or any, optional) — All conditions must match
    - `must_not` (object or object or object or object or object or object or object or list of object or object or object or object or object or object or object or any, optional) — All conditions must NOT match
- `shard_key` (string or uint64 or list of string or uint64 or object or any, optional)
- `key` (string, optional, nullable) — Assigns payload to each point that satisfy this path of property

## Response

### 200

successful operation

- `usage` (object or any, optional)
  - Usage
    - `hardware` (object or any, optional)
      - HardwareUsage
        - `cpu` (integer, required)
        - `payload_io_read` (integer, required)
        - `payload_io_write` (integer, required)
        - `payload_index_io_read` (integer, required)
        - `payload_index_io_write` (integer, required)
        - `vector_io_read` (integer, required)
        - `vector_io_write` (integer, required)
    - `inference` (object or any, optional)
      - InferenceUsage
        - `models` (map from string to object, required)
          - `tokens` (uint64, required)
- `time` (double, optional) — Time spent to process this request
- `status` (string, optional)
- `result` (object, optional)
  - `status` (enum, required) — `Acknowledged` - Request is saved to WAL and will be process in a queue. `Completed` - Request is completed, changes are actual. `WaitTimeout` - Request is waiting for timeout.
    - Allowed values: `acknowledged`, `completed`, `wait_timeout`
  - `operation_id` (uint64, optional, nullable) — Sequential number of the operation

## Examples

**Request**

```json
{}
```

**Response**

```json
{
  "usage": {
    "hardware": {
      "cpu": 1,
      "payload_io_read": 1,
      "payload_io_write": 1,
      "payload_index_io_read": 1,
      "payload_index_io_write": 1,
      "vector_io_read": 1,
      "vector_io_write": 1
    },
    "inference": {
      "models": {}
    }
  },
  "time": 0.002,
  "status": "ok",
  "result": {
    "status": "acknowledged",
    "operation_id": 1
  }
}
```

**SDK Code**

```csharp
using Qdrant.Client;
using Qdrant.Client.Grpc;

var client = new QdrantClient("localhost", 6334);

await client.SetPayloadAsync(
  collectionName: "{collection_name}",
  payload: new Dictionary<string, Value> { { "property1", "string" }, { "property2", "string" } },
  ids: new ulong[] { 0, 3, 10 }
);

```

```python
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")

client.set_payload(
    collection_name="{collection_name}",
    payload={
        "property1": "string",
        "property2": "string",
    },
    points=[0, 3, 10],
)

```

```rust
use qdrant_client::qdrant::{PointsIdsList, SetPayloadPointsBuilder};
use qdrant_client::{Qdrant, Payload};
use serde_json::json;

let client = Qdrant::from_url("http://localhost:6334").build()?;

let payload: Payload = json!({
    "property1": "string",
    "property2": "string",
})
.try_into()
.unwrap();

client
    .set_payload(
        SetPayloadPointsBuilder::new("{collection_name}", payload)
            .points_selector(PointsIdsList {
                ids: vec![0.into(), 3.into(), 10.into()],
            })
            .wait(true),
    )
    .await?;

```

```java
import static io.qdrant.client.PointIdFactory.id;
import static io.qdrant.client.ValueFactory.value;

import java.util.List;
import java.util.Map;

import io.qdrant.client.QdrantClient;
import io.qdrant.client.QdrantGrpcClient;

QdrantClient client = new QdrantClient(
                QdrantGrpcClient.newBuilder("localhost", 6334, false).build());

client
    .setPayloadAsync(
        "{collection_name}",
        Map.of("property1", value("string"), "property2", value("string")),
        List.of(id(0), id(3), id(10)),
        true,
        null,
        null)
    .get();

```

```go
package client

import (
	"context"
	"fmt"

	"github.com/qdrant/go-client/qdrant"
)

func setPayload() {
	client, err := qdrant.NewClient(&qdrant.Config{
		Host: "localhost",
		Port: 6334,
	})
	if err != nil {
		panic(err)
	}

	results, err := client.SetPayload(context.Background(), &qdrant.SetPayloadPoints{
		CollectionName: "{collection_name}",
		Payload: qdrant.NewValueMap(map[string]any{
			"property1": "string",
			"property2": "string",
		}),
		PointsSelector: qdrant.NewPointsSelector(qdrant.NewIDNum(0), qdrant.NewIDNum(3), qdrant.NewIDNum(10)),
	})
	if err != nil {
		panic(err)
	}
	fmt.Println("Results: ", results)
}

```

```typescript
import { QdrantClient } from "@qdrant/js-client-rest";

const client = new QdrantClient({ host: "localhost", port: 6333 });

client.setPayload("{collection_name}", {
  payload: {
    property1: "string",
    property2: "string",
  },
  points: [0, 3, 10],
});

```

```ruby
require 'uri'
require 'net/http'

url = URI("http://localhost:6333/collections/collection_name/points/payload")

http = Net::HTTP.new(url.host, url.port)

request = Net::HTTP::Post.new(url)
request["api-key"] = '<apiKey>'
request["Content-Type"] = 'application/json'
request.body = "{}"

response = http.request(request)
puts response.read_body
```

```php
<?php
require_once('vendor/autoload.php');

$client = new \GuzzleHttp\Client();

$response = $client->request('POST', 'http://localhost:6333/collections/collection_name/points/payload', [
  'body' => '{}',
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
let parameters = [] as [String : Any]

let postData = JSONSerialization.data(withJSONObject: parameters, options: [])

let request = NSMutableURLRequest(url: NSURL(string: "http://localhost:6333/collections/collection_name/points/payload")! as URL,
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