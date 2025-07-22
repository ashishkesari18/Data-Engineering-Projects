import boto3
import json
import time
import random
from faker import Faker

fake = Faker()
kinesis = boto3.client('kinesis', region_name='us-east-1')  # Update region if needed

def generate_event():
    return {
        "event_id": fake.uuid4(),
        "timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "device_id": fake.mac_address(),
        "location": fake.city(),
        "status": random.choice(["success", "failure", "timeout"]),
        "delivery_agent": fake.name(),
        "delivery_type": random.choice(["in-home", "in-garage", "in-car"]),
        "attempt": random.randint(1, 3)
    }

def send_event():
    event = generate_event()
    response = kinesis.put_record(
        StreamName="smartlock-unlock-stream",
        Data=json.dumps(event),
        PartitionKey=event["device_id"]
    )
    print(f"Sent: {event['event_id']} | Status: {event['status']}")
    return response

if __name__ == "__main__":
    while True:
        send_event()
        time.sleep(2)  
