import sqlite3
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import os


# Database setup
conn = sqlite3.connect("gym.db")
cursor = conn.cursor()
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        gym_name TEXT NOT NULL,
        address Text NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )"""
)
conn.commit()


class AuthSystem(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(40, 20))
        self.pack(fill=BOTH, expand=YES)
        self.master = master
        self.style = ttk.Style()
        self.style.configure("TEntry", padding=(10, 5), font=("Arial", 12))

        # Load and display the image
        self.image_path = "gym_image.png"  # Change this to your image path
        self.image = self.load_image(self.image_path)
        
        self.create_login_form()

    def load_image(self, path):
        """Load and resize the image"""
        try:
            img = Image.open(path)
            img = img.resize((250, 250))  # Resize image
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print("Error loading image:", e)
            return None

    def create_login_form(self):
        """Create a Sign In Form with Image"""
        self.clear_window()
        
        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=50, fill=BOTH, expand=YES)

        # Left side: Image
        if self.image:
            img_label = ttk.Label(main_frame, image=self.image)
            img_label.pack(side=LEFT, padx=20)

        # Right side: Login form
        form_frame = ttk.Frame(main_frame, padding=30, bootstyle="dark")
        form_frame.pack(side=RIGHT, ipadx=10, ipady=10)

        ttk.Label(form_frame, text="Sign In", font=("Arial", 18, "bold")).pack(pady=10)

        self.email = ttk.StringVar()
        self.password = ttk.StringVar()

        self.create_form_entry(form_frame, "Email", self.email)
        self.create_form_entry(form_frame, "Password", self.password, show="*")

        btn_container = ttk.Frame(form_frame)
        btn_container.pack(fill=X, expand=YES, pady=10)

        ttk.Button(btn_container, text="Login", command=self.sign_in, bootstyle=SUCCESS).pack(
            side=LEFT, padx=5, fill=X, expand=YES
        )
        ttk.Button(btn_container, text="Sign Up", command=self.create_signup_form, bootstyle=PRIMARY).pack(
            side=RIGHT, padx=5, fill=X, expand=YES
        )

        self.error_label = ttk.Label(form_frame, text="", foreground="red", font=("Arial", 10, "italic"))
        self.error_label.pack(pady=5)

    def create_signup_form(self):
        """Create a Sign Up Form with Image"""
        self.clear_window()

        main_frame = ttk.Frame(self)
        main_frame.pack(pady=20, padx=50, fill=BOTH, expand=YES)

        # Left side: Image
        if self.image:
            img_label = ttk.Label(main_frame, image=self.image)
            img_label.pack(side=LEFT, padx=20)

        # Right side: Sign Up form
        form_frame = ttk.Frame(main_frame, padding=30, bootstyle="dark")
        form_frame.pack(side=RIGHT, ipadx=10, ipady=10)

        ttk.Label(form_frame, text="Sign Up", font=("Arial", 18, "bold")).pack(pady=10)

        self.gym_name = ttk.StringVar()
        self.address = ttk.StringVar()
        self.email = ttk.StringVar()
        self.password = ttk.StringVar()
        self.confirm_password = ttk.StringVar()

        self.create_form_entry(form_frame, "Gym Name", self.gym_name)
        self.create_form_entry(form_frame, "Address", self.address)
        self.create_form_entry(form_frame, "Email", self.email)
        self.create_form_entry(form_frame, "Password", self.password, show="*")
        self.create_form_entry(form_frame, "Confirm Password", self.confirm_password, show="*")

        btn_container = ttk.Frame(form_frame)
        btn_container.pack(fill=X, expand=YES, pady=10)

        ttk.Button(btn_container, text="Register", command=self.sign_up, bootstyle=SUCCESS).pack(
            side=LEFT, padx=5, fill=X, expand=YES
        )
        ttk.Button(btn_container, text="Back to Login", command=self.create_login_form, bootstyle=SECONDARY).pack(
            side=RIGHT, padx=5, fill=X, expand=YES
        )

        self.error_label = ttk.Label(form_frame, text="", foreground="red", font=("Arial", 10, "italic"))
        self.error_label.pack(pady=5)

    def create_form_entry(self, parent, label, variable, show=None):
        """Create styled input fields"""
        container = ttk.Frame(parent)
        container.pack(fill=X, expand=YES, pady=5)

        ttk.Label(container, text=label, width=15).pack(side=LEFT, padx=5)
        entry = ttk.Entry(container, textvariable=variable, show=show, bootstyle="info")
        entry.pack(side=LEFT, padx=5, fill=X, expand=YES)

    def sign_in(self):
        """Sign In Process with UI feedback"""
        email = self.email.get().strip()
        password = self.password.get().strip()

        cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()

        if user:
            self.open_dashboard()
        else:
            self.error_label.config(text="Invalid email or password! Try again.")

    def sign_up(self):
        """Sign Up Process with validation feedback"""
        gym_name = self.gym_name.get().strip()
        address = self.address.get().strip()
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm_password = self.confirm_password.get().strip()

        if not gym_name or not email or not password or not confirm_password:
            self.error_label.config(text="All fields are required!")
            return

        if password != confirm_password:
            self.error_label.config(text="Passwords do not match!")
            return

        try:
            cursor.execute("INSERT INTO users (gym_name,address, email, password) VALUES (?, ?, ?,?)", 
                           (gym_name, address, email, password))
            conn.commit()
            self.error_label.config(text="Sign Up Successful! Please Login.", foreground="green")
            self.create_login_form()
        except sqlite3.IntegrityError:
            self.error_label.config(text="Email already registered!")

    def open_dashboard(self):
        """Open Dashboard"""
        self.quit()  # Close login window
        os.system("python dashboard.py")  # Open dashboard.py

    def clear_window(self):
        """Clear all widgets"""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = ttk.Window("Gym Management System", "superhero", resizable=(False, False))
    AuthSystem(app)
    app.mainloop()
