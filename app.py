import tkinter as tk
from tkinter import ttk, messagebox
from db_helper import get_db_connection

class GymApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gym Management System")
        self.geometry("800x500")
        self.configure(bg="#1c1c1c")

        self.frames = {}

        for Page in (LoginPage, DashboardPage, RegisterPage, ViewMembersPage):
            page_name = Page.__name__
            frame = Page(parent=self, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        tk.Label(self, text="Login", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=20)
        
        tk.Label(self, text="Username", fg="white", bg="black").pack()
        self.entry_username = tk.Entry(self, width=30)
        self.entry_username.pack(pady=5)

        tk.Label(self, text="Password", fg="white", bg="black").pack()
        self.entry_password = tk.Entry(self, width=30, show="*")
        self.entry_password.pack(pady=5)

        ttk.Button(self, text="Login", command=self.login).pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.controller.show_frame("DashboardPage")
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1c1c1c")
        self.controller = controller

        tk.Label(self, text="🏋️ Dashboard", font=("Arial", 16, "bold"), fg="white", bg="#1c1c1c").pack(pady=20)
        ttk.Button(self, text="Register Member", command=lambda: controller.show_frame("RegisterPage")).pack(pady=10)
        ttk.Button(self, text="View Members", command=lambda: controller.show_frame("ViewMembersPage")).pack(pady=10)
        ttk.Button(self, text="Logout", command=lambda: controller.show_frame("LoginPage")).pack(pady=10)

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        tk.Label(self, text="Register Member", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=20)

        tk.Label(self, text="Name", fg="white", bg="black").pack()
        self.entry_name = tk.Entry(self, width=30)
        self.entry_name.pack(pady=5)

        tk.Label(self, text="Phone", fg="white", bg="black").pack()
        self.entry_phone = tk.Entry(self, width=30)
        self.entry_phone.pack(pady=5)

        ttk.Button(self, text="Save", command=self.save_member).pack(pady=10)
        ttk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage")).pack(pady=10)

    def save_member(self):
        name = self.entry_name.get()
        phone = self.entry_phone.get()

        if not name or not phone:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO gym_users (name, phone_number, membership_plan, registration_date) VALUES (?, ?, ?, ?)",
                       (name, phone, "Monthly", "2024-02-10"))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Member registered successfully!")
        self.entry_name.delete(0, tk.END)
        self.entry_phone.delete(0, tk.END)

class ViewMembersPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        tk.Label(self, text="View Members", font=("Arial", 16, "bold"), fg="white", bg="black").pack(pady=20)
        self.display_members()
        ttk.Button(self, text="Back to Dashboard", command=lambda: controller.show_frame("DashboardPage")).pack(pady=10)

    def display_members(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone_number FROM gym_users")
        members = cursor.fetchall()
        conn.close()

        if not members:
            tk.Label(self, text="No members found.", fg="white", bg="black").pack()
        else:
            for name, phone in members:
                tk.Label(self, text=f"{name} - {phone}", fg="white", bg="black").pack()

if __name__ == "__main__":
    app = GymApp()
    app.mainloop()
