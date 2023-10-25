import mysql.connector


def connect_db(host: str = "localhost",
               database: str = "AMENITY_MANAGEMENT",
               user: str = "root",
               password: str = "password",
               port: int = "3306"):
    mydb = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
    )
    return mydb





