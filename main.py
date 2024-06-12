import tkinter as tk
from ui import create_add_student_ui, create_payment_ui, create_search_student_ui


def main():
    root = tk.Tk()
    root.title("School Meals Payment System")

    # Create the UI components
    create_add_student_ui(root)
    create_payment_ui(root)
    global result_tree
    result_tree = create_search_student_ui(root)

    root.mainloop()


if __name__ == "__main__":
    # If you want to run main directly, you can uncomment the following line
    # main()
    pass
