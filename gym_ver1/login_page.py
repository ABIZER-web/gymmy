import tkinter as tk
from tkinter import ttk, messagebox
import subprocess  # To open Dashboard
from db_helper import get_db_connection  # Import helper function

def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        messagebox.showinfo("Login Success", "Welcome to the Gym Dashboard!")
        root.destroy()  # Close login window
        subprocess.Popen(["python", "Dashboard.py"])  # Open Dashboard separately
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials!")

# Create the main window
root = tk.Tk()
root.title("Gym Management")
root.geometry("500x400")
root.configure(bg="#f0f2f5")

# Bind the Enter key to the login function
root.bind("<Return>", lambda event: login())

# Create a frame for the login form
frame = tk.Frame(root, bg="white", padx=40, pady=40, bd=2, relief=tk.RIDGE)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Title Label
title_label = tk.Label(frame, text="Welcome To Gymmy", font=("Arial", 16, "bold"), bg="white", fg="blue")
title_label.pack(pady=(0, 20))

# Login Label
login_label = tk.Label(frame, text="Login", font=("Arial", 14, "bold"), bg="white", fg="black")
login_label.pack(pady=(0, 20))

# Username Entry
username_label = tk.Label(frame, text="Username", bg="white", font=("Arial", 12))
username_label.pack(anchor='w')
username_entry = tk.Entry(frame, width=30, bg="#e0e0e0", font=("Arial", 12))
username_entry.pack(pady=(0, 20))

# Password Entry
password_label = tk.Label(frame, text="Password", bg="white", font=("Arial", 12))
password_label.pack(anchor='w')
password_entry = tk.Entry(frame, width=30, bg="#e0e0e0", show="*", font=("Arial", 12))
password_entry.pack(pady=(0, 20))

# Login Button
login_button = ttk.Button(frame, text="Login", command=login)
login_button.pack(pady=(20, 0))

# Run the Tkinter event loop
root.mainloop()
