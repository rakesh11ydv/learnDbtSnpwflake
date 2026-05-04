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
        dag_id="dbt_customer_orders",
        start_date=datetime(2026, 5, 4),
        schedule=None,
        catchup=None,
        template_searchpath=[
            "/opt/airflow/sql",
            "/opt/airflow/sql/streams"
        ]  # mounted to - learnSnowflake folder in repo
) as dag:
    setup_db = snowflakeTask("setup_db", "1_db_setup.sql")

    create_src_tables = snowflakeTask("create_src_tables", "create_source_table.sql")

    create_tgt_tables = snowflakeTask("create_tgt_tables", "create_target_table.sql")

    create_stream = snowflakeTask("create_stream", "create_stream.sql")

    change_in_source = snowflakeTask("change_in_source", "change_in_source.sql")

    update_customer_orders_stg = snowflakeTask("update_customer_orders_stg", "update_customer_orders_stg.sql")
    auto_refresh_task = snowflakeTask("auto_refresh_task", "create_task_auto_loading.sql")

    (
            setup_db
            >> create_src_tables
            >> create_tgt_tables
            >> create_stream
            >> change_in_source
            >> update_customer_orders_stg

            [change_in_source, update_customer_orders_stg] >> auto_refresh_task
    )
