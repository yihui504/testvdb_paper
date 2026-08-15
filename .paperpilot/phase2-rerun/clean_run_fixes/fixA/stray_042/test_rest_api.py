import requests
import json

# Step 1: Clean reproduction using REST API (not pymilvus)
print('=== STEP 1: CLEAN REPRO (REST API) ===')

base_url = "http://localhost:19530/v2/vectordb"

# Clean collection
response = requests.post(f"{base_url}/collections/drop", json={"collectionName": "test_vec_str", "dbName": "default"})
print(f'Drop collection: {response.status_code}')

# Create collection
response = requests.post(f"{base_url}/collections/create", json={"collectionName": "test_vec_str", "dimension": 4})
print(f'Create collection: {response.status_code} - {response.text}')

# Insert with vector as STRING (type coercion defect)
print('\nInserting vector as STRING: "[0.1,0.2,0.3,0.4]"')
payload = {
    "collectionName": "test_vec_str",
    "data": [{"id": 0, "vector": "[0.1,0.2,0.3,0.4]"}]
}
response = requests.post(f"{base_url}/entities/insert", json=payload)
print(f'Insert response: {response.status_code} - {response.text}')

if response.status_code == 200:
    result = response.json()
    print(f'Insert succeeded: {result}')
    print('TYPE COERCION ACCEPTED - BUG CONFIRMED')
else:
    print(f'Insert rejected - no type coercion bug')
