import mysql.connector


class School_Database_Creation:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor
        self.__databases = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
        self.__tables = ['payments_term1', 'payments_term2', 'payments_term3']

    def create_database(self):
        try:
            for database in self.__databases:
                self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database}')
                print(f'Creating database {database}')
            self.conn.commit()
            print('Created databases successfully :) ')

        except mysql.connector.Error as err:
            print(f'Error {err}')

    def create_tables(self):
        try:
            for database in self.__databases:
                self.cursor.execute(f'USE {database}')
                self.cursor.execute(
                    f'CREATE TABLE IF NOT EXISTS students (id  INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100) NOT NULL, admission_no INT(6) NOT NULl, stream VARCHAR(3) NOT NULL, grade INT(3) NOT NULL)')
                print(f'Creating table students in {database}')

                for table in self.__tables:
                    self.cursor.execute(
                        f'CREATE TABLE IF NOT EXISTS {table} (id INT AUTO_INCREMENT PRIMARY KEY, student_id INT, amount_expected INT(6), amount_paid INT(6), balance INT(6), date_of_payment DATE, method_of_payment VARCHAR(10) NOT NULL, transaction_code VARCHAR(20), FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE ON UPDATE CASCADE)')
                    print(f'Creating table {table}')

            self.conn.commit()
            print('Created tables successfully')

        except mysql.connector.Error as err:
            print(f'Error {err}')

        finally:
            self.cursor.close()
            self.conn.close()


def create_connection():
    return mysql.connector.connect(host="localhost", user="root", password="1998")


if __name__ == '__main__':
    conn = create_connection()
    cursor = conn.cursor()
    dat = School_Database_Creation(conn, cursor)
    dat.create_database()
    dat.create_tables()
