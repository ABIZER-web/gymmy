import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from db_helper import get_db_connection  # Import helper function for DB connection
from ttkbootstrap.constants import *
import ttkbootstrap as tb

def fetch_equipment():
    """Fetches all equipment details from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, status, unit, last_serviced, next_maintenance FROM equipment")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_equipment():
    """Adds new equipment to the database."""
    name = name_entry.get()
    status = status_var.get()
    unit = unit_entry.get()
    last_serviced = last_serviced_entry.get_date().strftime('%d/%m/%Y')
    next_maintenance = next_maintenance_entry.get_date().strftime('%d/%m/%Y')
    
    if not name or not unit or not last_serviced or not next_maintenance:
        messagebox.showwarning("Input Error", "Please fill all fields!")
        return
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO equipment (name, status, unit, last_serviced, next_maintenance) VALUES (?, ?, ?, ?, ?)",
                   (name, status, unit, last_serviced, next_maintenance))
    conn.commit()
    conn.close()
    refresh_table()
    add_window.destroy()

def delete_equipment():
    """Deletes selected equipment."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an equipment to delete!")
        return
    
    item_id = tree.item(selected_item)['values'][0]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM equipment WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    refresh_table()

def refresh_table():
    """Refreshes the equipment list."""
    for row in tree.get_children():
        tree.delete(row)
    
    equipment = fetch_equipment()
    for item in equipment:
        tree.insert("", "end", values=item)
    total_count_label.config(text=f"Total Equipment: {len(equipment)}")

def search_equipment():
    """Search equipment by name or status."""
    query = search_entry.get().lower()
    for row in tree.get_children():
        values = tree.item(row)['values']
        if query in str(values[1]).lower() or query in str(values[2]).lower():
            tree.selection_set(row)
            tree.see(row)
            return
    messagebox.showinfo("Search", "No matching equipment found.")

def open_add_equipment_window():
    """Opens a new window to add equipment."""
    global add_window, name_entry, status_var, unit_entry, last_serviced_entry, next_maintenance_entry
    add_window = tk.Toplevel(root)
    add_window.title("Add Equipment")
    add_window.geometry("300x300")
    
    tk.Label(add_window, text="Name:").pack()
    name_entry = tk.Entry(add_window)
    name_entry.pack()
    
    status_var = tk.StringVar(value="Available")
    tk.Label(add_window, text="Status:").pack()
    status_menu = ttk.Combobox(add_window, textvariable=status_var, values=["Available", "In Use", "Under Maintenance"])
    status_menu.pack()
    
    tk.Label(add_window, text="Unit:").pack()
    unit_entry = tk.Entry(add_window)
    unit_entry.pack()
    
    tk.Label(add_window, text="Last Serviced:").pack()
    last_serviced_entry = DateEntry(add_window, date_pattern='dd/mm/yyyy')
    last_serviced_entry.pack()
    
    tk.Label(add_window, text="Next Maintenance:").pack()
    next_maintenance_entry = DateEntry(add_window, date_pattern='dd/mm/yyyy')
    next_maintenance_entry.pack()
    
    tk.Button(add_window, text="Add Equipment", command=add_equipment).pack(pady=5)

# Tkinter Window
root = tb.Window(themename="superhero")
root.title("Gym Equipment Report")
root.geometry("800x500")

# Search Bar
search_frame = tk.Frame(root)
search_frame.pack(pady=10)
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
search_btn = tk.Button(search_frame, text="Search", command=search_equipment)
search_btn.pack(side=tk.LEFT)

# Equipment Table
columns = ("ID", "Name", "Status", "Unit", "Last Serviced", "Next Maintenance")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=10, padx=10)

# Total Equipment Count
total_count_label = tk.Label(root, text="Total Equipment: 0", font=("Arial", 12, "bold"))
total_count_label.pack()

# Add Equipment Button
add_equipment_btn = tk.Button(root, text="Add Equipment", command=open_add_equipment_window)
add_equipment_btn.pack(pady=10)

# Delete Button
delete_btn = tk.Button(root, text="Delete Selected", command=delete_equipment)
delete_btn.pack()

# Edit Unit Function
def open_edit_unit_window():
    """Opens a window to edit the unit count of selected equipment."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select equipment to edit!")
        return

    item_values = tree.item(selected_item)['values']
    item_id = item_values[0]
    current_unit = item_values[3]

    def save_new_unit():
        new_unit = unit_entry.get()
        if not new_unit.isdigit() or int(new_unit) < 0:
            messagebox.showerror("Input Error", "Enter a valid unit number!")
            return
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE equipment SET unit = ? WHERE id = ?", (new_unit, item_id))
        conn.commit()
        conn.close()

        edit_window.destroy()
        refresh_table()

    # Create Edit Window
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Unit Count")
    edit_window.geometry("250x150")

    tk.Label(edit_window, text=f"Editing: {item_values[1]}").pack(pady=5)
    tk.Label(edit_window, text="New Unit Count:").pack()
    
    unit_entry = tk.Entry(edit_window)
    unit_entry.insert(0, current_unit)  # Pre-fill with current value
    unit_entry.pack()

    tk.Button(edit_window, text="Save", command=save_new_unit).pack(pady=10)

# Add "Edit Unit" Button
edit_unit_btn = tk.Button(root, text="Edit Unit", command=open_edit_unit_window)
edit_unit_btn.pack(pady=10)

refresh_table()
root.mainloop()