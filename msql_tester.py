import mysql.connector

myconn = mysql.connector.connect(host='localhost', user='root', password="")

if myconn.is_connected():
    print('Successful')
