# speedtyper.py

A Speed Typing Test written in Python
# Setting up the codespace
Load python packages onto computer, we will be using tkinter (GUI), pyodbc (Data Base), random and nltk (Natural Language toolkit)

there is a connection with the database via pyodbc, we are using an access database which pydobc has a driver for the package SQL queries to the database to retrieve data. 
# Main Menu
Main menu consists of New user, Exit and Login buttons to direct workflow, on press eaach close the current window instance and open a new one. Triggering either register menu: a screen that crates a table if one doesn't exist (it does), and allows data entry into several boxes which are then inserted into the users table.

#Login or Register
A primary key or ID is created here also. Once submitted, we check that all fields are full and inputs are only allowable to prevent SQL injection or repition within the table. After registration a newgame is initialised and the window is destroyed.
</br>
<img width="300" height="200" alt="Screenshot 2025-07-20 192143" src="https://github.com/user-attachments/assets/65bc24aa-39bd-4ab1-855c-7af261c22847" />
</br>
 Triggering either register menu: a screen that crates a table if one doesn't exist (it does), and allows data entry into several boxes which are then inserted into the users table. A primary key or ID is created here also. Once submitted, we check that all fields are full and inputs are only allowable to prevent SQL injection or repition within the table. After registration a newgame is initialised and the window is destroyed.
</br>
<img width="300" height="200" alt="Screenshot 2025-07-20 192220" src="https://github.com/user-attachments/assets/6e15e2d2-1a86-464b-9d8f-8811570efc45" />
</br>
<img width="389" height="244" alt="Screenshot 2025-07-20 192319" src="https://github.com/user-attachments/assets/7d0147c2-8504-49cd-9d18-c14e318359f3" />
</br>
For Login, input is checked against all usernames and passwords. should both match, and given that usernames must also be unique when registering a new game is initialised. 
</br>
<img width="445" height="246" alt="Screenshot 2025-07-20 192247" src="https://github.com/user-attachments/assets/560ddd9d-d7db-4947-b539-703706616559" />
</br>
# Word set
For each new game, 250 random words are taken from natural language toolkit, ensured to be between 3 and 7 characters, and made lower case. The Database is checked for any saved error substrings specific to the current user. If they dont exist, 250 random words are generated, if they do errors from the last 3 days occur at 5% and the last 7 days at 1% in order to attempt a spaced repition learning curve.
# The Game
Words are then displayed and tagged based on which word the user is on, index moves by space keypress. each word is tagged as completed (green vs red if correct or incorrect), in bold if current and grey if future. Window updates colour after space release and moves the list of words along.
</br>
<img width="500" height="250" alt="Screenshot 2025-07-20 192343" src="https://github.com/user-attachments/assets/40791e1b-f864-462a-bd7c-0bc09eb14928" />
</br>
The words being moved along:
</br>
<img width="300" height="100" alt="Screenshot 2025-07-20 192406" src="https://github.com/user-attachments/assets/faf26ca7-237c-468e-b17e-beac37f205cf" />
</br>
words will turn red if what is typed is wrong but return to black if the error is corrected. This will be counted as a lack of confidence but not affect overall accuracy. If the word remains erroneous it will stay red and at least one error substring will be created/tracked to determine which letter combinations a user struggles with.
</br>
<img width="300" height="100" alt="Screenshot 2025-07-20 192406" src="https://github.com/user-attachments/assets/faf26ca7-237c-468e-b17e-beac37f205cf" />
</br>
# Database statistics
At this point, the user's statistics for the last game are displayed. The error substrings are live updated to the database in the Errors Table but the final calulations as to accuracy, confidence and speed are logged now. Speed is traditional Words Per Minute, Confidence is 1 - proportion of keystrokes that were backspaces as a percentage adn accuracy is a percentage of erroneous words vs total number of words completed. These are saved against datetime so they can be sorted by how recent they are.
</br>
<img width="595" height="788" alt="Screenshot 2025-07-20 192459" src="https://github.com/user-attachments/assets/d1a8b1dc-9578-4a71-b818-496688666fe5" />
</br>
# Graphs
I then used matplotlib to generate graphs to display these statistics over time by including the last 20 games (should they exist) The user data is fetched from the access database via pyodbc and an SQL query, sorted by datetime and the top 20 taken. I quickly realised using the datetime as the x axis made very little sense, so it just shows most recent progress.
</br>
<img width="964" height="840" alt="Screenshot 2025-07-20 192611" src="https://github.com/user-attachments/assets/18bb1b79-448e-4228-a5a0-35c748164010" />
</br>
<img width="958" height="821" alt="Screenshot 2025-07-20 192554" src="https://github.com/user-attachments/assets/37f8af3e-2f31-4b53-82bc-072f42b3f0fc" />
</br>
<img width="962" height="826" alt="Screenshot 2025-07-20 192519" src="https://github.com/user-attachments/assets/6c101c36-6e58-467f-8f3c-db366e4df66d" />
</br>
# Final
Afterwards, a new game can be initialised or the user can log out. Every window has escape binded to close the application and the x is easily accessible. Quit is also available from the logged out screen, and the user ID is refreshed to prevent logging in accidentally again.

# Thoughts
I completed this project to try and finish a project I did in school. That was compelted in c#, and a more established GUI made some parts easier. I've learnt a lot about Python, despite having to refamiliarise myself with syntax and the package functions too. I coded this faster than anticipated, and added graphs and an SQL accessible database rather that reading to and from two .csv files this time. I think this is vastly preferable. It certainly made handling the error substrings much easier.



