import mysql.connector
from db_connection import create_connection
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


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


def create_student_pdf(student_id, name, logged_in_user):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT name, class, admission_date, balance FROM students WHERE id = %s", (student_id,))
        student_data = cursor.fetchone()
        if not student_data:
            messagebox.showerror("Error", "No student found with that ID")
            return

        name, student_class, admission_date, balance = student_data

        # Create PDF
        c = canvas.Canvas(f"{name}_student_details.pdf", pagesize=letter)
        c.drawString(100, 750, f"Name: {name}")
        c.drawString(100, 725, f"Class: {student_class}")
        c.drawString(100, 700, f"Admission Date: {admission_date}")
        c.drawString(100, 675, f"Balance Remaining: {balance}")

        c.drawString(400, 750, f"Signed by: {logged_in_user}")
        c.drawString(400, 725, "Signature: ___________")

        # Save PDF to a specific directory
        directory = "path/to/your/directory"  # Change this to your desired directory
        if not os.path.exists(directory):
            os.makedirs(directory)

        pdf_path = os.path.join(directory, f"{name}_student_details.pdf")
        c.save()

        messagebox.showinfo(
            "Success", f"PDF created successfully at {pdf_path}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
