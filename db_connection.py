import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1998",
        database="school_meals_db"
    )
