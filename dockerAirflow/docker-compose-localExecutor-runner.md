# Airflow Local Setup with Docker + dbt

This project runs Apache Airflow locally using Docker Compose with `LocalExecutor` and integrates dbt with Snowflake.

---

## Start Airflow

### 1. Stop existing containers

```bash
docker compose -f .\docker-compose-localExecutor.yaml down
```

To also remove volumes (fresh database reset):

```bash
docker compose -f .\docker-compose-localExecutor.yaml down -v
```

---

### 2. Initialize Airflow metadata database

Run Airflow initialization:

```bash
docker compose -f .\docker-compose-localExecutor.yaml up airflow-init
```

This step:
- creates Airflow metadata database tables
- initializes users/roles
- prepares required folders

---

### 3. Start Airflow services

Launch Airflow in detached mode:

```bash
docker compose -f .\docker-compose-localExecutor.yaml up -d
```

This starts:
- Airflow API server
- Scheduler
- Postgres

---

## Refresh Scheduler After DAG Changes

Open scheduler container:

```bash
docker exec -it dockerairflow-airflow-scheduler-1 bash
```

Reserialize DAGs:

```bash
airflow dags reserialize
```

This forces Airflow to reload DAG metadata.

---

## Install dbt Inside Container

Install dbt packages inside scheduler container:

```bash
pip install dbt-core dbt-snowflake
```

Verify installation:

```bash
dbt --version
```

---

## Important dbt Setup Notes

Do **not** mount these generated dbt folders from local machine:

- `target/`
- `logs/`
- `dbt_packages/`

These folders can cause stale artifact issues and parsing failures inside Docker.

Example error:

```text
KeyError: 'dbt_snowflake://macros/get_custom_name.sql'
```

---

## Cleanup dbt Generated Artifacts (if already mounted)

Inside scheduler container:

```bash
cd /opt/airflow/dbt
rm -rf target logs dbt_packages
```

Or one-line command:

```bash
cd /opt/airflow/dbt && rm -rf target logs dbt_packages
```

---

## Recommended .gitignore Entries

```gitignore
learnDbtSnowflake/target/
learnDbtSnowflake/logs/
learnDbtSnowflake/dbt_packages/
dockerAirflow/logs/
```

---

## Useful Commands

### Check DAG import errors

```bash
airflow dags list-import-errors
```

### List DAGs

```bash
airflow dags list
```

### Test dbt connection

```bash
cd /opt/airflow/dbt
dbt debug --profiles-dir /opt/airflow/dbt/profiles
```

---

## Notes

- Keep `profiles.yml` inside repo and mount it into container.
- Use mounted dbt project path:

```text
/opt/airflow/dbt
```

- Use profiles path:

```text
/opt/airflow/dbt/profiles
```

---



