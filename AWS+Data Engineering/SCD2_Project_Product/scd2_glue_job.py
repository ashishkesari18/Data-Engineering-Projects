
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, current_date

spark = SparkSession.builder.appName("SCD2 Job").getOrCreate()

df_new = spark.read.option("header", True).csv("s3://amazon-product-catalog-scd2/raw/product_catalog_v2.csv")

df_new = df_new.withColumn("price", col("price").cast("double")) \
               .withColumn("last_updated", col("last_updated").cast("date"))

jdbc_url = "jdbc:redshift://your-cluster.redshift.amazonaws.com:5439/dev"
connection_props = {
    "user": "your-user",
    "password": "your-password",
    "driver": "com.amazon.redshift.jdbc.Driver"
}

df_existing = spark.read.jdbc(jdbc_url, "product_catalog_scd2", properties=connection_props)
df_existing = df_existing.filter(col("is_current") == True)

df_joined = df_existing.alias("old").join(df_new.alias("new"), "product_id")

df_changed = df_joined.filter(
    (col("old.product_name") != col("new.product_name")) |
    (col("old.price") != col("new.price")) |
    (col("old.image_url") != col("new.image_url"))
)

df_expired = df_changed.select("old.surrogate_key").withColumn("valid_to", current_date()).withColumn("is_current", lit(False))

df_new_records = df_changed.select(
    col("new.product_id").alias("product_id"),
    col("new.product_name").alias("product_name"),
    col("new.price").alias("price"),
    col("new.image_url").alias("image_url"),
    col("new.last_updated").alias("valid_from")
).withColumn("valid_to", lit(None).cast("date")) \
 .withColumn("is_current", lit(True))

df_expired.write.jdbc(jdbc_url, "product_catalog_scd2", mode="append", properties=connection_props)
df_new_records.write.jdbc(jdbc_url, "product_catalog_scd2", mode="append", properties=connection_props)
