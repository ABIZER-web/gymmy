import sqlite3
from tkinter import *
from tkinter import messagebox
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

# Colors and Styling
BG_COLOR = "#1E1E1E"
FG_COLOR = "#FFFFFF"
BUTTON_COLOR = "#4CAF50"
BUTTON_HOVER = "#45A049"
ENTRY_BG = "#2E2E2E"
ENTRY_FG = "#FFFFFF"

# Function to handle button hover effect
def on_enter(e):
    e.widget["background"] = BUTTON_HOVER

def on_leave(e):
    e.widget["background"] = BUTTON_COLOR

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
        messagebox.showinfo("Success", "Member added successfully!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Member ID already exists!")
    finally:
        conn.close()

# Function to update member details
def update_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID to update.")
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
    messagebox.showinfo("Success", "Member updated successfully!")
    conn.close()

# Function to delete member
def delete_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID to delete.")
        return
    
    conn = sqlite3.connect("gym_members.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
    conn.commit()
    messagebox.showinfo("Success", "Member deleted successfully!")
    conn.close()

# Function to search for a member
def search_member():
    member_id = entries["Member ID"].get()
    if not member_id:
        messagebox.showerror("Error", "Please enter a Member ID to search.")
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
        messagebox.showerror("Error", "Member not found!")

# Tkinter UI
root = Tk()
root.title("Gym Management System")
root.geometry("800x700")
root.configure(bg=BG_COLOR)

frame = Frame(root, bg=BG_COLOR, padx=20, pady=20)
frame.pack(pady=10)

fields = ["Member ID", "Name", "Mobile", "Date of Birth", "Address", "Joining Date", "Paid Amount", "Due Amount", "Plan", "Batch Time"]
entries = {}
for i, field in enumerate(fields):
    Label(frame, text=field + ":", fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=i, column=0, sticky=W, pady=5)
    entry = Entry(frame, bg=ENTRY_BG, fg=ENTRY_FG, font=("Arial", 12), width=30, insertbackground=FG_COLOR)
    entry.grid(row=i, column=1, pady=5, padx=10)
    entries[field] = entry

# Gender Selection
gender_var = StringVar(value="Male")
Label(frame, text="Gender:", fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=3, column=2, padx=10, pady=5)
gender_menu = OptionMenu(frame, gender_var, "Male", "Female")
gender_menu.config(bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12))
gender_menu.grid(row=3, column=3, pady=5)

# Training Type
training_var = StringVar(value="Personal Trainer")
Label(frame, text="Training Type:", fg=FG_COLOR, bg=BG_COLOR, font=("Arial", 12, "bold")).grid(row=4, column=2, padx=10, pady=5)
training_menu = OptionMenu(frame, training_var, "Personal Trainer", "Group Class")
training_menu.config(bg=BUTTON_COLOR, fg=FG_COLOR, font=("Arial", 12))
training_menu.grid(row=4, column=3, pady=5)

# Button Frame
button_frame = Frame(root, bg=BG_COLOR)
button_frame.pack(pady=20)

buttons = [
    ("Add Member", add_member),
    ("Update Member", update_member),
    ("Delete Member", delete_member),
    ("Search Member", search_member),
    ("Clear Fields", clear_fields)
]

for text, cmd in buttons:
    btn = Button(button_frame, text=text, font=("Arial", 12, "bold"), bg=BUTTON_COLOR, fg=FG_COLOR, width=18, height=2, command=cmd, relief=RAISED, bd=3)
    btn.pack(side=LEFT, padx=10)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)

root.mainloop()
