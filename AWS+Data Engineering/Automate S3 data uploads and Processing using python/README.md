# AWS Lambda-Based S3 Data Processing Pipeline

## 🚀 Project Overview
This project automates the processing of CSV files uploaded to an **Amazon S3 bucket** using **AWS Lambda**. The Lambda function reads the data, processes it using **Pandas**, and stores the cleaned version in a separate S3 bucket.

## 🏗️ Architecture Flow
1️⃣ **User Uploads CSV File** → **Amazon S3 (Raw Data Bucket)**  
2️⃣ **S3 Event Triggers AWS Lambda**  
3️⃣ **Lambda Downloads & Processes CSV** using Pandas  
4️⃣ **Lambda Saves Processed Data** → **Amazon S3 (Processed Data Bucket)**  
5️⃣ **Logs Execution** → **Amazon CloudWatch**  

## 📂 Project Structure
```
📁 my_lambda_function/
├── lambda_function.py    # Main Lambda function script
├── README.md             # Project documentation
```
└── 

## 🛠️ Setup Instructions

### 1️⃣ Prerequisites
Ensure you have the following installed:
- **Python 3.x**
- **AWS CLI** (Configured with IAM role access to S3, Lambda, and CloudWatch)
- **Boto3 & Pandas** (For handling AWS services and data processing)

### 2️⃣ Local Development Setup
```sh
# Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3️⃣ Deploy Lambda Function
#### Option 1: Upload Code as ZIP
```sh
# Install dependencies inside the package directory
pip install -r requirements.txt -t .

# Create a ZIP package
zip -r function.zip .

# Upload function.zip to AWS Lambda via AWS Console or CLI
```
#### Option 2: Upload to S3 & Deploy
```sh
aws s3 cp function.zip s3://lambdafnctnupld/
```
Then, update the Lambda function to use this ZIP from S3.

### 4️⃣ Configure S3 Event Trigger
- Go to **AWS S3 Console** → Select the **Raw Data Bucket**
- Under **Properties**, configure an **Event Notification**
- Set the event trigger as **Object Created (All Events)**
- Set destination to **AWS Lambda Function**

### 5️⃣ Test the Function
1. Upload a sample CSV file to the **S3 raw data bucket**
2. Check **AWS CloudWatch Logs** for Lambda execution details
3. Verify processed CSV in the **S3 processed data bucket**

## 🔍 Example Lambda Function Code
```python
import boto3
import pandas as pd

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    
    # Download file
    s3_client.download_file(bucket_name, file_key, '/tmp/input.csv')
    df = pd.read_csv('/tmp/input.csv')
    
    # Data processing (Example: Display first 5 rows)
    print(df.head())
    
    # Save processed data
    output_bucket = 'processed-amazon-data'
    df.to_csv('/tmp/processed_data.csv', index=False)
    s3_client.upload_file('/tmp/processed_data.csv', output_bucket, 'processed_data.csv')
    
    return {'statusCode': 200, 'body': 'Processing Complete'}
```

## 📊 Monitoring & Logs
- **AWS CloudWatch**: View logs for debugging and performance monitoring.
- **AWS Lambda Metrics**: Monitor execution time, memory usage, and errors.

## 🎯 Future Enhancements
✅ Integrate with **AWS Glue** for automated ETL pipelines.  
✅ Use **Amazon Athena** for querying processed data directly.  
✅ Implement **SNS notifications** for successful processing alerts.  

---
📢 **Author:** Ashish Kesari 
🚀 **#AWS #Lambda #S3 #DataEngineering**
