from tkinter import filedialog
from student import still_in_development, get_greeting, add_student, update_student_download, delete_student_download, \
    show_data_main, show_data_search, process_file, add_student_details, create_student_pdf, show_data_download, \
    update_student, create_all_student_pdf, delete_student
import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry
import logging
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.tooltip import ToolTip

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize selected student_id
selected_student_id = None


def create_main_page_ui(tab, logged_in_user) -> None:
    # Showcase the database being used
    database_used_frame = ttk.Frame(tab)
    database_used_frame.grid(padx=15, pady=15, sticky='news')

    greeting = get_greeting(logged_in_user)
    greetings_label = ttk.Label(database_used_frame, text=f'{greeting}', font=('Gabriola', 18))
    greetings_label.grid(row=0, column=10, padx=150, sticky='e')

    # Search database labelframe
    search_input_labelframe = ttk.Labelframe(database_used_frame, text='Search database')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='w')

    dat: list[str] = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    database_choice_label = ttk.Label(search_input_labelframe, text='Database')
    database_choice_label.grid(row=0, column=2, sticky='e')
    database_choice_combobox = ttk.Combobox(search_input_labelframe, textvariable=dat_var, values=dat, state='readonly',
                                            bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=3, pady=10, sticky='e')
    database_choice_combobox.current(0)

    # Label to display the greeting and number of students
    info_label = ttk.Label(database_used_frame, text='', font=('Times-Roman', 12))
    info_label.grid(row=1, column=0, padx=15, pady=10, sticky='w')

    # Search frame for displaying results
    search_frame = ttk.Frame(tab)
    search_frame.grid(padx=15, pady=10, ipady=60, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns: list[str] = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade']
    result_tree1 = ttk.Treeview(search_frame, columns=columns, show='headings', bootstyle='SUCCESS')
    result_tree1.grid(row=0, column=0, padx=15, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree1.heading(col, text=col, anchor='center')
        result_tree1.column(col, width=210, anchor='center', minwidth=25)

    # Add vertical scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(search_frame, orient='vertical', command=result_tree1.yview, bootstyle='SUCCESS')
    result_tree1.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Show button to retrieve data
    show_button = ttk.Button(search_input_labelframe, text='Show',
                             command=lambda: show_data_main(result_tree1, dat_var, info_label), bootstyle='PRIMARY')
    show_button.grid(row=0, column=5, padx=20, ipadx=20, pady=5, sticky='e')

    # Labelframe for upload of student information
    upload_frame = ttk.Frame(tab)
    upload_frame.grid(padx=15, pady=15, sticky='ew')

    upload_labelframe = ttk.Labelframe(upload_frame, text='Upload')
    upload_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    def open_file() -> None:
        file_path = filedialog.askopenfilename(filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')])
        if file_path:
            process_file(file_path, dat_var)

    upload_button = ttk.Button(upload_labelframe, text='Upload', command=lambda: open_file(),
                               bootstyle=('INFO', 'OUTLINE'))
    upload_button.grid(row=0, column=0, padx=12, pady=5, sticky='ew')


def create_search_student_ui(tab, logged_in_user) -> None:
    # Showcase the database being used
    greetings_frame = ttk.Frame(tab)
    greetings_frame.grid(padx=15, pady=15, sticky='wn')

    greeting = get_greeting(logged_in_user)
    greetings_label = ttk.Label(greetings_frame, text=f'{greeting}', font=('Gabriola', 18))
    greetings_label.grid(row=0, column=0, sticky='wn')

    # create a search input frame
    search_input_frame = ttk.Frame(tab)
    search_input_frame.grid(padx=15, pady=15, sticky='ew')

    # Search input labelframe
    search_input_labelframe = ttk.Labelframe(search_input_frame, text='Search Inputs')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    # Search input label, entry, database and button
    dat: list[str] = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    search_label = ttk.Label(search_input_labelframe, text='Enter Name')
    search_label.grid(row=0, column=0, padx=12, pady=5, sticky='w')
    search_entry = ttk.Entry(search_input_labelframe, bootstyle='SUCCESS')
    search_entry.grid(row=0, column=1, padx=5, sticky='ew')
    database_choice_label = ttk.Label(search_input_labelframe, text='Database')
    database_choice_label.grid(row=0, column=2, padx=12, pady=5)
    database_choice_combobox = ttk.Combobox(search_input_labelframe, textvariable=dat_var, values=dat, state='readonly',
                                            bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=3, pady=10, sticky='ns')
    database_choice_combobox.current(0)

    # Search frame for displaying results
    search_frame = ttk.Frame(tab)
    search_frame.grid(padx=15, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns: list[str] = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade']
    result_tree2 = ttk.Treeview(search_frame, columns=columns, show='headings', bootstyle='SUCCESS')
    result_tree2.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree2.heading(col, text=col, anchor='center')
        result_tree2.column(col, width=125, anchor='center', minwidth=25)  # Set a fixed width for each column

    # Add vertical scrollbar to the Treeview
    scrollbar = ttk.Scrollbar(search_frame, orient='vertical', command=result_tree2.yview, bootstyle='SUCCESS')
    result_tree2.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Search button to retrieve data
    search_button = ttk.Button(search_input_labelframe, text='Search',
                               command=lambda: show_data_search(search_entry, result_tree2, dat_var))
    search_button.grid(row=0, column=5, padx=18, ipadx=20, sticky='ew')

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

    save_button = ttk.Button(edits_labelframe, text='Save Edit',
                             command=lambda: update_student_info(name_entry, adm_entry, stream_entry, grade_entry,
                                                                 dat_var, result_tree2, search_entry),
                             bootstyle=('SUCCESS', 'OUTLINE'))
    save_button.grid(row=0, column=0, padx=12, pady=5, sticky='ew')

    add_button = ttk.Button(edits_labelframe, text='Add Student',
                            command=lambda: add_student(name_entry.get(), adm_entry.get(), stream_entry.get(),
                                                        grade_entry.get(), dat_var.get()),
                            bootstyle=('WARNING', 'OUTLINE'))
    add_button.grid(row=0, column=1, padx=12, pady=5, sticky='ew')

    delete_button = ttk.Button(edits_labelframe, text='Delete Student',
                               command=lambda: delete_student_info(result_tree2, dat_var),
                               bootstyle=('DANGER', 'OUTLINE'))
    delete_button.grid(row=0, column=2, padx=12, pady=5, sticky='ew')

    # Function to handle the selection of an item for editing
    def on_edit_selected(event) -> None:
        item = result_tree2.selection()[0]
        if item:
            values = result_tree2.item(item, 'values')
            name_entry.delete(0, ttk.END)
            name_entry.insert(0, values[1])
            adm_entry.delete(0, ttk.END)
            adm_entry.insert(0, values[2])
            stream_entry.delete(0, ttk.END)
            stream_entry.insert(0, values[3])
            grade_entry.delete(0, ttk.END)
            grade_entry.insert(0, values[4])

    result_tree2.bind('<Double-1>', on_edit_selected)


def update_student_info(name_entry, adm_entry, stream_entry, grade_entry, dat_var, result_tree, search_entry) -> None:
    selected_item = result_tree.selection()
    if not selected_item:
        Messagebox.show_error('No student selected for editing', 'Error')
        return

    student_id: int = result_tree.item(selected_item, 'values')[0]
    name: str = name_entry.get()
    admission_number: int = adm_entry.get()
    stream: str = stream_entry.get()
    grade: int = grade_entry.get()
    database: str = dat_var.get()

    if not all([name, admission_number, stream, grade]):
        Messagebox.show_error('All fields must be filled out to update a student.', 'Error')
        return

    update_student(student_id, name, admission_number, stream, grade, database)
    show_data_search(search_entry, result_tree, dat_var)
    Messagebox.show_info('Student information updated successfully', 'Success')


def delete_student_info(result_tree, dat_var) -> None:
    selected_item = result_tree.selection()
    if not selected_item:
        Messagebox.show_error('No student selected for deletion', 'Error')
        return

    student_id = result_tree.item(selected_item, 'values')[0]
    database = dat_var.get()

    res = Messagebox.show_question('Are you sure you would like to delete this students info?', 'Confirmation',
                                   alert=True, buttons=['No:primary', 'Yes:danger'])
    if res == 'Yes':
        success, message = delete_student(student_id, database)
        if success:
            result_tree.delete(selected_item)
            Messagebox.show_info('Student deleted successfully', 'Success')
        else:
            Messagebox.show_error(f'Error: {message}', 'Error')


def create_download_ui(tab, logged_in_user) -> None:
    # Create a search input frame
    search_input_frame = ttk.Frame(tab)
    search_input_frame.grid(padx=15, pady=15, sticky='ew')

    # Search input labelframe
    search_input_labelframe = ttk.Labelframe(search_input_frame, text='Search Inputs')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    # Search input label, entry, term and button
    terms: list[str] = ['payments_term1', 'payments_term2', 'payments_term3']
    terms_var = ttk.StringVar()
    search_label = ttk.Label(search_input_labelframe, text='Student ID')
    search_label.grid(row=0, column=0, padx=12, pady=5, sticky='w')
    search_entry = ttk.Entry(search_input_labelframe, bootstyle='SUCCESS')
    search_entry.grid(row=0, column=1, padx=5, sticky='ew')
    term_label = ttk.Label(search_input_labelframe, text='Term')
    term_label.grid(row=0, column=2, padx=12, pady=5)
    term_combobox = ttk.Combobox(search_input_labelframe, textvariable=terms_var, values=terms, state='readonly',
                                 bootstyle='SUCCESS')
    term_combobox.grid(row=0, column=3, padx=5, sticky='ew')
    dat: list[str] = ['school_meals_2024', 'school_meals_2025', 'school_meals_2026']
    dat_var = ttk.StringVar()
    database_choice_label = ttk.Label(search_input_labelframe, text='Database', font=('Times-Roman', 12))
    database_choice_label.grid(row=0, column=4, sticky='w')
    database_choice_combobox = ttk.Combobox(search_input_labelframe, textvariable=dat_var, values=dat, state='readonly',
                                            bootstyle='SUCCESS')
    database_choice_combobox.grid(row=0, column=5, pady=10, sticky='w')

    # Input frame for displaying the searched student's name
    searched_name_frame = ttk.Frame(tab)
    searched_name_frame.grid(sticky='ew', padx=15, pady=10)
    searched_name_label = ttk.Label(searched_name_frame, text='', bootstyle='INFO', font=('Times-Roman', 18))
    searched_name_label.grid(row=0, column=0, padx=20, sticky='w')

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
    columns: list[str] = ['ID', 'Student ID', 'Amount Expected', 'Amount Paid', 'Balance', 'Date OP', 'Payment Method',
                          'Transaction']
    result_tree = ttk.Treeview(search_frame, columns=columns, show='headings', bootstyle='SUCCESS')
    result_tree.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree.heading(col, text=col, anchor='center')
        result_tree.column(col, anchor='center', width=125, minwidth=25)

    search_button = ttk.Button(search_input_labelframe, text='Search',
                               command=lambda: show_data_download(search_entry.get(), dat_var.get(), terms_var.get(),
                                                                  result_tree, searched_name_label))
    search_button.grid(row=0, column=6, padx=18, ipadx=20, sticky='ew')

    # Input frame for inputting data
    input_frame = ttk.Frame(tab)
    input_frame.grid(padx=15, pady=15, sticky='ew')

    input_labelframe = ttk.Labelframe(input_frame, text='Edit Inputs')
    input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    student_id_input_label = ttk.Label(input_labelframe, text='Student ID')
    student_id_input_label.grid(row=0, column=0, padx=5, sticky='w')
    student_id_input_entry = ttk.Entry(input_labelframe)
    student_id_input_entry.grid(row=0, column=1, padx=5, sticky='ew')

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
    dop_entry = DateEntry(input_labelframe, dateformat='%Y-%m-%d', bootstyle='SUCCESS')
    dop_entry.grid(row=1, column=1, padx=5, pady=8, sticky='ew')

    method_of_payment: list[str] = ['Mpesa', 'Cash']
    method_of_payment_var = ttk.StringVar()
    method_of_payment_label = ttk.Label(input_labelframe, text='Method Of Payment')
    method_of_payment_label.grid(row=1, column=2, padx=5, pady=8, sticky='w')
    method_of_payment_entry = ttk.Combobox(input_labelframe, textvariable=method_of_payment_var,
                                           values=method_of_payment, state='readonly', bootstyle='SUCCESS')
    method_of_payment_entry.grid(row=1, column=3, padx=5, pady=8, sticky='ew')

    transaction_label = ttk.Label(input_labelframe, text='Transaction')
    transaction_label.grid(row=1, column=4, padx=5, pady=8, sticky='w')
    transaction_entry = ttk.Entry(input_labelframe)
    transaction_entry.grid(row=1, column=5, padx=5, pady=8, sticky='ew')

    save_button = ttk.Button(input_labelframe, text='Update Record (Edit)',
                             command=lambda: update_student_info_downloadui(student_id_input_entry,
                                                                            amount_expected_entry, amount_paid_entry,
                                                                            balance_entry, dop_entry,
                                                                            method_of_payment_var, transaction_entry,
                                                                            dat_var, terms_var, result_tree,
                                                                            search_entry),
                             bootstyle=('SUCCESS', 'OUTLINE'))
    save_button.grid(row=2, column=3, padx=12, pady=5, sticky='ew')

    add_button = ttk.Button(input_labelframe, text='Add Record',
                            command=lambda: add_student_details(student_id_input_entry.get(),
                                                                amount_expected_entry.get(), amount_paid_entry.get(),
                                                                balance_entry.get(), dop_entry.entry.get(),
                                                                method_of_payment_var.get(), transaction_entry.get(),
                                                                dat_var.get(), terms_var.get()),
                            bootstyle=('WARNING', 'OUTLINE'))
    add_button.grid(row=2, column=4, padx=12, pady=5, sticky='ew')

    delete_button = ttk.Button(input_labelframe, text='Delete Record',
                               command=lambda: delete_student_info_download(result_tree, dat_var, terms_var),
                               bootstyle=('DANGER', 'OUTLINE'))
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

    id_download_label = ttk.Label(download_labelframe, text='ID')
    id_download_label.grid(row=0, column=2, padx=3, pady=8, sticky='w')
    id_download_entry = ttk.Entry(download_labelframe)
    id_download_entry.grid(row=0, column=3, padx=5, pady=8, sticky='ew')

    student_id_download_label = ttk.Label(download_labelframe, text='Student ID')
    student_id_download_label.grid(row=0, column=4, padx=3, pady=8, sticky='w')
    student_id_download_entry = ttk.Entry(download_labelframe)
    student_id_download_entry.grid(row=0, column=5, padx=5, pady=8, sticky='ew')

    grade_label = ttk.Label(download_labelframe, text='Grade')
    grade_label.grid(row=0, column=6, padx=5, pady=8, sticky='w')
    grade_entry = ttk.Entry(download_labelframe)
    grade_entry.grid(row=0, column=7, padx=5, pady=8, sticky='ew')

    single_button = ttk.Button(download_labelframe, text='Single Download', bootstyle=('SUCCESS', 'OUTLINE'),
                               command=lambda: create_student_pdf(
                                   id_download_entry.get(), student_id_download_entry.get(), dat_var.get(),
                                   terms_var.get(), logged_in_user))
    single_button.grid(row=1, column=2, columnspan=2, padx=6, pady=5, sticky='ew')

    multiple_button = ttk.Button(download_labelframe, text='Multiple Download', bootstyle=('SUCCESS', 'OUTLINE'),
                                 command=lambda: create_all_student_pdf(
                                     terms_var.get(), dat_var.get(), logged_in_user, grade_entry.get()))
    multiple_button.grid(row=1, column=4, columnspan=2, padx=6, pady=5, sticky='ew')

    ToolTip(multiple_button, 'Ensure you have select the grade, year and database required',
            bootstyle=('INFO', 'INVERSE'))

    upload_button = ttk.Button(download_labelframe, text='Upload', bootstyle=('SUCCESS', 'OUTLINE'),
                               command=still_in_development)
    upload_button.grid(row=1, column=6, columnspan=2, padx=6, pady=5, sticky='ew')

    # Function to handle the selection of an item for editing
    def on_edit_selected2(event) -> None:
        item = result_tree.selection()[0]
        if item:
            values = result_tree.item(item, 'values')
            student_id_input_entry.delete(0, ttk.END)
            student_id_input_entry.insert(0, values[1])
            amount_expected_entry.delete(0, ttk.END)
            amount_expected_entry.insert(0, values[2])
            amount_paid_entry.delete(0, ttk.END)
            amount_paid_entry.insert(0, values[3])
            balance_entry.delete(0, ttk.END)
            balance_entry.insert(0, values[4])
            dop_entry.entry.delete(0, ttk.END)
            dop_entry.entry.insert(0, values[5])
            method_of_payment_var.set(values[6])
            transaction_entry.delete(0, ttk.END)
            transaction_entry.insert(0, values[7])

    result_tree.bind('<Double-1>', on_edit_selected2)


def update_student_info_downloadui(student_id_entry, amount_expected_entry, amount_paid_entry, balance_entry, dop_entry,
                                   method_of_payment_var, transaction_entry, dat_var, terms_var, result_tree,
                                   search_entry) -> None:
    selected_item = result_tree.selection()
    if not selected_item:
        Messagebox.show_error('No student selected for editing', 'Error')
        return

    first_id = result_tree.item(selected_item, 'values')[0]
    student_id: int = student_id_entry.get()
    amount_expected: int = amount_expected_entry.get()
    amount_paid: int = amount_paid_entry.get()
    balance: int = balance_entry.get()
    dop: str = dop_entry.entry.get()
    method_of_payment: str = method_of_payment_var.get()
    transaction: str = transaction_entry.get()
    database: str = dat_var.get()
    term: str = terms_var.get()

    if not all(
            [student_id, amount_expected, amount_paid, balance, dop, method_of_payment, transaction, database, term]):
        Messagebox.show_error('All fields must be filled out to update a student.', 'Error')
        return

    update_student_download(first_id, student_id, amount_expected, amount_paid, balance, dop, method_of_payment,
                            transaction, database, term)
    show_data_download(search_entry, dat_var, terms_var, result_tree)
    Messagebox.show_info('Student information updated successfully', 'Success')


def delete_student_info_download(result_tree, dat_var, terms_var) -> None:
    selected_item = result_tree.selection()
    if not selected_item:
        Messagebox.show_error('No student selected for deletion', 'Error')
        return

    student_id = result_tree.item(selected_item, 'values')[0]
    database = dat_var.get()
    term = terms_var.get()

    res = Messagebox.show_question('Are you sure you would like to delete this students info?', 'Confirmation',
                                   alert=True, buttons=['No:secondary', 'Yes:danger'])

    if res == 'Yes':
        success, message = delete_student_download(student_id, database, term)
        if success:
            result_tree.delete(selected_item)
            Messagebox.show_info('Student deleted successfully', 'Success')
        else:
            Messagebox.show_error(f'Error: {message}', 'Error')