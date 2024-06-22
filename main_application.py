from ui import create_student_ui, create_search_student_ui, create_download_ui, create_upload_ui
import tkinter as tk
from tkinter import ttk


def open_main_application(logged_in_user):
    root = tk.Tk()
    root.title('Nyabondo Boys Student Meal Management System')

    tab_control = ttk.Notebook(root)

    add_student_tab = tk.Frame(tab_control)
    search_student_tab = tk.Frame(tab_control)
    download_and_upload_tab = tk.Frame(tab_control)
    upload_tab = tk.Frame(tab_control)

    tab_control.add(add_student_tab, text='Add Student')
    tab_control.add(search_student_tab, text='Search Student')
    tab_control.add(download_and_upload_tab, text='Download')
    tab_control.add(upload_tab, text='Upload')

    tab_control.pack(expand=1, fill='both')

    create_student_ui(add_student_tab)
    create_search_student_ui(search_student_tab)
    create_download_ui(download_and_upload_tab, logged_in_user)
    create_upload_ui(upload_tab)

    root.mainloop()
