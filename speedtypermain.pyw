import tkinter as tk
from tkinter import messagebox, font
from unittest import defaultTestLoader
import pyodbc as db
import nltk
import random
from nltk.corpus import words
# Ensure you have the words corpus downloaded
nltk.download('words')

# connect to database
db.drivers()
cnxn = db.connect(driver="Microsoft Access Driver (*.mdb, *.accdb)", DBQ="C:/Users/aimro/OneDrive/Documents/Visual Studio 2022/Projects/speedtyper.py/speedtypedb.accdb")
cursor = cnxn.cursor()

class Login:
    def __init__(self):
        self.welcomemenu = tk.Tk()
        self.welcomemenu.title("Welcome")
        self.welcomemenu.geometry("400x300")
        self.welcomemenu.configure(bg="#f0f4f8")
        self.welcomemenu.bind("<Escape>", self.on_escape) 

        title_font = font.Font(family="Courier", size=18, weight="bold")
        button_font = font.Font(family="Courier", size=12)

        tk.Label(self.welcomemenu, text="Welcome to SpeedTyper!", font=title_font, bg="#f0f4f8").pack(pady=20)

        self.login_button = tk.Button(self.welcomemenu, text="Login", font=button_font, width=15, command=self.logininitialise)
        self.login_button.pack(pady=10)

        self.register_button = tk.Button(self.welcomemenu, text="Register", font=button_font, width=15, command=self.registerinitialise)
        self.register_button.pack(pady=10)

        self.quit_button = tk.Button(self.welcomemenu, text="Quit", font=button_font, width=15, command=self.welcomemenu.destroy)
        self.quit_button.pack(pady=10)

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
        self.registerwindow.bind("<Escape>", self.on_escape) 

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

        tk.Label(self.loginwin, text="Password", font=label_font, bg="#f0f4f8").pack(pady=5)
        self.password_field = tk.Entry(self.loginwin, show="*", font=entry_font)
        self.password_field.pack(pady=5)
        self.password_field.bind("<Return>", lambda event: self.login())

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
        booluser = cursor.fetchone()
        if booluser:
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
        word_list = words.words()
        filtered_words = [
            w.lower() for w in word_list
            if 3 <= len(w) <= 7 and w.isalpha() and w.islower()
        ]
        unique_words = list(set(filtered_words))
        random.shuffle(unique_words)
        selected_words = unique_words[:250] #250 so as to not run out nor overload the program
        self.words = selected_words
        self.current_word_index = 0
        self.errors = []
        self.word_results = [None] * len(self.words)  # None = not attempted, True = correct, False = incorrect

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
        # will enter timer and word count here later. 

        self.word_window.tag_configure("center", justify='center')
        self.word_window.pack(pady=(50, 0))
        self.input_field = tk.Entry(self.newgamewin, font=title_font, width=50,)
        self.input_field.pack(pady=(30, 20))
        self.input_field.focus_set()
        self.input_field.bind("<KeyRelease>", self.on_key_release)

        self.update_word_window("")  # Initial display

    def update_word_window(self, typed):
        self.word_window.config(state=tk.NORMAL)
        self.word_window.delete("1.0", tk.END)

        window_size = 9  # Total words to show (odd number for centering, ensure less than the entry box width)
        half_window = window_size // 2
        total_words = len(self.words)

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
        self.word_window.tag_configure("current", foreground="black", font=font.BOLD)
        self.word_window.tag_configure("current_wrong", foreground="red", font=font.BOLD)
        self.word_window.tag_configure("future", foreground="gray")

        for idx in range(start, end):
            word = self.words[idx]
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

    def on_key_release(self, event):
        typed = self.input_field.get()
        current_word = self.words[self.current_word_index]

        # Live feedback: update word window with color
        self.update_word_window(typed)

        # If space is pressed, check errors, advance word, and reset input
        if event.keysym == "space":
            typed_word = typed.strip()
            # Check for errors and correctness
            correct = typed_word == current_word
            self.word_results[self.current_word_index] = correct

            for i, (typed_char, correct_char) in enumerate(zip(typed_word, current_word)):
                if typed_char != correct_char:
                    before = current_word[i-1] if i > 0 else " "
                    after = current_word[i+1] if i+1 < len(current_word) else " "
                    self.errors.append(f"{before}[{typed_char}->{correct_char}]{after}")
            if len(typed_word) < len(current_word):
                for i in range(len(typed_word), len(current_word)):
                    before = current_word[i-1] if i > 0 else " "
                    after = current_word[i+1] if i+1 < len(current_word) else " "
                    self.errors.append(f"{before}[->{current_word[i]}]{after}")
            elif len(typed_word) > len(current_word):
                for i in range(len(current_word), len(typed_word)):
                    before = typed_word[i-1] if i > 0 else " "
                    after = " "
                    self.errors.append(f"{before}[{typed_word[i]}->]{after}")

            # Advance to next word
            self.current_word_index += 1
            if self.current_word_index < len(self.words):
                self.input_field.delete(0, tk.END)
                self.update_word_window("")
            else:
                messagebox.showinfo("Game Over", "You've completed all words!" + ", ".join(self.errors))
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
    app = Login()
    tk.mainloop()








