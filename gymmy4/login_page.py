import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import subprocess  # Import subprocess to open dashboard

def create_db():
    conn = sqlite3.connect("gym_users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    
    # Insert a default admin user if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        conn.commit()
    
    conn.close()

def login(event=None):  # Accept event argument for key binding
    username = username_entry.get()
    password = password_entry.get()
    
    conn = sqlite3.connect("gym_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Login Success", "Welcome to the Gym Dashboard!")
        root.destroy()  # Close login window
        subprocess.Popen(["python", "Dashboard.py"])  # Open the dashboard
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials!")

# Initialize Database
create_db()

# Create the main window
root = tk.Tk()
root.title("Gym Management")
root.geometry("500x400")
root.configure(bg="#f0f2f5")

# Bind the Enter key to the login function
root.bind("<Return>", login)

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
