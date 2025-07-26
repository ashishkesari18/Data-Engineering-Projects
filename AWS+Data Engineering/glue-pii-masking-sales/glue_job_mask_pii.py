import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import lit

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

datasource = glueContext.create_dynamic_frame.from_options(
    format_options={"withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={"paths": ["s3://your-bucket/sales_raw/"], "recurse": True}
)

df = datasource.toDF()

masked_df = df.withColumn("email", lit("***@***.com")) \
              .withColumn("phone", lit("**********"))

masked_dyf = glueContext.create_dynamic_frame.from_dataframe(masked_df, glueContext)

glueContext.write_dynamic_frame.from_options(
    frame=masked_dyf,
    connection_type="s3",
    format="csv",
    connection_options={"path": "s3://your-bucket/sales_masked/", "partitionKeys": []}
)

job.commit()
