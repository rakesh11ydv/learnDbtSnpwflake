use warehouse compute_wh;
use database learn_db;
use schema RAW;
COPY INTO CUSTOMERS
FROM @RAW.OLIST_INTERNAL_STAGE/olist_customers_dataset.csv
FILE_FORMAT = learn_db.raw.CSV_FORMAT;

COPY INTO ORDERS FROM (
    SELECT $1 AS order_id,
    $2 AS customer_id,
    $3 AS order_status,
    $4 AS order_purchase_timestamp
    FROM @RAW.OLIST_INTERNAL_STAGE/olist_orders_dataset.csv
    )
    FILE_FORMAT = learn_db.raw.CSV_FORMAT;