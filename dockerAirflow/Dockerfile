FROM apache/airflow:3.2.1

USER root

RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow

RUN pip install --no-cache-dir dbt-core dbt-snowflake