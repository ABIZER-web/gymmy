import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

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

root = tk.Tk()
root.title("Gym Management System")
root.geometry("600x400")

frame = tk.Frame(root)
frame.pack(pady=10)

# Entry fields
entry_first_name = tk.Entry(frame, width=15)
entry_first_name.grid(row=0, column=1)
tk.Label(frame, text="First Name:").grid(row=0, column=0)

entry_last_name = tk.Entry(frame, width=15)
entry_last_name.grid(row=1, column=1)
tk.Label(frame, text="Last Name:").grid(row=1, column=0)

entry_email = tk.Entry(frame, width=15)
entry_email.grid(row=2, column=1)
tk.Label(frame, text="Email:").grid(row=2, column=0)

entry_membership_plan = tk.Entry(frame, width=15)
entry_membership_plan.grid(row=3, column=1)
tk.Label(frame, text="Membership Plan ID:").grid(row=3, column=0)

btn_add = tk.Button(frame, text="Add Member", command=add_member)
btn_add.grid(row=4, columnspan=2, pady=5)

btn_delete = tk.Button(frame, text="Delete Member", command=delete_member)
btn_delete.grid(row=5, columnspan=2, pady=5)

# Treeview for displaying members
tree = ttk.Treeview(root, columns=("ID", "First Name", "Last Name", "Email"), show="headings")
tree.heading("ID", text="ID")
tree.heading("First Name", text="First Name")
tree.heading("Last Name", text="Last Name")
tree.heading("Email", text="Email")
tree.pack()

refresh_members()
root.mainloop()
