import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import time
from db_helper import get_db_connection  # Import helper function for DB connection
import ttkbootstrap as tb


def sign_out():
    """Closes the dashboard and reopens the login page"""
    root.destroy()
    subprocess.Popen(["python", "login_page.py"])

def open_register_member():
    subprocess.Popen(["python", "Register_Member.py"])

def open_view_member_details():
    subprocess.Popen(["python", "crm.py"])

def membership_plans():
    messagebox.showinfo("Membership Plans", "Available Plans:\n- Monthly\n- Quarterly\n- Yearly")

def open_equipment_report():
    subprocess.Popen(["python", "equipment_report.py"])

def open_payment_page():
    subprocess.Popen(["python", "payment_page.py"])

def open_user_management():
    subprocess.Popen(["python", "user_management.py"])

def open_join_us():
    subprocess.Popen(["python", "join_us.py"])  # Opens Join Us page

def open_about():
    messagebox.showinfo("About Olympia Gym", "Welcome to Olympia Gym!\nWe help you achieve your fitness goals with the best trainers and equipment.")

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
def update_total_members_meter():
    """Updates the total members meter with the current count."""
    total_members = get_total_members()
    total_members_meter.configure(amountused=total_members)
    root.after(10000, update_total_members_meter)  # Update every 10 seconds

def update_clock():
    """Updates the real-time clock display."""
    current_time = time.strftime("%H:%M:%S")
    clock_label.config(text=current_time)
    root.after(1000, update_clock)  # Update every second

def run_dashboard():
    """Function to initialize and run the Gym Dashboard"""
    global root, total_members_meter, clock_label
    root = tb.Window(themename="darkly")  # Use ttkbootstrap theme
    root.title("Gym Management Dashboard")
    root.geometry("800x500")

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
    
    equipment_btn = tk.Button(sidebar, text="Equipment Report", command=open_equipment_report, bg="#8E44AD", fg="white", font=("Arial", 10, "bold"))
    equipment_btn.pack(pady=10, padx=10, fill=tk.X)
    
    payment_btn = tk.Button(sidebar, text="Payment Page", command=open_payment_page, bg="#D35400", fg="white", font=("Arial", 10, "bold"))
    payment_btn.pack(pady=10, padx=10, fill=tk.X)
    
    user_management_btn = tk.Button(sidebar, text="User Management", command=open_user_management, bg="#3498DB", fg="white", font=("Arial", 10, "bold"))
    user_management_btn.pack(pady=10, padx=10, fill=tk.X)

    # New Buttons: Join Us? & About
    join_us_btn = tk.Button(sidebar, text="Join Us?", command=open_join_us, bg="#27AE60", fg="white", font=("Arial", 10, "bold"))
    join_us_btn.pack(pady=10, padx=10, fill=tk.X)

    about_btn = tk.Button(sidebar, text="About", command=open_about, bg="#16A085", fg="white", font=("Arial", 10, "bold"))
    about_btn.pack(pady=10, padx=10, fill=tk.X)

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

    # Real-Time Clock
    clock_label = tk.Label(header, text="", font=("Arial", 12), bg="#2b2b2b", fg="white")
    clock_label.pack(side=tk.RIGHT, padx=20)
    
    # Dashboard Content
    content = tk.Frame(root, bg="#1c1c1c")
    content.pack(expand=True, fill=tk.BOTH)

    # Members Count Meter
    total_members_meter = tb.Meter(
        master=content,
        bootstyle="success",
        subtext="Total Members",
        interactive=False,
        textright="Members",
        textfont=("Arial", 12, "bold"),
        subtextfont=("Arial", 10),
        amounttotal=100,  # You can adjust this based on expected max members
        amountused=0,
    )
    total_members_meter.pack(pady=20)

    # Initialize database table
    initialize_database()

    # Update total members label initially and then periodically
    update_total_members_meter()
    update_clock()

    # Run Tkinter Event Loop
    root.mainloop()

# Ensure Dashboard only runs when this script is executed directly
if __name__ == "__main__":
    run_dashboard()
