from ast import Attribute
from sqlite3 import Row
import tkinter as tk
from tkinter import messagebox, font
from unittest import defaultTestLoader
from matplotlib.pylab import f
import pyodbc as db
import nltk
import random
from nltk.corpus import words
import time
import datetime
from datetime import datetime, timedelta
import re 
# Ensure you have the words corpus downloaded
nltk.download('words')

# connect to database
db.drivers()
cnxn = db.connect(driver="Microsoft Access Driver (*.mdb, *.accdb)", DBQ="C:/Users/aimro/OneDrive/Documents/Visual Studio 2022/Projects/speedtyper.py/speedtypedb.accdb")
cursor = cnxn.cursor()

class TyperGame:
    def __init__(self):
        self.welcomemenu = tk.Tk()
        self.welcomemenu.title("Welcome")
        self.welcomemenu.geometry("400x300")
        self.welcomemenu.configure(bg="#f0f4f8")
        self.welcomemenu.bind("<Escape>", self.on_escape) 
        self.CurrentUser = 0

        title_font = font.Font(family="Courier", size=18, weight="bold")
        button_font = font.Font(family="Courier", size=12)

        tk.Label(self.welcomemenu, text="Welcome to SpeedTyper!", font=title_font, bg="#f0f4f8").pack(pady=20)

        self.login_button = tk.Button(self.welcomemenu, text="Login", font=button_font, width=15, command=self.logininitialise)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.welcomemenu, text="Register", font=button_font, width=15, command=self.registerinitialise)
        self.register_button.pack(pady=10)

        self.quit_button = tk.Button(self.welcomemenu, text="Quit", font=button_font, width=15, command=self.welcomemenu.destroy)
        self.quit_button.pack(pady=10)

        def table_exists(cursor, table_name):
            for row in cursor.tables(tableType='TABLE'):
                if row.table_name.lower() == table_name.lower():
                    return True
            return False
        cnxn.commit()


        #creating databases
        if table_exists(cursor, "Users") == False:
            cursor.execute("""
            CREATE TABLE Users(
                ID AUTOICREMENT,
                Name TEXT(50) UNIQUE,
                Pass TEXT(50));""")
            cnxn.commit()
        if table_exists(cursor, "ErrorLog") == False:
            cursor.execute("""
            CREATE TABLE ErrorLog(
                User_ID INTEGER,
                Error MEMO, 
                TimeData DATETIME
                );""")
            cnxn.commit()
        if table_exists(cursor, "GameLog") == False:
            cursor.execute("""
            CREATE TABLE GameLog(
                Gametime DATETIME,
                User_ID INTEGER,
                Accuracy DOUBLE,
                Confidence DOUBLE,
                Speed INTEGER);
                """)
            cnxn.commit()

    def logininitialise(self):
        self.welcomemenu.destroy()
        self.loginwindow()

    def registerinitialise(self):
        self.welcomemenu.destroy()
        self.registerwindow()

    def registerwindow(self):
        self.registerwin = tk.Tk()
        self.registerwin.title('Register')
        self.registerwin.geometry("400x300")
        self.registerwin.configure(bg="#f0f4f8")
        self.registerwin.bind("<Escape>", self.on_escape) 

        label_font = font.Font(family="Courier", size=12)
        entry_font = font.Font(family="Courier", size=12)
        button_font = font.Font(family="Courier", size=12)

        tk.Label(self.registerwin, text="Name", font=label_font, bg="#f0f4f8").pack(pady=(20, 5))
        self.username_field = tk.Entry(self.registerwin, font=entry_font)
        self.username_field.pack(pady=5)

        tk.Label(self.registerwin, text="Password", font=label_font, bg="#f0f4f8").pack(pady=5)
        self.password_field = tk.Entry(self.registerwin, show="*", font=entry_font)
        self.password_field.pack(pady=5)
        self.password_field.bind("<Return>", lambda event: self.register())

        # Set focus to username field after window is visible
        self.registerwin.focus()
        self.registerwin.after(100, lambda: self.username_field.focus())

        self.register_butt = tk.Button(self.registerwin, text="Register", font=button_font, width=15, command=self.register)
        self.register_butt.pack(pady=10)

        self.back_butt = tk.Button(self.registerwin, text="Back", font=button_font, width=15, command=self.backmenu_from_register)
        self.back_butt.pack(pady=5)

    def backmenu_from_register(self):
        self.registerwin.destroy()
        self.__init__()

    def register(self):
        username = self.username_field.get()
        password = self.password_field.get()
        def sanitize(nom):
            if re.fullmatch(r'^[A-Za-z0-9_]{3,30}$', nom):
                return nom
            else:
                return ""
        sanitize(username)
        sanitize(password)
        if not username or not password:
            messagebox.showwarning('Registration Failed', 'Please fill in all fields.')
            return
        if len(password) < 6:
            messagebox.showwarning('Registration Failed', 'Password must be at least 6 characters long.')
            return
        cursor.execute("SELECT * FROM Users WHERE Name = ?;", (username,))
        if cursor.fetchone():
            messagebox.showwarning('Registration Failed', 'Username already exists. Please choose a different username.')
            return
        cursor.execute("INSERT INTO Users (Name, Pass) VALUES (?, ?);", (username, password))
        cnxn.commit()
        cursor.execute("SELECT ID FROM Users WHERE Name = ?;", (username,))
        userid = cursor.fetchone()
        self.CurrentUser = userid[0]
        self.username_field.delete(0, tk.END)
        self.password_field.delete(0, tk.END)
        messagebox.showinfo('Registration Successful', 'You have successfully registered!')
        self.registerwin.destroy()
        self.NewGame()

    def loginwindow(self):
        self.loginwin = tk.Tk()
        self.loginwin.title('Login')
        self.loginwin.geometry("400x300")
        self.loginwin.configure(bg="#f0f4f8")
        self.loginwin.bind("<Escape>", self.on_escape) 

        label_font = font.Font(family="Courier", size=12)
        entry_font = font.Font(family="Courier", size=12)
        button_font = font.Font(family="Courier", size=12)

        tk.Label(self.loginwin, text="Name", font=label_font, bg="#f0f4f8").pack(pady=(20, 5))
        self.username_field = tk.Entry(self.loginwin, font=entry_font)
        self.username_field.pack(pady=5)
        self.username_field.bind("<Return>", lambda event: self.password_field.focus())

        tk.Label(self.loginwin, text="Password", font=label_font, bg="#f0f4f8").pack(pady=5)
        self.password_field = tk.Entry(self.loginwin, show="*", font=entry_font)
        self.password_field.pack(pady=5)
        self.password_field.bind("<Return>", lambda event: self.login())

        self.loginwin.focus()
        self.loginwin.after(100, lambda: self.username_field.focus())

        self.login_butt = tk.Button(self.loginwin, text="Enter", font=button_font, width=15, command=self.login)
        self.login_butt.pack(pady=10)

        self.back_butt = tk.Button(self.loginwin, text="Back", font=button_font, width=15, command=self.backmenu_from_login)
        self.back_butt.pack(pady=5)

    def backmenu_from_login(self):
        self.loginwin.destroy()
        self.__init__()

    def login(self):
        username = self.username_field.get()
        passwrd = self.password_field.get()
        cursor.execute("SELECT * FROM Users WHERE Name = ? AND Pass = ?;", (username, passwrd))
        row = cursor.fetchone()
        self.CurrentUser = row[0]
        cnxn.commit()
        if row:
            self.loginwin.destroy()
            self.NewGame()
        else:
            messagebox.showwarning('Login Failed', 'Incorrect name or password or user does not exist.')
       
    def NewGame(self):

        self.newgamewin = tk.Tk()
        self.newgamewin.title('SpeedTyper')
        self.newgamewin.geometry("20000x600")
        self.newgamewin.configure(bg="#f0f4f8")
        self.newgamewin.bind("<Escape>", self.on_escape) 

        
        title_font = font.Font(family="Courier", size=18, weight="bold")
        wordlist_font = font.Font(family="Courier", size=14)

        self.time_left = True # Global variable to control the game loop
        self.time_limit = 10 #1 minute time limit
        self.time_left = self.time_limit
        self.timer_started = False
        self.timer_label = tk.Label(self.newgamewin, text=f"{self.time_left}", font=("Courier", 20), bg="#f0f4f8")
        self.timer_label.pack(pady=(10, 0))
        self.keystroke_count = 0



        # ------------------------------create an adaptive word list -----------------------------------------#
        word_list = words.words()
        filtered_words = [
            w.lower() for w in word_list
            if 3 <= len(w) <= 7 and w.isalpha() and w.islower()
        ]
        unique_words = list(set(filtered_words))
        #250 so as to not run out nor overload the program
        word_set_size = 250
        self.selected_words = []

        #check errors exist
        cursor.execute("SELECT COUNT(*) FROM ErrorLog WHERE User_ID = ?", (self.CurrentUser,))
        if cursor.fetchone()[0] == 0:
            self.selected_words = random.sample(unique_words, word_set_size)
            messagebox.showinfo("No Errors", "Cannot access error data.")
        else:
            three_days = datetime.now() - timedelta(hours=36)
            seven_days = datetime.now() - timedelta(hours=168)

            bias = []

            # First bias window
            cursor.execute("SELECT Error FROM ErrorLog WHERE User_ID = ? AND TimeData >= ?", (self.CurrentUser, three_days))
            error_parts = [row.Error for row in cursor.fetchall()]
            percent = 0.05
            bias_section = []

            for l in error_parts:
                for w in unique_words:
                    if len(bias_section) >= word_set_size * percent:
                        break
                    if l in w or (l.startswith(" ") and l[1:2] == w[0:1]) or (len(l) > 2 and l[2] == " " and l[0:1] == w[-2:]):
                        bias_section.append(w)
            bias.extend(bias_section)

            # Second bias window
            cursor.execute("""
                SELECT Error FROM ErrorLog
                WHERE User_ID = ? AND TimeData >= ? AND TimeData <= ?;
            """, (self.CurrentUser, three_days, seven_days))
            error_parts = [row.Error for row in cursor.fetchall()]
            percent = 0.01
            bias_section = []

            for l in error_parts:
                for w in unique_words:
                    if len(bias_section) >= word_set_size * percent:
                        break
                    if l in w or (l.startswith(" ") and l[1:2] == w[0:1]) or (len(l) > 2 and l[2] == " " and l[0:1] == w[-2:]):
                        bias_section.append(w)
            bias.extend(bias_section)

            # Final selection
            if len(bias) < word_set_size:
                additional = random.sample(unique_words, word_set_size - len(bias))
                bias.extend(additional)
            self.selected_words = random.sample(bias, word_set_size)

            self.current_word_index = 0
            self.word_results = [None] * len(self.selected_words)

        #statistics measuring

        self.total_word_count = 0
        self.correct_word_count = 0
        self.backspace_count = 0
        self.error_substr = []


        # Use a Text widget for colored word window, centered and matching entry width
        self.word_window = tk.Text(
            self.newgamewin,
            height=1,
            width=80,
            font=wordlist_font,
            bg="#f0f4f8",
            bd=0,
            highlightthickness=0,
            wrap="none"
        )

        self.word_window.tag_configure("center", justify='center')
        self.word_window.pack(pady=(50, 0))
        self.input_field = tk.Entry(self.newgamewin, font=title_font, width=50,)
        self.input_field.pack(pady=(30, 20))
        self.input_field.bind("<KeyRelease>", self.on_key_release)

        self.input_field.focus_set()
        self.newgamewin.after(100, self.input_field.focus_set)
        self.update_word_window("")

    def update_word_window(self, typed):
            self.word_window.config(state=tk.NORMAL)
            self.word_window.delete("1.0", tk.END)

            window_size = 9  # Total words to show (odd number for centering, ensure less than the entry box width)
            half_window = window_size // 2
            total_words = len(self.selected_words)

            # Calculate window bounds
            start = max(0, self.current_word_index - half_window)
            end = min(total_words, self.current_word_index + half_window + 1)

            # Adjust window if at the start or end
            if self.current_word_index < (half_window):
                end = min(window_size, total_words)
            elif self.current_word_index + half_window >= total_words:
                start = max(0, total_words - window_size)
                end = total_words

            # Tag configuration
            self.word_window.tag_configure("done_correct", foreground="green")
            self.word_window.tag_configure("done_wrong", foreground="red")
            self.word_window.tag_configure("current", font=font.Font(family="Courier", weight="bold"), foreground="black")
            self.word_window.tag_configure("current_wrong", font=font.Font(family="Courier", weight="bold"), foreground="red")
            self.word_window.tag_configure("future", foreground="gray")

            for idx in range(start, end):
                word = self.selected_words[idx]
                if idx < self.current_word_index:
                    if self.word_results[idx] is True:
                        self.word_window.insert(tk.END, word + " ", "done_correct")

                    else:
                        self.word_window.insert(tk.END, word + " ", "done_wrong")

                elif idx == self.current_word_index:
                    if typed and not word.startswith(typed):
                        self.word_window.insert(tk.END, word + " ", "current_wrong")
                    else:
                        self.word_window.insert(tk.END, word + " ", "current")
                else:
                    self.word_window.insert(tk.END, word + " ", "future")

            self.word_window.tag_add("left", "1.0", "end")
            self.word_window.config(state=tk.DISABLED)

    def RecapPage(self):
        self.NewGame.destroy()
        self.endgame()
    def endgame(self):
        # Save game results to database

        self.endwin = tk.Tk()
        self.endwin.title('Game Over')
        self.endwin.geometry("400x300")
        self.endwin.configure(bg="#f0f4f8")
        self.endwin.bind("<Escape>", self.on_escape) 
        self.endwin.focus()

        label_font = font.Font(family="Courier", size=12)
        entry_font = font.Font(family="Courier", size=12)
        button_font = font.Font(family="Courier", size=12)



        if self.CurrentUser is not None:
            user = self.CurrentUser
            accuracy = (self.correct_word_count / self.total_word_count) * 100 if self.total_word_count > 0 else 0
            confidence = (100 - ((self.backspace_count / self.keystroke_count)*100)) if self.keystroke_count > 0 else 0
            speed = (self.total_word_count / self.time_limit) * 60 if self.time_limit > 0 else 0
            # saving gameresults to database
            cursor.execute("INSERT INTO GameLog (Gametime, User_ID, Accuracy, Confidence, Speed) VALUES (?, ?, ?, ?, ?);",(datetime.now(), user, accuracy, confidence, speed))
            cnxn.commit()
            #tracking which errors came up
            for error in self.error_substr:
                cursor.execute("INSERT INTO ErrorLog (User_ID, Error, TimeData) VALUES (?, ?, ?);", (user, error, datetime.now()))
            cnxn.commit()

    def on_key_release(self, event):
            if not self.timer_started and event.keysym != "BackSpace":
                self.timer_started = True
                self.update_timer()
            typed = self.input_field.get()
            current_word = self.selected_words[self.current_word_index]

            self.keystroke_count +=1 

            # Live feedback: update word window with color
            self.update_word_window(typed)

            if event.keysym == "BackSpace":
                self.backspace_count += 1

            # If space is pressed, check errors, advance word, and reset input
            if event.keysym == "space":
                typed_word = typed.strip()
                correct = typed_word == current_word
                self.word_results[self.current_word_index] = correct

                # Count completed words only once
                self.total_word_count += 1
                if correct:
                    self.correct_word_count += 1
                elif current_word != "":
                    # Collect error substrings for incorrect words
                    for i in range(len(current_word)):
                        typed_c = typed_word[i] if i < len(typed_word) else ""
                        correct_c = current_word[i]
                        if typed_c != correct_c:
                            before = current_word[i-1] if i > 0 else " "
                            after = current_word[i+1] if i+1 < len(current_word) else " "
                            self.error_substr.append(f"{before}{correct_c}{after}")

                # Advance to next word
                self.current_word_index += 1
                if self.current_word_index < len(self.selected_words):
                    self.input_field.delete(0, tk.END)
                    self.update_word_window("")
                else:
                    self.endgame()

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"{self.time_left}")
            self.newgamewin.after(1000, self.update_timer)
        else:
            self.endgame()
            self.newgamewin.destroy()
           
    def on_escape(self, event):
            # Cleanly close all windows and exit
            root = tk._default_root
            windows = [root] + list(root.children.values())

            for win in windows:
                try:
                    win.destroy()
                except:
                    pass
            try:
                root.quit()
            except Exception:
                pass

if __name__ == "__main__":
    app = TyperGame()
    tk.mainloop()
    cnxn.close
