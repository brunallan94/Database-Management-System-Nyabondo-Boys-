from tkinter import messagebox
from db_connection import create_connection
import mysql.connector
import ttkbootstrap as ttk
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def authenticate(username, password) -> tuple[bool, any]:
    global cursor, conn
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('USE school_meals_2024')
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            return True, username  # Return username if authentication is successful
        else:
            return False, None
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        logging.error(f'Database Error: {err}')
        return False, None
    finally:
        cursor.close()
        conn.close()


def login_command(open_main_application):
    username = username_entry.get()
    password = password_entry.get()
    success, logged_in_user = authenticate(username, password)
    if success:
        app.destroy() # Close the login window
        ttk.Style.instance = None
        open_main_application(logged_in_user)
    else:
        messagebox.showerror("Error", "Invalid username or password")
        logging.warning(f'Login failed for user: {username}')


def create_login_window(open_main_application) -> None:
    global app, username_entry, password_entry

    app = ttk.Window(themename='darkly', title='Login', size=(500, 350), position=(450, 250), resizable=(False, False))
    frame = ttk.Frame(app)
    frame.pack(padx=10, pady=10)

    text_label = ttk.Label(frame, text="LOGIN", font=('GothicE', 38))
    text_label.grid(row=0, column=0, columnspan=3, pady=20, sticky='ns')

    f_size = 14
    username_label = ttk.Label(frame, text="Username", font=('Times-Roman', f_size))
    username_label.grid(row=1, column=0, sticky='ns')
    username_entry = ttk.Entry(frame, font=('Times-Roman', f_size), bootstyle='SUCCESS')
    username_entry.grid(row=1, column=1, pady=10, sticky='ns')

    password_label = ttk.Label(frame, text="Password", font=('Times-Roman', f_size))
    password_label.grid(row=2, column=0, sticky='ns')
    password_entry = ttk.Entry(frame, show="*", font=('Times-Roman', f_size), bootstyle='SUCCESS')
    password_entry.grid(row=2, column=1, pady=10, sticky='ns')

    login_button = ttk.Button(frame, text="Login", command=lambda: login_command(open_main_application), bootstyle=('SUCCESS', 'OUTLINE'))
    login_button.grid(row=4, column=1, columnspan=3, sticky='e', ipadx=5, ipady=10, padx=40)

    quit_button = ttk.Button(frame, text='Quit', command=app.destroy, bootstyle=('DANGER', 'OUTLINE'))
    quit_button.grid(row=4, column=3, columnspan=3, sticky='e', ipadx=5, ipady=10, padx=40)

    app.mainloop()


