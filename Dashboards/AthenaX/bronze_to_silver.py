import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql.functions import col, to_timestamp, year, month
from pyspark.sql.window import Window
from pyspark.sql import functions as F

# AWS Glue boilerplate
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = glueContext.create_job(args['JOB_NAME'])

# Load Bronze data
df = spark.read.option("header", "true").csv("s3://athenax-bronze-layer/bronze/")

# Convert timestamp to actual datetime
df = df.withColumn("timestamp", to_timestamp("timestamp"))

# 1: Aggregation for leadership_score per employee
leadership_scores = df.filter(df.signal_type == "leadership_score") \
    .withColumn("score", col("value").cast("double")) \
    .groupBy("employee_id") \
    .agg(F.avg("score").alias("avg_leadership_score"))

# 2: Count mentorship completions per employee
mentorships = df.filter((df.signal_type == "mentorship_completion") & (df.value == "completed")) \
    .groupBy("employee_id") \
    .agg(F.count("*").alias("completed_mentorships"))

# 3: Promotion status (latest record)
promotions = df.filter(df.signal_type == "promotion_flag") \
    .withColumn("row_num", F.row_number().over(Window.partitionBy("employee_id").orderBy(F.desc("timestamp")))) \
    .filter(col("row_num") == 1) \
    .select("employee_id", col("value").alias("last_promotion_status"))

# Join them
silver_df = leadership_scores.join(mentorships, on="employee_id", how="outer") \
    .join(promotions, on="employee_id", how="outer") \
    .fillna({"avg_leadership_score": 0, "completed_mentorships": 0, "last_promotion_status": "unknown"})

# Writing to Silver Layer
silver_df.write.mode("overwrite").option("header", "true").csv("s3://athenax-bronze-layer/silver/")

job.commit()
