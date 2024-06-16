from tkinter import filedialog
import tkinter as tk


def open_file():
    file = filedialog.askopenfile(
        mode='r',
        filetypes=[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')]
    )
    # Handle file as needed


def create_excel_ui():
    root = tk.Tk()
    root.title('Open Excel')
    root.geometry('600x400')

    button = tk.Button(root, text='Open', command=open_file)
    button.pack()

    root.mainloop()
