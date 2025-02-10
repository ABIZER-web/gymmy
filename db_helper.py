import sqlite3

def get_db_connection():
    """Returns a connection to the gym_users database."""
    return sqlite3.connect("gym_users.db")

def initialize_database():
    """Creates necessary tables if they don't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gym_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            address TEXT,
            phone_number TEXT NOT NULL UNIQUE,
            membership_plan TEXT NOT NULL,
            amount REAL,
            amount_due REAL,
            registration_date DATE,
            membership_expiry DATE
        )
    ''')

    # Insert default admin user if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        conn.commit()
    
    conn.commit()
    conn.close()

# Call the function to ensure database is initialized
initialize_database()
