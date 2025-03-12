import boto3
import pandas as pd
import os

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    bucket_name = "amznproductdata"
    file_key = "marketing_sample_for_amazon_com-ecommerce__20200101_20200131__10k_data.csv"
    local_file_path = "/tmp/data.csv"
    output_file_path = "/tmp/processed_data.csv"

    try:
        # Download the file from S3
        s3_client.download_file(bucket_name, file_key, local_file_path)
        print("✅ File downloaded successfully!")

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(local_file_path)
        print(f"First 5 rows:\n{df.head()}")

        # Perform your data processing (example: clean data, filter rows, etc.)
        df_processed = df.dropna()  # Example: drop rows with missing values

        # Save the processed DataFrame back to CSV
        df_processed.to_csv(output_file_path, index=False)
        print("✅ Data processed successfully!")

        # Upload the processed file back to a different S3 location
        output_bucket = "amznproductdata"
        output_key = "processed/processed_data.csv"
        s3_client.upload_file(output_file_path, output_bucket, output_key)
        print(f"✅ Processed file uploaded to {output_bucket}/{output_key}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}

    return {"statusCode": 200, "body": "Processing and upload complete"}
