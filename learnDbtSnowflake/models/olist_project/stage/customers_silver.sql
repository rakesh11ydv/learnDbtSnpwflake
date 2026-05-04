{{ config(materialized= 'table')}}

SELECT * FROM
RAW.CUSTOMERS WHERE CUSTOMER_STATE = "SP";