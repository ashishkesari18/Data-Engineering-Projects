import boto3
import json
from boto3.dynamodb.conditions import Key

# DynamoDB table
DYNAMODB_TABLE = "slot_availability"

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(DYNAMODB_TABLE)
    
    # Incoming search results (from OpenSearch)
    delivery_candidates = event.get("candidates", [])

    final_results = []
    
    for candidate in delivery_candidates:
        product_id = candidate["product_id"]
        delivery_slot = candidate["delivery_slot"]
        
        response = table.get_item(
            Key={
                "product_id": product_id,
                "delivery_slot": delivery_slot
            }
        )
        
        status = response.get("Item", {}).get("status", "not available")
        
        final_results.append({
            "product_id": product_id,
            "delivery_slot": delivery_slot,
            "status": status
        })
    
    return {
        "statusCode": 200,
        "body": json.dumps(final_results)
    }
