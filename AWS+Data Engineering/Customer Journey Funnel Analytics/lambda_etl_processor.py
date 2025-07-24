import json
import datetime
import random

def lambda_handler(event, context):
    enriched_events = []
    for record in event['Records']:
        payload = json.loads(record['body'])  # Simulate Kinesis event
        payload['processed_at'] = datetime.datetime.utcnow().isoformat()
        payload['device_type'] = random.choice(['mobile', 'desktop', 'tablet'])
        enriched_events.append(payload)

    # Simulate write to S3 or downstream
    print("Processed and enriched events:", enriched_events)
    return {"statusCode": 200, "body": "Events processed successfully."}
