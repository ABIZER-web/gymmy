import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from db_helper import get_db_connection  # Import helper function for DB connection

def sign_out():
    """Closes the dashboard and reopens the login page"""
    root.destroy()  # Close Dashboard
    subprocess.Popen(["python", "login_page.py"])  # Open Login Page

def open_register_member():
    subprocess.Popen(["python", "Register_Member.py"])  # Open Register_Member file

def open_view_member_details():
    subprocess.Popen(["python", "view_member_details.py"])  # Open view_member_details file

def membership_plans():
    messagebox.showinfo("Membership Plans", "Available Plans:\n- Monthly\n- Quarterly\n- Yearly")

def initialize_database():
    """Ensures the members table exists in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            membership_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_total_members():
    """Fetches the total number of members from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM gym_users")
    total_members = cursor.fetchone()[0]
    conn.close()
    return total_members

def update_total_members_label():
    """Updates the total members label with the current count."""
    total_members = get_total_members()
    members_label.config(text=f"Total Members: {total_members}")
    root.after(10000, update_total_members_label)  # Update every 10 seconds

def run_dashboard():
    """Function to initialize and run the Gym Dashboard"""
    global root, members_label
    root = tk.Tk()
    root.title("Gym Management Dashboard")
    root.geometry("800x500")
    root.configure(bg="#1c1c1c")

    # Sidebar Frame
    sidebar = tk.Frame(root, bg="#2b2b2b", width=200, height=500)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    # Gym Logo
    logo_label = tk.Label(sidebar, text="🏋️ Olympia Gym", font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white")
    logo_label.pack(pady=10)

    # Buttons
    register_btn = tk.Button(sidebar, text="Register Member +", command=open_register_member, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
    register_btn.pack(pady=10, padx=10, fill=tk.X)

    view_btn = tk.Button(sidebar, text="View Member Details", command=open_view_member_details, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
    view_btn.pack(pady=10, padx=10, fill=tk.X)

    membership_btn = tk.Button(sidebar, text="Membership Plans", command=membership_plans, bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
    membership_btn.pack(pady=10, padx=10, fill=tk.X)

    # Sign Out Button
    signout_btn = tk.Button(sidebar, text="Sign Out 🚪", command=sign_out, bg="#F44336", fg="white", font=("Arial", 10, "bold"))
    signout_btn.pack(pady=20, padx=10, fill=tk.X)

    # Dashboard Header
    header = tk.Frame(root, bg="#2b2b2b", height=50)
    header.pack(fill=tk.X)

    dashboard_label = tk.Label(header, text="Dashboard", font=("Arial", 14, "bold"), bg="#2b2b2b", fg="white")
    dashboard_label.pack(side=tk.LEFT, padx=20)

    gmail_label = tk.Label(header, text="📧 owner@gmail.com", font=("Arial", 10), bg="#2b2b2b", fg="white")
    gmail_label.pack(side=tk.RIGHT, padx=20)

    # Dashboard Content
    content = tk.Frame(root, bg="#1c1c1c")
    content.pack(expand=True, fill=tk.BOTH)

    members_label = tk.Label(content, text="", font=("Arial", 12), bg="gray", fg="white", width=30, height=5)
    members_label.pack(pady=20)

    # Initialize database table
    initialize_database()

    # Update total members label initially and then periodically
    update_total_members_label()

    # Run Tkinter Event Loop
    root.mainloop()

# Ensure Dashboard only runs when this script is executed directly
if __name__ == "__main__":
    run_dashboard()
