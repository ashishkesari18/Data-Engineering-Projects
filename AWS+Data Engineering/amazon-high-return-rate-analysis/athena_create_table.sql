CREATE EXTERNAL TABLE refund_table (
  order_id STRING,
  order_date STRING,
  customer_id STRING,
  sku STRING,
  product_name STRING,
  category STRING,
  price STRING,
  return_flag STRING,
  return_reason STRING,
  warehouse STRING
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\'
)
STORED AS TEXTFILE
LOCATION 's3://refunddata.csv/refund_table/'
TBLPROPERTIES (
  'skip.header.line.count'='1'
);
