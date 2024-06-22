import mysql.connector
from db_connection import create_connection
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os
import num2words
import datetime


def add_student(name, admission_no, stream, grade, amount_expected, amount_paid, balance, term, year, show_messagebox=True):
    conn = create_connection()
    cursor = conn.cursor()
    table_name = f'year_{year}_term_{term}' # Construct the table name based on term and year
    try:
        cursor.execute(
            f"INSERT INTO {table_name} (name, admission_no, stream, grade, amount_expected, amount_paid, balance) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (name, admission_no, stream, grade, amount_expected, amount_paid, balance))
        conn.commit()
        if show_messagebox:
            messagebox.showinfo("Success", "Student added successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def search_students(name, term, year):
    conn = create_connection()
    cursor = conn.cursor()
    table_name = f'year_{year}_term_{term}' # Construct the table name based on term and year

    try:
        cursor.execute(f"SELECT id, name, admission_no, stream, grade, amount_expected, amount_paid, balance FROM {table_name} WHERE name LIKE %s",
            (f"%{name}%",))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def create_student_pdf(student_id, name, year, term,  logged_in_user):
    conn = create_connection()
    cursor = conn.cursor()
    table_name = f'year_{year}_term_{term}' # Construct the table name based on term and year

    try:
        cursor.execute(f"SELECT name, admission_no, stream, grade, amount_expected, amount_paid, balance FROM {table_name} WHERE id = %s", (student_id,))
        student_data = cursor.fetchone()
        if not student_data:
            messagebox.showerror("Error", "No student found with that ID")
            return

        name, admission_no, stream, grade, amount_expected, amount_paid, balance = student_data

        # Save PDF to a specific directory
        directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Nyabondo_boys_meals')
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        pdf_path = os.path.join(directory, f"{name}_meal_information.pdf")

        # Create pdf
        def number_to_words(balance):
            return num2words.num2words(balance, to='cardinal')

        image = 'logo.JPG'
        title = 'Nyabondo Boys Boarding Comprehensive School'
        subTitle01 = 'PO Box 212-Sondu Tel: 0741449228/0741455491'
        subTitle02 = 'Email: nyabondobb@yahoo.com'
        subTitle03 = 'SCHOOL OFFICIAL RECEIPT'
        receipt_no = 1
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        admission_date = 2021
        signed = 'admin'

        pdf = canvas.Canvas(pdf_path, pagesize=letter)
        pdf.setTitle('Personal student meal information receipt')

        # Vertical boundary line
        pdf.line(50, 800, 50, 100)  # Left
        pdf.line(550, 800, 550, 100)  # Right

        # Horizontal boundary line
        pdf.line(50, 800, 550, 800)  # Top
        pdf.line(50, 100, 550, 100)  # Bottom

        # Draw an image
        pdf.drawInlineImage(image, 60, 700)

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
        pdf.drawString(60, 650, f'Term: {term}  Year: {year}')
        pdf.drawString(250, 650, f'Adm No: {admission_no}')
        pdf.drawString(400, 650, f'Date: {date}')

        # SubTitle 5
        pdf.drawString(60, 630, f'Received From: {name}')
        pdf.drawString(400, 630, f'Class {grade}{stream}')
        pdf.line(50, 625, 550, 625)

        # SubTitle 6
        pdf.drawString(60, 600, f'Sum of Kshs: {number_to_words(balance)}')

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
        pdf.drawString(80, 530, 'Meal: Bread')
        pdf.drawString(80, 510, 'Amount Expected:')
        pdf.drawString(460, 510, f'{amount_expected}')
        pdf.drawString(80, 490, 'Amount Paid:')
        pdf.drawString(460, 490, f'{amount_paid}')

        # Internal vertical line
        pdf.line(70, 590, 70, 160)  # Left

        # Text
        pdf.drawString(80, 180, 'Total:')  # Total
        pdf.drawString(490, 180, f'{balance:,}')  # Amount: 134

        # Footer
        pdf.drawString(80, 145, f'Term {term} Fees balance:')
        pdf.drawString(490, 145, f'{balance}')
        pdf.drawString(60, 130, 'Mode of Payment:')
        pdf.drawString(490, 130, f'________')
        pdf.drawString(60, 110, 'Served By:')
        pdf.drawString(300, 110, f'{logged_in_user}')
        pdf.line(350, 110, 490, 110)

        pdf.save()

        messagebox.showinfo(
            "Success", f"PDF created successfully at {pdf_path}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def create_all_student_pdf(student_id, name, year, term, logged_in_user, selected_grade):
    conn = create_connection()
    cursor = conn.cursor()
    table_name = f'year_{year}_term_{term}' # Construct the table name based on term and year

    try:
        cursor.execute(
            f"SELECT name, admission_no, stream, grade, amount_expected, amount_paid, balance FROM {table_name} WHERE grade = %s",
            (selected_grade,))
        student_data = cursor.fetchall()
        if not student_data:
            messagebox.showerror("Error", "No student found in the selected grade")
            return

        # Save PDF to a specific directory
        directory = os.path.join(os.path.expanduser('~'), 'Downloads', 'Nyabondo_boys_meals')
        # Create directory if it doesn't exist
        if not os.path.exists(directory):
            os.makedirs(directory)

        pdf_path = os.path.join(directory, f"Grade{selected_grade}_students_meal_information_for_year{year}_term{term}.pdf")

        # Create PDF document
        pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

        # PDF Content
        image_path = 'logo.JPG'
        title = 'Nyabondo Boys Boarding Comprehensive School'
        subTitle01 = 'PO Box 212-Sondu Tel: 0741449228/0741455491'
        subTitle02 = 'Email: nyabondobb@yahoo.com'
        subTitle03 = 'SCHOOL OFFICIAL MEAL RECEIPT'
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Styles
        styles = getSampleStyleSheet()
        styleH = styles['Heading1']
        styleN = styles['Normal']

        # Build the PDF elements
        elements = []

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
        elements.append(Paragraph(f'Date: {date}', styleN))
        elements.append(Spacer(1, 12))

        # Table data
        data = [['No', 'Name', 'Admission No', 'Stream', 'Grade', 'Amount Expected', 'Amount Paid', 'Balance']]
        for idx, student in enumerate(student_data, start=1):
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

        messagebox.showinfo(
            "Success", f"PDF created successfully at {pdf_path}")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()


def update_student(student_id, name, admission_no, stream, grade, amount_exp, amount_paid, balance, year, term):
    conn = create_connection()
    cursor = conn.cursor()
    table_name = f'year_{year}_term_{term}' # Construct the table name based on term and year

    try:
        cursor.execute(
            f"UPDATE {table_name} SET name = %s, admission_no = %s, stream = %s, grade = %s, amount_expected = %s, amount_paid = %s, balance = %s WHERE id = %s", (name, admission_no, stream, grade, amount_exp, amount_paid, balance, student_id))
        conn.commit()
        messagebox.showinfo("Success", "Student updated successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
