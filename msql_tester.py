import tkinter as tk
from tkinter import ttk, messagebox
from student import add_student, search_students
from payment import handle_payment
from db_connection import create_connection
import mysql.connector


def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        messagebox.showinfo("Success", "Login successful")
        root.destroy()  # Close the login window
        open_main_application()  # Open the main application window
    else:
        messagebox.showerror("Error", "Invalid username or password")


def create_login_window():
    global root, username_entry, password_entry

    root = tk.Tk()
    root.title("Login")
    root.configure(bg='#333333')

    frame = tk.Frame(root, bg='#333333')
    frame.pack(padx=10, pady=10)

    text_label = tk.Label(frame, text="LOGIN", bg='#333333',
                          fg='#FF3399', font=('Arial', 30), pady=40)
    text_label.grid(row=0, column=0, columnspan=2, sticky='news')

    username_label = tk.Label(frame, text="Username",
                              bg='#333333', fg='#FFFFFF', font=('Arial', 16))
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(frame, font=('Arial', 16))
    username_entry.grid(row=1, column=1, pady=10)

    password_label = tk.Label(frame, text="Password",
                              bg='#333333', fg='#FFFFFF', font=('Arial', 16))
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(frame, show="*", font=('Arial', 16))
    password_entry.grid(row=2, column=1, pady=10)

    login_button = tk.Button(
        frame, text="Login", command=login, bg='#FF3399', fg='#FFFFFF', font=('Arial', 10), pady=8)
    login_button.grid(row=3, columnspan=3)

    root.mainloop()


def create_add_student_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    name_label = tk.Label(frame, text="Name")
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    class_label = tk.Label(frame, text="Class")
    class_label.grid(row=1, column=0, padx=5, pady=5)
    class_entry = tk.Entry(frame)
    class_entry.grid(row=1, column=1, padx=5, pady=5)

    student_id_label = tk.Label(frame, text='Student ID')
    student_id_label.grid(row=2, column=0)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=2, column=1, pady=5)

    amount_paid_label = tk.Label(frame, text='Amount Paid')
    amount_paid_label.grid(row=3, column=0)
    amount_paid_entry = tk.Entry(frame)
    amount_paid_entry.grid(row=3, column=1, pady=5)

    add_button = tk.Button(frame, text="Add Student", command=lambda: add_student_callback(
        name_entry.get(), class_entry.get(), student_id_entry.get(), amount_paid_entry.get()))
    add_button.grid(row=4, columnspan=2, pady=10)


def download_file_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    student_id_label = tk.Label(frame, text='Student ID')
    student_id_label.grid(row=1, column=0)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=1, column=1)

    download_button = tk.Button(frame, text='Download', command=None)
    download_button.grid(row=2, columnspan=3, pady=10)

    upload_button = tk.Button(frame, text='Upload', command=None)
    upload_button.grid(row=3, column=0, pady=15)


def create_payment_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    student_id_label = tk.Label(frame, text="Student ID")
    student_id_label.grid(row=0, column=0, padx=5, pady=5)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=0, column=1, padx=5, pady=5)

    meal_id_label = tk.Label(frame, text="Meal ID")
    meal_id_label.grid(row=1, column=0, padx=5, pady=5)
    meal_id_entry = tk.Entry(frame)
    meal_id_entry.grid(row=1, column=1, padx=5, pady=5)

    amount_label = tk.Label(frame, text="Amount")
    amount_label.grid(row=2, column=0, padx=5, pady=5)
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=2, column=1, padx=5, pady=5)

    pay_button = tk.Button(frame, text="Make Payment", command=lambda: handle_payment_callback(
        student_id_entry.get(), meal_id_entry.get(), amount_entry.get()))
    pay_button.grid(row=3, columnspan=2, pady=10)


def create_search_student_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    search_label = tk.Label(frame, text="Search Name")
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    search_button = tk.Button(
        frame, text="Search", command=lambda: search_student_callback(search_entry.get()))
    search_button.grid(row=0, column=2, padx=5, pady=5)

    result_tree = ttk.Treeview(frame, columns=(
        "ID", "Name", "Class"), show="headings")
    result_tree.heading("ID", text="ID")
    result_tree.heading("Name", text="Name")
    result_tree.heading("Class", text="Class")
    result_tree.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

    return result_tree


def add_student_callback(name, student_class):
    if not name or not student_class:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    add_student(name, student_class)


def handle_payment_callback(student_id, meal_id, amount):
    if not student_id or not meal_id or not amount:
        messagebox.showerror("Error", "Please fill in all fields")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount")
        return
    handle_payment(student_id, meal_id, amount)


def search_student_callback(name):
    results = search_students(name)
    if not results:
        messagebox.showinfo("No Results", "No students found")
    else:
        update_search_results(results)


def update_search_results(results):
    result_tree.delete(*result_tree.get_children())
    for row in results:
        result_tree.insert("", "end", values=row)


def open_main_application():
    root = tk.Tk()
    root.title("School Meals Payment System")

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, expand=True, fill='both')

    # Creating tabs
    add_student_tab = tk.Frame(notebook)
    notebook.add(add_student_tab, text='Add Student')
    create_add_student_ui(add_student_tab)

    download_file_ui_tab = tk.Frame(notebook)
    notebook.add(download_file_ui_tab, text='Download and Upload')
    download_file_ui(download_file_ui_tab)

    payment_tab = tk.Frame(notebook)
    notebook.add(payment_tab, text='Payment')
    create_payment_ui(payment_tab)

    search_student_tab = tk.Frame(notebook)
    notebook.add(search_student_tab, text='Search Student')
    global result_tree
    result_tree = create_search_student_ui(search_student_tab)

    root.mainloop()


if __name__ == "__main__":
    create_login_window()
