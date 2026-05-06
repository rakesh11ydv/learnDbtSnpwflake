# Airflow + Spark Local Pipeline

## Run
```bash
docker compose up --build
```

Airflow UI: http://localhost:8080  
Spark UI: http://localhost:8081  

## Project flow
Raw CSV -> Bronze parquet via PySpark job triggered from Airflow.
