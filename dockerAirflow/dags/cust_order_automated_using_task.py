from datetime import datetime

from airflow import DAG
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator


def snowflakeTask(task_id, sql):
    return SQLExecuteQueryOperator(
        task_id=task_id,
        conn_id="snowflake_connect",
        sql=sql
    )


with DAG(
        dag_id="dbt_customer_orders_automated",
        start_date=datetime(2026, 5, 4),
        schedule=None,
        catchup=None,
        template_searchpath=[
            "/opt/airflow/sql",
            "/opt/airflow/streamSql"
        ]  # mounted to - learnSnowflake folder in repo
) as dag:
    setup_db = snowflakeTask("setup_db", "1_db_setup.sql")

    create_src_tables = snowflakeTask("create_src_tables", "create_source_table.sql")

    create_tgt_tables = snowflakeTask("create_tgt_tables", "create_target_table.sql")

    create_stream = snowflakeTask("create_stream", "create_stream.sql")

    auto_refresh_task = snowflakeTask("auto_refresh_task", "create_task_auto_loading.sql")

    setup_db >> create_src_tables >> create_tgt_tables >> create_stream >> auto_refresh_task
