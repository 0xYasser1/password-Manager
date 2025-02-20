import tkinter as tk
from tkinter import messagebox
import password_manager as ps

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
    # Reposition the login frame in the center
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "admin" and password == "1": # change the ussername & password values 
        message_label.config(text="Login successful!", fg="green")
        root.after(200, open_password_manager)
    else:
        message_label.config(text="Invalid username or password", fg="red")
        entry_username.delete(0, tk.END)
        entry_password.delete(0, tk.END)

def open_password_manager():
    root.destroy()
    ps.start_password_manager()


root = tk.Tk()
root.title("Login System")
root.geometry("400x350")

start_color = (75, 0, 130)   # #4B0082
end_color = (25, 25, 112)    # #191970

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)
canvas.bind("<Configure>", on_resize)

# Create login frame
login_frame = tk.Frame(root, bd=2, relief=tk.GROOVE, bg='#222')
login_frame.columnconfigure(1, weight=1)

# Widgets
label_username = tk.Label(login_frame, text="Username:", bg='#222',fg='#fff')
label_password = tk.Label(login_frame, text="Password:", bg='#222',fg='#fff')
entry_username = tk.Entry(login_frame, bg='white')
entry_password = tk.Entry(login_frame, show="*", bg='white')
login_button = tk.Button(login_frame, text="Login", command=login, 
                        bg='#222', fg='white', activebackground='#222',background='#222')
message_label = tk.Label(login_frame, text="", bg='#222')

# Grid layout
label_username.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
entry_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.EW)
entry_password.grid(row=1, column=1, padx=10, pady=10, sticky=tk.EW)
login_button.grid(row=2, column=0, columnspan=2, pady=10, sticky=tk.EW)
message_label.grid(row=3, column=0, columnspan=2)

# Center login frame in the window
login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

root.mainloop()
