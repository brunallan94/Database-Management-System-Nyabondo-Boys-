import tkinter as tk
from tkinter import ttk
from student import add_student, search_students
from payment import handle_payment
from tkinter import messagebox


def create_add_student_ui(root):
    frame = tk.Frame(root)
    frame.pack()

    name_label = tk.Label(frame, text="Name")
    name_label.grid(row=0, column=0)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1)

    class_label = tk.Label(frame, text="Class")
    class_label.grid(row=1, column=0)
    class_entry = tk.Entry(frame)
    class_entry.grid(row=1, column=1)

    add_button = tk.Button(frame, text="Add Student", command=lambda: add_student_callback(
        name_entry.get(), class_entry.get()))
    add_button.grid(row=2, columnspan=2)


def create_payment_ui(root):
    frame = tk.Frame(root)
    frame.pack()

    student_id_label = tk.Label(frame, text="Student ID")
    student_id_label.grid(row=0, column=0)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=0, column=1)

    meal_id_label = tk.Label(frame, text="Meal ID")
    meal_id_label.grid(row=1, column=0)
    meal_id_entry = tk.Entry(frame)
    meal_id_entry.grid(row=1, column=1)

    amount_label = tk.Label(frame, text="Amount")
    amount_label.grid(row=2, column=0)
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=2, column=1)

    pay_button = tk.Button(frame, text="Make Payment", command=lambda: handle_payment_callback(
        student_id_entry.get(), meal_id_entry.get(), amount_entry.get()))
    pay_button.grid(row=3, columnspan=2)


def create_search_student_ui(root):
    frame = tk.Frame(root)
    frame.pack()

    search_label = tk.Label(frame, text="Search Name")
    search_label.grid(row=0, column=0)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=1)

    search_button = tk.Button(
        frame, text="Search", command=lambda: search_student_callback(search_entry.get()))
    search_button.grid(row=0, column=2)

    result_tree = ttk.Treeview(frame, columns=(
        "ID", "Name", "Class"), show="headings")
    result_tree.heading("ID", text="ID")
    result_tree.heading("Name", text="Name")
    result_tree.heading("Class", text="Class")
    result_tree.grid(row=1, column=0, columnspan=3)

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
