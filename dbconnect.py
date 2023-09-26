import mysql.connector

def connect_db (host= "localhost", database= "AMENITY_MANAGEMENT", user ="root", password= "josh123"):
    mydb = mysql.connector.connect(
        host=host,
        database= database,
        user=user ,
        password=password
    )
    return mydb


