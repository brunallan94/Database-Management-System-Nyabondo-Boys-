import tkinter as tk
from tkinter import messagebox
from db_connection import create_connection
import mysql.connector


def authenticate(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
        return False
    finally:
        cursor.close()
        conn.close()


def login(open_main_application):
    username = username_entry.get()
    password = password_entry.get()
    if authenticate(username, password):
        messagebox.showinfo("Success", "Login successful")
        root.destroy()  # Close the login window
        open_main_application()  # Open the main application window
    else:
        messagebox.showerror("Error", "Invalid username or password")


def create_login_window(open_main_application):
    global root, username_entry, password_entry

    root = tk.Tk()
    root.title("Login")
    root.configure(bg='#333333')

    frame = tk.Frame(root, bg='#333333')
    frame.pack(padx=10, pady=10)

    text_label = tk.Label(frame, text="LOGIN", bg='#333333',
                          fg='#FF3399', font=('Arial', 30), pady=40)
    text_label.grid(row=0, column=0, columnspan=2, sticky='news')

    username_label = tk.Label(frame, text="Username",
                              bg='#333333', fg='#FFFFFF', font=('Arial', 16))
    username_label.grid(row=1, column=0)
    username_entry = tk.Entry(frame, font=('Arial', 16))
    username_entry.grid(row=1, column=1, pady=10)

    password_label = tk.Label(frame, text="Password",
                              bg='#333333', fg='#FFFFFF', font=('Arial', 16))
    password_label.grid(row=2, column=0)
    password_entry = tk.Entry(frame, show="*", font=('Arial', 16))
    password_entry.grid(row=2, column=1, pady=10)

    login_button = tk.Button(
        frame, text="Login", command=lambda: login(open_main_application), bg='#FF3399', fg='#FFFFFF', font=('Arial', 10), pady=8)
    login_button.grid(row=3, columnspan=3)

    root.mainloop()
