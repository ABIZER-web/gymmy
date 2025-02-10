import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
from db_helper import get_db_connection  # Import database helper

# Function to calculate remaining days for a membership
def calculate_remaining_days(expiry_date):
    if not expiry_date:
        return "No expiry date set"
    try:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        today = datetime.today()
        remaining_days = (expiry - today).days
        return remaining_days if remaining_days >= 0 else "Expired"
    except ValueError:
        return "Invalid date format"

# Function to show member details in a new window
def show_member_info(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gym_users WHERE id=?", (member_id,))
    member = cursor.fetchone()
    conn.close()
    if not member:
        messagebox.showerror("Error", "Member not found!")
        return
    info_window = tk.Toplevel()
    info_window.title("Member Information")
    info_window.geometry("500x600")
    info_window.configure(bg="black")
    frame = tk.Frame(info_window, padx=20, pady=20, bg="black")
    frame.pack(pady=10)
    fields = ["ID", "Name", "Age", "Gender", "Address", "Phone Number", "Membership Plan", 
              "Amount", "Amount Due", "Registration Date", "Membership Expiry"]
    for i, field in enumerate(fields):
        tk.Label(frame, text=field, fg="white", bg="black", font=("Arial", 12)).grid(row=i, column=0, sticky=tk.W, pady=10, padx=10)
        tk.Label(frame, text=member[i], fg="white", bg="black", font=("Arial", 12)).grid(row=i, column=1, pady=10, padx=10)
    back_button = ttk.Button(info_window, text="Back", command=info_window.destroy)
    back_button.pack(pady=20)

# Function to fetch members from the database
def fetch_members(search_query=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, name, phone_number, membership_plan, registration_date, membership_expiry FROM gym_users"
    
    if search_query:
        query += " WHERE name LIKE ? OR phone_number LIKE ?"
        cursor.execute(query, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute(query)
    
    members = cursor.fetchall()
    conn.close()
    return members

# Function to update the displayed member list
def update_member_list(event=None):
    search_query = search_entry.get()
    members = fetch_members(search_query)
    
    for widget in member_frame.winfo_children():
        widget.destroy()
    
    row, col = 0, 0
    for member in members:
        member_id, name, phone, membership_plan, registration_date, membership_expiry = member
        remaining_days = calculate_remaining_days(membership_expiry)
        
        card_frame = tk.Frame(member_frame, bg="white", padx=5, pady=5, relief=tk.RIDGE, bd=2, width=180, height=150)
        card_frame.grid(row=row, column=col, padx=5, pady=5)
        card_frame.pack_propagate(False)

        tk.Label(card_frame, text=f"Name: {name}", font=("Arial", 10), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Phone: {phone}", font=("Arial", 10), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Plan: {membership_plan}", font=("Arial", 10), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Expiry: {membership_expiry}\n({remaining_days} days left)", font=("Arial", 10), bg="white").pack(anchor='w')
        
        card_frame.bind("<Button-1>", lambda e, member_id=member_id: show_member_info(member_id))
        
        col += 1
        if col > 3:
            col = 0
            row += 1

# Main application window
root = tk.Tk()
root.title("Member Details")
root.geometry("800x600")
root.configure(bg="black")

header_frame = tk.Frame(root, bg="gray", pady=10)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Member Details", font=("Arial", 16, "bold"), bg="gray", fg="white").pack()

search_frame = tk.Frame(root, bg="black", pady=10)
search_frame.pack(fill=tk.X, padx=10)
tk.Label(search_frame, text="Search by Name or Phone:", fg="white", bg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=10)
search_entry.bind("<KeyRelease>", update_member_list)

canvas = tk.Canvas(root, bg="black")
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="black")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

member_frame = tk.Frame(scrollable_frame, bg="black")
member_frame.pack(fill=tk.BOTH, expand=True)

update_member_list()
root.mainloop()
