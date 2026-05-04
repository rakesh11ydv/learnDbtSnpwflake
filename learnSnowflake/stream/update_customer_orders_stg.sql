use database learn_db;

merge into stg.CUSTOMER_ORDERS F
using (
    select
        C.C_CUSTKEY AS CUSTOMERID,
        C.C_NAME AS CUSTOMERNAME,
        O.O_ORDERSTATUS AS ORDERSTATUS,
        O.O_TOTALPRICE AS TOTALPRICE,
        N.N_NAME AS NATIONNAME
    from raw_src.SF10_CUSTOMER_stream C
    left join raw_src.SF10_ORDER_stream O ON C.C_CUSTKEY = O.O_CUSTKEY
    left join raw_src.SF10_CUSTOMER_NATION N on C.C_NATIONKEY = N.N_NATIONKEY
) U
on F.CUSTOMERID = U.CUSTOMERID
when matched
    then update
            set
                CUSTOMERID= u.CUSTOMERID,
                CUSTOMERNAME = u.CUSTOMERNAME,
                ORDERSTATUS = U.ORDERSTATUS,
                TOTALPRICE = U.TOTALPRICE,
                ROW_STATUS = 'UPDATE',
                OP_DATE = CURRENT_TIMESTAMP
when not matched
    then
        insert (CUSTOMERID, CUSTOMERNAME, ORDERSTATUS, TOTALPRICE, ROW_STATUS, OP_DATE)
        values (U.CUSTOMERID, U.CUSTOMERNAME, U.ORDERSTATUS, U.TOTALPRICE, 'INSERT', CURRENT_TIMESTAMP)