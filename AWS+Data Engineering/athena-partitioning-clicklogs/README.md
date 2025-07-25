# Project 8: Improving Athena Query Speed Using Partitioning 🚀

## Scenario

Let's say you are doing good as a Data Engineer But Analysts complain that querying click logs takes too long (~5 mins). Your job is to restructure the Athena table using **partitioning** to reduce scan time and cost.

## Dataset

Simulated click logs with:
- `event_date` (partition key 1)
- `region` (partition key 2)
- `user_id`
- `page`
- `timestamp`

## Before: Flat Table DDL (Slow)
CREATE EXTERNAL TABLE click_logs_flat (
  event_date DATE,
  region STRING,
  user_id STRING,
  page STRING,
  timestamp TIMESTAMP
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
LOCATION 's3://your-bucket/click_logs_flat/'
TBLPROPERTIES ('skip.header.line.count'='1');

## After: Partitioned Table DDL (Fast)
CREATE EXTERNAL TABLE click_logs_partitioned (
  user_id STRING,
  page STRING,
  timestamp TIMESTAMP
)
PARTITIONED BY (event_date DATE, region STRING)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES ('field.delim' = ',')
LOCATION 's3://your-bucket/click_logs_partitioned/'
TBLPROPERTIES ('skip.header.line.count'='1');

After upload, run:
MSCK REPAIR TABLE click_logs_partitioned;

## Sample Queries

**Unoptimized Query (flat table):**
SELECT COUNT(*) FROM click_logs_flat
WHERE region = 'Texas' AND event_date = DATE '2025-07-22';

**Optimized Query (partitioned table):**
SELECT COUNT(*) FROM click_logs_partitioned
WHERE region = 'Texas' AND event_date = DATE '2025-07-22';

## Outcome

- Query time drops from 5 min → under 10 sec
- Cost savings via less data scanned
- Amazon-level real ops impact

Built with ❤️ for the #100DaysOfAWSDataEngineering Challenge.
