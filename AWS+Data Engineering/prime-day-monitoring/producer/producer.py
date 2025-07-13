
import boto3, json, random, time
from datetime import datetime, timezone

stream_name = "payment-events-stream"
kinesis = boto3.client('kinesis')

def generate_event():
    return {
        "transaction_id": f"txn_{random.randint(1000,9999)}",
        "user_id": f"u{random.randint(10000,99999)}",
        "payment_status": random.choices(["SUCCESS", "FAIL"], weights=[97, 3])[0],
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "device": random.choice(["mobile", "desktop"]),
        "region": random.choice(["US-WEST", "US-EAST", "EU-WEST"])
    }

while True:
    for _ in range(10):
        payload = json.dumps(generate_event())
        print(payload)
        kinesis.put_record(StreamName=stream_name, Data=payload, PartitionKey="pk1")
    time.sleep(1)
