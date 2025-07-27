import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import lower, regexp_replace, col
from awsglue.context import GlueContext

# Init
glueContext = GlueContext(SparkContext.getOrCreate())
spark = glueContext.spark_session

# Load raw CSV from S3
input_path = "s3://sku-dedup-project/input/raw_products.csv"
df = spark.read.option("header", "true").csv(input_path)

# Normalize SKUs and product names
df_cleaned = df.withColumn("sku_normalized", lower(col("sku"))) \
               .withColumn("product_name_normalized", lower(regexp_replace(col("product_name"), "[^a-zA-Z0-9 ]", "")))

# Drop duplicates based on normalized values
df_deduped = df_cleaned.dropDuplicates(["sku_normalized", "product_name_normalized"])

# Save clean result
output_path = "s3://sku-dedup-project/output/clean_products/"
df_deduped.drop("sku_normalized", "product_name_normalized") \
          .coalesce(1) \
          .write.mode("overwrite").option("header", "true").csv(output_path)
