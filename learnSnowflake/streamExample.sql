--Cresting warehouse
create warehouse RKS_COMPUTE_WH
warehouse_size = 'SMALL'
auto_suspend = 60
auto_resume = true;

--use warehouse
use warehouse rks_compute_wh;

create user data_engineer;
create ROLE developer;

CREATE DATABASE IF NOT EXISTS NDW;
ALTER DATABASE NDW RENAME TO LERN_DB;
ALTER DATABASE LERN_DB RENAME TO LEARN_DB;

USE DATABASE LEARN_DB;

CREATE SCHEMA IF NOT EXISTS DEV;
CREATE SCHEMA IF NOT EXISTS src;
SHOW SCHEMAS;

create table learn_db.src.customer as
select * from snowflake_sample_data.tpch_sf10.customer;

describe table src.customer;

select count(*) from src.customer; -- 1500000
select count(*) from src.customer where lower(c_address) like '%usa%'; --1070

--creating a stream which capture changes from source(insert, update, delete)
create stream src.customer_stream on table src.customer;

--let's change the source
delete from src.customer where lower(c_address) not like '%usa%'; -- 1498930 deleted

select * from src.customer_stream;

drop table dev.customer;
create table dev.customer as
select C_CUSTKEY, C_name, c_phone from src.customer
where 1 = 0; -- create empty table with same schema

select * from dev.customer; -- 0 rows

--insert from stream table .
--insert/update using merge
merge into dev.customer c
using src.customer_stream cs
on c.C_CUSTKEY = cs.C_CUSTKEY
when matched
    then update
        set c.C_NAME = cs.C_NAME,
        c.C_PHONE = cs.C_PHONE
when not matched
    then insert (c_custkey, c_name, c_phone)
    values (cs.c_custkey,cs.c_name, cs.c_phone);

select count(*) from src.customer_stream; -- 0 , stream becomes empty after consuming(using merge)

truncate table src.customer;
select count(*) from src.customer_stream; --1070 rows inserted , let's consume it
-- it means we have to again run the same command that is written above. better to schedule a task

delete stage LEARN_DB.SRC.CONTROL; -- not working , created stage instead of schema by mistake

create schema learn_db.control;



create task control.customer_update
warehouse = rks_compute_wh
schedule = '1 minute'
as
    merge into dev.customer c
    using src.customer_stream cs
    on c.C_CUSTKEY = cs.C_CUSTKEY
    when matched
        then update
            set c.C_NAME = cs.C_NAME,
            c.C_PHONE = cs.C_PHONE
    when not matched
        then insert (c_custkey, c_name, c_phone)
        values (cs.c_custkey,cs.c_name, cs.c_phone);

alter task control.customer_update resume; -- resume after creating the task to make it run based on schedule

--src and stream should be empty by NOWAIT
select count(*) from src.customer;
select count(*) from src.customer_stream;

--let's push back all the rows back to src using task
alter task control.customer_update suspend;
create task control.customer_revert
after control.customer_update
as
insert into src.customer
select * from dev.customer;


show tasks;