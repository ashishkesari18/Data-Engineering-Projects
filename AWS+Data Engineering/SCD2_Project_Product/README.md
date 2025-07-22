
# 🛍️ Amazon-Scale SCD Type 2 Pipeline for Product Catalog

Track all historical changes to product details (like price, title, image) using a production-grade Slowly Changing Dimension (SCD) Type 2 implementation on AWS.

---

## Scenario

Product details change frequently — prices adjust, titles are revised, images get replaced. For auditability, financial accuracy, and legal traceability, it's essential to retain a full history of those changes.

---

## Business Problem Solved

- Enables **rollback** on accidental product updates
- Ensures **audit trails** for price fluctuations
- Supports **BI and legal compliance**
s
## AWS Services Used

- **Amazon S3** – Store product files (`v1`, `v2`, etc.)
- **AWS Glue** – PySpark job to compare product versions and apply SCD2 logic
- **Amazon Redshift Serverless** – Store full product history and current state
- **(Optional)**: Amazon QuickSight for visualization


## What Is SCD Type 2?

SCD Type 2 keeps full **historical versions** of records. When a tracked attribute (like price) changes:
- The old version is marked `is_current = false`
- A new version is inserted with a new `valid_from` date


## Redshift Table Schema
CREATE TABLE product_catalog_scd2 (
    surrogate_key INT IDENTITY(1,1),
    product_id INT,
    product_name VARCHAR(255),
    price DECIMAL(10,2),
    image_url VARCHAR(255),
    valid_from DATE,
    valid_to DATE,
    is_current BOOLEAN
);

## Glue SCD2 Logic Summary

1. Load new product version from S3
2. Load existing data from Redshift
3. Detect changes using joins
4. Mark old rows as `is_current = false`, set `valid_to`
5. Insert updated row with `is_current = true`, new `valid_from`

## What You Can Do With This Project

- Build it on **AWS Free Tier**
- Demo it in **interviews and portfolios**
- Extend it to include **inventory, promotions, or reviews**
