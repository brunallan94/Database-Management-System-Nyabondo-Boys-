import tkinter as tk
from tkinter import filedialog, messagebox, HORIZONTAL, Tk, ttk
from student import add_student, create_student_pdf, search_students, update_student, create_all_student_pdf
import pandas as pd
from tkcalendar import DateEntry

# Initialize selected student_id
selected_student_id = None


def create_student_ui(tab):
    frame = ttk.Frame(tab)
    frame.grid(padx=10, pady=10)

    # Create a dropdown menu for term and year
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    mode_of_payment = ['Mpesa', 'Cash']
    term_var = tk.IntVar()
    year_var = tk.IntVar()
    mode_of_payment_var = tk.StringVar()

    term_combobox = ttk.Combobox(frame, textvariable=term_var, values = terms, state='readonly')
    year_combobox = ttk.Combobox(frame, textvariable=year_var, values=years, state='readonly')

    term_combobox.grid(row=0, column=1, padx=5, pady=5)
    year_combobox.grid(row=1, column=1, padx=5, pady=5)
    term_combobox.current(0)
    year_combobox.current(0)
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

    date_of_payment_label = tk.Label(frame, text='Date Of Payment')
    date_of_payment_label.grid(row=4, column=2)
    date_of_payment_entry = DateEntry(frame, date_pattern='yyyy-mm-dd')
    date_of_payment_entry.grid(row=4, column=3)

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

    mode_of_payment_label = tk.Label(frame, text='Mode Of Payment')
    mode_of_payment_label.grid(row=9, column=0, padx=5, pady=5)
    mode_of_payment_combobox = ttk.Combobox(frame, textvariable=mode_of_payment_var, values=mode_of_payment, state='readonly')
    mode_of_payment_combobox.grid(row=9, column=1, padx=5, pady=5)
    mode_of_payment_combobox.current(0)

    transaction_label = tk.Label(frame, text='Transaction Code')
    transaction_label.grid(row=10, column=0, padx=5, pady=5, sticky='w')
    transaction_entry = ttk.Entry(frame)
    transaction_entry.grid(row=10, column=1, padx=5, pady=5, sticky='e')

    add_button = tk.Button(frame, text='Add Student',
                           command=lambda: add_student(name_entry.get(), admission_entry.get(), stream_entry.get(),
                                                       grade_entry.get(), amntexp_entry.get(), amntpaid_entry.get(),
                                                       balance_entry.get(), date_of_payment_entry.get_date(),
                                                       mode_of_payment_var.get(), transaction_entry.get(), term_var.get(), year_var.get()))
    add_button.grid(row=11, column=2, columnspan=2, pady=10)


def create_search_student_ui(tab):
    frame = ttk.Frame(tab)
    frame.grid(padx=15, pady=15, sticky='news')
    # Search label and entry
    search_label = tk.Label(frame, text='Enter Name')
    search_label.grid(row=0, column=4, padx=5, pady=5)
    search_entry = tk.Entry(frame)
    search_entry.grid(row=0, column=5, padx=5, pady=5)

    # Create a dropdown menu for terms and years
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])  # Set the default value
    term_dropdown = tk.OptionMenu(frame, term_var, *terms)
    year_dropdown = tk.OptionMenu(frame, year_var, *years)
    term_dropdown.grid(row=0, column=3, padx=5, pady=5)
    year_dropdown.grid(row=0, column=1, padx=5, pady=5)
    term_label = tk.Label(frame, text='Term: ')
    term_label.grid(row=0, column=2)
    year_label = tk.Label(frame, text='Year: ')
    year_label.grid(row=0, column=0)

    # Search frame for displaying results
    search_frame = tk.Frame(tab)
    search_frame.grid(padx=15, pady=15, sticky='news')
    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade', 'Amount Expected', 'Amount Paid', 'Balance',
        'Date Of Payment', 'Mode Of Payment', 'Transaction Code']
    result_tree = ttk.Treeview(search_frame, columns=columns, show='headings')

    # Set column headings and widths
    for col in columns:
        result_tree.heading(col, text=col)
        result_tree.column(col, width=150)  # Set a fixed width for each column

    # Create a horizontal scrollbar and configure it with the treeview
    h_scroll = ttk.Scrollbar(search_frame, orient='horizontal', command=result_tree.xview)
    result_tree.configure(xscrollcommand=h_scroll.set)
    h_scroll.grid(row=2, column=0, columnspan=4, sticky='ew')

    result_tree.grid(row=1, column=0, columnspan=4, pady=10, sticky='news')

    # Configure grid weights to allow treeview to expand
    search_frame.grid_rowconfigure(1, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(1, weight=1)
    search_frame.grid_columnconfigure(2, weight=1)

    # Edit frame for updating information
    edit_frame = tk.Frame(tab)
    edit_frame.grid(padx=15, pady=15)
    edit_frame.grid_remove()

    # fields for editing student information
    fields = [('Name', 2), ('Admission Number', 3), ('Stream', 4), ('Grade', 5), ('Amount Expected', 6), ('Amount Paid', 7), ('Balance', 8), ('Date Of Payment', 9), ('Mode Of Payment', 10), ('Transaction Code', 11)]

    entries = {}
    for field, row in fields:
        label = tk.Label(edit_frame, text=field)
        label.grid(row=row, column=0, padx=5, pady=5)
        entry= tk.Entry(edit_frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entries[field] = entry

    save_button = tk.Button(edit_frame, text='Save', command=lambda: update_student_info(search_entry, result_tree))
    save_button.grid(row=12, column=2, columnspan=2, pady=10)

    # Function to handle the selection of an item for editing
    def on_edit_selected(event):
        # store the student ID in a variable that can be accessed by update_student_info
        global selected_student_id

        item = result_tree.selection()[0]
        if item:
            values = result_tree.item(item, 'values')
            selected_student_id = values[0]
            for field, row in fields:
                entry = entries[field]
                entry.delete(0, tk.END)
                entry.insert(0, values[columns.index(field)])
            edit_frame.grid()

    result_tree.bind('<Double-1>', on_edit_selected)

    def update_student_info(search_entry, result_tree):
        # Use global variable to access the student ID
        global selected_student_id

        # update student into the database
        update_student(selected_student_id, entries['Name'].get(), entries['Admission Number'].get(), entries['Stream'].get(), entries['Grade'].get(), entries['Amount Expected'].get(),
                       entries['Amount Paid'].get(), entries['Balance'].get(), entries['Date Of Payment'].get(), entries['Mode Of Payment'].get(), entries['Transaction Code'].get(), year_var.get(),
                       term_var.get())

        # Refresh the tree view/ search results
        search_and_display()
        edit_frame.grid_remove()  # Hide edit form after update
        selected_student_id = None  # Reset selected student_id after updating

    def search_and_display():
        results = search_students(search_entry.get(), term_var.get(), year_var.get())
        # Clear the existing contents of the tree
        for r in result_tree.get_children():
            result_tree.delete(r)
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

    # Download information of a single student
    title_1 = ttk.Labelframe(frame_s, text='SINGLE STUDENT DOWNLOAD')
    title_1.grid(row=0, column=0, ipadx=100, ipady=10, columnspan=4, sticky='ew')
    # Combobox for year
    year_label_s = tk.Label(title_1, text='Year: ')
    year_label_s.grid(row=1, column=0, padx=5, pady=5, sticky='e')
    year_combobox_s = ttk.Combobox(title_1, textvariable=year_var, values=years, state='readonly')
    year_combobox_s.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    year_combobox_s.current(0)
    # Combobox for term
    term_label_s = tk.Label(title_1, text='Term: ')
    term_label_s.grid(row=2, column=0, padx=5, pady=5, sticky='e')
    term_combobox_s = ttk.Combobox(title_1, textvariable=term_var, values=terms, state='readonly')
    term_combobox_s.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    term_combobox_s.current(0)
    # Entry for student name
    name_label = tk.Label(title_1, text='Name')
    name_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')
    name_entry = tk.Entry(title_1)
    name_entry.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    # Entry for student ID
    student_id_label = tk.Label(title_1, text='Student ID')
    student_id_label.grid(row=4, column=0, sticky='e')
    student_id_entry = tk.Entry(title_1)
    student_id_entry.grid(row=4, column=1, padx=5, pady=5, sticky='w')

    pdf_button = tk.Button(title_1, text='Create PDF', command=lambda: create_student_pdf(
        student_id_entry.get(), name_entry.get(), year_var.get(), term_var.get(), logged_in_user))
    pdf_button.grid(row=5, columnspan=2, pady=10)

    frame_m = tk.Frame(tab)
    frame_m.pack(padx=10, pady=10)

    # Download information of multiple students
    title_2 = ttk.Labelframe(frame_m, text='MULTIPLE STUDENT DOWNLOAD')
    title_2.grid(row=0, column=1, ipadx=100, ipady=10, columnspan=4, sticky='ew')
    # Combobox for year
    year_label_m = tk.Label(title_2, text='Year: ')
    year_label_m.grid(row=1, column=0, sticky='e')
    year_combobox_m = ttk.Combobox(title_2, textvariable=year_var, values=years, state='readonly')
    year_combobox_m.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    year_combobox_m.current(0)
    # Combobox for term
    term_label_m = tk.Label(title_2, text='Term: ')
    term_label_m.grid(row=2, column=0, sticky='e')
    term_combobox_m = ttk.Combobox(title_2, textvariable=term_var, values=terms, state='readonly')
    term_combobox_m.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    term_combobox_m.current(0)
    # Combobox for grade
    grade_label = tk.Label(title_2, text='Grade: ')
    grade_label.grid(row=3, column=0, sticky='e')
    grade_combobox = ttk.Combobox(title_2, textvariable=grade_var, values=grades, state='readonly')
    grade_combobox.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    grade_combobox.current(0)

    generate_button = tk.Button(title_2, text='Generate all students PDF',
                                command=lambda: create_all_student_pdf(student_id_entry.get(), name_entry.get(),
                                                                       year_var.get(), term_var.get(), logged_in_user,
                                                                       grade_var.get()))
    generate_button.grid(row=4, columnspan=2, padx=5, pady=5)


def create_upload_ui(tab):
    frame = tk.Frame(tab)
    frame.pack(padx=10, pady=10)

    title_1 = ttk.Labelframe(frame, text='Upload student data to database')
    title_1.grid(row=0, column=1, ipadx=100, ipady=25)

    # Create a dropdown menu
    terms = [1, 2, 3]
    years = [2024, 2025, 2026]
    term_var = tk.StringVar()
    year_var = tk.StringVar()
    term_var.set(terms[0])  # Set the default value
    year_var.set(years[0])
    term_dropdown = tk.OptionMenu(title_1, term_var, *terms)
    year_dropdown = tk.OptionMenu(title_1, year_var, *years)
    term_dropdown.grid(row=1, column=1, padx=5, pady=5)
    year_dropdown.grid(row=2, column=1, padx=5, pady=5)
    term_label = tk.Label(title_1, text='Term: ')
    term_label.grid(row=1, column=0)
    year_label = tk.Label(title_1, text='Year: ')
    year_label.grid(row=2, column=0)

    upload_button = tk.Button(title_1, text='Upload', command=lambda: open_file())
    upload_button.grid(row=5, columnspan=2, pady=10)

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
        if file_path:
            process_file(file_path)

    def process_file(file_path):
        # Create a top-level window for progress bar
        progress_window = tk.Toplevel()
        progress_window.title('Processing data')

        # Set up the progress bar
        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=300, mode='determinate')
        progress_bar.pack(pady=10)

        lb = tk.Label(progress_window, text='', font='arial 15 bold')
        lb.pack(padx=80)
        try:
            df = pd.read_excel(file_path)
            # Calculate the step size for each update
            step_size = 100 / len(df.index)
            '''Assuming columns A, B, and C correspond to student_id, name, admission_no, stream, grade, amount_expected
            , amount_paid, balance, date_of_payment, mode_of_payment, transaction_code'''
            for index, row in df.iterrows():
                row = row.where(pd.notnull(row), None)
                add_student(row['Name'], row['Admission Number'], row['Stream'], row['Grade'], row['Amount Expected'],
                            row['Amount Paid'], row['Balance'], row['Date Of Payment'], row['Mode Of Payment'],
                            row['Transaction Code'], term_var.get(), year_var.get(), show_messagebox=False)

                # Update the progress bar
                progress_bar['value'] += step_size
                lb.config(text=f'{int(progress_bar['value'])}%')
                progress_window.update_idletasks()

            messagebox.showinfo("Success", "File processed and students added successfully")

            # close the progress window after completion
            progress_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")
