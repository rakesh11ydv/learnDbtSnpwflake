{{ config(materialized = 'table') }}

SELECT * FROM RAW.ORDERS
WHERE ORDER_STATUS IN ('delivered', 'cancelled')