import json
import requests

# UPDATE THIS with your actual endpoint (DO NOT include a trailing slash)
ES_ENDPOINT = "https://search-prime-slot-search-vb6sbv5555dxh2fxjf6uef5rti.us-east-1.es.amazonaws.com"
INDEX = "delivery_options"
AUTH = ("admin", "Admin@123")  # Username and password from fine-grained access

# Step 1: Create the index with a mapping
mapping = {
    "mappings": {
        "properties": {
            "product_id": { "type": "keyword" },
            "zip_code": { "type": "keyword" },
            "delivery_slot": { "type": "date" },
            "stock": { "type": "integer" }
        }
    }
}

print("Creating index...")
res = requests.put(f"{ES_ENDPOINT}/{INDEX}", auth=AUTH, json=mapping)
print("Index response:", res.status_code, res.text)

# Step 2: Upload delivery slot data
with open("delivery_data.json") as f:
    data = json.load(f)
    for doc in data:
        r = requests.post(f"{ES_ENDPOINT}/{INDEX}/_doc", auth=AUTH, json=doc)
        print("Upload:", r.status_code, r.text)
