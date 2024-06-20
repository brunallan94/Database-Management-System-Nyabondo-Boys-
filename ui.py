import tkinter as tk
from tkinter import ttk, filedialog, messagebox, HORIZONTAL, Tk
from student import add_student, create_student_pdf, search_students, update_student, create_all_student_pdf
import pandas as pd

# Initialize selected student_id
selected_student_id = None


def create_student_ui(tab):
    frame = tk.Frame(tab)
    frame.grid(padx=10, pady=10)

    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    class_label = tk.Label(frame, text='Class')
    class_label.grid(row=1, column=0, padx=5, pady=5)
    class_entry = tk.Entry(frame)
    class_entry.grid(row=1, column=1, padx=5, pady=5)

    admissiond_label = tk.Label(
        frame, text='Admission Date (Use figures only e.g 2020, 2021)')
    admissiond_label.grid(row=2, column=0, padx=5, pady=5)
    admissiond_entry = tk.Entry(frame)
    admissiond_entry.grid(row=2, column=1, padx=5, pady=5)

    balance_label = tk.Label(frame, text='Balance')
    balance_label.grid(row=3, column=0, padx=5, pady=5)
    balance_entry = tk.Entry(frame)
    balance_entry.grid(row=3, column=1, padx=5, pady=5)

    admission_label = tk.Label(frame, text='Admission Number')
    admission_label.grid(row=4, column=0, padx=5, pady=5)
    admission_entry = tk.Entry(frame)
    admission_entry.grid(row=4, column=1, padx=5, pady=5)

    grade_label = tk.Label(frame, text= 'Grade')
    grade_label.grid(row=5, column=0, padx=5, pady=5)
    grade_entry = tk.Entry(frame)
    grade_entry.grid(row=5, column=1, padx=5, pady=5)

    add_button = tk.Button(frame, text='Add Student', command=lambda: add_student(
        name_entry.get(), class_entry.get(), admissiond_entry.get(), balance_entry.get(), admission_entry.get(), grade_entry.get()))
    add_button.grid(row=6, columnspan=2, pady=10)


def create_search_student_ui(tab):
    frame = tk.Frame(tab)
    frame.grid(padx=10, pady=10)

    search_label = tk.Label(frame, text='Search Student by Name')
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=1, padx=5, pady=5)

    result_tree = ttk.Treeview(frame, columns=(
        'ID', 'Name', 'Class', 'Admission Date', 'Balance', 'Admission Number', 'Grade'), show='headings')
    result_tree.heading('ID', text='ID')
    result_tree.heading('Name', text='Name')
    result_tree.heading('Class', text='Class')
    result_tree.heading('Admission Date', text='Admission Date')
    result_tree.heading('Balance', text='Balance')
    result_tree.heading('Admission Number', text='Admission Number')
    result_tree.heading('Grade', text='Grade')

    result_tree.grid(row=1, column=0, columnspan=3, pady=10, sticky='news')

    # Configure grid weights to allow treeview to expand
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)

    # Edit form
    edit_frame = tk.Frame(tab)
    edit_frame.grid(padx=10, pady=10)
    edit_frame.grid_remove()

    edit_name_label = tk.Label(edit_frame, text='Name')
    edit_name_label.grid(row=1, column=0, padx=5, pady=5)
    edit_name_entry = tk.Entry(edit_frame)
    edit_name_entry.grid(row=1, column=1, padx=5, pady=5)

    edit_balance_label = tk.Label(edit_frame, text='Balance')
    edit_balance_label.grid(row=2, column=0, padx=5, pady=5)
    edit_balance_entry = tk.Entry(edit_frame)
    edit_balance_entry.grid(row=2, column=1, padx=5, pady=5)

    save_button = tk.Button(edit_frame, text='Save',
                            command=lambda: update_student_info(search_entry, result_tree))
    save_button.grid(row=3, columnspan=2, pady=10)

    def on_edit_selected(event):
        # store the student ID in a variable that can be accessed by update_student_info
        global selected_student_id
        item = result_tree.selection()[0]
        values = result_tree.item(item, 'values')

        selected_student_id = values[0]

        edit_name_entry.delete(0, tk.END)
        edit_name_entry.insert(0, values[1])
        edit_balance_entry.delete(0, tk.END)
        edit_balance_entry.insert(0, values[4])
        edit_frame.grid()

    result_tree.bind('<Double-1>', on_edit_selected)

    def update_student_info(search_entry, result_tree):
        # Use global variable to access the student ID
        global selected_student_id
        student_id = selected_student_id
        name = edit_name_entry.get()
        balance = edit_balance_entry.get()
        # update student into the database
        update_student(student_id, name, balance)
        # Refresh the tree view/ search results
        search_and_display(search_entry.get(), result_tree)
        edit_frame.grid_remove()  # Hide edit form after update
        selected_student_id = None  # Reset selected student_id after updating

    def search_and_display(search_query, tree):
        results = search_students(search_query)
        for row in tree.get_children():
            tree.delete(row)
        for result in results:
            tree.insert('', 'end', values=result)

    search_button = tk.Button(
        frame, text='Search', command=lambda: search_and_display(search_entry.get(), result_tree))
    search_button.grid(row=0, column=2, padx=5, pady=5)


def create_download_and_upload_ui(tab, logged_in_user):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    # Download information of a single student
    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    student_id_label = tk.Label(frame, text='Student ID')
    student_id_label.grid(row=1, column=0, padx=5, pady=5)
    student_id_entry = tk.Entry(frame)
    student_id_entry.grid(row=1, column=1, padx=5, pady=5)

    pdf_button = tk.Button(frame, text='Create PDF', command=lambda: create_student_pdf(
        student_id_entry.get(), name_entry.get(), logged_in_user))
    pdf_button.grid(row=2, columnspan=2, pady=10)

    # Download information of multiple students
    grade_label = tk.Label(frame, text='Select Student Grade: ')
    grade_label.grid(row=3, column=0, padx=5, pady=5)

    # Create a dropdown menu
    grades = [4, 5, 6, 7, 8, 9]
    grade_var = tk.StringVar()
    grade_var.set(grades[0])  # Set the default value
    grade_dropdown = tk.OptionMenu(frame, grade_var, *grades)
    grade_dropdown.grid(row=3, column=1, padx=5, pady=5)

    generate_button = tk.Button(frame, text='Generate all students PDF', command=lambda: create_all_student_pdf(student_id_entry.get(), name_entry.get(), logged_in_user, grade_var.get()))
    generate_button.grid(row=4, columnspan=2, padx=5, pady=5)

    upload_button = tk.Button(frame, text='Upload from Excel', command=open_file)
    upload_button.grid(row=5, columnspan=2, pady=10)


def open_file():
    file_path = filedialog.askopenfilename(
        filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
    if file_path:
        process_file(file_path)


def process_file(file_path):
    try:
        df = pd.read_excel(file_path)
        # Create a top-level window for progress bar
        progress_window = Tk()
        progress_window.title('Processing data')

        # Set up the progress bar
        progress_bar = ttk.Progressbar(
            progress_window, orient=HORIZONTAL, length=300, mode='determinate')
        progress_bar.pack(pady=10)

        # Calculate the step size for each update
        step_size = 100 / len(df.index)

        # Assuming columns A, B, and C correspond to student_id, name, and class, admission_date, balance, admission_no, grade
        for index, row in df.iterrows():
            row = row.where(pd.notnull(row), None)
            add_student(row['Name'], row['Class'], row['Admission Date'],
                        row['Balance'], row['Admission Number'],row['Grade'], show_messagebox=False)

            # Update the progess bar
            progress_bar['value'] += step_size
            progress_window.update_idletasks()

        messagebox.showinfo(
            "Success", "File processed and students added successfully")

        # close the progress window after completion
        progress_window.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {e}")
