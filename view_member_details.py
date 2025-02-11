import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

def calculate_remaining_days(expiry_date):
    if expiry_date is None:
        return "No expiry date set"
    try:
        expiry = datetime.strptime(expiry_date, "%Y-%m-%d")
        today = datetime.today()
        remaining_days = (expiry - today).days
        return remaining_days if remaining_days >= 0 else "Expired"
    except ValueError:
        return "Invalid date format"

def show_member_info(member_id):
    conn = sqlite3.connect("gym_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM gym_users WHERE id=?", (member_id,))
    member = cursor.fetchone()
    conn.close()

    if not member:
        return

    info_window = tk.Toplevel(root)
    info_window.title("Member Information")
    info_window.geometry("400x400")
    info_window.configure(bg="black")

    frame = tk.Frame(info_window, padx=10, pady=10, bg="black")
    frame.pack(pady=5)

    fields = ["ID", "Name", "Phone Number", "Membership Plan", "Registration Date", "Membership Expiry"]

    for i, field in enumerate(fields):
        tk.Label(frame, text=field, fg="white", bg="black", font=("Arial", 10)).grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
        tk.Label(frame, text=member[i], fg="white", bg="black", font=("Arial", 10)).grid(row=i, column=1, pady=5, padx=5)

def fetch_members(search_query=None, filter_option="All"):
    conn = sqlite3.connect("gym_users.db")
    cursor = conn.cursor()
    query = "SELECT id, name, phone_number, membership_plan, registration_date, membership_expiry FROM gym_users"
    
    conditions = []
    params = []

    if search_query:
        conditions.append("(name LIKE ? OR phone_number LIKE ?)")
        params.extend([f"%{search_query}%", f"%{search_query}%"])

    if filter_option == "Expired Memberships":
        conditions.append("(membership_expiry <= date('now'))")
    elif filter_option == "Active Members":
        conditions.append("(membership_expiry > date('now'))")
    elif filter_option not in ["All", "Expired Memberships", "Active Members"]:
        conditions.append("(membership_plan = ?)")
        params.append(filter_option)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    members = cursor.fetchall()
    conn.close()
    return members

def update_member_list(event=None):
    search_query = search_entry.get()
    filter_option = filter_var.get()
    members = fetch_members(search_query, filter_option)
    
    for widget in member_frame.winfo_children():
        widget.destroy()
    
    row = 0
    col = 0
    for member in members:
        member_id, name, phone, membership_plan, registration_date, membership_expiry = member
        remaining_days = calculate_remaining_days(membership_expiry)
        
        # Stylish Card
        card_frame = tk.Frame(member_frame, bg="#f8f9fa", padx=10, pady=10, relief=tk.RIDGE, bd=2, width=250, height=220)
        card_frame.grid(row=row, column=col, padx=10, pady=10)
        card_frame.pack_propagate(False)

        # Name Banner (Like a Board)
        name_banner = tk.Label(card_frame, text=name, font=("Arial", 12, "bold"), bg="#007BFF", fg="white", pady=5)
        name_banner.pack(fill="x", pady=(0, 5))

        # Member Details
        tk.Label(card_frame, text=f"Phone: {phone}", font=("Arial", 10), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Plan: {membership_plan}", font=("Arial", 10), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Expiry: {membership_expiry}\n({remaining_days} days left)", font=("Arial", 10), bg="white").pack(anchor='w')

        # Button Frame
        button_frame = tk.Frame(card_frame, bg="white")
        button_frame.pack(pady=5)

        # Send Receipt Button
        receipt_button = tk.Button(button_frame, text="Send Receipt", bg="#2CA02C", fg="white", width=12, font=("Arial", 10))
        receipt_button.grid(row=0, column=0, padx=5)

        # Renew Membership Button
        renew_button = tk.Button(button_frame, text="Renew Plan", bg="#FF5733", fg="white", width=12, font=("Arial", 10))
        renew_button.grid(row=0, column=1, padx=5)

        # Bind click event to show member info
        card_frame.bind("<Button-1>", lambda e, member_id=member_id: show_member_info(member_id))
        
        col += 1
        if col > 2:  # Adjust to fit 3 boxes in a row
            col = 0
            row += 1

root = tk.Tk()
root.title("Member Details")
root.geometry("900x600")
root.configure(bg="black")

header_frame = tk.Frame(root, bg="gray", pady=10)
header_frame.pack(fill=tk.X)
tk.Label(header_frame, text="Member Details", font=("Arial", 16, "bold"), bg="gray", fg="white").pack()

search_frame = tk.Frame(root, bg="black", pady=10)
search_frame.pack(fill=tk.X, padx=10)

# Search Label
tk.Label(search_frame, text="Search:", fg="white", bg="black", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

# Search Entry
search_entry = tk.Entry(search_frame, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=10)
search_entry.bind("<KeyRelease>", update_member_list)

# Filter Dropdown
filter_var = tk.StringVar()
filter_var.set("All")  # Default selection

filter_options = ["All", "Expired Memberships", "Active Members", "Monthly", "Quarterly", "Yearly"]
filter_dropdown = ttk.Combobox(search_frame, textvariable=filter_var, values=filter_options, state="readonly", font=("Arial", 12), width=18)
filter_dropdown.pack(side=tk.LEFT, padx=10)
filter_dropdown.bind("<<ComboboxSelected>>", update_member_list)

# Scrollable Member Frame
canvas = tk.Canvas(root, bg="black")
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="black")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

member_frame = tk.Frame(scrollable_frame, bg="black")
member_frame.pack(fill=tk.BOTH, expand=True)

update_member_list()
root.mainloop()
