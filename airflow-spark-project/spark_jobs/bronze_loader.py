from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("bronze-loader") \
    .getOrCreate()

df = spark.read.option("header", True).csv("/opt/airflow/data/raw/customers.csv")

df.write.mode("overwrite").parquet("/opt/airflow/data/bronze/customers")

spark.stop()
