import mysql.connector


def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1998",
        database="school_meals_db"
    )


def payment_columns():
    conn = create_connection()
    cursor = conn.cursor()
    tables = ['year_2024_term_1', 'year_2024_term_2', 'year_2024_term_3', 'year_2025_term_1', 'year_2025_term_2', 'year_2025_term_3', 'year_2026_term_1', 'year_2026_term_2', 'year_2026_term_3']
    try:
        for table in tables:
            cursor.execute(f'ALTER TABLE {table} ADD date_of_payment DATE DEFAULT NULL, ADD mode_of_payment VARCHAR(50) NOT NULL, ADD transaction_code VARCHAR(50)')
            print(f'Columns added to {table}')
            conn.commit()
            print('Changes committed successfully!')

    except mysql.connector.Error as err:
        print(f'Error: {err}')

    finally:
        cursor.close()
        conn.close()

payment_columns()