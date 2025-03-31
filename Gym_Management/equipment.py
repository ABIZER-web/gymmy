from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from tkinter import colorchooser
from configparser import ConfigParser
from ttkbootstrap import *
from ttkbootstrap.dialogs import Messagebox
import ttkbootstrap as tb
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from datetime import datetime

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
    c.execute("SELECT * FROM equipment")
    records = c.fetchall()

    # Initialize counter for row colors
    count = 0

    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='', 
                       values=(record[0], record[1], record[2], record[3], record[4]), 
                       tags=('evenrow' if count % 2 == 0 else 'oddrow'))
        count += 1  # Increment counter

    # Commit and close connection
    conn.commit()
    conn.close()

style = tb.Style(theme="solar")  # Change "solar" to any preferred theme

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
    c.execute("SELECT * FROM equipment WHERE name LIKE ?", ('%' + lookup_record + '%',))
    records = c.fetchall()

    # Initialize counter for row colors
    count = 0

    for record in records:
        my_tree.insert(parent='', index='end', iid=count, text='',
                       values=(record[0], record[1], record[2], record[3], record[4]),
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
    search_button = tb.Button(search, text="Search Records", bootstyle="info.Outline", command=search_records)
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

data = [
    ("Treadmill", "Cardio", "2023-01-01", "Good"),
    ("Elliptical", "Cardio", "2022-12-01", "Excellent"),
    ("Bench Press", "Strength", "2023-03-15", "Good"),
    ("Dumbbells", "Strength", "2021-07-10", "Fair"),
    ("Rowing Machine", "Cardio", "2023-05-20", "Good"),
]

# Do some database stuff
# Create a database or connect to one that exists
conn = sqlite3.connect('gym.db')

# Create a cursor instance
c = conn.cursor()

# Create Table
c.execute("""CREATE TABLE IF NOT EXISTS equipment (
    id INTEGER PRIMARY KEY, 
    name TEXT, 
    type TEXT, 
    purchase_date TEXT, 
    condition TEXT
    )
""")

# Add dummy data to table (Uncomment to insert initial data)

# for record in data:
#     c.execute("INSERT INTO equipment (name, type, purchase_date, condition) VALUES (:name, :type, :purchase_date, :condition)", 
#         {
#             'name': record[0],
#             'type': record[1],
#             'purchase_date': record[2],
#             'condition': record[3]
#         }
#     )

conn.commit()  # ✅ Save changes

conn.close()

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
my_tree = tb.Treeview(tree_frame, yscrollcommand=tree_scroll.set, bootstyle="success", selectmode="extended")
my_tree.pack()

# Configure the Scrollbar
tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Equipment ID", "Name", "Type", "Purchase Date", "Condition")

# Format Our Columns
my_tree.column("#0", width=0, stretch=NO)  # Hides the first column
my_tree.column("Equipment ID", anchor=CENTER, width=100)
my_tree.column("Name", anchor=W, width=140)
my_tree.column("Type", anchor=CENTER, width=100)
my_tree.column("Purchase Date", anchor=CENTER, width=120)
my_tree.column("Condition", anchor=CENTER, width=100)

# Create Headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Equipment ID", text="Equipment ID", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Type", text="Type", anchor=CENTER)
my_tree.heading("Purchase Date", text="Purchase Date", anchor=CENTER)
my_tree.heading("Condition", text="Condition", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background=saved_secondary_color)
my_tree.tag_configure('evenrow', background=saved_primary_color)

# Add Record Entry Boxes
data_frame = LabelFrame(root, text="Equipment Details")
data_frame.pack(fill="x", expand="yes", padx=20, pady=10)

# Equipment ID
id_label = tb.Label(data_frame, text="Equipment ID", bootstyle="success")
id_label.grid(row=0, column=0, padx=10, pady=10)
id_entry = tb.Entry(data_frame, bootstyle="success")
id_entry.grid(row=0, column=1, padx=10, pady=10)

# Name
n_label = tb.Label(data_frame, text="Name", bootstyle="success")
n_label.grid(row=0, column=2, padx=10, pady=10)
n_entry = tb.Entry(data_frame, bootstyle="success")
n_entry.grid(row=0, column=3, padx=10, pady=10)

# Type
type_label = Label(data_frame, text="Type")
type_label.grid(row=0, column=4, padx=10, pady=10)
type_entry = Entry(data_frame)
type_entry.grid(row=0, column=5, padx=10, pady=10)

# Purchase Date
purchase_date_label = Label(data_frame, text="Purchase Date (YYYY-MM-DD)")
purchase_date_label.grid(row=1, column=0, padx=10, pady=10)
purchase_date_entry = Entry(data_frame)
purchase_date_entry.grid(row=1, column=1, padx=10, pady=10)

# Condition
condition_label = Label(data_frame, text="Condition")
condition_label.grid(row=1, column=2, padx=10, pady=10)
condition_entry = Entry(data_frame)
condition_entry.grid(row=1, column=3, padx=10, pady=10)

# Move Row Up
def up():
    rows = my_tree.selection()
    for row in rows:
        my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

# Move Row Down
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
    equipment_id = selected_values[0]  # Assuming 'ID' is the first column

    # Delete from Treeview
    my_tree.delete(selected)

    # Delete from database
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()
    c.execute("DELETE FROM equipment WHERE id = ?", (equipment_id,))
    conn.commit()
    conn.close()

    # Clear Entry Boxes
    clear_entries()

    messagebox.showinfo("Deleted!", f"Equipment ID {equipment_id} has been deleted.")

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
        c.executemany("DELETE FROM equipment WHERE id = ?", [(equipment_id,) for equipment_id in ids_to_delete])
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
        c.execute("DROP TABLE IF EXISTS equipment")  # Ensures no error if table doesn't exist
        conn.commit()
        conn.close()

        # Clear Entry Boxes
        clear_entries()

        # Recreate the table structure
        create_table_again()

        messagebox.showinfo("Deleted!", "All records have been deleted, and the table structure has been recreated.")

# Function to clear all entry fields
def clear_entries():
    id_entry.delete(0, END)
    n_entry.delete(0, END)
    type_entry.delete(0, END)
    purchase_date_entry.delete(0, END)
    condition_entry.delete(0, END)

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
    id_entry.insert(0, values[0])  # Equipment ID
    n_entry.insert(0, values[1])  # Name
    type_entry.insert(0, values[2])  # Type
    purchase_date_entry.insert(0, values[3])  # Purchase Date
    condition_entry.insert(0, values[4])  # Condition

# Update record
def update_record():
    # Grab the record number
    selected = my_tree.focus()
    # Update record
    my_tree.item(selected, text="", values=(
        id_entry.get(), n_entry.get(), type_entry.get(), purchase_date_entry.get(), condition_entry.get()
    ))
    # Update the database
    # Create a database or connect to one that exists
    conn = sqlite3.connect('gym.db')

    # Create a cursor instance
    c = conn.cursor()

    # Update record in the database
    c.execute("""UPDATE equipment SET
        name = :name,
        type = :type,
        purchase_date = :purchase_date,
        condition = :condition
        WHERE id = :id""",
        {
            'name': n_entry.get(),
            'type': type_entry.get(),
            'purchase_date': purchase_date_entry.get(),
            'condition': condition_entry.get(),
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

    # Validate Purchase Date format
    try:
        datetime.strptime(purchase_date_entry.get(), '%Y-%m-%d')
    except ValueError:
        messagebox.showerror("Error", "Purchase Date must be in YYYY-MM-DD format!")
        return

    # Create a database or connect to one that exists
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Add New Record
    c.execute("INSERT INTO equipment (id, name, type, purchase_date, condition) VALUES (?, ?, ?, ?, ?)",
              (id_entry.get(), n_entry.get(), type_entry.get(), purchase_date_entry.get(), condition_entry.get()))
    
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

# Create equipment table if it does not exist
def create_table_again():
    conn = sqlite3.connect('gym.db')
    c = conn.cursor()

    # Create Table
    c.execute("""CREATE TABLE IF NOT EXISTS equipment (
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        purchase_date TEXT,
        condition TEXT
    )""")

    # Commit and close
    conn.commit()
    conn.close()

# Add Buttons
button_frame = LabelFrame(root, text="Commands")
button_frame.pack(fill="x", expand="yes", padx=20, pady=20)

update_button = tb.Button(button_frame, text="Update Record", bootstyle="success", command=update_record)
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

clear_entries_button = Button(button_frame, text="Clear Entry Boxes", command=clear_entries)
clear_entries_button.grid(row=0, column=7, padx=10, pady=10)

# Bind the treeview
my_tree.bind("<ButtonRelease-1>", select_record)

# Run to pull data from database on start
query_database()

root.mainloop()