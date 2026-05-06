from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="spark_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False
) as dag:

    bronze = BashOperator(
        task_id="bronze_load",
        bash_command="""
spark-submit --master spark://spark-master:7077 /opt/airflow/spark_jobs/bronze_loader.py
"""
    )

    bronze
