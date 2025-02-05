import sqlite3
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Messagebox
from datetime import datetime

# Database Setup
def setup_database():
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        member_id TEXT UNIQUE,
                        name TEXT,
                        mobile TEXT,
                        dob TEXT,
                        address TEXT,
                        joining_date TEXT,
                        paid_amount REAL,
                        due_amount REAL,
                        plan TEXT,
                        batch_time TEXT,
                        gender TEXT,
                        training_type TEXT)''')
    conn.commit()
    conn.close()

setup_database()

# Function to clear fields
def clear_fields():
    for field in fields:
        entries[field].delete(0, END)
    gender_var.set("Male")
    training_var.set("Personal Trainer")

# Function to add member
def add_member():
    data = {field: entries[field].get() for field in fields}
    data["Gender"] = gender_var.get()
    data["Training Type"] = training_var.get()
    
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute('''INSERT INTO members 
                          (member_id, name, mobile, dob, address, joining_date, paid_amount, due_amount, plan, batch_time, gender, training_type) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (data["Member ID"], data["Name"], data["Mobile"], data["Date of Birth"], data["Address"],
                        data["Joining Date"], data["Paid Amount"], data["Due Amount"], data["Plan"],
                        data["Batch Time"], data["Gender"], data["Training Type"]))
        conn.commit()
        Messagebox.show_info("Member added successfully!", "Success")
    except sqlite3.IntegrityError:
        Messagebox.show_error("Member ID already exists!", "Error")
    finally:
        conn.close()

# Function to update member details
def update_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        Messagebox.show_error("Please enter a Member ID to update.", "Error")
        return
    
    data = {field: entries[field].get() for field in fields}
    data["Gender"] = gender_var.get()
    data["Training Type"] = training_var.get()
    
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    cursor.execute('''UPDATE members SET name=?, mobile=?, dob=?, address=?, joining_date=?, paid_amount=?, due_amount=?, 
                      plan=?, batch_time=?, gender=?, training_type=? WHERE member_id=?''',
                   (data["Name"], data["Mobile"], data["Date of Birth"], data["Address"], data["Joining Date"],
                    data["Paid Amount"], data["Due Amount"], data["Plan"], data["Batch Time"], data["Gender"],
                    data["Training Type"], member_id))
    conn.commit()
    Messagebox.show_info("Member updated successfully!", "Success")
    conn.close()

# Function to delete member
def delete_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        Messagebox.show_error("Please enter a Member ID to delete.", "Error")
        return
    
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
    conn.commit()
    Messagebox.show_info("Member deleted successfully!", "Success")
    conn.close()

# Function to search for a member
def search_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        Messagebox.show_error("Please enter a Member ID to search.", "Error")
        return
    
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM members WHERE member_id=?", (member_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        for i, field in enumerate(fields):
            entries[field].delete(0, END)
            entries[field].insert(0, result[i + 1])
        gender_var.set(result[-2])
        training_var.set(result[-1])
    else:
        Messagebox.show_error("Member not found!", "Error")

# ttkbootstrap UI
app = ttk.Window(themename="darkly")  # Using a dark theme
app.title("Gym Management System")
app.geometry("900x750")

style = Style("darkly")

# Custom fonts
custom_font = ("Helvetica", 12)

frame = ttk.Frame(app, padding=20)
frame.pack(pady=10)

fields = ["Member ID", "Name", "Mobile", "Date of Birth", "Address", "Joining Date", "Paid Amount", "Due Amount", "Plan", "Batch Time"]
entries = {}
for i, field in enumerate(fields):
    label = ttk.Label(frame, text=field + ":", font=custom_font)
    label.grid(row=i, column=0, sticky=W, pady=5)
    entry = ttk.Entry(frame, font=custom_font, width=30)
    entry.grid(row=i, column=1, pady=5, padx=10)
    entries[field] = entry

# Gender Selection
gender_var = StringVar(value="Male")
gender_label = ttk.Label(frame, text="Gender:", font=custom_font)
gender_label.grid(row=3, column=2, padx=10, pady=5)
gender_menu = ttk.Combobox(frame, textvariable=gender_var, values=["Male", "Female"], state="readonly", width=28, font=custom_font)
gender_menu.grid(row=3, column=3, pady=5)

# Training Type
training_var = StringVar(value="Personal Trainer")
training_label = ttk.Label(frame, text="Training Type:", font=custom_font)
training_label.grid(row=4, column=2, padx=10, pady=5)
training_menu = ttk.Combobox(frame, textvariable=training_var, values=["Personal Trainer", "Group Class"], state="readonly", width=28, font=custom_font)
training_menu.grid(row=4, column=3, pady=5)

# Button Frame
button_frame = ttk.Frame(app)
button_frame.pack(pady=20)

buttons = [
    ("Add Member", add_member, "success"),
    ("Update Member", update_member, "warning"),
    ("Delete Member", delete_member, "danger"),
    ("Search Member", search_member, "info"),
    ("Clear Fields", clear_fields, "secondary")
]

for text, cmd, style_name in buttons:
    btn = ttk.Button(button_frame, text=text, command=cmd, bootstyle=f"{style_name}-gradient", width=18)
    btn.pack(side=LEFT, padx=10, ipadx=5, ipady=5)

app.mainloop()
