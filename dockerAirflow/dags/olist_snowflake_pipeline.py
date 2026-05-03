from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

def print_role(**context):
    result = context['ti'].xcom_pull(task_ids='check_role')
    print("Current Role:", result)

def upload_files_to_stage() -> None:
    hook = SnowflakeHook(snowflake_conn_id="snowflake_connect")
    conn = hook.get_conn()
    cursor = conn.cursor()

    files = [
        "olist_customers_dataset.csv",
        "olist_orders_dataset.csv",
    ]

    try:
        for file_name in files:
            cursor.execute(
                f"""
                PUT file:///opt/airflow/srcData/{file_name}
                @LEARN_DB.RAW.OLIST_INTERNAL_STAGE
                AUTO_COMPRESS=FALSE
                OVERWRITE=TRUE;
                """
            )
    finally:
        cursor.close()
        conn.close()


with DAG(
    dag_id="olist_snowflake_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    template_searchpath=["/opt/airflow/sql"]
) as dag:
    check_role = SQLExecuteQueryOperator(
        task_id="check_role",
        conn_id="snowflake_connect",
        sql="SELECT CURRENT_ROLE();",
        do_xcom_push=True
    )

    print_role_task = PythonOperator(
        task_id="print_role",
        python_callable=print_role
    )

    create_database = SQLExecuteQueryOperator(
        task_id="create_database",
        conn_id="snowflake_default",
        sql="CREATE DATABASE IF NOT EXISTS LEARN_DB;",
    )

    create_stage = SQLExecuteQueryOperator(
        task_id="create_stage",
        conn_id="snowflake_default",
        sql="createStage.sql",
    )

    upload_to_stage = PythonOperator(
        task_id="upload_to_stage",
        python_callable=upload_files_to_stage,
    )

    create_tables = SQLExecuteQueryOperator(
        task_id="create_tables",
        conn_id="snowflake_default",
        sql="createTables.sql",
    )

    load_tables = SQLExecuteQueryOperator(
        task_id="load_tables",
        conn_id="snowflake_default",
        sql="copyIntoTablesFromStage.sql",
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/dbt &&
        dbt run --profiles-dir /opt/airflow/dbt/profiles
        """,
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/dbt &&
        dbt test --profiles-dir /opt/airflow/dbt/profiles
        """,
    )

    (
        check_role
        >> print_role_task
        >> create_database
        >> create_stage
        >> upload_to_stage
        >> create_tables
        >> load_tables
        >> dbt_run
        >> dbt_test
    )

