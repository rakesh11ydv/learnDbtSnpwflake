{{ config(materialized = 'table')}}

SELECT
    CUST.*,
    ORD.ORDER_ID,
    ORD.ORDER_STATUS,
    ORD.ORDER_PURCHASE_TIMESTAMP
FROM ref('customers_silver') CUST
INNER JOIN ref('orders_silver') ORD
ON CUST.CUSTOMER_ID = ORD.CUSTOMER_ID
