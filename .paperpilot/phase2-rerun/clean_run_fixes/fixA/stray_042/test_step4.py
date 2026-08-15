from pymilvus import MilvusClient
import json

client = MilvusClient(host='localhost', port='19530')

# Step 4: Falsification - verify data is NOT actually inserted with wrong type
print('=== STEP 4: FALSIFICATION ===')
try:
    # Clean collection
    client.drop_collection(collection_name='test_vec_str')
except:
    pass

# Create collection
client.create_collection(collection_name='test_vec_str', dimension=4)

# Try to insert with vector as string
print('Testing if data was actually inserted with wrong type...')
try:
    result = client.insert(
        collection_name='test_vec_str',
        data={'id': [0], 'vector': ['[0.1,0.2,0.3,0.4]']}
    )
    print(f'Insert succeeded: {result}')

    # Try to query back to see if data was stored
    query_result = client.query(
        collection_name='test_vec_str',
        filter='id == 0',
        output_fields=['id', 'vector']
    )
    print(f'Query result: {query_result}')

    # Check if we can actually search (this would fail if vector is corrupted)
    search_result = client.search(
        collection_name='test_vec_str',
        data=[[0.1, 0.2, 0.3, 0.4]],
        anns_field='vector',
        limit=5,
        output_fields=['id']
    )
    print(f'Search result: {search_result}')

except Exception as e:
    print(f'Operation failed (confirms type coercion is rejected): {e}')
