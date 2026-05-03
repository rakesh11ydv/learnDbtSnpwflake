from airflow import DAG
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime


def upload_files_to_stage():
    hook = SnowflakeHook(snowflake_conn_id="snowflake_default")
    conn = hook.get_conn()
    cursor = conn.cursor()

    files = [
        "olist_customers_dataset.csv",
        "olist_orders_dataset.csv"
    ]

    for file in files:
        cursor.execute(
            f"""
            PUT file:///opt/airflow/data/{file}
            @OLIST_DB.RAW.OLIST_INTERNAL_STAGE
            AUTO_COMPRESS=FALSE
            OVERWRITE=TRUE;
            """
        )

    cursor.close()


with DAG(
    dag_id="olist_snowflake_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False
) as dag:

    create_database = SnowflakeOperator(
        task_id="create_database",
        snowflake_conn_id="snowflake_default",
        sql="/opt/airflow/sql/create_database.sql"
    )

    create_stage = SnowflakeOperator(
        task_id="create_stage",
        snowflake_conn_id="snowflake_default",
        sql="/opt/airflow/sql/create_stage.sql"
    )

    upload_to_stage = PythonOperator(
        task_id="upload_to_stage",
        python_callable=upload_files_to_stage
    )

    create_tables = SnowflakeOperator(
        task_id="create_tables",
        snowflake_conn_id="snowflake_default",
        sql="/opt/airflow/sql/create_tables.sql"
    )

    load_tables = SnowflakeOperator(
        task_id="load_tables",
        snowflake_conn_id="snowflake_default",
        sql="/opt/airflow/sql/copy_into.sql"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="""
        cd /opt/airflow/dbt/olist_dbt_project &&
        dbt run
        """
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="""
        cd /opt/airflow/dbt/olist_dbt_project &&
        dbt test
        """
    )

    (
        create_database
        >> create_stage
        >> upload_to_stage
        >> create_tables
        >> load_tables
        >> dbt_run
        >> dbt_test
    )