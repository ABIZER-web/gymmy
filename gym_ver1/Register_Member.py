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

def save_data():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    gender = gender_var.get().strip()
    address = entry_address.get().strip()
    phone_number = entry_phone.get().strip()
    email = entry_email.get().strip()
    weight = entry_weight.get().strip()
    height = entry_height.get().strip()
    bmi = entry_bmi.get().strip()
    membership_plan = membership_plan_var.get().strip()
    amount = entry_amount.get().strip()
    amount_due = entry_due.get().strip()
    registration_date = datetime.now().strftime("%Y-%m-%d")

    # Validate required fields
    if not name or not phone_number or not email or not membership_plan:
        messagebox.showerror("Error", "Please fill in all required fields!")
        return

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO gym_users (name, age, gender, address, phone_number, email, weight, height, bmi, membership_plan, amount, amount_due, registration_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, age, gender, address, phone_number, email, weight, height, bmi, membership_plan, amount, amount_due, registration_date))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Member registered successfully!")
        root.destroy()
    except Exception as e:
        messagebox.showerror("Database Error", f"An error occurred: {e}")

def calculate_bmi(event=None):
    try:
        weight = float(entry_weight.get().strip())  # Get weight in kg
        height_feet = float(entry_height.get().strip())  # Get height in feet

        height_meters = height_feet * 0.3048  # Convert feet to meters

        if height_meters > 0:  # Avoid division by zero
            bmi = round(weight / (height_meters ** 2), 2)  # Calculate BMI
            entry_bmi.config(state=NORMAL)  # Enable BMI field before updating
            entry_bmi.delete(0, END)
            entry_bmi.insert(0, str(bmi))
            entry_bmi.config(state=DISABLED)  # Set back to readonly
        else:
            entry_bmi.config(state=NORMAL)
            entry_bmi.delete(0, END)
            entry_bmi.insert(0, "Invalid")
            entry_bmi.config(state=DISABLED)
    except ValueError:
        entry_bmi.config(state=NORMAL)
        entry_bmi.delete(0, END)
        entry_bmi.insert(0, "Invalid")
        entry_bmi.config(state=DISABLED)


# Clear all input fields
def clear_entries():
    entry_name.delete(0, END)
    entry_age.delete(0, END)
    gender_var.set("")  # Clear gender selection
    entry_address.delete(0, END)
    entry_phone.delete(0, END)
    entry_email.delete(0, END)  # Clear email field
    entry_weight.delete(0, END)  # Clear weight field
    entry_height.delete(0, END)  # Clear height field
    entry_bmi.config(state=NORMAL)  # Enable BMI field before clearing
    entry_bmi.delete(0, END)  # Clear BMI field
    entry_bmi.config(state=DISABLED)  # Disable BMI field again
    membership_plan_var.set("")  # Clear membership plan selection
    entry_amount.delete(0, END)
    entry_due.delete(0, END)

    # Reset the registration date
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

# Name (Row 0)
Label(frame, text="Name", fg="white", bg="black", font=("Arial", 12)).grid(row=0, column=0, sticky=W, pady=5, padx=10)
entry_name = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_name.grid(row=0, column=1, pady=5, padx=10)

# Age (Row 1)
Label(frame, text="Age", fg="white", bg="black", font=("Arial", 12)).grid(row=1, column=0, sticky=W, pady=5, padx=10)
entry_age = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_age.grid(row=1, column=1, pady=5, padx=10)

# Gender (Row 2)
Label(frame, text="Gender", fg="white", bg="black", font=("Arial", 12)).grid(row=2, column=0, sticky=W, pady=5, padx=10)
gender_var = StringVar()
gender_dropdown = ttk.Combobox(frame, textvariable=gender_var, width=33, state="readonly", font=("Arial", 12))
gender_dropdown["values"] = ("Male", "Female")
gender_dropdown.grid(row=2, column=1, pady=5, padx=10)

# Address (Row 3)
Label(frame, text="Address", fg="white", bg="black", font=("Arial", 12)).grid(row=3, column=0, sticky=W, pady=5, padx=10)
entry_address = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_address.grid(row=3, column=1, pady=5, padx=10)

# Phone Number (Row 4)
Label(frame, text="Phone Number", fg="white", bg="black", font=("Arial", 12)).grid(row=4, column=0, sticky=W, pady=5, padx=10)
entry_phone = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_phone.grid(row=4, column=1, pady=5, padx=10)

# Email (Row 5)
Label(frame, text="Email", fg="white", bg="black", font=("Arial", 12)).grid(row=5, column=0, sticky=W, pady=5, padx=10)
entry_email = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_email.grid(row=5, column=1, pady=5, padx=10)

# Weight (Row 6)
Label(frame, text="Weight (kg)", fg="white", bg="black", font=("Arial", 12)).grid(row=6, column=0, sticky=W, pady=5, padx=10)
entry_weight = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_weight.grid(row=6, column=1, pady=5, padx=10)
entry_weight.bind("<KeyRelease>", calculate_bmi)  # Bind weight field

# Height (Row 7)
Label(frame, text="Height (m)", fg="white", bg="black", font=("Arial", 12)).grid(row=7, column=0, sticky=W, pady=5, padx=10)
entry_height = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_height.grid(row=7, column=1, pady=5, padx=10)
entry_height.bind("<KeyRelease>", calculate_bmi)  # Bind height field

# BMI (Row 8)
Label(frame, text="BMI", fg="white", bg="black", font=("Arial", 12)).grid(row=8, column=0, sticky=W, pady=5, padx=10)
entry_bmi = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12), state="readonly")
entry_bmi.grid(row=8, column=1, pady=5, padx=10)

# Membership Plan (Row 9)
Label(frame, text="Membership Plan", fg="white", bg="black", font=("Arial", 12)).grid(row=9, column=0, sticky=W, pady=5, padx=10)
membership_plan_var = StringVar()
membership_dropdown = ttk.Combobox(frame, textvariable=membership_plan_var, width=33, state="readonly", font=("Arial", 12))
membership_dropdown["values"] = ("Yearly", "Half-Yearly", "Monthly")
membership_dropdown.grid(row=9, column=1, pady=5, padx=10)
membership_dropdown.bind("<<ComboboxSelected>>", update_amount)

# Amount (Row 10)
Label(frame, text="Amount", fg="white", bg="black", font=("Arial", 12)).grid(row=10, column=0, sticky=W, pady=5, padx=10)
entry_amount = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_amount.grid(row=10, column=1, pady=5, padx=10)

# Amount Due (Row 11)
Label(frame, text="Amount Due", fg="white", bg="black", font=("Arial", 12)).grid(row=11, column=0, sticky=W, pady=5, padx=10)
entry_due = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_due.grid(row=11, column=1, pady=5, padx=10)

# Registration Date
Label(frame, text="Registration Date", fg="white", bg="black", font=("Arial", 12)).grid(row=12, column=0, sticky=W, pady=5, padx=10)
entry_date = Entry(frame, width=35, bg="gray", fg="white", insertbackground="white", font=("Arial", 12))
entry_date.grid(row=12, column=1, pady=5, padx=10)
entry_date.insert(0, datetime.now().strftime("%Y-%m-%d"))  # Default to today's date
entry_date.config(state=DISABLED)  # Make it read-only


# Save Button
save_button = Button(root, text="Save", bg="#1F77B4", fg="white", width=12, font=("Arial", 12), command=save_data)
save_button.pack(pady=10)

# Clear Entries Button
clear_button = Button(root, text="Clear Entries", bg="#D9534F", fg="white", width=12, font=("Arial", 12), command=clear_entries)
clear_button.pack(pady=10)



root.mainloop()
