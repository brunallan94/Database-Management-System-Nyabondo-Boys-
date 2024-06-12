from db_connection import create_connection
from tkinter import messagebox


def handle_payment(student_id, meal_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO payments (student_id, meal_id, amount, payment_date) VALUES (%s, %s, %s, CURDATE())",
                   (student_id, meal_id, amount))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Payment recorded successfully")
