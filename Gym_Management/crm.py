from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser
from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb
import os
import os
from tkinter import StringVar, messagebox
from ttkbootstrap.constants import *
from reportlab.lib.pagesizes import letter
from datetime import datetime
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Line, String, Group, Rect
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics.shapes import Circle
# Register a font
registerFont(TTFont("Times", "Times.ttf"))  # Ensure "Times.ttf" is available on your system

root = tb.Window(themename="superhero")
root.title('Gym Management- TreeBase')
root.geometry("1000x550")

# Read our config file and get colors
parser = ConfigParser()
parser.read("treebase.ini")
saved_primary_color = parser.get('colors', 'primary_color')
saved_secondary_color = parser.get('colors', 'secondary_color')
saved_highlight_color = parser.get('colors', 'highlight_color')




def query_database():
    # Clear the Treeview
    my_tree.delete(*my_tree.get_children())

    # Connect to database
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Fetch all records
    c.execute("SELECT * FROM customers")
    records = c.fetchall()

    # Initialize counter for row colors
    count = 0

    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='', 
                       values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10],record[11]), 
                       tags=('evenrow' if count % 2 == 0 else 'oddrow'))
        count += 1  # Increment counter

    # Commit and close connection
    conn.commit()
    conn.close()

def filter_records(filter_type):
    filter_window = Toplevel(root)
    filter_window.title("Filter Records")
    filter_window.geometry("400x200")

    Label(filter_window, text="Filter Options", font=("Helvetica", 14)).pack(pady=10)

    if filter_type == "expired":
        filter_button = Button(filter_window, text="Show Expired Memberships", command=show_expired)
    elif filter_type == "due":
        filter_button = Button(filter_window, text="Show Amount Due", command=show_due)

    filter_button.pack(pady=10)

# Function to filter expired memberships
def show_expired():
    my_tree.delete(*my_tree.get_children())  # Clear Treeview

    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE status = 'Expired'")
    records = c.fetchall()

    count = 0
    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='',
                       values=(record[0], record[1], record[2], record[3], record[4], 
                               record[5], record[6], record[7], record[8], record[9], record[10], record[11]),
                       tags=('evenrow' if count % 2 == 0 else 'oddrow'))
        count += 1

    conn.commit()
    conn.close()

# Function to filter members with due amount
def show_due():
    my_tree.delete(*my_tree.get_children())  # Clear Treeview

    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE amount_due > 0")
    records = c.fetchall()

    count = 0
    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='',
                       values=(record[0], record[1], record[2], record[3], record[4], 
                               record[5], record[6], record[7], record[8], record[9], record[10], record[11]),
                       tags=('evenrow' if count % 2 == 0 else 'oddrow'))
        count += 1

    conn.commit()
    conn.close()

style = tb.Style(theme="solar")  # Change "darkly" to any preferred theme




def search_records():
    lookup_record = search_entry.get().strip()

    if not lookup_record:
        messagebox.showerror("Error", "Please enter a name to search!")
        return

    # Close the search box
    search.destroy()

    # Clear the Treeview
    my_tree.delete(*my_tree.get_children())

    # Connect to database
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Secure search query with wildcard for partial matches
    c.execute("SELECT * FROM customers WHERE name LIKE ?", ('%' + lookup_record + '%',))
    records = c.fetchall()

    # Initialize counter for row colors
    count = 0

    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='',
                       values=(record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10],record[11]),
                       tags=('evenrow' if count % 2 == 0 else 'oddrow'))
        count += 1  # Increment counter

    # Commit and close connection
    conn.commit()
    conn.close()

    # Show message if no results found
    if not records:
        messagebox.showinfo("Not Found", "No records matched your search.")




def lookup_records():
	global search_entry, search

	search = Toplevel(root)
	search.title("Lookup Records")
	search.geometry("400x200")
	

	# Create label frame
	search_frame = LabelFrame(search, text=" Name")
	search_frame.pack(padx=10, pady=10)

	# Add entry box
	search_entry = Entry(search_frame, font=("Helvetica", 18))
	search_entry.pack(pady=20, padx=20)

	# Add button
	search_button = tb.Button(search, text="Search Records",bootstyle = "info.Outline", command=search_records)
	search_button.pack(padx=20, pady=20)


def primary_color():
	# Pick Color
	primary_color = colorchooser.askcolor()[1]

	# Update Treeview Color
	if primary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('evenrow', background=primary_color)

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'primary_color', primary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)


def secondary_color():
	# Pick Color
	secondary_color = colorchooser.askcolor()[1]
	
	# Update Treeview Color
	if secondary_color:
		# Create Striped Row Tags
		my_tree.tag_configure('oddrow', background=secondary_color)
		
		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'secondary_color', secondary_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def highlight_color():
	# Pick Color
	highlight_color = colorchooser.askcolor()[1]

	#Update Treeview Color
	# Change Selected Color
	if highlight_color:
		style.map('Treeview',
			background=[('selected', highlight_color)])

		# Config file
		parser = ConfigParser()
		parser.read("treebase.ini")
		# Set the color change
		parser.set('colors', 'highlight_color', highlight_color)
		# Save the config file
		with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)

def reset_colors():
	# Save original colors to config file
	parser = ConfigParser()
	parser.read('treebase.ini')
	parser.set('colors', 'primary_color', 'lightblue')
	parser.set('colors', 'secondary_color', 'white')
	parser.set('colors', 'highlight_color', '#347083')
	with open('treebase.ini', 'w') as configfile:
			parser.write(configfile)
	# Reset the colors
	my_tree.tag_configure('oddrow', background='white')
	my_tree.tag_configure('evenrow', background='lightblue')
	style.map('Treeview',
			background=[('selected', '#347083')])

# Add Menu
my_menu = Menu(root)
root.config(menu=my_menu)



# Configure our menu
option_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Options", menu=option_menu)
# Drop down menu
option_menu.add_command(label="Primary Color", command=primary_color)
option_menu.add_command(label="Secondary Color", command=secondary_color)
option_menu.add_command(label="Highlight Color", command=highlight_color)
option_menu.add_separator()
option_menu.add_command(label="Reset Colors", command=reset_colors)
option_menu.add_separator()
option_menu.add_command(label="Exit", command=root.quit)

#Search Menu
search_menu = Menu(my_menu, tearoff=0)
my_menu.add_cascade(label="Search", menu=search_menu)
# Drop down menu
search_menu.add_command(label="Search", command=lookup_records)
search_menu.add_separator()
search_menu.add_command(label="Reset", command=query_database)
# Direct menu options
my_menu.add_command(label="Expired Memberships", command=lambda: filter_records("expired"))
my_menu.add_command(label="Amount Due", command=lambda: filter_records("due"))
my_menu.add_command(label="Reset", command=query_database)  # Reset to show all records
# Dummy data to insert into the database
dummy_data = [
    ("John Doe", 25, "123 Elm Street", "john.doe@example.com", "1234567890", "2023-01-01", "Monthly", 500.0, 0.0, "2023-01-31", "Active"),
    ("Jane Smith", 30, "456 Oak Avenue", "jane.smith@example.com", "9876543210", "2023-02-01", "Quarterly", 1500.0, 500.0, "2023-04-30", "Active"),
    ("Alice Johnson", 28, "789 Pine Road", "alice.johnson@example.com", "5551234567", "2022-12-01", "Yearly", 6000.0, 0.0, "2023-11-30", "Expired"),
    ("Bob Brown", 35, "321 Maple Lane", "bob.brown@example.com", "4449876543", "2023-03-01", "Monthly", 500.0, 500.0, "2023-03-31", "Active"),
    ("Charlie Davis", 40, "654 Cedar Drive", "charlie.davis@example.com", "3334567890", "2023-01-15", "Monthly", 500.0, 0.0, "2023-02-14", "Expired"),
]

# Insert dummy data into the database
conn = sqlite3.connect('gym.db')
c = conn.cursor()

for record in dummy_data:
    c.execute("""
        INSERT INTO customers (name, age, address, email, phone, join_date, membership_plan, amount, amount_due, membership_expiry, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, record)

conn.commit()
conn.close()


# Do some database stuff
# Create a database or connect to one that exists
conn = sqlite3.connect('gym.db')

# Connect to database
conn = sqlite3.connect('gym.db')

# Create a cursor instance
c = conn.cursor()

# Create Table
c.execute('''CREATE TABLE IF NOT EXISTS customers (
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

# # Add dummy data to table (Uncomment to insert initial data)

# # Add dummy data to table

# for record in data:
#     c.execute("INSERT INTO customers (name, age, id, address, email, phone, join_date, membership_plan,amount, amount_due, membership_expiry, status) VALUES (:name, :age, :id, :address, :email, :phone, :join_date, :membership_plan,:amount, :amount_due, :membership_expiry, :status)", 
#         {
#             'name': record[0],
#             'age': record[1],
#             'id': record[2],
#             'address': record[3],
#             'email': record[4],
#             'phone': record[5],
#             'join_date': record[6],
#             'membership_plan': record[7],
#             'amount': record[8],
#             'amount_due': record[9],
#             'membership_expiry': record[10],
#             'status': record[11]
#         }
#     )


# conn.commit()  # ✅ Save changes

# conn.close()



# Add Some Style
style = ttk.Style()

# Pick A Theme
style.theme_use('default')

# Configure the Treeview Colors
style.configure("Treeview",
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	fieldbackground="#D3D3D3")

# Change Selected Color #347083
style.map('Treeview',
	background=[('selected', saved_highlight_color)])

# Create a Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)

# Create a Treeview Scrollbar
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

# Create The Treeview
my_tree = tb.Treeview(tree_frame, yscrollcommand=tree_scroll.set,bootstyle = "success", selectmode="extended")
my_tree.pack()


# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Member ID", "Name", "Age", "Address", "Email", "Phone", "Join Date", "Membership Plan","Amount", "Amount Due", "Membership Expiry", "Status")


# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)  # Hides the first column
my_tree.column("Member ID", anchor=CENTER, width=100)
my_tree.column("Name", anchor=W, width=140)
my_tree.column("Age", anchor=CENTER, width=60)
my_tree.column("Address", anchor=W, width=180)
my_tree.column("Email", anchor=W, width=180)
my_tree.column("Phone", anchor=CENTER, width=120)
my_tree.column("Join Date", anchor=CENTER, width=100)
my_tree.column("Membership Plan", anchor=CENTER, width=140)
my_tree.column("Amount", anchor=CENTER, width=100)
my_tree.column("Amount Due", anchor=CENTER, width=100)
my_tree.column("Membership Expiry", anchor=CENTER, width=120)
my_tree.column("Status", anchor=CENTER, width=100)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Member ID", text="Member ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Age", text="Age", anchor=CENTER)
my_tree.heading("Address", text="Address", anchor=W)
my_tree.heading("Email", text="Email", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=CENTER)
my_tree.heading("Join Date", text="Join Date", anchor=CENTER)
my_tree.heading("Membership Plan", text="Membership Plan", anchor=CENTER)
my_tree.heading("Amount", text="Amount", anchor=CENTER)
my_tree.heading("Amount Due", text="Amount Due", anchor=CENTER)
my_tree.heading("Membership Expiry", text="Membership Expiry", anchor=CENTER)
my_tree.heading("Status", text="Status", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)


# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Member Details")
data_frame.pack(fill="x", expand="yes", padx=20, pady=10)

# Name
n_label = tb.Label(data_frame, text="Name",bootstyle="success")
n_label.grid(row=0, column=0, padx=10, pady=10)
n_entry = tb.Entry(data_frame,bootstyle="success")
n_entry.grid(row=0, column=1, padx=10, pady=10)

# Age
age_label = Label(data_frame, text="Age")
age_label.grid(row=0, column=2, padx=10, pady=10)
age_entry = Entry(data_frame)
age_entry.grid(row=0, column=3, padx=10, pady=10)

# Member ID
id_label = Label(data_frame, text="Member ID")
id_label.grid(row=0, column=4, padx=10, pady=10)
id_entry = Entry(data_frame)
id_entry.grid(row=0, column=5, padx=10, pady=10)

# Address
address_label = Label(data_frame, text="Address")
address_label.grid(row=1, column=0, padx=10, pady=10)
address_entry = Entry(data_frame)
address_entry.grid(row=1, column=1, padx=10, pady=10)

# Email
email_label = Label(data_frame, text="Email")
email_label.grid(row=1, column=2, padx=10, pady=10)
email_entry = Entry(data_frame)
email_entry.grid(row=1, column=3, padx=10, pady=10)

# Phone
phone_label = Label(data_frame, text="Phone")
phone_label.grid(row=1, column=4, padx=10, pady=10)
phone_entry = Entry(data_frame)
phone_entry.grid(row=1, column=5, padx=10, pady=10)

# Join Date
join_date_label = Label(data_frame, text="Join Date (YYYY-MM-DD)")
join_date_label.grid(row=2, column=0, padx=10, pady=10)
join_date_entry = Entry(data_frame)
join_date_entry.grid(row=2, column=1, padx=10, pady=10)

# Membership Plan
membership_label = Label(data_frame, text="Membership Plan")
membership_label.grid(row=2, column=2, padx=10, pady=10)
membership_entry = Entry(data_frame)
membership_entry.grid(row=2, column=3, padx=10, pady=10)


# Amount Due
amount_due_label = Label(data_frame, text="Amount Due")
amount_due_label.grid(row=2, column=4, padx=10, pady=10)
amount_due_entry = Entry(data_frame)
amount_due_entry.grid(row=2, column=5, padx=10, pady=10)

# Membership Expiry
expiry_label = Label(data_frame, text="Membership Expiry (YYYY-MM-DD)")
expiry_label.grid(row=3, column=0, padx=10, pady=10)
expiry_entry = Entry(data_frame)
expiry_entry.grid(row=3, column=1, padx=10, pady=10)

# Membership Status
status_label = Label(data_frame, text="Status")
status_label.grid(row=3, column=2, padx=10, pady=10)
status_entry = Entry(data_frame)
status_entry.grid(row=3, column=3, padx=10, pady=10)

#Amount
amount_label = Label(data_frame, text="Amount")
amount_label.grid(row=3, column=4, padx=10, pady=10)
amount_entry = Entry(data_frame)
amount_entry.grid(row=3, column=5, padx=10, pady=10)

# Move Row Up
def up():
	rows = my_tree.selection()
	for row in rows:
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Rown Down
def down():
	rows = my_tree.selection()
	for row in reversed(rows):
		my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)

# Remove One Record
def remove_one():
    selected = my_tree.selection()

    if not selected:
        messagebox.showerror("Error", "No record selected!")
        return

    # Get selected record's ID
    selected_values = my_tree.item(selected, 'values')
    member_id = selected_values[0]  # Assuming 'ID' is the first column

    # Delete from Treeview
    my_tree.delete(selected)

    # Delete from database
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    c.execute("DELETE FROM customers WHERE id = ?", (member_id,))
    conn.commit()
    conn.close()

    # Clear Entry Boxes
    clear_entries()

    messagebox.showinfo("Deleted!", f"Member ID {member_id} has been deleted.")


# Remove Multiple Selected Records
def remove_many():
    selected_items = my_tree.selection()

    if not selected_items:
        messagebox.showerror("Error", "No records selected!")
        return

    # Confirm deletion
    response = messagebox.askyesno("Confirm", "Are you sure you want to delete the selected records?")

    if response == 1:
        # Collect IDs to delete
        ids_to_delete = [my_tree.item(item, 'values')[0] for item in selected_items]

        # Delete from Treeview
        for item in selected_items:
            my_tree.delete(item)

        # Delete from database
        conn = sqlite3.connect('gym.db')
        c = conn.cursor()
        c.executemany("DELETE FROM customers WHERE id = ?", [(member_id,) for member_id in ids_to_delete])
        conn.commit()
        conn.close()

        # Clear Entry Boxes
        clear_entries()

        messagebox.showinfo("Deleted!", "Selected records have been deleted.")

## Remove All Records (Drop Table and Recreate)
def remove_all():
    response = messagebox.askyesno("Confirm", "Are you sure you want to DELETE ALL records and DROP the table?")

    if response == 1:
        # Clear the Treeview
        my_tree.delete(*my_tree.get_children())

        # Drop the table (completely removes it)
        conn = sqlite3.connect('gym.db')
        c = conn.cursor()
        c.execute("DROP TABLE IF EXISTS customers")  # Ensures no error if table doesn't exist
        conn.commit()
        conn.close()

        # Clear Entry Boxes
        clear_entries()

        # Recreate the table structure
        create_table_again()

        messagebox.showinfo("Deleted!", "All records have been deleted, and the table structure has been recreated.")


# Function to clear all entry fields
def clear_entries():
    n_entry.delete(0, END)
    age_entry.delete(0, END)
    id_entry.delete(0, END)
    address_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_entry.delete(0, END)  # Added missing phone field
    join_date_entry.delete(0, END)
    membership_entry.delete(0, END)
    amount_entry.delete(0, END)  # Added missing amount field
    amount_due_entry.delete(0, END)
    expiry_entry.delete(0, END)
    status_entry.delete(0, END)  # Added missing status field

# Select Record
def select_record(e):
    # Clear existing entries
    clear_entries()

    # Grab the selected row
    selected = my_tree.focus()
    
    # Grab record values
    values = my_tree.item(selected, 'values')

    # Ensure values exist before inserting into entry fields
    if not values:
        return  # Avoids errors if no row is selected

    # Output values to entry boxes
    id_entry.insert(0, values[0])  # Member ID
    n_entry.insert(0, values[1])  # Name
    age_entry.insert(0, values[2])  # Age
    address_entry.insert(0, values[3])  # Address
    email_entry.insert(0, values[4])  # Email
    phone_entry.insert(0, values[5])  # Phone (Added missing field)
    join_date_entry.insert(0, values[6])  # Join Date
    membership_entry.insert(0, values[7])  # Membership Plan
    amount_entry.insert(0, values[8])  # Amount (Added missing field)
    amount_due_entry.insert(0, values[8])  # Amount Due
    expiry_entry.insert(0, values[9])  # Membership Expiry
    status_entry.insert(0, values[10])  # Membership Status (Added missing field)


# Update record
def update_record():
	# Grab the record number
	selected = my_tree.focus()
	# Update record
	my_tree.item(selected, text="", values=(
		id_entry.get(), n_entry.get(), age_entry.get(), address_entry.get(), email_entry.get(),
		phone_entry.get(), join_date_entry.get(), membership_entry.get(),amount_entry.get(), amount_due_entry.get(),
		expiry_entry.get(), status_entry.get()
	))
	# Update the database
	# Create a database or connect to one that exists
	conn = sqlite3.connect('gym.db')

	# Create a cursor instance
	c = conn.cursor()

	# Update record in the database
	c.execute("""UPDATE customers SET
		name = :name,
		age = :age,
		address = :address,
		email = :email,
		phone = :phone,
		join_date = :join_date,
		membership_plan = :membership_plan,
        amount = :amount,
		amount_due = :amount_due,
		membership_expiry = :membership_expiry,
		status = :status
		WHERE id = :id""",
		{
			'name': n_entry.get(),
			'age': age_entry.get(),
			'address': address_entry.get(),
			'email': email_entry.get(),
			'phone': phone_entry.get(),
			'join_date': join_date_entry.get(),
			'membership_plan': membership_entry.get(),
            'amount': amount_entry.get(),
            'amount_due': amount_due_entry.get(),
			'membership_expiry': expiry_entry.get(),
			'status': status_entry.get(),
			'id': id_entry.get()
		})

	# Commit changes and close connection
	conn.commit()
	conn.close()

	# Clear entry boxes
	clear_entries()

	# Show success message
	messagebox.showinfo("Success", "Record updated successfully!")

# Add new record to database
def add_record():
    # Check if required fields are filled
    if not n_entry.get() or not id_entry.get():
        messagebox.showerror("Error", "Name and ID are required!")
        return

    # Create a database or connect to one that exists
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Add New Record
    c.execute("INSERT INTO customers (id, name, age, address, email, phone, join_date, membership_plan, amount_due, membership_expiry, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (id_entry.get(), n_entry.get(), age_entry.get(), address_entry.get(), email_entry.get(), phone_entry.get(),
               join_date_entry.get(), membership_entry.get(), amount_entry.get(),amount_due_entry.get(), expiry_entry.get(), status_entry.get()))

    # Commit changes and close connection
    conn.commit()
    conn.close()

    # Clear entry boxes
    clear_entries()

    # Refresh Treeview to show the new data
    my_tree.delete(*my_tree.get_children())
    query_database()

    # Show success message
    messagebox.showinfo("Success", "Record added successfully!")

# Create customers table if it does not exist
def create_table_again():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Create Table
    c.execute('''CREATE TABLE IF NOT EXISTS customers (
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

    # Commit and close
    conn.commit()
    conn.close()



# Fetch Data from Database
def fetch_customer_details(customer_name):
    conn = sqlite3.connect("gym.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT gym_name, address FROM users LIMIT 1")
    gym_data = cursor.fetchone()
    gym_name, gym_address = gym_data if gym_data else ("My Gym", "No Address Available")
    
    cursor.execute("""
        SELECT id, name, phone, join_date, membership_expiry, amount 
        FROM customers WHERE name LIKE ? LIMIT 1
    """, (f"%{customer_name}%",))
    customer_data = cursor.fetchone()
    
    conn.close()
    
    if customer_data:
        return {
            "id": customer_data[0],
            "gym_name": gym_name,
            "gym_address": gym_address,
            "name": customer_data[1],
            "phone": customer_data[2],
            "join_date": customer_data[3],
            "membership_expiry": customer_data[4],
            "amount": customer_data[5],
            "date": datetime.today().strftime("%Y-%m-%d")
        }
    return None

def create_dumbbell():
    """Create a simple dumbbell logo using lines and circles."""
    return Group(
        Line(40, 100, 160, 100, strokeWidth=8, strokeColor=colors.black),  # Bar
        Line(40, 110, 40, 90, strokeWidth=10, strokeColor=colors.black),   # Left Weight
        Line(160, 110, 160, 90, strokeWidth=10, strokeColor=colors.black)  # Right Weight
    )
    dumbbell.translate(150, -30)  # Move it lower
    return dumbbell
# Generate Receipt PDF

def generate_receipt(customer_name):
    data = fetch_customer_details(customer_name)
    if not data:
        messagebox.showerror("Error", "No customer data found!")
        return
    
    receipt_folder = "receipt"
    os.makedirs(receipt_folder, exist_ok=True)
    receipt_path = os.path.join(receipt_folder, f"{data['name']}_receipt.pdf")
    
    c = canvas.Canvas(receipt_path, pagesize=letter)
    width, height = letter
    
    # Drawing Gym Name & Logo
    drawing = Drawing(200, 50)
    drawing.add(create_dumbbell())
    drawing.add(String(60, 120, data["gym_name"], fontName="Times", fontSize=16, fillColor=colors.black))
    drawing.drawOn(c, 150, 650)

    # Separator Line
    c.setStrokeColor(colors.grey)
    c.setLineWidth(2)
    c.line(50, 680, 550, 680)

    # Gym Address
    c.setFont("Times", 12)
    c.drawString(180, 660, f"Address: {data['gym_address']}")

    # Receipt Details
    c.drawString(50, 620, f"Date: {data['date']}")
    c.drawString(350, 620, f"Mobile No: {data['phone']}")
    
    c.drawString(50, 590, f"Received with thanks from: {data['name']}")
    c.drawString(50, 560, f"Being fees for the gymnasium from {data['join_date']} to {data['membership_expiry']}")
    
    c.setFont("Times-Bold", 14)
    c.drawString(50, 520, f"Rs. {data['amount']}")

    # Signature Lines
    c.setFont("Times", 12)
    c.line(50, 450, 200, 450)
    c.drawString(80, 435, "Member's Signature")

    c.line(350, 450, 500, 450)
    c.drawString(390, 435, "Sir's Signature")
    
    c.save()
    messagebox.showinfo("Success", f"Receipt saved at: {receipt_path}")

def generate_receipt_ui():
    selected = my_tree.focus()
    values = my_tree.item(selected, 'values')

    if not values:
        messagebox.showerror("Error", "No record selected!")
        return
    
    customer_name = values[1]  # Assuming Name is the second column
    generate_receipt(customer_name)
def show_reports():
    print("Show Reports button clicked!")  # Replace with actual functionality

# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20, pady= 20 )

update_button = tb.Button(button_frame, text="Update Record", bootstyle="success",command=update_record)
update_button.grid(row=0, column=0, padx=10, pady=10)

add_button = Button(button_frame, text="Add Record", command=add_record)
add_button.grid(row=0, column=1, padx=10, pady=10)

remove_all_button = Button(button_frame, text="Remove All Records", command=remove_all)
remove_all_button.grid(row=0, column=2, padx=10, pady=10)

remove_one_button = Button(button_frame, text="Remove One Selected", command=remove_one)
remove_one_button.grid(row=0, column=3, padx=10, pady=10)

remove_many_button = Button(button_frame, text="Remove Many Selected", command=remove_many)
remove_many_button.grid(row=0, column=4, padx=10, pady=10)

move_up_button = Button(button_frame, text="Move Up", command=up)
move_up_button.grid(row=0, column=5, padx=10, pady=10)

move_down_button = Button(button_frame, text="Move Down", command=down)
move_down_button.grid(row=0, column=6, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

select_record_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
select_record_button.grid(row=0, column=7, padx=10, pady=10)

receipt_button = Button(button_frame, text="Generate Receipt", command=generate_receipt_ui)
receipt_button.grid(row=0, column=8, padx=10, pady=10)

show_reports_button = Button(button_frame, text="Show Reports", command=show_reports)
show_reports_button.grid(row=0, column=9, padx=10, pady=10)




# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()