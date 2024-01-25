import mysql.connector
import dbconnect
# from torch import _fake_quantize_per_tensor_affine_cachemask_tens
CNX: mysql.connector.connect = None


def login(username: str, password: str) -> bool:
    if username is None:
        return False
    return check_user(username, password)


def check_user(username, password):
    global CNX
    if CNX is None:
        CNX = dbconnect.connect_db()
    with CNX.cursor() as cur:
        cur.execute("SELECT FIRSTNAME, LASTNAME, USERTYPE FROM USER_LIST WHERE USERNAME = %s AND LOGINPASSWORD = %s;",
                    [username, password])
        result = cur.fetchone()
        return result