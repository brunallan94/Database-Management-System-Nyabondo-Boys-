import ttkbootstrap as ttk
from tkinter import StringVar

def search_and_display():
    # Placeholder for search functionality
    pass

def create_download_student_ui() -> None:
    root = ttk.Window(title='Download Window Test', themename='darkly')

    # Showcase the database being used
    database_used_frame = ttk.Frame(root)
    database_used_frame.grid(padx=15, pady=15, sticky='n')
    chosen_database_text = ttk.Label(database_used_frame, text='school_database_2024', bootstyle='INFO', font=('Times-Roman', 15))
    chosen_database_text.grid(row=0, column=0, pady=5, sticky='n')

    # Create a search input frame
    search_input_frame = ttk.Frame(root)
    search_input_frame.grid(padx=15, pady=15, sticky='ew')

    # Search input labelframe
    search_input_labelframe = ttk.Labelframe(search_input_frame, text='Search Inputs')
    search_input_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    # Search input label, entry, term and button
    terms = ['payments_term1', 'payments_term2', 'payments_term3']
    terms_var = StringVar()
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
    search_frame = ttk.Frame(root)
    search_frame.grid(padx=15, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Student ID', 'Amount Expected', 'Amount Paid', 'Balance', 'Date OP', 'Payment Method', 'Transaction']
    result_tree = ttk.Treeview(search_frame, columns=columns, show='headings')
    result_tree.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree.heading(col, text=col, anchor='center')
        result_tree.column(col, width=125, minwidth=25)

    # Edit frame for updating information
    edit_frame = ttk.Frame(root)
    edit_frame.grid(padx=15, pady=15, sticky='ew')
    edit_frame.grid_remove()

    # Input frame for inputting data
    input_frame = ttk.Frame(root)
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
    download_frame = ttk.Frame(root)
    download_frame.grid(padx=15, pady=15, sticky='ew')

    download_labelframe = ttk.Labelframe(download_frame, text=' Downloads')
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

    single_button = ttk.Button(download_labelframe, text='Single Download', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    single_button.grid(row=1, column=2, columnspan=2, padx=6, pady=5, sticky='ew')

    multiple_button = ttk.Button(download_labelframe, text='Multiple Download', command='disabled', bootstyle=('SUCCESS', 'OUTLINE'))
    multiple_button.grid(row=1, column=4, columnspan=2, padx=6, pady=5, sticky='ew')

    root.mainloop()

if __name__ == '__main__':
    create_download_student_ui()