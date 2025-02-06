import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('gym_users.db')

# Create a cursor object
cursor = conn.cursor()

# SQL command to create the table
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

# Commit changes and close the connection
conn.commit()
conn.close()

print("Table created successfully!")
