import boto3
import json

lambda_client = boto3.client('lambda')

with open('test_events.json') as f:
    events = json.load(f)

for i, event in enumerate(events):
    print(f"\n Test #{i+1}: Sending for {event['customer_name']} ({event['language_code']})...")
    
    response = lambda_client.invoke(
        FunctionName='multilingualOrderNotifier', 
        InvocationType='RequestResponse',
        Payload=json.dumps(event)
    )
    
    result = json.load(response['Payload'])
    print(f"Success: {result['message']}")
