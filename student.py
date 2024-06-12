from db_connection import create_connection
from tkinter import messagebox
import mysql.connector


def add_student(name, student_class):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, class) VALUES (%s, %s)", (name, student_class))
        conn.commit()
        messagebox.showinfo("Success", "Student added successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def search_students(name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM students WHERE name LIKE %s", (f"%{name}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
