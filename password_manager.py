import sqlite3
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import viewing_password as view
import delete_password as Delete
import os

KEY_FILE = "secret.key"
DB_FILE = "file.db"
def create_gradient(canvas, width, height, start_color, end_color):
    for y in range(height):
        r = int(start_color[0] + (end_color[0] - start_color[0]) * (y/height))
        g = int(start_color[1] + (end_color[1] - start_color[1]) * (y/height))
        b = int(start_color[2] + (end_color[2] - start_color[2]) * (y/height))
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_line(0, y, width, y, fill=color)

def on_resize(event):
   
    canvas.delete("all")
    create_gradient(canvas, event.width, event.height, start_color, end_color)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def generate_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

key = load_key()
cipher = Fernet(key)

def encrypt_password(password):
    return cipher.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS passwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        website TEXT NOT NULL,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL)''')
    conn.commit()
    conn.close()
def connect_db():
    return sqlite3.connect(DB_FILE)

def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()

    if not website or not username or not password:
        messagebox.showerror("Error", "All fields are required!")
        return


    try:
        encrypted_password = encrypt_password(password)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)", (website, username, encrypted_password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password saved successfully!")
    
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

    website_entry.delete(0, tk.END)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)


def showing_password_start():
    root.destroy()
    view.showing_password_start()

def deleteing_passwords_start():
    root.destroy()
    Delete.deleteing_passwords_start()
def start_password_manager():
    global website_entry, username_entry, password_entry, canvas, login_frame, start_color, end_color,root
    initialize_db()
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("400x350")

    start_color = (75, 0, 130)  
    end_color = (25, 25, 112)   

    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Configure>", on_resize)

    login_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, bg='#222', padx=10, pady=10)
    login_frame.columnconfigure(1, weight=1)

    tk.Label(login_frame, text="Website", bg='#222', fg='#fff').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    website_entry = tk.Entry(login_frame, width=30)
    website_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Username", bg='#222', fg='#fff').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    username_entry = tk.Entry(login_frame, width=30)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Password", bg='#222', fg='#fff').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
    password_entry = tk.Entry(login_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, padx=5, pady=5)

    saving = tk.Button(login_frame, text="Save Password", command=save_password, 
                       bg='#444', fg='#fff', highlightbackground="red", highlightthickness=2)
    saving.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)

    viewing = tk.Button(login_frame, text="View Passwords",command=showing_password_start , 
                        bg='#444', fg='#fff', highlightbackground="red", highlightthickness=2)
    viewing.grid(row=4, column=0, columnspan=2, pady=5, sticky=tk.EW)
    
    deleting = tk.Button(login_frame, text="Deleting passwords",command= deleteing_passwords_start, 
                        bg='#444', fg='#fff', highlightbackground="red", highlightthickness=2)
    deleting.grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.EW)

    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    root.mainloop()

