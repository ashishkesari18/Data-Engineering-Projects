# 🛒 Identifying Products with High Return Rates (Amazon Refund Data Project)

**Goal:** Identify SKUs with high return rates from Amazon refund data, grouped by category, with a breakdown of common return reasons.

## 📊 Business Use Case

Amazon sellers and category managers want to track products that are frequently returned due to quality issues, misfit, or defects. This can reduce shipping losses, improve seller feedback, and optimize restocking.

> We flag SKUs with a **return rate greater than 15%**, summarize return reasons, and group insights by product category.

---

## 🔧 Tech Stack

- **Amazon S3** — Raw CSV data storage
- **Amazon Athena** — Serverless SQL querying
- **AWS Glue SerDe** — For parsing CSV files
- *(Optional)*: Pandas / QuickSight for visualization

---

## 🧾 Sample Data

| order_id | order_date | customer_id | sku    | product_name        | category   | price  | return_flag | return_reason | warehouse |
|----------|------------|-------------|--------|---------------------|------------|--------|-------------|----------------|-----------|
| 1001     | 2025-04-01 | CUST743     | SKU130 | Fitness Tracker     | Health     | 132.83 | 0           | NaN            | SEA-1     |
| 1002     | 2025-04-15 | CUST637     | SKU123 | Wireless Mouse      | Electronics| 13.24  | 0           | NaN            | DFW-2     |
| 1003     | 2025-06-07 | CUST839     | SKU124 | LED Bulb            | Home       | 148.15 | 0           | NaN            | DFW-2     |

---

## 📁 Folder Structure

amazon-high-return-rate-analysis/
├── refund_data.csv # Sample dataset
├── athena_create_table.sql # DDL to create external table
├── athena_return_rate_query.sql # Business logic query
├── README.md # This documentation
└── project_summary.md # Optional business insight summary