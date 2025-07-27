CREATE EXTERNAL TABLE IF NOT EXISTS clean_products (
  product_id STRING,
  sku STRING,
  product_name STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  "separatorChar" = ",",
  "quoteChar" = "\"",
  "escapeChar" = "\\"
)
STORED AS TEXTFILE
LOCATION 's3://sku-dedup-project/output/clean_products/'
TBLPROPERTIES (
  "skip.header.line.count"="1"
);
