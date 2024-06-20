import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
import num2words


def number_to_words(money):
    return num2words.num2words(money, to='cardinal')


image = 'logo.JPG'
name = 'Brun Allan'
title = 'Nyabondo Boys Boarding Comprehensive School'
subTitle01 = 'PO Box 212-Sondu Tel: 0741449228/0741455491'
subTitle02 = 'Email: nyabondobb@yahoo.com'
subTitle03 = 'SCHOOL OFFICIAL RECEIPT'
admission_no = 8714
receipt_no = 1
grade = '4'
date = datetime.time()
stream = 'W'
money = round(8550)
admission_date = 2021
balance = 1000
signed = 'admin'

pdf = canvas.Canvas('test_file.pdf')
pdf.setTitle('Creating a pdf')

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
pdf.drawString(60, 650, f'Receipt No: {receipt_no}')
pdf.drawString(250, 650, f'Adm No: {admission_no}')
pdf.drawString(400, 650, f'Date: {date}')

# SubTitle 5
pdf.drawString(60, 630, f'Received From: {name}')
pdf.drawString(400, 630, f'Class {grade}{stream}')
pdf.line(50, 625, 550, 625)

# SubTitle 6
pdf.drawString(60, 600, f'Sum of Kshs: {number_to_words(money)}')

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

# Internal vertical line
pdf.line(70, 590, 70, 160)  # Left

# Text
pdf.drawString(80, 180, 'Total:')  # Total
pdf.drawString(490, 180, f'{money:,}')  # Amount: 134

pdf.save()
