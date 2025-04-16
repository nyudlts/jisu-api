import requests
import json

#SOLR_HOST = os.getenv("SOLR_HOST", "http://localhost:8983")
#http://localhost:8983/api/collections/bookCollection/schema

# Define Solr URL
SOLR_URL = "http://solr:8983/api/collections/bookCollection/schema"

# Define JSON payload
payload = {
    "add-field": [
        {
            "name": "href",
            "type": "string",
            "stored": True,
            "indexed": True
        },
        {
            "name": "content",
            "type": "text_general",
            "stored": True,
            "indexed": True
        },
        {
            "name": "chars",
            "type": "pint",  # Ensure "pint" is a valid Solr type
            "stored": True,
            "indexed": True
        },
        {
            "name": "chapterTitle",
            "type": "string",
            "stored": True,
            "indexed": True
        },
        {
            "name": "bookTitle",
            "type": "string",
            "stored": True,
            "indexed": True
        },
        {
            "name": "bookID",
            "type": "string",
            "stored": True,
            "indexed": True
        }
    ]
}

# Set headers
headers = {
    "Content-Type": "application/json"
}

# Send POST request
try:
    response = requests.post(SOLR_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
    print("✅ Solr schema update successful.")
except requests.exceptions.RequestException as e:
    print("❌ Error updating pk schema:", e)
