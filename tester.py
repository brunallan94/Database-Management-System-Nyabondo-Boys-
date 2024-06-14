from ui import create_student_ui, create_search_student_ui, create_download_and_upload_ui
import tkinter as tk


def open_main_application(logged_in_user):
    root = tk.Tk()
    root.title('Student Management System')

    tab_control = tk.ttk.Notebook(root)

    add_student_tab = tk.Frame(tab_control)
    payment_tab = tk.Frame(tab_control)
    search_student_tab = tk.Frame(tab_control)
    download_and_upload_tab = tk.Frame(tab_control)

    tab_control.add(add_student_tab, text='Add Student')
    tab_control.add(payment_tab, text='Payment')
    tab_control.add(search_student_tab, text='Search Student')
    tab_control.add(download_and_upload_tab, text='Download and Upload')

    tab_control.pack(expand=1, fill='both')

    create_student_ui(add_student_tab)
    # Uncomment and define create_payment_ui if you need it
    # create_payment_ui(payment_tab)
    create_search_student_ui(search_student_tab)
    create_download_and_upload_ui(download_and_upload_tab, logged_in_user)

    root.mainloop()
