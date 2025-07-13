
import json, boto3
from datetime import datetime, timedelta

cw = boto3.client('cloudwatch')
sns = boto3.client('sns')

event_buffer = []

SNS_TOPIC_ARN = 'arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:PrimeDayPaymentAlerts'

def lambda_handler(event, context):
    global event_buffer
    now = datetime.utcnow()

    for record in event['Records']:
        try:
            payload = json.loads(record['kinesis']['data'], strict=False)
            ts = datetime.strptime(payload['timestamp'], "%Y-%m-%dT%H:%M:%S.%f%z").replace(tzinfo=None)
            status = payload['payment_status']
            event_buffer.append((ts, status))
        except Exception as e:
            print(f"Error parsing record: {e}")
            continue

    event_buffer = [(ts, s) for ts, s in event_buffer if (now - ts).total_seconds() < 60]

    total = len(event_buffer)
    fails = sum(1 for _, s in event_buffer if s == "FAIL")
    failure_rate = (fails / total) * 100 if total > 0 else 0

    print(f"Failure Rate: {failure_rate:.2f}%")

    cw.put_metric_data(
        Namespace='PrimeDay2025',
        MetricData=[{
            'MetricName': 'PaymentFailureRate',
            'Timestamp': now,
            'Value': failure_rate,
            'Unit': 'Percent'
        }]
    )

    if failure_rate > 2:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject='Payment Failure Alert',
            Message=f"Failure rate: {failure_rate:.2f}% at {now.isoformat()}"
        )

    return {'statusCode': 200}
