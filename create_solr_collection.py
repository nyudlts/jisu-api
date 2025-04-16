import requests

SOLR_URL = "http://solr:8983/solr/admin/collections"
SOLR_COLLECTION = "bookCollection"
PARAMS = {
    "action": "CREATE",
    "name": SOLR_COLLECTION,
    "numShards": "1",
    "collection.configName": "_default"
}

try:
    response = requests.get(SOLR_URL, params=PARAMS)
    response.raise_for_status()  # Raise an error for bad responses
    print(f"✅ Solr collection {SOLR_COLLECTION} created successfully.")
except requests.exceptions.RequestException as e:
    print("❌ Error creating Solr collection:", e)
