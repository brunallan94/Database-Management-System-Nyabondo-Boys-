import mysql.connector
from db_connection import create_connection
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


def add_student(name, student_class, admission_date, balance, admission_no, show_messagebox=True):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO students (name, class, admission_date, balance, admission_no) VALUES (%s, %s, %s, %s, %s)", (name, student_class, admission_date, balance, admission_no))
        conn.commit()
        if show_messagebox:
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
            "SELECT id, name, class, admission_date, balance, admission_no FROM students WHERE name LIKE %s", (f"%{name}%",))
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
            "SELECT name, class, admission_date, balance, admission_no FROM students WHERE id = %s", (student_id,))
        student_data = cursor.fetchone()
        if not student_data:
            messagebox.showerror("Error", "No student found with that ID")
            return

        name, student_class, admission_date, balance, admission_no = student_data

        # Create PDF
        c = canvas.Canvas(f"{name}_student_details.pdf", pagesize=letter)
        c.drawString(100, 750, f"Name: {name}")
        c.drawString(100, 725, f"Admission Number: {admission_no}")
        c.drawString(100, 700, f"Class: {student_class}")
        c.drawString(100, 675, f"Admission Date: {admission_date}")
        c.drawString(100, 650, f"Balance Remaining: {balance}")

        c.drawString(400, 750, f"Signed by: {logged_in_user}")
        c.drawString(400, 725, "Signature: ___________")

        # Save PDF to a specific directory
        # Change this to your desired directory
        directory = os.path.join(os.environ['USERPROFILE'], 'Downloads')
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


def update_student(student_id, name, student_class):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE students SET name = %s, class = %s WHERE id = %s", (name, student_class, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
