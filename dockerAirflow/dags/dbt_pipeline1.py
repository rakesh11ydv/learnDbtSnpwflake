from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator


DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = DBT_PROJECT_DIR+"/profiles"


with DAG(
    dag_id="dbt_pipeline1",
    start_date=datetime(2025, 1, 1),
    schedule=None,   # manual trigger
    catchup=False,
    tags=["dbt", "snowflake"],
) as dag:

    dbt_debug = BashOperator(
        task_id="dbt_debug",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} &&
        dbt debug --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} &&
        dbt run --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command=f"""
        cd {DBT_PROJECT_DIR} &&
        dbt test --profiles-dir {DBT_PROFILES_DIR}
        """,
    )

    dbt_debug >> dbt_run >> dbt_test