from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from db_helper import get_db_connection  # Import database connection helper

# Function to update the amount based on selected membership plan
def update_amount(event):
    selected_plan = membership_plan_var.get()
    if selected_plan == "Yearly":
        entry_amount.delete(0, END)
        entry_amount.insert(0, "5000")
    elif selected_plan == "Half-Yearly":
        entry_amount.delete(0, END)
        entry_amount.insert(0, "2500")
    elif selected_plan == "Monthly":
        entry_amount.delete(0, END)
        entry_amount.insert(0, "1000")
    else:
        entry_amount.delete(0, END)

# Save data to database
def save_data():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = gender_var.get().strip()
    address = entry_address.get().strip()
    phone_number = entry_phone.get().strip()
    membership_plan = membership_plan_var.get().strip()
    amount = entry_amount.get().strip()
    amount_due = entry_due.get().strip()
    registration_date = datetime.now().strftime("%Y-%m-%d")

    if membership_plan == "Yearly":
        membership_expiry = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    elif membership_plan == "Half-Yearly":
        membership_expiry = (datetime.now() + timedelta(days=182)).strftime("%Y-%m-%d")
    elif membership_plan == "Monthly":
        membership_expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        membership_expiry = None

    # Validate required fields
    if not name or not phone_number or not membership_plan:
        messagebox.showerror("Error", "Please fill in all required fields!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gym_users (name, age, gender, address, phone_number, membership_plan, amount, amount_due, registration_date, membership_expiry)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, address, phone_number, membership_plan, amount, amount_due, registration_date, membership_expiry))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Member registered successfully!")
        clear_entries()
        root.destroy()  # Close the registration window
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

# Clear all input fields
def clear_entries():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    gender_var.set("")  # Clear gender selection
    entry_address.delete(0, END)
    entry_phone.delete(0, END)
    membership_plan_var.set("")  # Clear membership plan selection
    entry_amount.delete(0, END)
    entry_due.delete(0, END)
    entry_date.config(state=NORMAL)  # Enable the entry widget before clearing
    entry_date.delete(0, END)
    entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Re-insert the current date
    entry_date.config(state=DISABLED)  # Disable the entry widget again

# Tkinter UI
root = Tk()
root.title("Register Member")
root.geometry("500x600")
root.configure(bg="black")

Label(root, text="Register Member", font=("Arial", 18, "bold"), bg="gray", fg="white", pady=10).pack(fill=X, pady=10)

# Form fields
frame = Frame(root, padx=20, pady=20, bg="black")
frame.pack(pady=10)

Label(frame, text="Name", fg="white", bg="black", font=("Arial", 12)).grid(row=0, column=0, sticky=W, pady=10, padx=10)
entry_name = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_name.grid(row=0, column=1, pady=10, padx=10)

Label(frame, text="Age", fg="white", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=10, padx=10)
entry_age = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_age.grid(row=1, column=1, pady=10, padx=10)

# Dropdown for Gender
Label(frame, text="Gender", fg="white", bg="black", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=10, padx=10)
gender_var = StringVar()
gender_dropdown = ttk.Combobox(frame, textvariable=gender_var, width=33, state="readonly", font=("Arial", 12))
gender_dropdown["values"] = ("Male", "Female")
gender_dropdown.grid(row=2, column=1, pady=10, padx=10)

Label(frame, text="Address", fg="white", bg="black", font=("Arial", 12)).grid(row=3, column=0, sticky=W, pady=10, padx=10)
entry_address = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_address.grid(row=3, column=1, pady=10, padx=10)

Label(frame, text="Phone Number", fg="white", bg="black", font=("Arial", 12)).grid(row=4, column=0, sticky=W, pady=10, padx=10)
entry_phone = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_phone.grid(row=4, column=1, pady=10, padx=10)

# Membership Plan with Dropdown
Label(frame, text="Membership Plan", fg="white", bg="black", font=("Arial", 12)).grid(row=5, column=0, sticky=W, pady=10, padx=10)
membership_plan_var = StringVar()
membership_dropdown = ttk.Combobox(frame, textvariable=membership_plan_var, width=33, state="readonly", font=("Arial", 12))
membership_dropdown["values"] = ("Yearly", "Half-Yearly", "Monthly")
membership_dropdown.grid(row=5, column=1, pady=10, padx=10)
membership_dropdown.bind("<<ComboboxSelected>>", update_amount)

Label(frame, text="Amount", fg="white", bg="black", font=("Arial", 12)).grid(row=6, column=0, sticky=W, pady=10, padx=10)
entry_amount = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_amount.grid(row=6, column=1, pady=10, padx=10)

Label(frame, text="Amount Due", fg="white", bg="black", font=("Arial", 12)).grid(row=7, column=0, sticky=W, pady=10, padx=10)
entry_due = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_due.grid(row=7, column=1, pady=10, padx=10)

Label(frame, text="Registration Date", fg="white", bg="black", font=("Arial", 12)).grid(row=8, column=0, sticky=W, pady=10, padx=10)
entry_date = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
entry_date.grid(row=8, column=1, pady=10, padx=10)
entry_date.config(state=DISABLED)

# Save Button
save_button = Button(root, text="Save", bg="#1F77B4", fg="white", width=12, font=("Arial", 12), command=save_data)
save_button.pack(pady=10)

root.mainloop()
