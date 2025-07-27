import boto3, json
from datetime import datetime

s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb')
lambda_client = boto3.client('lambda')

BUCKET = 'siliconprimex-log-archive'
TABLE = 'SiliconPrimeX_Incidents'
RCA_LAMBDA = 'SiliconPrimeX_RCAEngine'  # Replace with actual RCA Lambda name

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    try:
        timestamp = datetime.utcnow().isoformat()
        detail = event.get('detail', {})
        job_id = detail.get('jobName', 'unknown')
        run_id = detail.get('jobRunId', 'unknown')
        state = detail.get('state', 'UNKNOWN')

        filename = f"logs/{timestamp}_{job_id}.json"

        # Save raw event to S3
        s3.put_object(
            Bucket=BUCKET,
            Key=filename,
            Body=json.dumps(event, indent=2)
        )
        print(f"Log saved to S3: {filename}")

        # Save summary to DynamoDB
        dynamo.put_item(
            TableName=TABLE,
            Item={
                'job_id': {'S': job_id},
                'timestamp': {'S': timestamp},
                'status': {'S': state},
                'raw_event': {'S': json.dumps(event)}
            }
        )
        print("✅ Event summary saved to DynamoDB")

        # 🧠 If the job FAILED, trigger RCA Lambda
        if state.upper() == "FAILED":
            print(" Job FAILED. Triggering RCA Engine Lambda...")
            lambda_client.invoke(
                FunctionName=RCA_LAMBDA,
                InvocationType='Event',
                Payload=json.dumps({'filename': filename})
            )
            print("📡 RCA Lambda invoked with filename.")

        return {"status": "success", "job_id": job_id, "triggered_rca": state.upper() == "FAILED"}

    except Exception as e:
        print(" ERROR:", str(e))
        return {"status": "error", "message": str(e)}
