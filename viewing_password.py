import sqlite3
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
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

def decrypt_password(encrypted_password):
    return cipher.decrypt(encrypted_password.encode()).decode()

def connect_db():
    return sqlite3.connect(DB_FILE)

def website ():
    website = website_entry.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM passwords WHERE website = ?", (website,))
    records = cursor.fetchall()
    conn.close()
    
    if records:
        result = "\n".join([f"Username: {row[0]} \nPassword: {decrypt_password(row[1])}" for row in records])
        result_text.delete("1.0", tk.END)
        result_text.insert("end", result)
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert("end", "No passwords found for this website.")
        
def username():
    username = username_entry.get()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT website, password FROM passwords WHERE username = ?", (username,))
    records = cursor.fetchall()
    conn.close()
    
    if records:
        result = "\n".join([f"Website: {row[0]} \nPassword: {decrypt_password(row[1])}" for row in records])
        result_text.delete("1.0", tk.END)
        result_text.insert("end", result)
    else:
        result_text.delete("1.0", tk.END)
        result_text.insert("end", "No passwords found for this username.")
        
        
def showing_password_start():
    global website_entry,username_entry,canvas,login_frame,start_color,end_color,result_text
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

    
    website_search = tk.Button(login_frame,text= " based on website", command = website,bg='#444', fg='#fff', highlightbackground="red", highlightthickness=2)
    website_search.grid(row=3, column=0, columnspan=2, pady=10, sticky=tk.EW)
    username_search = tk.Button(login_frame, text="based on username ", command=username, bg='#444', fg='#fff', highlightbackground="red", highlightthickness=2)   
    username_search.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.EW)
    result_text = tk.Text(login_frame, height=10, width=50, state="normal",background="#333",fg="green")
    result_text.grid(row=5,column=0,columnspan=2, pady=10, sticky=tk.EW)
    
    
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root.mainloop()

