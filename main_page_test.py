import ttkbootstrap as ttk


def create_main_page_ui() -> None:
    root = ttk.Window(title='Search Window Test', themename='darkly')

    # Showcase the database being used
    database_used_frame = ttk.Frame(root)
    database_used_frame.grid(padx=15, pady=15, sticky='n')
    chosen_database_text = ttk.Label(database_used_frame, text='school_database_2024', bootstyle='INFO', font=('Times-Roman', 15))
    chosen_database_text.grid(row=0, column=0, pady=5, sticky='n')

    # Search frame for displaying results
    search_frame = ttk.Frame(root)
    search_frame.grid(padx=15, pady=15, sticky='news')
    search_frame.grid_rowconfigure(0, weight=1)
    search_frame.grid_columnconfigure(0, weight=1)

    # Treeview for displaying search results with horizontal scrollbar
    columns = ['ID', 'Name', 'Admission Number', 'Stream', 'Grade']
    result_tree = ttk.Treeview(search_frame, columns=columns, show='headings')
    result_tree.grid(row=0, column=0, columnspan=4, pady=10, sticky='news')

    # Set column headings and widths
    for col in columns:
        result_tree.heading(col, text=col, anchor='center')
        result_tree.column(col, width=125, minwidth=25)

    # Labelframe for upload of student information
    upload_frame = ttk.Frame(root)
    upload_frame.grid(padx=15, pady=15, sticky='ew')

    upload_labelframe = ttk.Labelframe(upload_frame, text='Upload')
    upload_labelframe.grid(row=0, column=0, ipadx=120, ipady=5, sticky='ew')

    save_button = ttk.Button(upload_labelframe, text='Upload', command='disabled', bootstyle=('INFO', 'OUTLINE'))
    save_button.grid(row=0, column=0, padx=12, pady=5, sticky='ew')

    root.mainloop()


if __name__ == '__main__':
    create_main_page_ui()