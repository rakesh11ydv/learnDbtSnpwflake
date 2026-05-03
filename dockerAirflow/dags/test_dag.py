from datetime import datetime
from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator

with DAG(
    dag_id="test_dag.py",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
) as dag:

    test_task = BashOperator(
        task_id="test_task",
        bash_command="echo hello airflow"
    )