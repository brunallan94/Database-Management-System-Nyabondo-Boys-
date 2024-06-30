from tkinter import filedialog, messagebox, HORIZONTAL, Tk
from student import add_student, add_student_details, create_student_pdf, search_students, update_student, create_all_student_pdf
import pandas as pd
import ttkbootstrap as ttk

# Initialize selected student_id
selected_student_id = None


def create_main_page_ui(tab) -> None:
    # Showcase the database being used
    database_used_frame = ttk.Frame(tab)
    database_used_frame.grid(padx=5, pady=5, sticky='w')

    dat = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    database_choice_label = ttk.Label(database_used_frame, text='Database', font=('Times-Roman', 14))
    database_choice_label.grid(row=0, column=0, sticky='ns')
    database_choice_combobox = ttk.Combobox(database_used_frame, textvariable=dat_var, values=dat, state='readonly', bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=1, pady=10, sticky='ns')
    database_choice_combobox.current(0)

    # Search frame for displaying results
    search_frame = ttk.Frame(tab)
    search_frame.grid(padx=30, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade']
    result_tree1 = ttk.Treeview(search_frame, columns=columns, show='headings')
    result_tree1.grid(row=0, column=0, columnspan=4, ipadx = 15, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree1.heading(col, text=col, anchor='center')
        result_tree1.column(col, width=125, minwidth=25)

    # Labelframe for upload of student information
    upload_frame = ttk.Frame(tab)
    upload_frame.grid(padx=15, pady=15, sticky='ew')

    upload_labelframe = ttk.Labelframe(upload_frame, text='Upload')
    upload_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    upload_button = ttk.Button(upload_labelframe, text='Upload', command=lambda: open_file(), bootstyle=('INFO', 'OUTLINE'))
    upload_button.grid(row=0, column=0, padx=12, pady=5, sticky='ew')

    def open_file():
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
        if file_path:
            process_file(file_path)

    def process_file(file_path):
        # Create a top-level window for progress bar
        progress_window = ttk.Toplevel()
        progress_window.title('Processing data')

        # Set up the progress bar
        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=300, mode='determinate')
        progress_bar.pack(pady=10)

        lb = ttk.Label(progress_window, text='', font='arial 15 bold')
        lb.pack(padx=80)
        try:
            df = pd.read_excel(file_path)
            # Calculate the step size for each update
            step_size = 100 / len(df.index)
            # Assuming columns A, B, and C correspond to student_id, name, admission_no, stream, grade
            for index, row in df.iterrows():
                row = row.where(pd.notnull(row), None)
                add_student(row['Name'], row['Admission Number'], row['Stream'], row['Grade'], dat_var.get(), show_messagebox=False)

                # Update the progress bar
                progress_bar['value'] += step_size
                lb.config(text=f'{int(progress_bar['value'])}%')
                progress_window.update_idletasks()

            messagebox.showinfo("Success", "File processed and students added successfully")

            # close the progress window after completion
            progress_window.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to process file: {e}")


def create_search_student_ui(tab) -> None:
    # Showcase the database being used
    database_used_frame = ttk.Frame(tab)
    database_used_frame.grid(padx=15, pady=15, sticky='wn')

    dat = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    database_choice_label = ttk.Label(database_used_frame, text='Database', font=('Times-Roman', 12))
    database_choice_label.grid(row=0, column=0, sticky='ns')
    database_choice_combobox = ttk.Combobox(database_used_frame, textvariable=dat_var, values=dat, state='readonly', bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=1, pady=10, sticky='ns')
    database_choice_combobox.current(0)

    # create a search input frame
    search_input_frame = ttk.Frame(tab)
    search_input_frame.grid(padx=15, pady=15, sticky='ew')

    # Search input labelframe
    search_input_labelframe = ttk.Labelframe(search_input_frame, text='Search Inputs')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    # Search input label, entry, term and button
    terms = ['payments_term1', 'payments_term2', 'payments_term3']
    terms_var2 = ttk.StringVar()
    search_label = ttk.Label(search_input_labelframe, text='Enter Name')
    search_label.grid(row=0, column=0, padx=12, pady=5, sticky='w')
    search_entry = ttk.Entry(search_input_labelframe, bootstyle='SUCCESS')
    search_entry.grid(row=0, column=1, padx=5, sticky='ew')
    term_label = ttk.Label(search_input_labelframe, text='Term')
    term_label.grid(row=0, column=2, padx=12, pady=5)
    term_combobox = ttk.Combobox(search_input_labelframe, textvariable=terms_var2, values=terms, state='readonly')
    term_combobox.grid(row=0, column=3, padx=5, sticky='ew')
    term_combobox.current(0)
    search_button = ttk.Button(search_input_labelframe, text='Search', command=lambda: search_and_display(search_entry, result_tree2, terms_var2))
    search_button.grid(row=0, column=5, padx=18, ipadx=20, sticky='ew')

    # Search frame for displaying results
    search_frame = ttk.Frame(tab)
    search_frame.grid(padx=15, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade']
    result_tree2 = ttk.Treeview(search_frame, columns=columns, show='headings')
    result_tree2.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree2.heading(col, text=col, anchor='center')
        result_tree2.column(col, width=125, minwidth=25)  # Set a fixed width for each column

    # Input frame for inputting data
    input_frame = ttk.Frame(tab)
    input_frame.grid(padx=15, pady=15, sticky='ew')

    input_labelframe = ttk.Labelframe(input_frame, text='Edit Inputs')
    input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    name_label = ttk.Label(input_labelframe, text='Name')
    name_label.grid(row=0, column=0, padx=5, sticky='w')
    name_entry = ttk.Entry(input_labelframe)
    name_entry.grid(row=0, column=1, padx=5, sticky='ew')

    adm_label = ttk.Label(input_labelframe, text='Admission Number')
    adm_label.grid(row=0, column=2, padx=5, sticky='w')
    adm_entry = ttk.Entry(input_labelframe)
    adm_entry.grid(row=0, column=3, padx=5, sticky='ew')

    stream_label = ttk.Label(input_labelframe, text='Stream')
    stream_label.grid(row=0, column=4, padx=5, sticky='w')
    stream_entry = ttk.Entry(input_labelframe)
    stream_entry.grid(row=0, column=5, padx=5, sticky='ew')

    grade_label = ttk.Label(input_labelframe, text='Grade')
    grade_label.grid(row=0, column=6, padx=5, sticky='w')
    grade_entry = ttk.Entry(input_labelframe)
    grade_entry.grid(row=0, column=7, padx=5, sticky='ew')

    # Labelframe for update of student information
    button_frame = ttk.Frame(tab)
    button_frame.grid(padx=15, pady=15, sticky='news')

    edits_labelframe = ttk.Labelframe(button_frame, text='Buttons')
    edits_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    save_button = ttk.Button(edits_labelframe, text='Save Edit', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    save_button.grid(row=0, column=0, padx=12, pady=5, sticky='ew')

    add_button = ttk.Button(edits_labelframe, text='Add Student', command=add_student(name_entry.get(), adm_entry.get(), stream_entry.get(), grade_entry.get(), dat_var.get()), bootstyle=('SUCCESS', 'OUTLINE'))
    add_button.grid(row=0, column=1, padx=12, pady=5, sticky='ew')

    delete_button = ttk.Button(edits_labelframe, text='Delete Student', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    delete_button.grid(row=0, column=2, padx=12, pady=5, sticky='ew')

    # Function to handle the selection of an item for editing
    def on_edit_selected(event):
        # store the student ID in a variable that can be accessed by update_student_info
        global selected_student_id

        item = result_tree2.selection()[0]
        if item:
            values = result_tree2.item(item, 'values')
            selected_student_id = values[0]
            name_entry.delete(0, ttk.END)
            name_entry.insert(0,)
            adm_entry.delete(0, ttk.END)
            adm_entry.insert(0, )
            stream_entry.delete(0, ttk.END)
            stream_entry.insert(0, )
            grade_entry.delete(0, ttk.END)
            grade_entry.insert(0, )

    result_tree2.bind('<Double-1>', on_edit_selected)

    def update_student_info(search_entry, result_tree2):
        # Use global variable to access the student ID
        global selected_student_id

        # update student into the database
        update_student(selected_student_id, name_entry.get(), adm_entry.get(), stream_entry.get(), grade_entry.get(), terms_var2.get())

        # Refresh the tree view/ search results
        search_and_display(search_entry, result_tree2, terms_var2)
        selected_student_id = None  # Reset selected student_id after updating


def search_and_display(search_entry, result_tree2, terms_var2):
    # Get search query and term
    query = search_entry.get()
    term = terms_var2.get()
    # Perform Search
    results = search_students(query, term)
    # Clear the existing contents of the treeview
    for r in result_tree2.get_children():
        result_tree2.delete(r)
    # Insert new search results
    for result in results:
        result_tree2.insert('', 'end', values=result)


def create_download_ui(tab, logged_in_user) -> None:
    # Showcase the database being used
    database_used_frame = ttk.Frame(tab)
    database_used_frame.grid(padx=15, pady=15, sticky='w')
    dat = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    database_choice_label = ttk.Label(database_used_frame, text='Database', font=('Times-Roman', 12))
    database_choice_label.grid(row=0, column=0, sticky='w')
    database_choice_combobox = ttk.Combobox(database_used_frame, textvariable=dat_var, values=dat, state='readonly', bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=1, pady=10, sticky='w')
    database_choice_combobox.current(0)

    # Create a search input frame
    search_input_frame = ttk.Frame(tab)
    search_input_frame.grid(padx=15, pady=15, sticky='ew')

    # Search input labelframe
    search_input_labelframe = ttk.Labelframe(search_input_frame, text='Search Inputs')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    # Search input label, entry, term and button
    terms = ['payments_term1', 'payments_term2', 'payments_term3']
    terms_var = ttk.StringVar()
    search_label = ttk.Label(search_input_labelframe, text='Student ID')
    search_label.grid(row=0, column=0, padx=12, pady=5, sticky='w')
    search_entry = ttk.Entry(search_input_labelframe, bootstyle='SUCCESS')
    search_entry.grid(row=0, column=1, padx=5, sticky='ew')
    term_label = ttk.Label(search_input_labelframe, text='Term')
    term_label.grid(row=0, column=2, padx=12, pady=5)
    term_combobox = ttk.Combobox(search_input_labelframe, textvariable=terms_var, values=terms, state='readonly')
    term_combobox.grid(row=0, column=3, padx=5, sticky='ew')
    term_combobox.current(0)
    search_button = ttk.Button(search_input_labelframe, text='Search', command=search_and_display)
    search_button.grid(row=0, column=5, padx=18, ipadx=20, sticky='ew')

    # Search frame for displaying results
    search_frame = ttk.Frame(tab)
    search_frame.grid(padx=15, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=2)
    search_frame.grid_columnconfigure(0, weight=3)
    search_frame.grid_columnconfigure(0, weight=4)
    search_frame.grid_columnconfigure(0, weight=5)
    search_frame.grid_columnconfigure(0, weight=6)

    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Student ID', 'Amount Expected', 'Amount Paid', 'Balance', 'Date OP', 'Payment Method', 'Transaction']
    result_tree = ttk.Treeview(search_frame, columns=columns, show='headings')
    result_tree.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree.heading(col, text=col, anchor='center')
        result_tree.column(col, width=125, minwidth=25)

    # Input frame for inputting data
    input_frame = ttk.Frame(tab)
    input_frame.grid(padx=15, pady=15, sticky='ew')

    input_labelframe = ttk.Labelframe(input_frame, text='Edit Inputs')
    input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    student_id_label = ttk.Label(input_labelframe, text='Student ID')
    student_id_label.grid(row=0, column=0, padx=5, sticky='w')
    student_id_entry = ttk.Entry(input_labelframe)
    student_id_entry.grid(row=0, column=1, padx=5, sticky='ew')

    amount_expected_label = ttk.Label(input_labelframe, text='Amount Expected')
    amount_expected_label.grid(row=0, column=2, padx=5, sticky='w')
    amount_expected_entry = ttk.Entry(input_labelframe)
    amount_expected_entry.grid(row=0, column=3, padx=5, sticky='ew')

    amount_paid_label = ttk.Label(input_labelframe, text='Amount Paid')
    amount_paid_label.grid(row=0, column=4, padx=5, sticky='w')
    amount_paid_entry = ttk.Entry(input_labelframe)
    amount_paid_entry.grid(row=0, column=5, padx=5, sticky='ew')

    balance_label = ttk.Label(input_labelframe, text='Balance')
    balance_label.grid(row=0, column=6, padx=5, sticky='w')
    balance_entry = ttk.Entry(input_labelframe)
    balance_entry.grid(row=0, column=7, padx=5, sticky='ew')

    dop_label = ttk.Label(input_labelframe, text='Date Of Payment')
    dop_label.grid(row=1, column=0, padx=5, pady=8, sticky='w')
    dop_entry = ttk.Entry(input_labelframe)
    dop_entry.grid(row=1, column=1, padx=5, pady=8, sticky='ew')

    method_of_payment_label = ttk.Label(input_labelframe, text='Method Of Payment')
    method_of_payment_label.grid(row=1, column=2, padx=5, pady=8, sticky='w')
    method_of_payment_entry = ttk.Entry(input_labelframe)
    method_of_payment_entry.grid(row=1, column=3, padx=5, pady=8, sticky='ew')

    transaction_label = ttk.Label(input_labelframe, text='Transaction')
    transaction_label.grid(row=1, column=4, padx=5, pady=8, sticky='w')
    transaction_entry = ttk.Entry(input_labelframe)
    transaction_entry.grid(row=1, column=5, padx=5, pady=8, sticky='ew')

    save_button = ttk.Button(input_labelframe, text='Save Edit', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    save_button.grid(row=2, column=3, padx=12, pady=5, sticky='ew')

    add_button = ttk.Button(input_labelframe, text='Add Student', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    add_button.grid(row=2, column=4, padx=12, pady=5, sticky='ew')

    delete_button = ttk.Button(input_labelframe, text='Delete Student', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    delete_button.grid(row=2, column=5, padx=12, pady=5, sticky='ew')

    # Labelframe for update of student information
    download_frame = ttk.Frame(tab)
    download_frame.grid(padx=15, pady=15, sticky='ew')

    download_labelframe = ttk.Labelframe(download_frame, text=' Downloads and upload')
    download_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    term_label = ttk.Label(download_labelframe, text='Term')
    term_label.grid(row=0, column=0, padx=5, pady=8, sticky='w')
    term_combobox = ttk.Combobox(download_labelframe, textvariable=terms_var, values=terms, state='readonly')
    term_combobox.grid(row=0, column=1, padx=5, pady=8, sticky='ew')
    term_combobox.current(0)

    student_id_label = ttk.Label(download_labelframe, text='Student ID')
    student_id_label.grid(row=0, column=2, padx=3, pady=8, sticky='w')
    student_id_entry = ttk.Entry(download_labelframe)
    student_id_entry.grid(row=0, column=3, padx=5, pady=8, sticky='ew')

    grade_label = ttk.Label(download_labelframe, text='Grade')
    grade_label.grid(row=0, column=4, padx=5, pady=8, sticky='w')
    grade_entry = ttk.Entry(download_labelframe)
    grade_entry.grid(row=0, column=5, padx=5, pady=8, sticky='ew')

    single_button = ttk.Button(download_labelframe, text='Single Download', bootstyle=('SUCCESS', 'OUTLINE'), command=lambda: create_student_pdf(
        student_id_entry.get(), terms_var.get(), logged_in_user))
    single_button.grid(row=1, column=2, columnspan=2, padx=6, pady=5, sticky='ew')

    multiple_button = ttk.Button(download_labelframe, text='Multiple Download', bootstyle=('SUCCESS', 'OUTLINE'), command=lambda: create_all_student_pdf(
        terms_var, logged_in_user, grade_entry.get()))
    multiple_button.grid(row=1, column=4, columnspan=2, padx=6, pady=5, sticky='ew')

    upload_button = ttk.Button(download_labelframe, text='Upload', bootstyle=('SUCCESS', 'OUTLINE'), command='disabled')
    upload_button.grid(row=1, column=6, columnspan=2, padx=6, pady=5, sticky='ew')
