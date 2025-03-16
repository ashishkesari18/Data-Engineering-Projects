import boto3
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

# AWS DynamoDB Connection
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)
table = dynamodb.Table("WalmartAisles")

# API Key for Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# API URL for Google Gemini
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

# Request Model
class AisleRequest(BaseModel):
    product: str
    store_id: str

@app.get("/get_aisle")
async def get_aisle(product: str, store_id: str):
    product = product.lower()

    #**Check DynamoDB Cache**
    try:
        response = table.get_item(Key={"store_id": store_id, "product": product})
        if "Item" in response:
            return {"store_id": store_id, "product": product, "aisle": response["Item"]["aisle"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying DynamoDB: {str(e)}")

    # **Ask Google Gemini to Determine Aisle**
    try:
        prompt = {
            "contents": [
                {"parts": [{"text": f"Provide ONLY the Walmart aisle number (e.g., A3, B7, C10) where '{product}' is located in store {store_id}. STRICTLY NO EXPLANATION, JUST THE AISLE NUMBER."}]}
            ]
        }

        gemini_response = requests.post(GEMINI_URL, json=prompt)
        gemini_response.raise_for_status()
        gemini_data = gemini_response.json()

        aisle_info = gemini_data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()

        # Ensure response is valid (e.g., A3, B7, C10)
        if not aisle_info or not (aisle_info[0].isalpha() and aisle_info[1:].isdigit()):
            raise HTTPException(status_code=500, detail="Invalid aisle format from Gemini")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error querying Google Gemini API: {str(e)}")

    # **Store in DynamoDB (Cache)**
    try:
        table.put_item(Item={"store_id": store_id, "product": product, "aisle": aisle_info})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error storing data in DynamoDB: {str(e)}")

    return {"store_id": store_id, "product": product, "aisle": aisle_info}
