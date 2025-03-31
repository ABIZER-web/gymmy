import os
import sqlite3
import ttkbootstrap as tb
from tkinter import StringVar, messagebox
from ttkbootstrap.constants import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Line, String, Group, Rect
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.graphics.shapes import Circle

# Register a font
registerFont(TTFont("Times", "Times.ttf"))  # Ensure "Times.ttf" is available on your system

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
    customer_name = search_var.get().strip()
    if not customer_name:
        messagebox.showerror("Error", "Please enter a valid Member Name.")
        return
    generate_receipt(customer_name)

# GUI Setup
root = tb.Window(themename="superhero")
root.title("Gym Receipt Generator")
root.geometry("400x250")

tb.Label(root, text="Enter Member Name:", font=("Arial", 12)).pack(pady=10)
search_var = StringVar()
search_entry = tb.Entry(root, textvariable=search_var, font=("Arial", 12))
search_entry.pack(pady=5)

generate_btn = tb.Button(root, text="Generate Receipt", bootstyle=PRIMARY, command=generate_receipt_ui)
generate_btn.pack(pady=10)

root.mainloop()
