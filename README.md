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

