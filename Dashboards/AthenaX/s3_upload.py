import boto3

bucket_name = 'athenax-bronze-layer'  
file_path = 'athenax_hr_signals.csv'
key = 'bronze/athenax_hr_signals.csv'

s3 = boto3.client('s3')

try:
    s3.upload_file(file_path, bucket_name, key)
    print(f"File uploaded to s3://{bucket_name}/{key}")
except Exception as e:
    print(f"Upload failed: {e}")