# speedtyper.py
A Speed Typing Test written in Python

Load python packages onto computer, we will be using tkinter (GUI), pyodbc (Data Base), random and nltk (Natural Language toolkit)

there is a connection with the database via pyodbc, we are using an access database which pydobc has a driver for the package SQL queries to the database to retrieve data. 

Main menu consists of New user, Exit and Login buttons to direct workflow, on press eaach close the current window instance and open a new one. Triggering either register menu: a screen that crates a table if one doesn't exist (it does), and allows data entry into several boxes which are then inserted into the users table. A primary key or ID is created here also. Once submitted, we check that all fields are full and inputs are only allowable to prevent SQL injection or repition within the table. After registration a newgame is initialised and the window is destroyed.

For Login, input is checked against all usernames and passwords. should both match, and given that usernames must also be unique when registering a new game is initialised. 

For each new game, 250 random words are taken from natural language toolkit, ensured to be between 3 and 7 characters, and made lower case. 

Words are then displayed and tagged based on which word the user is on, index moves by space keypress. each word is tagged as completed (green vs red if correct or incorrect), in bold if current and grey if future. Window updates colour after each key release and moves the list of words along.
