from ui import create_main_page_ui, create_search_student_ui, create_download_ui
import ttkbootstrap as ttk


def open_main_application(logged_in_user=None):
    root = ttk.Window(title='Nyabondo Boys Student Meal Management System')

    tab_control = ttk.Notebook(root)

    # Create the tabs
    main_student_tab = ttk.Frame(tab_control)
    search_student_tab = ttk.Frame(tab_control)
    download_ui_tab = ttk.Frame(tab_control)

    # Add the tabs to the notebook
    tab_control.add(main_student_tab, text='Main')
    tab_control.add(search_student_tab, text='Search Student')
    tab_control.add(download_ui_tab, text='Downloads')

    tab_control.pack(expand=1, fill='both')

    create_main_page_ui(main_student_tab)
    create_search_student_ui(search_student_tab)
    create_download_ui(download_ui_tab, logged_in_user)

    root.mainloop()

if __name__ == '__main__':
    open_main_application()
