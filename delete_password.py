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
    
def connect_db():
    return sqlite3.connect(DB_FILE)

def delete_a_password():
    website = website_entry.get().strip()
    username = username_entry.get().strip()

    if not website and not username:
        messagebox.showwarning("Warning", "Please enter at least a website or username to delete.")
        return

    try:
        conn = connect_db()
        cursor = conn.cursor()
        
        # Check if the entry exists
        query = "SELECT * FROM passwords WHERE website = ? OR username = ?;"
        cursor.execute(query, (website, username))
        record = cursor.fetchone()

        if not record:
            messagebox.showinfo("Not Found", "No matching password found.")
            conn.close()
            return

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?")
        if not confirm:
            conn.close()
            return

        # Delete the entry
        delete_query = "DELETE FROM passwords WHERE website = ? OR username = ?;"
        cursor.execute(delete_query, (website, username))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password deleted successfully.")
    
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

def deleteing_passwords_start():
    global website_entry, username_entry, canvas, login_frame, start_color, end_color
    
    root = tk.Tk()
    root.title("Delete Password")
    root.geometry("400x350")

    start_color = (75, 0, 130)  
    end_color = (25, 25, 112)   

    canvas = tk.Canvas(root)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.bind("<Configure>", on_resize)

    login_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, bg='#222', padx=10, pady=10)
    login_frame.columnconfigure(1, weight=1)
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    tk.Label(login_frame, text="Website", bg='#222', fg='#fff').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
    website_entry = tk.Entry(login_frame, width=30)
    website_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_frame, text="Username", bg='#222', fg='#fff').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
    username_entry = tk.Entry(login_frame, width=30)
    username_entry.grid(row=1, column=1, padx=5, pady=5)

    delete_button = tk.Button(login_frame, text="Delete Password", command=delete_a_password, bg="red", fg="white")
    delete_button.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)

    root.mainloop()

    