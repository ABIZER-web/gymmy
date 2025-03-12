from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sqlite3

# ---------------- DATABASE CONNECTION ---------------- #
def get_db_connection():
    """Returns a connection to the gym database."""
    return sqlite3.connect("gym.db")

def initialize_database():
    """Creates the customers table if it does not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY, 
            name TEXT, 
            age TEXT, 
            address TEXT, 
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL, 
            join_date TEXT NOT NULL, 
            membership_plan TEXT NOT NULL, 
            amount INTEGER, 
            amount_due INTEGER, 
            membership_expiry TEXT NOT NULL, 
            status TEXT
        )
    ''')

    conn.commit()
    conn.close()

# ---------------- MEMBERSHIP PLANS & PRICING ---------------- #
plan_prices = {
    "3 Months": (1500, 90),
    "6 Months": (3000, 180),
    "1 Year": (5500, 365)
}

# ---------------- CALCULATE MEMBERSHIP EXPIRY & AMOUNT ---------------- #
def update_amount_and_expiry(*args):
    """Automatically updates the amount and membership expiry based on plan."""
    membership_plan = membership_plan_var.get()

    if membership_plan in plan_prices:
        amount, days = plan_prices[membership_plan]
        amount_var.set(amount)  # Auto-fill Amount
        expiry_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        expiry_var.set(expiry_date)  # Auto-fill Expiry Date

# ---------------- SAVE MEMBER FUNCTION ---------------- #
def save_data():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    address = entry_address.get().strip()
    email = entry_email.get().strip()
    phone_number = phone_code_var.get() + entry_phone.get().strip()
    membership_plan = membership_plan_var.get().strip()
    amount = amount_var.get()
    amount_due = entry_due.get().strip()
    join_date = datetime.now().strftime("%Y-%m-%d")
    membership_expiry = expiry_var.get()
    status = "Active" if membership_expiry > join_date else "Expired"

    # Validate required fields
    if not name or not phone_number or not email or not membership_plan:
        messagebox.showerror("Error", "Please fill in all required fields!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, age, address, email, phone, join_date, membership_plan, amount, amount_due, membership_expiry, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, address, email, phone_number, join_date, membership_plan, amount, amount_due, membership_expiry, status))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Member registered successfully!")

        # Clear fields after successful registration
        clear_entries()

        # Refresh the View Members page (if applicable)
        refresh_view_members_page()

    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Phone number or email already exists in the database.")
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# ---------------- REFRESH MEMBER LIST ---------------- #
def refresh_view_members_page():
    """Refreshes the View Members Page by reloading data from gym.db."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customers")
        members = cursor.fetchall()
        conn.close()

        print("Members refreshed:", members)  # Debugging purpose

    except Exception as e:
        messagebox.showerror("Database Error", f"Error refreshing members: {e}")

# ---------------- CLEAR FORM FIELDS ---------------- #
def clear_entries():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    entry_address.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)
    membership_plan_var.set("")
    amount_var.set("")
    entry_due.delete(0, END)
    expiry_var.set("")
    join_date_var.set(datetime.now().strftime("%Y-%m-%d"))  # Reset join date

# ---------------- UI SETUP ---------------- #
root = Tk()
root.title("Register Member")
root.geometry("500x700")
root.configure(bg="black")

Label(root, text="Register Member", font=("Arial", 18, "bold"), bg="gray", fg="white", pady=10).pack(fill=X, pady=10)

frame = Frame(root, padx=20, pady=20, bg="black")
frame.pack(pady=10)

# Name
Label(frame, text="Name", fg="white", bg="black", font=("Arial", 12)).grid(row=0, column=0, sticky=W, pady=5)
entry_name = Entry(frame, width=30, bg="gray", fg="white", font=("Arial", 12))
entry_name.grid(row=0, column=1, pady=5)

# Age
Label(frame, text="Age", fg="white", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=5)
entry_age = Entry(frame, width=30, bg="gray", fg="white", font=("Arial", 12))
entry_age.grid(row=1, column=1, pady=5)

# Address
Label(frame, text="Address", fg="white", bg="black", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=5)
entry_address = Entry(frame, width=30, bg="gray", fg="white", font=("Arial", 12))
entry_address.grid(row=2, column=1, pady=5)

# Email
Label(frame, text="Email", fg="white", bg="black", font=("Arial", 12)).grid(row=3, column=0, sticky=W, pady=5)
entry_email = Entry(frame, width=30, bg="gray", fg="white", font=("Arial", 12))
entry_email.grid(row=3, column=1, pady=5)

# Phone Number + Country Code
Label(frame, text="Phone", fg="white", bg="black", font=("Arial", 12)).grid(row=4, column=0, sticky=W, pady=5)
phone_code_var = StringVar(value="+1")  
phone_code_dropdown = ttk.Combobox(frame, textvariable=phone_code_var, values=["+1", "+91", "+44", "+61", "+81", "+49", "+33"], width=5, state="readonly", font=("Arial", 12))
phone_code_dropdown.grid(row=4, column=1, sticky=W, pady=5)

entry_phone = Entry(frame, width=22, bg="gray", fg="white", font=("Arial", 12))
entry_phone.grid(row=4, column=1, sticky=E, pady=5)


# Join Date (Auto-filled)
Label(frame, text="Join Date", fg="white", bg="black", font=("Arial", 12)).grid(row=5, column=0, sticky=W, pady=5)
join_date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
join_date_entry = Entry(frame, textvariable=join_date_var, width=30, bg="gray", fg="white", font=("Arial", 12), state="readonly")
join_date_entry.grid(row=5, column=1, pady=5)

# Membership Plan
Label(frame, text="Membership Plan", fg="white", bg="black", font=("Arial", 12)).grid(row=6, column=0, sticky=W, pady=5)
membership_plan_var = StringVar()
membership_plan_var.trace_add("w", update_amount_and_expiry)
membership_dropdown = ttk.Combobox(frame, textvariable=membership_plan_var, values=list(plan_prices.keys()), width=28, state="readonly", font=("Arial", 12))
membership_dropdown.grid(row=6, column=1, pady=5)

# Amount (Auto-filled)
Label(frame, text="Amount", fg="white", bg="black", font=("Arial", 12)).grid(row=7, column=0, sticky=W, pady=5)
amount_var = StringVar()
amount_entry = Entry(frame, textvariable=amount_var, width=30, bg="gray", fg="white", font=("Arial", 12), state="readonly")
amount_entry.grid(row=7, column=1, pady=5)

# Amount Due (Editable)
Label(frame, text="Amount Due", fg="white", bg="black", font=("Arial", 12)).grid(row=8, column=0, sticky=W, pady=5)
amount_due_var = StringVar()
amount_due_entry = Entry(frame, textvariable=amount_due_var, width=30, bg="gray", fg="white", font=("Arial", 12))
amount_due_entry.grid(row=8, column=1, pady=5)


# Save & Clear Buttons
Button(root, text="Save", command=save_data, bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
Button(root, text="Clear Entries", command=clear_entries, bg="#D9534F", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

initialize_database()
root.mainloop()
