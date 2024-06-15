This program consists of 9 files:

a). db_connection.py
-Deals with connecting the python code to the database by taking in inputs:
=host
=user
=password
=database

b). excel_tkinter_test.py
-Connects the ui with the option to add excel file (In the required format) to the database.
-It carries 2 functions: open_file() and create_excel_ui()
-open_file() handles the excel formats required and create_excel_ui() creates a front-end to easen the access of the function.

c). login.py
-Handles the login page ui and authentication of the user/password in the database to access the main application.
-It has 3 fuctions authenticate(), login() and create_login_window()
-authenticate() first connects to the database(user table) and checks if the char in the user and password columns align with the ones inserted into the front-end. If not an error window pops up.
-login() moves to the next step of opening the main application if its a success or error box if username or password fails.
-create_login_window() deals with the design of the login ui.

d). main.py
-Deals with launching the the entire app from login page to the main application.

e). payment.py
-Handles the payments for the students by inserting the:
=student_id
=meal_id
=amount into the database.
-If it succeds a message box appears to alert the user of the success.

f). student.py -
-Handles the student data by: 1. Inserting student data into the database. 2. Searching for students from the database throught the ui. 3. Updating student data in the database. 4. Deleting student data from the database. 5. Creates a pdf that holds students data.
-It has 5 functions: insert_student(), search_student(), update_student(), delete_student().
