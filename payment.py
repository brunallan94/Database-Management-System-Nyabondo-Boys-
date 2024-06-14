from db_connection import create_connection
from tkinter import messagebox


def handle_payment(student_id, meal_id, amount):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO payments (student_id, meal_id, amount) VALUES (%s, %s, %s)",
        (student_id, meal_id, amount)
    )
    conn.commit()
    cursor.close()
    conn.close()
    messagebox.showinfo("Success", "Payment recorded successfully")
