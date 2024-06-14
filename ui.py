import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from student import add_student, create_student_pdf, search_students
import pandas as pd


def create_student_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    class_label = tk.Label(frame, text='Class')
    class_label.grid(row=1, column=0, padx=5, pady=5)
    class_entry = tk.Entry(frame)
    class_entry.grid(row=1, column=1, padx=5, pady=5)

    add_button = tk.Button(frame, text='Add Student', command=lambda: add_student(
        name_entry.get(), class_entry.get()))
    add_button.grid(row=2, columnspan=2, pady=10)


def create_search_student_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    search_label = tk.Label(frame, text='Search Student by Name')
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    result_tree = ttk.Treeview(frame, columns=(
        'ID', 'Name', 'Class', 'Admission Date', 'Balance'), show='headings')
    result_tree.heading('ID', text='ID')
    result_tree.heading('Name', text='Name')
    result_tree.heading('Class', text='Class')
    result_tree.heading('Admission Date', text='Admission Date')
    result_tree.heading('Balance', text='Balance')
    result_tree.grid(row=1, column=0, columnspan=2, pady=10)

    search_button = tk.Button(frame, text='Search', command=lambda: search_students(
        search_entry.get(), result_tree))
    search_button.grid(row=2, columnspan=2, pady=10)


def create_download_and_upload_ui(tab, logged_in_user):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    student_id_label = tk.Label(frame, text='Student ID')
    student_id_label.grid(row=1, column=0, padx=5, pady=5)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=1, column=1, padx=5, pady=5)

    upload_button = tk.Button(frame, text='Upload', command=open_file)
    upload_button.grid(row=2, columnspan=2, pady=10)

    pdf_button = tk.Button(frame, text='Create PDF', command=lambda: create_student_pdf(
        student_id_entry.get(), name_entry.get(), logged_in_user))
    pdf_button.grid(row=3, columnspan=2, pady=10)


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
    if file_path:
        process_file(file_path)


def process_file(file_path):
    try:
        df = pd.read_excel(file_path)
        # Assuming columns A, B, and C correspond to student_id, name, and class
        for index, row in df.iterrows():
            add_student(row['Name'], row['Class'])
        messagebox.showinfo(
            "Success", "File processed and students added successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")
