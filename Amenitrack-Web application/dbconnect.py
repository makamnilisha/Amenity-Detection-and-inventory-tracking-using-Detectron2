import mysql.connector


def connect_db(host: str = "localhost",
               database: str = "amenity_management",
               user: str = "root",
               password: str = "password",
               port: int = "portnumber"):
    mydb = mysql.connector.connect(
        host=host,
        database=database,
        user=user,
        password=password,
        port=port,
    )
    return mydb





