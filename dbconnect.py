import mysql.connector

def connect_db(host: str = "localhost",
               database: str = "AMENITY_MANAGEMENT",
               user: str = "root",
               password: str = "1234567"):
    mydb = mysql.connector.connect(
        host=host,
        database= database,
        user=user ,
        password=password
    )
    return mydb


