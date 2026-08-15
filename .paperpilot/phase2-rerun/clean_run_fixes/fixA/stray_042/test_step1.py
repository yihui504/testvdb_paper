from pymilvus import MilvusClient
import json

client = MilvusClient(host='localhost', port='19530')

# Step 1: Clean reproduction with minimal request
# Recreate the exact issue: vector as string instead of array
print('=== STEP 1: CLEAN REPRO ===')
try:
    # Clean collection
    client.drop_collection(collection_name='test_vec_str', db_name='default')
except:
    pass

# Create collection
client.create_collection(collection_name='test_vec_str', dimension=4)

# Insert with vector as STRING (type coercion defect)
print('Inserting vector as STRING: "[0.1,0.2,0.3,0.4]"')
try:
    result = client.insert(
        collection_name='test_vec_str',
        data={'id': [0], 'vector': ['[0.1,0.2,0.3,0.4]']}
    )
    print(f'Insert result: {result}')
    print('Type coercion ACCEPTED - bug confirmed')
except Exception as e:
    print(f'Insert failed (expected): {e}')
