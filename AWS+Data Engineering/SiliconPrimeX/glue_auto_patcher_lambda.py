import json, boto3, re
from boto3.dynamodb.conditions import Key

# AWS clients
glue = boto3.client('glue')
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

# Constants
TABLE_NAME = 'glue_rca_logs'
SNS_TOPIC_ARN = '*********'

def lambda_handler(event, context):
    print("🚀 Triggered SiliconPrimeX_GlueAutoPatcher")

    job_id = event.get('job_id')
    if not job_id:
        return {"statusCode": 400, "error": "Missing job_id in event"}

    try:
        # 1. Look up RCA from DynamoDB
        table = dynamodb.Table(TABLE_NAME)
        response = table.query(
            KeyConditionExpression=Key('job_id').eq(job_id),
            ScanIndexForward=False,
            Limit=1
        )
        items = response.get('Items', [])

        # Fallback: try shortened job ID
        if not items and "_" in job_id:
            fallback_id = job_id.split('_')[-1]
            print(f"Trying fallback job_id: {fallback_id}")
            response = table.query(
                KeyConditionExpression=Key('job_id').eq(fallback_id),
                ScanIndexForward=False,
                Limit=1
            )
            items = response.get('Items', [])

        if not items:
            raise Exception(f"No RCA found for job_id: {job_id}")

        item = items[0]
        rca = item.get('rca_summary', '')
        print("RCA Summary Found")

        # Extract suggested fix (first code block inside RCA)
        suggested_fix = extract_suggested_fix(rca)

        # 2. Extract patch info
        worker_type, num_workers = extract_patch(rca)
        if not worker_type or not num_workers:
            raise Exception("Could not extract WorkerType/NumberOfWorkers from RCA")

        print(f"🛠️ Patch to apply: WorkerType={worker_type}, Workers={num_workers}")

        # 3. Fetch Role & Command from Glue job
        job_details = glue.get_job(JobName=job_id)['Job']
        role = job_details['Role']
        command = job_details['Command']

        # 4. Update Glue job
        glue.update_job(
            JobName=job_id,
            JobUpdate={
                'WorkerType': worker_type,
                'NumberOfWorkers': num_workers,
                'Role': role,
                'Command': command
            }
        )
        print("Glue job patched successfully.")

        # 5. Send success SNS
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=f"SiliconPrimeX Patch Applied: {job_id}",
            Message=f"""Glue job: {job_id}
Patch Applied:

RCA Summary:
{rca}

Suggested Fix:
{suggested_fix}

Patch Applied:
WorkerType = {worker_type}
NumberOfWorkers = {num_workers}
"""
        )

        return {
            "statusCode": 200,
            "message": f"Patch applied to Glue job: {job_id}",
            "worker_type": worker_type,
            "number_of_workers": num_workers
        }

    except Exception as e:
        print(f" ERROR: {e}")
        try:
            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject=f"SiliconPrimeX Patch Failed: {job_id}",
                Message=f"""Glue job: {job_id}
Patch Applied:

Error:
{e}

RCA Summary (if any):
{rca if 'rca' in locals() else 'Not Found'}

Suggested Fix:
{suggested_fix if 'suggested_fix' in locals() else 'Not Available'}
"""
            )
        except Exception as sns_err:
            print(" Failed to send SNS alert:", sns_err)

        return {
            "statusCode": 500,
            "error": str(e)
        }

def extract_patch(rca_text):
    match1 = re.search(r"(G\.\d+X).*?(\d+)\s+workers", rca_text, re.IGNORECASE)
    if match1:
        return match1.group(1).upper(), int(match1.group(2))

    match2 = re.search(r'"WorkerType"\s*:\s*"(.+?)"', rca_text)
    match3 = re.search(r'"NumberOfWorkers"\s*:\s*(\d+)', rca_text)
    if match2 and match3:
        return match2.group(1).upper(), int(match3.group(1))

    return None, None

def extract_suggested_fix(rca_text):
    """Extract first Python code block from the RCA (suggested fix)"""
    match = re.search(r'```python(.*?)```', rca_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "Not found in RCA"
