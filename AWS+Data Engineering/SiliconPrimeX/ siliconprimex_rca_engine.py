import json, boto3, urllib.request
from datetime import datetime
import traceback

# AWS Clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('glue_rca_logs')

# Constants
BUCKET = 'siliconprimex-log-archive'
GEMINI_API_KEY = '*******'
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    try:
        # Validate input
        if 'filename' not in event:
            raise ValueError("Missing 'filename' in event payload.")
        
        filename = event['filename']
        print(f"📁 Fetching log file from S3: {filename}")

        # Get log file from S3
        response = s3.get_object(Bucket=BUCKET, Key=filename)
        log_data = response['Body'].read().decode('utf-8')
        print("Log content retrieved successfully.")

        # Build prompt
        prompt = f"""
You are an expert AWS Glue Engineer.

Analyze the following AWS Glue job failure log and return an RCA with these sections:

1. **Root Cause Summary** – Clearly explain why the job failed and which code line caused it.
2. **Suggested Fix (Code or Configuration)** – Provide actual code or settings needed to fix the issue.
3. **Patch Recommendation** – Recommend a specific WorkerType and NumberOfWorkers in *both* formats below:
    - Example: "Use G.2X with 3 workers"
    - And include a JSON code block:
      ```json
      {{
        "WorkerType": "G.2X",
        "NumberOfWorkers": 3
      }}
      ```

Log:
{log_data}
        """

        # Gemini API request
        headers = {"Content-Type": "application/json"}
        payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")

        print("Sending RCA request to Gemini...")
        req = urllib.request.Request(GEMINI_URL, data=payload, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))

        # Extract RCA message
        try:
            message = result['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError) as parse_err:
            raise ValueError(f"Gemini response format error: {parse_err}")

        print("Gemini RCA Response:", message)

        # Store in DynamoDB
        job_id = filename.split('_')[-1].replace('.json', '')
        timestamp = datetime.utcnow().isoformat()

        table.put_item(
            Item={
                'job_id': job_id,
                'timestamp': timestamp,
                'rca_summary': message,
                'status_code': 200,
                's3_filename': filename
            }
        )
        print("RCA saved to DynamoDB.")

        return {
            'statusCode': 200,
            'filename': filename,
            'rca_summary': message
        }

    except Exception as e:
        print("ERROR OCCURRED:")
        traceback.print_exc()
        return {
            'statusCode': 500,
            'error': str(e)
        }
