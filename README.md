# learnDbtSnpwflake
### step 1: install python
### step 2: Install dbt using : pip install dbt-snowflake
### step 3: create dbt project 
    dbt init learnDbtSnowflake

    Fill details
        Enter a number: 1
        account (https://<this_value>.snowflakecomputing.com): FSCEYGI-HYB67970
        user (dev username): DBT_RKS
        [1] password
        [2] keypair
        [3] sso
        Desired authentication type option (enter a number): 1
        password (dev password): 
        role (dev role): developer
        warehouse (warehouse name): compute_wh
        database (default database that dbt will build objects in): learn_db
        schema (default schema that dbt will build objects in): dev
        threads (1 or more) [1]: 4
        08:23:22  Profile learnDbtSnowflake written to C:\Users\rakes\.dbt\profiles.yml using target's profile_template.yml and your supplied values. Run 'dbt debug' to validate the connection.
        
    dbt project is created.

### write your sql in the project 
cd into your dbt project directory : cd learnDbtSnowflake
- check snowflake connection using dbt debug
- compile - dbt debug
- run - dbt run 

###
    python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"


### run airflow 
- docker compose -f .\docker-compose-localExecutor.yaml down (give `-v` for deleting volumes)                                                                                     
- docker compose -f .\docker-compose-localExecutor.yaml up airflow-init
- docker compose -f .\docker-compose-localExecutor.yaml up -d
- then refresh the scheduler 
  - docker exec -it dockerairflow-airflow-scheduler-1 bash
    - airflow dags reserialize 
    - pip install dbt-core dbt-snowflake
    - don't mount  target logs dbt_packages
      - remove if done
        - cd /opt/airflow/dbt && rm -rf target logs dbt_packages

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



