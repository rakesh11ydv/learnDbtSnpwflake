docker compose -f .\docker-compose-localExecutor-automated.yaml build

docker compose -f .\docker-compose-localExecutor-automated.yaml up airflow-init

docker compose -f .\docker-compose-localExecutor-automated.yaml up -d

docker exec -it dockerairflow-airflow-scheduler-1 bash
  airflow dags reserialize
  airflow connections get snowflake_default