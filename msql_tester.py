import mysql.connector

myconn = mysql.connector.connect(
    host='localhost', user='root', password="1998")

if myconn.is_connected():
    print('Successful')
