import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

def fetch_members():
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT member_id, first_name, last_name, email FROM Members")
    rows = cursor.fetchall()
    conn.close()
    return rows

def refresh_members():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_members():
        tree.insert('', 'end', values=row)

def add_member():
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    email = entry_email.get()
    membership_plan = entry_membership_plan.get()
    if not first_name or not last_name or not email:
        messagebox.showerror("Input Error", "Please fill in all required fields.")
        return
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''INSERT INTO Members (first_name, last_name, email, membership_plan_id)
                          VALUES (?, ?, ?, ?)''', (first_name, last_name, email, membership_plan))
        conn.commit()
        messagebox.showinfo("Success", "Member added successfully!")
        refresh_members()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Email already exists!")
    finally:
        conn.close()

def delete_member():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select a member to delete.")
        return
    member_id = tree.item(selected_item)['values'][0]
    conn = sqlite3.connect('gym_management.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Members WHERE member_id = ?", (member_id,))
    conn.commit()
    conn.close()
    messagebox.showinfo("Success", "Member deleted successfully!")
    refresh_members()

# Initialize the main window with ttkbootstrap
root = ttk.Window(themename='darkly')
root.title("Gym Management System")
root.geometry("700x500")

# Main frame
frame = ttk.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=TRUE)

# Entry fields with labels
entry_fields = [
    ('First Name:', 'first_name'),
    ('Last Name:', 'last_name'),
    ('Email:', 'email'),
    ('Membership Plan ID:', 'membership_plan'),
]

entries = {}
for idx, (label_text, var_name) in enumerate(entry_fields):
    label = ttk.Label(frame, text=label_text)
    label.grid(row=idx, column=0, sticky=W, pady=5)
    entry = ttk.Entry(frame, width=30)
    entry.grid(row=idx, column=1, pady=5)
    entries[var_name] = entry

entry_first_name = entries['first_name']
entry_last_name = entries['last_name']
entry_email = entries['email']
entry_membership_plan = entries['membership_plan']

# Buttons with styling
button_style = ttk.Style()
button_style.configure('TButton', padding=6, relief='flat', font=('Helvetica', 10))

btn_frame = ttk.Frame(frame)
btn_frame.grid(row=len(entry_fields), column=0, columnspan=2, pady=15)

btn_add = ttk.Button(btn_frame, text="Add Member", command=add_member, style='success.TButton')
btn_add.pack(side=LEFT, padx=5)

btn_delete = ttk.Button(btn_frame, text="Delete Member", command=delete_member, style='danger.TButton')
btn_delete.pack(side=LEFT, padx=5)

# Treeview for displaying members with dark theme
columns = ("ID", "First Name", "Last Name", "Email")
tree = ttk.Treeview(root, columns=columns, show="headings", bootstyle="dark")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=CENTER)
tree.pack(fill=BOTH, expand=TRUE, padx=20, pady=10)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(tree, orient=VERTICAL, command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side=RIGHT, fill=Y)

refresh_members()
root.mainloop()
