This program consists of 7 python files and 1 image:

a). db_connection.py
-Deals with connecting the python code to the database by taking in inputs:
=host
=user
=password
=database

b). login.py
-Handles the login page ui and authentication of the user/password in the database to access the main application.
-It has 3 functions authenticate(), login() and create_login_window()
-authenticate() first connects to the database(user table) and checks if the char in the user and password columns align with the ones inserted into the front-end. If not an error window pops up.
-login() moves to the next step of opening the main application if its a success or error box if username or password fails.
-create_login_window() deals with the design of the login ui.

c). main.py
-Deals with launching the the entire app from login page to the main application.

d). student.py -
-Handles the student data by: 1. Inserting student data into the database. 2. Searching for students from the database throught the ui. 3. Updating student data in the database. 4. Deleting student data from the database. 5. Creates a pdf that holds students data.
-It has 5 functions: insert_student(), search_student(), update_student(), delete_student().

e). main_application.py
-Connects all the ui elements in one place.

f). ui.py