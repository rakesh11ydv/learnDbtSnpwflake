CREATE OR REPLACE TABLE RAW.CUSTOMERS (
    customer_id STRING,
    customer_unique_id STRING,
    customer_zip_code_prefix STRING,
    customer_city STRING,
    customer_state STRING
);

CREATE OR REPLACE TABLE RAW.ORDERS (
    order_id STRING,
    customer_id STRING,
    order_status STRING,
    order_purchase_timestamp STRING
);