import sqlite3

def get_db_connection():
    """Returns a connection to the gym_users database."""
    return sqlite3.connect("gym.db")

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
        CREATE TABLE IF NOT EXISTS equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT CHECK(status IN ('Available', 'In Use', 'Under Maintenance')) NOT NULL,
            last_serviced DATE,
            next_maintenance DATE
        )
    ''')

    # Check if the 'unit' column exists, if not, add it
    cursor.execute("PRAGMA table_info(equipment)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'unit' not in columns:
        cursor.execute("ALTER TABLE equipment ADD COLUMN unit TEXT NOT NULL DEFAULT 'Piece'")


    # Insert default admin user if the table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
        conn.commit()
    
    conn.commit()
    conn.close()

# Call the function to ensure database is initialized
initialize_database()
