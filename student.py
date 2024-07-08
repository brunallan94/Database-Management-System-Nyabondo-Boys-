from datetime import datetime
from typing import LiteralString
import mysql.connector
from db_connection import create_connection
from tkinter import HORIZONTAL
import ttkbootstrap as ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import pandas as pd
import sys
import num2words
import datetime
import logging
from ttkbootstrap.dialogs.dialogs import Messagebox

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def still_in_development() -> None:
    Messagebox.show_info('We are still working on this feature', 'Development')


def add_student(name, admission_no, stream, grade, database, show_messagebox=True) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'USE {database}')
        cursor.execute("INSERT INTO students (name, admission_no, stream, grade) VALUES (%s, %s, %s, %s)",
                       (name, admission_no, stream, grade))
        conn.commit()
        if show_messagebox:
            Messagebox.show_info("Student added successfully", "Success")
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
        logging.error(f'Error adding student {err}')
    finally:
        cursor.close()
        conn.close()


def show_data_main(tree, database, info_label) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'USE {database.get()}')
        cursor.execute('SELECT * FROM students')
        records = cursor.fetchall()

        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)

        # Insert new rows
        for record in records:
            tree.insert('', 'end', values=record)

        # update the info_label with the number of students and greeting
        num_students: int = len(records)
        info_label.config(text=f'Number of students: {num_students}')

    except mysql.connector.Error as err:
        Messagebox.show_error(f'Error: {err}', 'Error')
        logging.error(f'Error fetching data: {err}')

    finally:
        cursor.close()
        conn.close()


def get_greeting(logged_in_user) -> str:
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        return f'Good Morning,  {logged_in_user}'
    elif 12 <= current_hour < 18:
        return f'Good Afternoon, {logged_in_user}'

    else:
        return f'Good Evening, {logged_in_user}'


def show_data_search(search_entry, tree, database) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    query = search_entry.get()
    try:
        cursor.execute(f'USE {database.get()}')
        cursor.execute(f"SELECT * FROM students WHERE name LIKE '%{query}%'")
        records = cursor.fetchall()
        # Clear existing rows
        for row in tree.get_children():
            tree.delete(row)
        # Insert new rows
        for record in records:
            tree.insert('', 'end', values=record)

    except mysql.connector.Error as err:
        Messagebox.show_error(f'Error: {err}', 'Error')
        logging.error(f'Error fetching data: {err}')

    finally:
        cursor.close()
        conn.close()


def process_file(file_path, dat_var) -> None:
    # Create a top-level window for progress bar
    progress_window = ttk.Toplevel()
    progress_window.title('Processing data')

    # Set up the progress bar
    progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=300, mode='determinate',
                                   bootstyle=('SUCCESS', 'STRIPED'))
    progress_bar.pack(pady=10)

    lb = ttk.Label(progress_window, text='', font='arial 15 bold')
    lb.pack(padx=80)
    try:
        df = pd.read_excel(file_path)
        # Calculate the step size for each update
        step_size = 100 / len(df.index)
        # Assuming columns A, B, and C correspond to student_id, name, admission_no, stream, grade
        for index, row in df.iterrows():
            row = row.where(pd.notnull(row), None)
            add_student(row['Name'], row['Admission Number'], row['Stream'], row['Grade'], dat_var.get(),
                        show_messagebox=False)

            # Update the progress bar
            progress_bar['value'] += step_size
            lb.config(text=f'{int(progress_bar["value"])}%')
            progress_window.update_idletasks()

        Messagebox.show_info("File processed and students added successfully", "Success")

        # Close the progress window after completion
        progress_window.destroy()

    except Exception as e:
        Messagebox.show_error(f"Failed to process file: {e}", 'Error')
        logging.error(f'Error processing file: {e}')


def add_student_details(student_id, amount_expected, amount_paid, balance, date_of_payment, method_of_payment,
                        transaction_code, dat_var, term, show_messagebox=True) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'USE {dat_var}')
        cursor.execute(
            f"INSERT INTO {term} (student_id, amount_expected, amount_paid, balance, date_of_payment, method_of_payment, transaction_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (student_id, amount_expected, amount_paid, balance, date_of_payment, method_of_payment, transaction_code))
        conn.commit()
        if show_messagebox:
            Messagebox.show_info("Student added successfully", "Success")
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
        logging.error(f'Error adding student {err}')
    finally:
        cursor.close()
        conn.close()


def update_student(student_id, name, admission_no, stream, grade, database) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'USE {database}')
        cursor.execute(f"UPDATE students SET name = %s, admission_no = %s, stream = %s, grade = %s WHERE id = %s",
                       (name, admission_no, stream, grade, student_id))
        conn.commit()
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
    finally:
        cursor.close()
        conn.close()


def update_student_download(first_id, student_id, amount_expected, amount_paid, balance, dop, method_of_payment,
                            transaction, database, term) -> None:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f'USE {database}')
        cursor.execute(
            f"UPDATE {term} SET student_id = %s, amount_expected = %s, amount_paid = %s, balance = %s, date_of_payment = %s, method_of_payment = %s, transaction_code = %s WHERE id = %s",
            (student_id, amount_expected, amount_paid, balance, dop, method_of_payment, transaction, first_id))
        conn.commit()
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
    finally:
        cursor.close()
        conn.close()


def delete_student(student_id, database) -> tuple[bool, str]:
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {database}')
        query = 'DELETE FROM students WHERE id = %s'
        cursor.execute(query, (student_id,))
        conn.commit()
        return True, 'Success'
    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()


def show_data_download(student_id, database, term, tree, searched_name) -> None:
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {database}')

        # Fetch and display the student's name
        cursor.execute(f'SELECT name FROM students WHERE id = %s', (student_id,))
        student_name = cursor.fetchone()
        if student_name:
            searched_name.config(text=f'{student_name[0]}')
        else:
            searched_name.config(text='Name not found')

        # Clear existing rows in the tree
        for row in tree.get_children():
            tree.delete(row)

        # Fetch and display the payment details
        cursor.execute(f"SELECT * FROM {term} WHERE student_id = {student_id}")
        results = cursor.fetchall()

        # Insert new rows
        for result in results:
            tree.insert('', 'end', values=result)

    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
        logging.error(f'Err {err}')

    finally:
        cursor.close()
        conn.close()


def delete_student_download(student_id, database, term) -> tuple[bool, str]:
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {database}')
        query = f'DELETE FROM {term} WHERE id = %s'
        cursor.execute(query, (student_id,))
        conn.commit()
        return True, 'Success'

    except mysql.connector.Error as err:
        return False, str(err)
    finally:
        cursor.close()
        conn.close()


def resource_path(relative_path) -> LiteralString | str | bytes:
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_student_pdf(id, student_id, database, term_var, logged_in_user) -> None:
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {database}')
        cursor.execute(f'SELECT name, admission_no, stream, grade FROM students WHERE id = %s', (student_id,))
        student_data = cursor.fetchone()
        if not student_data:
            Messagebox.show_error("No student found with that ID", 'Error')
            return

        cursor.execute(
            f'SELECT amount_expected, amount_paid, balance, date_of_payment, method_of_payment, transaction_code FROM {term_var} WHERE id = %s ORDER BY date_of_payment DESC LIMIT 1',
            (id,))
        details_data = cursor.fetchone()
        if not details_data:
            Messagebox.show_error('No payment details found for that student', 'Error')
            return

        name, admission_no, stream, grade = student_data
        amount_expected, amount_paid, balance, date_of_payment, mode_of_payment, transaction_code = details_data

        # Save PDF to a specific directory
        directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Nyabondo_boys_meals')
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        pdf_path = os.path.join(directory, f"{name}_meal_information.pdf")

        # Create pdf
        def number_to_words(amount_p) -> str:
            return num2words.num2words(amount_p, to='cardinal')

        image_path = resource_path('logo.JPG')
        title: str = 'Nyabondo Boys Boarding Comprehensive School'
        subTitle01: str = 'PO Box 212-Sondu Tel: 0741449228/0741455491'
        subTitle02: str = 'Email: nyabondobb@yahoo.com'
        subTitle03: str = 'SCHOOL OFFICIAL RECEIPT'
        date: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        pdf.setTitle('Personal student meal information receipt')

        # Vertical boundary line
        pdf.line(50, 785, 50, 100)  # Left
        pdf.line(550, 785, 550, 100)  # Right

        # Horizontal boundary line
        pdf.line(50, 785, 550, 785)  # Top
        pdf.line(50, 100, 550, 100)  # Bottom

        # Draw an image
        pdf.drawInlineImage(image_path, 60, 685)

        # Title
        pdf.setFont('Courier-Bold', 14)
        pdf.drawString(170, 770, title)
        pdf.line(170, 765, 530, 765)

        # SubTitle 1
        pdf.setFillColorRGB(0, 0, 255)
        pdf.setFont('Times-Roman', 14)
        pdf.drawString(170, 740, subTitle01)
        pdf.line(170, 735, 450, 735)

        # SubTitle 2
        pdf.drawString(250, 710, subTitle02)
        pdf.line(250, 705, 430, 705)

        # SubTitle 3
        pdf.drawString(230, 680, subTitle03)
        pdf.line(230, 675, 420, 675)

        # SubTitle 4
        pdf.drawString(60, 650, f'Term: {term_var[-1]}  Year: {database[-4:]}')
        pdf.drawString(250, 650, f'Adm No: {admission_no}')
        pdf.drawString(400, 650, f'Date: {date_of_payment}')

        # SubTitle 5
        pdf.drawString(60, 630, f'Received From: {name}')
        pdf.drawString(400, 630, f'Class {grade}{stream}')
        pdf.line(50, 625, 550, 625)

        # SubTitle 6
        pdf.drawString(60, 600, f'Sum of Kshs: {number_to_words(amount_paid)} Shillings Only.')

        # Heading
        pdf.setFillColorRGB(r=0, g=0, b=0)
        pdf.setFont('Times-Roman', 14)
        pdf.drawString(80, 570, 'Vote head')  # Vote head
        pdf.drawString(460, 570, 'Amount (Kshs)')  # Amount (Kshs)

        # Internal horizontal line
        pdf.line(70, 590, 550, 590)  # Top 1
        pdf.line(70, 550, 550, 550)  # Top 2
        pdf.line(70, 200, 550, 200)  # Bottom 1
        pdf.line(70, 160, 550, 160)  # Bottom 2

        # Text
        pdf.drawString(80, 530, 'Bread')
        #pdf.drawString(80, 510, 'Paid')
        pdf.drawString(490, 510, f'{amount_paid}')

        # Internal vertical line
        pdf.line(70, 590, 70, 160)  # Left

        # Text
        pdf.drawString(80, 180, 'Total:')  # Total
        pdf.drawString(490, 180, f'{amount_paid:,}')  # Amount: 134

        # Footer
        pdf.drawString(80, 145, f'Term {term_var[-1]} balance:')
        pdf.drawString(490, 145, f'{balance}')
        pdf.drawString(60, 130, f'Mode of Payment: {mode_of_payment}')
        pdf.drawString(440, 130, f'{transaction_code}')
        pdf.drawString(60, 110, f'Served By: {logged_in_user}')
        pdf.line(350, 110, 490, 110)
        pdf.setFont('Times-Roman', 9)
        pdf.drawString(430, 90, f'Print Date: {date}')

        pdf.save()
        Messagebox.show_info(f"PDF created successfully at {pdf_path}", "Success")
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
    finally:
        cursor.close()
        conn.close()


def create_all_student_pdf(term, database, logged_in_user, selected_grade) -> None:
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f'USE {database}')
        cursor.execute(f'SELECT id, name, admission_no, stream, grade FROM students WHERE grade = %s',
                       (selected_grade,))
        student_data = cursor.fetchall()
        if not student_data:
            Messagebox.show_error("No student found in the selected grade", 'Error')
            return

        # Prepare a list to hold combined student and payment data
        combined_data: list = []

        # Fetch payment details for each student from the term-specific table
        for student in student_data:
            student_id, name, admission_no, stream, grade = student
            cursor.execute(f'USE {database}')
            cursor.execute(
                f"SELECT amount_expected, amount_paid, balance FROM {term} WHERE student_id = %s ORDER BY date_of_payment DESC LIMIT 1",
                (student_id,))
            payment_data = cursor.fetchone()

            if payment_data:
                amount_expected, amount_paid, balance = payment_data
                combined_data.append((name, admission_no, stream, grade, amount_expected, amount_paid, balance))

        # Save PDF to a specific directory
        directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Nyabondo_boys_meals')
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        pdf_path = os.path.join(directory, f"Grade{selected_grade}_students_meal_information_for_{database[-4:]}_term{term[-1]}.pdf")

        # Create PDF document
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

        # PDF Content
        image_path = resource_path('logo.JPG')
        title: str = 'Nyabondo Boys Boarding Comprehensive School'
        subTitle01: str = 'PO Box 212-Sondu Tel: 0741449228/0741455491'
        subTitle02: str = 'Email: nyabondobb@yahoo.com'
        subTitle03: str = 'SCHOOL OFFICIAL MEAL RECEIPT STUDENT LIST'
        date: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Styles
        styles = getSampleStyleSheet()
        styleH = styles['Heading1']
        styleN = styles['Normal']

        # Build the PDF elements
        elements: list = []

        # Draw an image
        if os.path.exists(image_path):
            img = Image(image_path)
            img.drawHeight = 1.25 * inch
            img.drawWidth = 1.25 * inch
            elements.append(img)

        # Title and Subtitle
        elements.append(Paragraph(title, styleH))
        elements.append(Paragraph(subTitle01, styleN))
        elements.append(Paragraph(subTitle02, styleN))
        elements.append(Paragraph(subTitle03, styleN))
        elements.append(Paragraph(f'Date Printed: {date}', styleN))
        elements.append(Spacer(1, 12))

        # Table data
        data: list[list[str]] = [
            ['No', 'Name', 'Admission No', 'Stream', 'Grade', 'Amount Expected', 'Amount Paid', 'Balance']]
        for idx, student in enumerate(combined_data, start=1):
            data.append([idx] + list(student))

        # Create a Table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)

        # Footer
        elements.append(Spacer(1, 48))
        elements.append(Paragraph(f'Signed by: {logged_in_user}', styleN))

        # Build the pdf
        pdf.build(elements)

        Messagebox.show_info(f"PDF created successfully at {pdf_path}", "Success")
    except mysql.connector.Error as err:
        Messagebox.show_error(f"Error: {err}", 'Error')
    finally:
        cursor.close()
        conn.close()
