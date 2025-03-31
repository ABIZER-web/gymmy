import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sqlite3
import time
import os

# Database connection
def get_db_connection():
    return sqlite3.connect("gym.db")

def get_gym_name():
    """Fetch gym name from database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT gym_name FROM users LIMIT 1")
    gym_name = cursor.fetchone()
    conn.close()
    return gym_name[0] if gym_name else "My Gym"

# Initialize Main Window
app = ttk.Window("Gym Management Dashboard", "superhero", resizable=(False, False))
app.geometry("900x500")

# Sidebar Frame
sidebar = ttk.Frame(app, width=250, height=500, bootstyle="dark")
sidebar.pack(side="left", fill="y")

# Sidebar Title
ttk.Label(sidebar, text="Gym Management System", font=("Arial", 18, "bold"), bootstyle="inverse-light").pack(pady=20)

# Dashboard Title
ttk.Label(sidebar, text="Dashboard", font=("Arial", 14, "bold"), bootstyle="inverse-light").pack(pady=10)

# Sidebar Buttons
def create_button(parent, text, command, style=SUCCESS):
    btn = ttk.Button(parent, text=text, bootstyle=style, command=command, width=22)
    btn.pack(pady=5, padx=10, fill="x")
    return btn

def open_page(page):
    os.system(f"python {page}.py")

# Navigation Buttons
create_button(sidebar, "Member Registration", lambda: open_page("Register_Member"))
create_button(sidebar, "Receipt Generation", lambda: open_page("Receipt_Generation"))
create_button(sidebar, " CRM", lambda: open_page("crm"))
create_button(sidebar, "Add Equipment", lambda: open_page("equipment"))
create_button(sidebar, "Reports", lambda: open_page("reports"))

# Sign Out Button
create_button(sidebar, "Sign Out", app.quit, style=DANGER)

# Main Content Frame
content = ttk.Frame(app, padding=20, bootstyle="light")
content.pack(expand=True, fill="both")

# Gym Name Header
gym_name = get_gym_name()
ttk.Label(content, text=gym_name, font=("Arial", 24, "bold"), bootstyle="inverse-dark").pack(pady=20)

# Real-time Clock Label
clock_label = ttk.Label(content, text="", font=("Arial", 16), bootstyle="inverse-dark")
clock_label.pack(pady=10)

def update_clock():
    """Update real-time clock."""
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    app.after(1000, update_clock)

update_clock()
app.mainloop()
