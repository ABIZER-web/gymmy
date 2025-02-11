import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from db_helper import get_db_connection

# Function to sign out
def sign_out():
    root.destroy()
    subprocess.Popen(["python", "login_page.py"])

# Open other windows
def open_register_member():
    subprocess.Popen(["python", "Register_Member.py"])
    root.after(3000, update_members)

def open_view_member_details():
    subprocess.Popen(["python", "view_member_details.py"])

def membership_plans():
    messagebox.showinfo("Membership Plans", "Available Plans:\n- Monthly\n- Quarterly\n- Yearly")

# Function to fetch total members
def get_member_count(filter_option="All"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filter_option == "All":
        cursor.execute("SELECT COUNT(*) FROM gym_users")
    else:
        cursor.execute("SELECT COUNT(*) FROM gym_users WHERE membership_plan = ?", (filter_option,))
    
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Function to fetch members
def fetch_member_details(filter_option="All"):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if filter_option == "All":
        cursor.execute("SELECT name, phone_number, membership_plan FROM gym_users")
    else:
        cursor.execute("SELECT name, phone_number, membership_plan FROM gym_users WHERE membership_plan = ?", (filter_option,))
    
    members = cursor.fetchall()
    conn.close()
    return members

# Update UI dynamically
def update_members(event=None):
    selected_filter = filter_var.get()
    new_count = get_member_count(selected_filter)
    members_label.config(text=f"Total Members: {new_count}")
    
    member_listbox.delete(0, tk.END)
    members = fetch_member_details(selected_filter)
    for member in members:
        member_listbox.insert(tk.END, f"{member[0]} | {member[1]} | {member[2]}")
    
    root.after(2000, update_members)

# Initialize Tkinter window
root = tk.Tk()
root.title("Gym Management Dashboard")
root.geometry("900x500")
root.configure(bg="#1c1c1c")

# Sidebar
sidebar = tk.Frame(root, bg="#2b2b2b", width=200, height=500)
sidebar.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(sidebar, text="🏋️ Olympia Gym", font=("Arial", 12, "bold"), bg="#2b2b2b", fg="white").pack(pady=10)

tk.Button(sidebar, text="Register Member +", command=open_register_member, bg="#4CAF50", fg="white", font=("Arial", 10, "bold")).pack(pady=10, padx=10, fill=tk.X)
tk.Button(sidebar, text="View Member Details", command=open_view_member_details, bg="#2196F3", fg="white", font=("Arial", 10, "bold")).pack(pady=10, padx=10, fill=tk.X)
tk.Button(sidebar, text="Membership Plans", command=membership_plans, bg="#FF9800", fg="white", font=("Arial", 10, "bold")).pack(pady=10, padx=10, fill=tk.X)
tk.Button(sidebar, text="Sign Out 🚪", command=sign_out, bg="#F44336", fg="white", font=("Arial", 10, "bold")).pack(pady=20, padx=10, fill=tk.X)

# Header
header = tk.Frame(root, bg="#2b2b2b", height=50)
header.pack(fill=tk.X)

tk.Label(header, text="Dashboard", font=("Arial", 14, "bold"), bg="#2b2b2b", fg="white").pack(side=tk.LEFT, padx=20)
tk.Label(header, text="📧 owner@gmail.com", font=("Arial", 10), bg="#2b2b2b", fg="white").pack(side=tk.RIGHT, padx=20)

# Content
content = tk.Frame(root, bg="#1c1c1c")
content.pack(expand=True, fill=tk.BOTH)

top_frame = tk.Frame(content, bg="#1c1c1c")
top_frame.pack(pady=10)

members_label = tk.Label(top_frame, text=f"Total Members: {get_member_count()}", font=("Arial", 12), bg="gray", fg="white", width=20, height=2)
members_label.pack(side=tk.LEFT, padx=10)

filter_var = tk.StringVar()
filter_var.set("All")  
filter_options = ["All", "Monthly", "Quarterly", "Yearly"]
filter_dropdown = ttk.Combobox(top_frame, textvariable=filter_var, values=filter_options, state="readonly", font=("Arial", 12), width=12)
filter_dropdown.pack(side=tk.LEFT, padx=10)
filter_dropdown.bind("<<ComboboxSelected>>", update_members)

member_listbox = tk.Listbox(content, font=("Arial", 10), width=80, height=15, bg="#f0f0f0")
member_listbox.pack(pady=20)

update_members()
root.mainloop()
