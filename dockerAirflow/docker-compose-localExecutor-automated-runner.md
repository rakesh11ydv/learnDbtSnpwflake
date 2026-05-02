# Airflow Local Setup with Docker + dbt (Automated dbt Installation)

This project runs **Apache Airflow locally using Docker Compose with LocalExecutor** and integrates **dbt + Snowflake**.

dbt dependencies are preinstalled automatically using a custom Docker image, so no manual installation inside containers is required.

---

## Project Structure

```text
dockerAirflow/
├── Dockerfile
├── docker-compose-localExecutor.yaml
├── dags/
├── logs/
├── plugins/
└── config/
```

---

## Custom Docker Image

A custom Airflow image is used to preinstall dbt.

### Dockerfile

```dockerfile
FROM apache/airflow:3.2.1

USER root

RUN apt-get update && apt-get install -y git && apt-get clean

USER airflow

RUN pip install --no-cache-dir dbt-core dbt-snowflake
```

This image:
- starts from official Airflow image
- installs `git`
- installs:
  - `dbt-core`
  - `dbt-snowflake`

---

## Docker Compose Configuration

In `docker-compose-localExecutor.yaml`, use:

```yaml
build: .
```

instead of:

```yaml
image: apache/airflow:3.2.1
```

Example:

```yaml
x-airflow-common:
  &airflow-common
  build: .
```

This ensures all Airflow services use the custom image.

---

## Start Airflow

### 1. Stop existing containers

```bash
docker compose -f .\docker-compose-localExecutor.yaml down
```

To also reset database volumes:

```bash
docker compose -f .\docker-compose-localExecutor.yaml down -v
```

Use `-v` only when you want a fresh Airflow metadata database.

---

### 2. Build custom image

Build Airflow image with dbt preinstalled:

```bash
docker compose -f .\docker-compose-localExecutor.yaml build
```

---

### 3. Initialize Airflow metadata database

```bash
docker compose -f .\docker-compose-localExecutor.yaml up airflow-init
```

This step:
- initializes metadata database
- creates tables
- prepares Airflow environment

---

### 4. Start Airflow services

```bash
docker compose -f .\docker-compose-localExecutor.yaml up -d
```

This starts:
- Airflow API Server
- Scheduler
- Postgres

---

## Verify dbt Installation

Open scheduler container:

```bash
docker exec -it dockerairflow-airflow-scheduler-1 bash
```

Check dbt:

```bash
dbt --version
```

Expected output should include:

```text
Core:
  - installed: 1.x.x

Plugins:
  - snowflake: 1.x.x
```

---

## dbt Project Mounting

Mount dbt project into Airflow container.

Example volume:

```yaml
- C:/Users/rakes/PycharmProjects/learnDbtSnpwflake/learnDbtSnowflake:/opt/airflow/dbt
```

Expected container structure:

```text
/opt/airflow/dbt
├── dbt_project.yml
├── models
├── macros
├── profiles
│   └── profiles.yml
```

Use in DAG:

```python
DBT_PROJECT_DIR = "/opt/airflow/dbt"
DBT_PROFILES_DIR = "/opt/airflow/dbt/profiles"
```

---

## Important: Do Not Mount Generated dbt Artifacts

Do **not** keep these folders in mounted project:

- `target/`
- `logs/`
- `dbt_packages/`

These can cause stale parsing/cache issues.

Common error:

```text
KeyError: 'dbt_snowflake://macros/get_custom_name.sql'
```

---

## Cleanup Generated dbt Artifacts

If these folders already exist:

```bash
cd /opt/airflow/dbt && rm -rf target logs dbt_packages
```

Or delete locally from host machine.

---

## Recommended .gitignore

```gitignore
# dbt artifacts
learnDbtSnowflake/target/
learnDbtSnowflake/logs/
learnDbtSnowflake/dbt_packages/

# airflow logs
dockerAirflow/logs/
```

If already tracked:

```bash
git rm -r --cached learnDbtSnowflake/target
git rm -r --cached learnDbtSnowflake/logs
git rm -r --cached learnDbtSnowflake/dbt_packages
git rm -r --cached dockerAirflow/logs
```

Then commit:

```bash
git commit -m "Ignore generated dbt and airflow artifacts"
```

---

## Useful Commands

### Check DAGs

```bash
airflow dags list
```

### Check DAG import errors

```bash
airflow dags list-import-errors
```

### Test dbt connection manually

```bash
cd /opt/airflow/dbt
dbt debug --profiles-dir /opt/airflow/dbt/profiles
```

### Run dbt manually

```bash
dbt run --profiles-dir /opt/airflow/dbt/profiles
```

---

## Notes

- Keep `profiles.yml` inside repo for portability.
- Avoid mounting `/root/.dbt`.
- Use project-local profiles directory.

Recommended paths:

```text
Project:  /opt/airflow/dbt
Profiles: /opt/airflow/dbt/profiles
```

---

## Access Airflow UI

Open:

```text
http://localhost:8080
```

Default credentials depend on your compose configuration.

---