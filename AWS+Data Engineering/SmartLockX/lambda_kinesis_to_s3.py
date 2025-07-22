import base64
import boto3
import json
import uuid
import datetime

s3 = boto3.client("s3")
bucket_name = "smartlockx-unlock-events-raw"

def lambda_handler(event, context):
    for record in event['Records']:
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(payload)
        
        # Optional: Add server-side ingestion timestamp
        data["ingested_at"] = datetime.datetime.utcnow().isoformat()
        
        # Save each event as a separate JSON file
        filename = f"{data['timestamp'].split('T')[0]}/event_{uuid.uuid4()}.json"
        
        s3.put_object(
            Bucket=bucket_name,
            Key=filename,
            Body=json.dumps(data)
        )
        print(f"Stored event to S3: {filename}")
