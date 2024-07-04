import mysql.connector
from mysql.connector.abstracts import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


class School_Database_Creation:
    def __init__(self, conn, cursor) -> None:
        self.conn = conn
        self.cursor = cursor
        self.__databases = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
        self.__tables = ['payments_term1', 'payments_term2', 'payments_term3']

    def create_database(self) -> None:
        try:
            for database in self.__databases:
                self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
                print(f'Creating database {database}')
            self.conn.commit()
            print('Created databases successfully :) ')
        except mysql.connector.Error as err:
            print(f'Error {err}')

    def create_tables(self) -> None:
        try:
            for database in self.__databases:
                self.cursor.execute(f'USE {database}')
                self.cursor.execute(
                    'CREATE TABLE IF NOT EXISTS users ('
                    'id INT AUTO_INCREMENT PRIMARY KEY, '
                    'username VARCHAR(100), '
                    'password VARCHAR(100))'
                )
                self.cursor.execute(
                    'CREATE TABLE IF NOT EXISTS students ('
                    'id INT AUTO_INCREMENT PRIMARY KEY, '
                    'name VARCHAR(100) NOT NULL, '
                    'admission_no INT(6) NOT NULL, '
                    'stream VARCHAR(3) NOT NULL, '
                    'grade INT(3) NOT NULL)'
                )
                print(f'Creating table students in {database}')

                for table in self.__tables:
                    self.cursor.execute(
                        f'CREATE TABLE IF NOT EXISTS {table} ('
                        'id INT AUTO_INCREMENT PRIMARY KEY, '
                        'student_id INT, '
                        'amount_expected INT(6), '
                        'amount_paid INT(6), '
                        'balance INT(6), '
                        'date_of_payment DATE, '
                        'method_of_payment VARCHAR(10) NOT NULL, '
                        'transaction_code VARCHAR(20), '
                        'FOREIGN KEY (student_id) REFERENCES students(id) '
                        'ON DELETE CASCADE ON UPDATE CASCADE)'
                    )
                    print(f'Creating table {table} in {database}')
            self.conn.commit()
            print('Created tables successfully')
        except mysql.connector.Error as err:
            print(f'Error {err}')

    def insert_dummy_data(self) -> None:
        try:
            for database in self.__databases:
                self.cursor.execute(f'USE {database}')

                # Insert dummy user
                self.cursor.execute(
                    "INSERT INTO users (username, password) VALUES ('admin', 'Vortex'), ('Aduongo', 'Motemapembe')"
                )
                print(f'Inserted user admin into {database}')

                # Insert dummy student
                self.cursor.execute(
                    "INSERT INTO students (name, admission_no, stream, grade) VALUES "
                    "('Brun Allan', 8714, 'W', 8)"
                )
                student_id = self.cursor.lastrowid  # Get the last inserted id
                print(f'Inserted student Brun Allan with ID {student_id} into {database}')

                # Insert dummy payments
                for table in self.__tables:
                    self.cursor.execute(
                        f"INSERT INTO {table} (student_id, amount_expected, amount_paid, balance, date_of_payment, method_of_payment, transaction_code) VALUES "
                        f"({student_id}, 5000, 4500, 500, '2024-01-15', 'Mpesa', 'TRX12345')"
                    )
                    print(f'Inserted payment entry into {table} in {database}')
            self.conn.commit()
            print('Inserted dummy data successfully')
        except mysql.connector.Error as err:
            print(f'Error {err}')
        finally:
            self.cursor.close()
            self.conn.close()


def create_connection() -> PooledMySQLConnection | MySQLConnectionAbstract:
    return mysql.connector.connect(host="localhost", user="root", password="1998")


if __name__ == '__main__':
    conn = create_connection()
    cursor = conn.cursor()
    dat = School_Database_Creation(conn, cursor)
    dat.create_database()
    dat.create_tables()
    dat.insert_dummy_data()
