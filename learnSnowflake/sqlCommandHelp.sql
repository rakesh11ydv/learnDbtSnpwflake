
use database learn_db;

create warehouse compute_wh_xs
warehouse_size = 'x-small'
auto_suspend = 60
auto_resume = true;

use warehouse compute_wh_xs;

create role if not exists developer;
create user if not exists data_engineer;

grant role developer to user data_engineer;

grant usage, monitor, operate on warehouse compute_wh_xs to role developer;

grant create database on <account> to role developer;

create database if not exists learn_db;

grant usage, create schema on database learn_db to role developer;

use role developer;
create schema if not exists stg;

user role accountadmin;
grant usage, create, modify, delete table
