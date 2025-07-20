import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, when
from pyspark.sql import functions as F

# AWS Glue boilerplate
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Load Silver data
silver_df = spark.read.option("header", "true").csv("s3://athenax-bronze-layer/silver/")

# Clean and enrich data
gold_df = silver_df.withColumn("high_potential_flag", when(col("avg_leadership_score") >= 3.5, "yes").otherwise("no")) \
                   .withColumn("promotion_ready_flag", when((col("completed_mentorships") >= 2) & 
                                                           (col("last_promotion_status") != "promoted"), "yes").otherwise("no"))

# Write to Gold Layer
gold_df.write.mode("overwrite").option("header", "true").csv("s3://athenax-bronze-layer/gold/")