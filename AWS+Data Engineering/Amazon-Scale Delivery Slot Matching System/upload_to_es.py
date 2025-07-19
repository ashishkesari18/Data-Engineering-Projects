import requests
from requests.auth import HTTPBasicAuth
import json

ES_ENDPOINT = "https://search-prime-slot-search-vb6sbv5555dxh2fxjf6uef5rti.us-east-1.es.amazonaws.com"  # update with your real endpoint
INDEX = "delivery_options"
USERNAME = "admin"        # Default fine-grained user
PASSWORD = "Admin@123"  # You set this while creating OpenSearch

AUTH = HTTPBasicAuth(USERNAME, PASSWORD)

mapping = {
    "mappings": {
        "properties": {
            "product_id": {"type": "keyword"},
            "delivery_slot": {"type": "date"},
            "status": {"type": "keyword"}
        }
    }
}

print("Creating index...")
res = requests.put(f"{ES_ENDPOINT}/{INDEX}", auth=AUTH, json=mapping)
print("Index response:", res.status_code, res.text)

docs = [
    {"product_id": "P123", "delivery_slot": "2025-07-25T10:00:00", "status": "available"},
    {"product_id": "P234", "delivery_slot": "2025-07-25T10:00:00", "status": "not available"},
    {"product_id": "P345", "delivery_slot": "2025-07-26T14:00:00", "status": "available"}
]

for doc in docs:
    r = requests.post(f"{ES_ENDPOINT}/{INDEX}/_doc", auth=AUTH, json=doc)
    print("Upload:", r.status_code, r.text)
