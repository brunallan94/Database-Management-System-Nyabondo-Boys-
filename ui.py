import tkinter as tk
from tkinter import ttk, filedialog, messagebox, HORIZONTAL, Tk
from student import add_student, create_student_pdf, search_students, update_student, create_all_student_pdf
import pandas as pd
import threading


# Initialize selected student_id
selected_student_id = None


def create_student_ui(tab):
    frame = tk.Frame(tab)
    frame.grid(padx=10, pady=10)

    # Create a dropdown menu for term and year
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])
    term_dropdown = tk.OptionMenu(frame, term_var, *terms)
    year_dropdown = tk.OptionMenu(frame, year_var, *years)
    term_dropdown.grid(row=0, column=1, padx=5, pady=5)
    year_dropdown.grid(row=1, column=1, padx=5, pady=5)
    term_label = tk.Label(frame, text='Term: ')
    term_label.grid(row=0, column=0)
    year_label = tk.Label(frame, text='Year: ')
    year_label.grid(row=1, column=0)

    name_label = tk.Label(frame, text='Name')
    name_label.grid(row=2, column=0, padx=5, pady=5)
    name_entry = tk.Entry(frame)
    name_entry.grid(row=2, column=1, padx=5, pady=5)

    admission_label = tk.Label(frame, text='Admission Number')
    admission_label.grid(row=3, column=0, padx=5, pady=5)
    admission_entry = tk.Entry(frame)
    admission_entry.grid(row=3, column=1, padx=5, pady=5)

    stream_label = tk.Label(frame, text='Stream')
    stream_label.grid(row=4, column=0, padx=5, pady=5)
    stream_entry = tk.Entry(frame)
    stream_entry.grid(row=4, column=1, padx=5, pady=5)

    grade_label = tk.Label(frame, text='Grade')
    grade_label.grid(row=5, column=0, padx=5, pady=5)
    grade_entry = tk.Entry(frame)
    grade_entry.grid(row=5, column=1, padx=5, pady=5)

    amntexp_label = tk.Label(frame, text='Amount Expected')
    amntexp_label.grid(row=6, column=0, padx=5, pady=5)
    amntexp_entry = tk.Entry(frame)
    amntexp_entry.grid(row=6, column=1, padx=5, pady=5)

    amntpaid_label = tk.Label(frame, text='Amount Paid')
    amntpaid_label.grid(row=7, column=0, padx=5, pady=5)
    amntpaid_entry = tk.Entry(frame)
    amntpaid_entry.grid(row=7, column=1, padx=5, pady=5)

    balance_label = tk.Label(frame, text='Balance')
    balance_label.grid(row=8, column=0, padx=5, pady=5)
    balance_entry = tk.Entry(frame)
    balance_entry.grid(row=8, column=1, padx=5, pady=5)

    add_button = tk.Button(frame, text='Add Student',
                           command=lambda: add_student(name_entry.get(), admission_entry.get(), stream_entry.get(),
                                                       grade_entry.get(), amntexp_entry.get(), amntpaid_entry.get(),
                                                       balance_entry.get(), term_var.get(), year_var.get()))
    add_button.grid(row=9, column=2, columnspan=2, pady=10)


def create_search_student_ui(tab):
    frame = tk.Frame(tab)
    frame.grid(padx=15, pady=15, sticky='news')

    search_label = tk.Label(frame, text='Enter Name')
    search_label.grid(row=0, column=4, padx=5, pady=5)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=5, padx=5, pady=5)

    # Create a dropdown menu
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])
    term_dropdown = tk.OptionMenu(frame, term_var, *terms)
    year_dropdown = tk.OptionMenu(frame, year_var, *years)
    term_dropdown.grid(row=0, column=3, padx=5, pady=5)
    year_dropdown.grid(row=0, column=1, padx=5, pady=5)
    term_label = tk.Label(frame, text='Term: ')
    term_label.grid(row=0, column=2)
    year_label = tk.Label(frame, text='Year: ')
    year_label.grid(row=0, column=0)

    # Search frame
    search_frame = tk.Frame(tab)
    search_frame.grid(padx=15, pady=15, sticky='news')

    result_tree = ttk.Treeview(search_frame, columns=(
        'ID', 'Name', 'Admission Number', 'Stream', 'Grade', 'Amount Expected', 'Amount Paid', 'Balance'),
                               show='headings')
    result_tree.heading('ID', text='ID')
    result_tree.heading('Name', text='Name')
    result_tree.heading('Admission Number', text='Admission Number')
    result_tree.heading('Stream', text='Stream')
    result_tree.heading('Grade', text='Grade')
    result_tree.heading('Amount Expected', text='Amount Expected')
    result_tree.heading('Amount Paid', text='Amount Paid')
    result_tree.heading('Balance', text='Balance')

    result_tree.grid(row=1, column=0, columnspan=4, pady=10, sticky='news')

    # Configure grid weights to allow treeview to expand
    search_frame.grid_rowconfigure(1, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)
    search_frame.grid_columnconfigure(2, weight=1)

    # Edit frame
    edit_frame = tk.Frame(tab)
    edit_frame.grid(padx=15, pady=15)
    edit_frame.grid_remove()

    edit_name_label = tk.Label(edit_frame, text='Name')
    edit_name_label.grid(row=2, column=0, padx=5, pady=5)
    edit_name_entry = tk.Entry(edit_frame)
    edit_name_entry.grid(row=2, column=1, padx=5, pady=5)

    edit_admission_no_label = tk.Label(edit_frame, text='Admission Number')
    edit_admission_no_label.grid(row=3, column=0, padx=5, pady=5)
    edit_admission_no_entry = tk.Entry(edit_frame)
    edit_admission_no_entry.grid(row=3, column=1, padx=5, pady=5)

    edit_stream_label = tk.Label(edit_frame, text='Stream')
    edit_stream_label.grid(row=4, column=0, padx=5, pady=5)
    edit_stream_entry = tk.Entry(edit_frame)
    edit_stream_entry.grid(row=4, column=1, padx=5, pady=5)

    edit_grade_label = tk.Label(edit_frame, text='Grade')
    edit_grade_label.grid(row=5, column=0, padx=5, pady=5)
    edit_grade_entry = tk.Entry(edit_frame)
    edit_grade_entry.grid(row=5, column=1, padx=5, pady=5)

    edit_amountexp_label = tk.Label(edit_frame, text='Amount Expected')
    edit_amountexp_label.grid(row=6, column=0, padx=5, pady=5)
    edit_amountexp_entry = tk.Entry(edit_frame)
    edit_amountexp_entry.grid(row=6, column=1, padx=5, pady=5)

    edit_amountpaid_label = tk.Label(edit_frame, text='Amount Paid')
    edit_amountpaid_label.grid(row=7, column=0, padx=5, pady=5)
    edit_amountpaid_entry = tk.Entry(edit_frame)
    edit_amountpaid_entry.grid(row=7, column=1, padx=5, pady=5)

    edit_balance_label = tk.Label(edit_frame, text='Balance')
    edit_balance_label.grid(row=8, column=0, padx=5, pady=5)
    edit_balance_entry = tk.Entry(edit_frame)
    edit_balance_entry.grid(row=8, column=1, padx=5, pady=5)

    save_button = tk.Button(edit_frame, text='Save', command=lambda: update_student_info(search_entry, result_tree))
    save_button.grid(row=8, column=2, columnspan=2, pady=10)

    def on_edit_selected(event):
        # store the student ID in a variable that can be accessed by update_student_info
        global selected_student_id

        item = result_tree.selection()[0]
        if item:
            values = result_tree.item(item, 'values')
            selected_student_id = values[0]
            edit_name_entry.delete(0, tk.END)
            edit_name_entry.insert(0, values[1])
            edit_admission_no_entry.delete(0, tk.END)
            edit_admission_no_entry.insert(0, values[2])
            edit_stream_entry.delete(0, tk.END)
            edit_stream_entry.insert(0, values[3])
            edit_grade_entry.delete(0, tk.END)
            edit_grade_entry.insert(0, values[4])
            edit_amountexp_entry.delete(0, tk.END)
            edit_amountexp_entry.insert(0, values[5])
            edit_amountpaid_entry.delete(0, tk.END)
            edit_amountpaid_entry.insert(0, values[6])
            edit_balance_entry.delete(0, tk.END)
            edit_balance_entry.insert(0, values[-1])
            edit_frame.grid()

    result_tree.bind('<Double-1>', on_edit_selected)

    def update_student_info(search_entry, result_tree):
        # Use global variable to access the student ID
        global selected_student_id

        # update student into the database
        update_student(selected_student_id, edit_name_entry.get(), edit_admission_no_entry.get(),
                       edit_stream_entry.get(), edit_grade_entry.get(),
                       edit_amountexp_entry.get(), edit_amountpaid_entry.get(), edit_balance_entry.get(),
                       year_var.get(), term_var.get())

        # Refresh the tree view/ search results
        search_and_display()
        edit_frame.grid_remove()  # Hide edit form after update
        selected_student_id = None  # Reset selected student_id after updating

    def search_and_display():
        results = search_students(search_entry.get(), term_var.get(), year_var.get())
        # Clear the existing contents of the tree
        for row in result_tree.get_children():
            result_tree.delete(row)
        # Insert new search results
        for result in results:
            result_tree.insert('', 'end', values=result)

    search_button = tk.Button(frame, text='Search', command=search_and_display)
    search_button.grid(row=0, column=6, padx=5, pady=5)


def create_download_ui(tab, logged_in_user):
    frame_s = tk.Frame(tab)
    frame_s.pack(padx=10, pady=10)

    # Create a dropdown menu
    grades = [4, 5, 6, 7, 8, 9]
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    grade_var = tk.StringVar()
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    grade_var.set(grades[0])  # Set the default value
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])

    # Download information of a single student
    title_1 = tk.Label(frame_s, text='SINGLE STUDENT DOWNLOAD')
    title_1.grid(row=0, column=1, padx=5, pady=5)
    year_label_s = tk.Label(frame_s, text='Year: ')
    year_label_s.grid(row=1, column=0)
    year_dropdown_s = tk.OptionMenu(frame_s, year_var, *years)
    year_dropdown_s.grid(row=1, column=1, padx=5, pady=5)
    term_label_s = tk.Label(frame_s, text='Term: ')
    term_label_s.grid(row=2, column=0)
    term_dropdown_s = tk.OptionMenu(frame_s, term_var, *terms)
    term_dropdown_s.grid(row=2, column=1, padx=5, pady=5)
    name_label = tk.Label(frame_s, text='Name')
    name_label.grid(row=3, column=0)
    name_entry = tk.Entry(frame_s)
    name_entry.grid(row=3, column=1, padx=5, pady=5)
    student_id_label = tk.Label(frame_s, text='Student ID')
    student_id_label.grid(row=4, column=0)
    student_id_entry = tk.Entry(frame_s)
    student_id_entry.grid(row=4, column=1, padx=5, pady=5)

    pdf_button = tk.Button(frame_s, text='Create PDF', command=lambda: create_student_pdf(
        student_id_entry.get(), name_entry.get(), year_var.get(), term_var.get(), logged_in_user))
    pdf_button.grid(row=5, columnspan=2, pady=10)

    frame_m = tk.Frame(tab)
    frame_m.pack(padx=10, pady=10)

    # Download information of multiple students
    title_2 = tk.Label(frame_m, text='MULTIPLE STUDENT DOWNLOAD')
    title_2.grid(row=0, column=1)
    year_label_m = tk.Label(frame_m, text='Year: ')
    year_label_m.grid(row=1, column=0)
    year_dropdown_m = tk.OptionMenu(frame_m, year_var, *years)
    year_dropdown_m.grid(row=1, column=1, padx=5, pady=5)
    term_label_m = tk.Label(frame_m, text='Term: ')
    term_label_m.grid(row=2, column=0)
    term_dropdown_m = tk.OptionMenu(frame_m, term_var, *terms)
    term_dropdown_m.grid(row=2, column=1, padx=5, pady=5)
    grade_label = tk.Label(frame_m, text='Grade: ')
    grade_label.grid(row=3, column=0)
    grade_dropdown = tk.OptionMenu(frame_m, grade_var, *grades)
    grade_dropdown.grid(row=3, column=1, padx=5, pady=5)

    generate_button = tk.Button(frame_m, text='Generate all students PDF',
                                command=lambda: create_all_student_pdf(student_id_entry.get(), name_entry.get(),
                                                                       year_var.get(), term_var.get(), logged_in_user,
                                                                       grade_var.get()))
    generate_button.grid(row=4, columnspan=2, padx=5, pady=5)


def create_upload_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    # Create a dropdown menu
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])
    term_dropdown = tk.OptionMenu(frame, term_var, *terms)
    year_dropdown = tk.OptionMenu(frame, year_var, *years)
    term_dropdown.grid(row=0, column=1, padx=5, pady=5)
    year_dropdown.grid(row=1, column=1, padx=5, pady=5)
    term_label = tk.Label(frame, text='Term: ')
    term_label.grid(row=0, column=0)
    year_label = tk.Label(frame, text='Year: ')
    year_label.grid(row=1, column=0)

    upload_button = tk.Button(frame, text='Upload', command=lambda: open_file())
    upload_button.grid(row=5, columnspan=2, pady=10)

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
        if file_path:
            threading.Thread(target=process_file, args=(file_path,)).start()

    def process_file(file_path):
        # Create a top-level window for progress bar
        progress_window = Tk()
        progress_window.title('Processing data')

        # Set up the progress bar
        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=300, mode='determinate')
        progress_bar.pack(pady=10)
        try:
            df = pd.read_excel(file_path)
            # Calculate the step size for each update
            step_size = 100 / len(df.index)
            # Assuming columns A, B, and C correspond to student_id, name, admission_no, stream, grade, amount_expected, amount_paid, balance
            for index, row in df.iterrows():
                row = row.where(pd.notnull(row), None)
                add_student(row['Name'], row['Admission Number'], row['Stream'], row['Grade'], row['Amount Expected'],
                            row['Amount Paid'], row['Balance'], term_var.get(), year_var.get(), show_messagebox=False)

                # Update the progress bar
                progress_bar['value'] += step_size
                progress_window.update_idletasks()

            messagebox.showinfo("Success", "File processed and students added successfully")

            # close the progress window after completion
            progress_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")
