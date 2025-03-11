# Query Large Amazon Reviews Dataset on AWS S3 using Athena

## 📌 Overview
This project demonstrates how to query large datasets stored in Amazon S3 using AWS Athena, a serverless interactive query service that enables SQL queries on structured data.

## 🚀 Steps to Follow

### 1️⃣ Upload Dataset to S3
- Download the dataset from Kaggle: [Amazon Reviews Dataset](https://www.kaggle.com/datasets/kritanjalijain/amazon-reviews?resource=download)
- Extract the dataset and upload `test.csv` (or `train.csv` if needed) to an S3 bucket.
- Ensure the S3 bucket has the correct permissions.

### 2️⃣ Create AWS Athena Table
Run the following query in AWS Athena to create an external table:
```sql
CREATE EXTERNAL TABLE amazon_reviews (
    label INT,
    title STRING,
    review TEXT
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION 's3://your-bucket-name/';
```

### 3️⃣ Run SQL Queries
- Count total records:
```sql
SELECT COUNT(*) FROM amazon_reviews;
```
- Fetch the first 10 reviews:
```sql
SELECT * FROM amazon_reviews LIMIT 10;
```
- Find the most common words in reviews:
```sql
SELECT word, COUNT(*) as count 
FROM (SELECT explode(split(review, ' ')) AS word FROM amazon_reviews)
GROUP BY word 
ORDER BY count DESC
LIMIT 10;
```

## 📌 Prerequisites
- An AWS account with access to S3 and Athena.
- A properly configured IAM role with `AmazonAthenaFullAccess` and `AmazonS3ReadOnlyAccess` permissions.
- AWS CLI installed (optional for managing S3 uploads).

## 🔥 Results & Insights
Using AWS Athena, we can analyze large datasets efficiently without setting up infrastructure. The SQL queries provide insights into customer sentiments, common review words, and more.


## 📢 Conclusion
This project showcases the power of AWS Athena for analyzing large-scale datasets in minutes! 🚀 Feel free to modify the queries and explore deeper insights. 🎯
