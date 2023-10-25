## pip  install mysql-connector-python
import mysql.connector
import dbconnect
# from torch import _fake_quantize_per_tensor_affine_cachemask_tens
CNX: mysql.connector.connect = None

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False# pip  install mysql-connector-python
import mysql.connector
import dbconnect
# from torch import _fake_quantize_per_tensor_affine_cachemask_tens
CNX: mysql.connector.connect = None

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False
    args = [userName, password, 0]
    result_args = execute_sql_query("CheckUser", args)
    return (result_args[2] == 1)


def execute_sql_query(query, args):
    global CNX
    if (CNX is None):
        CNX = dbconnect.connect_db()
    with CNX.cursor() as cur:
        return cur.callproc(query, args)

    args = [userName, password, 0]
    result_args = execute_sql_query("CheckUser", args)
    return (result_args[2] == 1)


def execute_sql_query(query, args):
    global CNX
    if (CNX is None):
        CNX = dbconnect.connect_db()
    with CNX.cursor() as cur:
        return cur.callproc(query, args)
