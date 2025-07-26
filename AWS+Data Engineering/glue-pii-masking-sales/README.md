# Masking PII in Sales Reports Using AWS Glue

## Scenario
Lets say we are working on a sales data platform at Amazon. Analysts need access to customer sales, but **personally identifiable information (PII)** like `email` and `phone` must be masked before sharing.

This project uses **AWS Glue** to transform and mask PII fields.

## Dataset Fields

- `customer_id`
- `name`
- `email` → masked
- `phone` → masked
- `region`
- `total_sales`

## Tech Stack

- **Amazon S3** — raw and masked data storage
- **AWS Glue** — masking logic (Spark job)
- **Athena** — query masked output
- **(Optional)** — Lake Formation for row/column-level permissions

## Glue PII Masking Logic
masked_df = df.withColumn("email", lit("***@***.com")) \
              .withColumn("phone", lit("**********"))

## Example Query in Athena
SELECT region, COUNT(*) AS total_customers, SUM(total_sales) AS revenue
FROM sales_masked
GROUP BY region;

## Outcomes

- GDPR/CCPA-compliant data sharing
- Secure access for analysts
- Reusable Glue ETL job
- Lightweight but production-grade masking layer
