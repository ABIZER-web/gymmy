from tkinter import messagebox
import ttkbootstrap as ttk
import sqlite3
from ttkbootstrap.constants import *


# Database setup
def init_db():
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        address TEXT,
        email TEXT,
        phone TEXT,
        join_date TEXT,
        membership_plan TEXT,
        amount REAL,
        amount_due REAL,
        membership_expiry TEXT,
        status TEXT
    )''')
    conn.commit()
    conn.close()

class GymMemberRegistration(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(20, 10))
        self.pack(fill=BOTH, expand=YES)
        
        # Form variables
        self.name = ttk.StringVar()
        self.age = ttk.StringVar()
        self.address = ttk.StringVar()
        self.email = ttk.StringVar()
        self.phone = ttk.StringVar()
        self.join_date = ttk.StringVar()
        self.membership_plan = ttk.StringVar()
        self.amount = ttk.StringVar()   # New amount field
        self.amount_due = ttk.StringVar()
        self.membership_expiry = ttk.StringVar()
        self.status = ttk.StringVar()
        
        # Form Header
        hdr_txt = "Register New Gym Member"
        hdr = ttk.Label(master=self, text=hdr_txt, width=50, font=("Arial", 14, "bold"))
        hdr.pack(fill=X, pady=10)
        
        # Creating form fields
        self.create_form_entry("Name", self.name)
        self.create_form_entry("Age", self.age)
        self.create_form_entry("Address", self.address)
        self.create_form_entry("Email", self.email)
        self.create_form_entry("Phone", self.phone)
        self.create_form_entry("Join Date (YYYY-MM-DD)", self.join_date)
        self.create_form_entry("Membership Plan", self.membership_plan)
        self.create_form_entry("Amount", self.amount)   # New input field
        self.create_form_entry("Amount Due", self.amount_due)
        self.create_form_entry("Membership Expiry (YYYY-MM-DD)", self.membership_expiry)
        self.create_form_entry("Status (Active/Inactive)", self.status)
        
        self.create_buttonbox()
    
    def create_form_entry(self, label, variable):
        """Create a single form entry"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=5)
        
        lbl = ttk.Label(master=container, text=label, width=20)
        lbl.pack(side=LEFT, padx=5)
        
        ent = ttk.Entry(master=container, textvariable=variable)
        ent.pack(side=LEFT, padx=5, fill=X, expand=YES)
    
    def create_buttonbox(self):
        """Create buttons"""
        container = ttk.Frame(self)
        container.pack(fill=X, expand=YES, pady=(15, 10))
        
        sub_btn = ttk.Button(
            master=container,
            text="Submit",
            command=self.save_to_db,
            bootstyle=SUCCESS,
            width=8,
        )
        sub_btn.pack(side=RIGHT, padx=5)
        sub_btn.focus_set()
        
        cnl_btn = ttk.Button(
            master=container,
            text="Cancel",
            command=self.quit,
            bootstyle=DANGER,
            width=8,
        )
        cnl_btn.pack(side=RIGHT, padx=5)
    
    def save_to_db(self):
        """Save form data to SQLite database"""
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO customers (name, age, address, email, phone, join_date, 
                        membership_plan, amount, amount_due, membership_expiry, status) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            self.name.get(), self.age.get(), self.address.get(),
            self.email.get(), self.phone.get(), self.join_date.get(),
            self.membership_plan.get(), self.amount.get(),  # Added amount field
            self.amount_due.get(), self.membership_expiry.get(), self.status.get()
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Member Registered Successfully!")
        
if __name__ == "__main__":
    init_db()
    app = ttk.Window("Gym Member Registration", "superhero", resizable=(False, False))
    GymMemberRegistration(app)
    app.mainloop()
