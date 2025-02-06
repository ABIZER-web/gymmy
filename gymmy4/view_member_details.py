import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

# Initialize the root window
root = tk.Tk()
root.withdraw()  # Hide the root window as it is not used directly

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

    info_window = tk.Toplevel(root)
    info_window.title("Member Information")
    info_window.geometry("500x600")
    info_window.configure(bg="black")

    frame = tk.Frame(info_window, padx=20, pady=20, bg="black")
    frame.pack(pady=10)

    fields = ["ID", "Name", "Age", "Gender", "Address", "Phone Number", "Membership Plan", "Amount", "Amount Due", "Registration Date", "Membership Expiry"]

    for i, field in enumerate(fields):
        tk.Label(frame, text=field, fg="white", bg="black", font=("Arial", 12)).grid(row=i, column=0, sticky=tk.W, pady=10, padx=10)
        tk.Label(frame, text=member[i], fg="white", bg="black", font=("Arial", 12)).grid(row=i, column=1, pady=10, padx=10)

    back_button = ttk.Button(info_window, text="Back", command=info_window.destroy)
    back_button.pack(pady=20)

def view_member_details():
    conn = sqlite3.connect("gym_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, membership_plan, registration_date, membership_expiry FROM gym_users")
    members = cursor.fetchall()
    conn.close()

    details_window = tk.Toplevel(root)
    details_window.title("Member Details")
    details_window.geometry("800x600")
    details_window.configure(bg="black")

    header_frame = tk.Frame(details_window, bg="gray", pady=10)
    header_frame.pack(fill=tk.X)
    tk.Label(header_frame, text="Member Details", font=("Arial", 18, "bold"), bg="gray", fg="white").pack()

    for member in members:
        member_id, name, membership_plan, registration_date, membership_expiry = member
        remaining_days = calculate_remaining_days(membership_expiry)
        card_frame = tk.Frame(details_window, bg="white", padx=10, pady=10, relief=tk.RIDGE, bd=2)
        card_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(card_frame, text=f"Name: {name}", font=("Arial", 12), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Plan Enrollment: {membership_plan}", font=("Arial", 12), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Registration Date: {registration_date}", font=("Arial", 12), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Membership Expiry: {membership_expiry}", font=("Arial", 12), bg="white").pack(anchor='w')
        tk.Label(card_frame, text=f"Remaining Days: {remaining_days}", font=("Arial", 12), bg="white").pack(anchor='w')

        card_frame.bind("<Button-1>", lambda e, member_id=member_id: show_member_info(member_id))

    details_window.mainloop()

# Run the view_member_details function to display member details
view_member_details()
