import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="school_meals_db"
    )
