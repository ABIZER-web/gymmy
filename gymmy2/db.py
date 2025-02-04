import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('gym_management.db')
cursor = conn.cursor()

# Enable foreign key constraint enforcement
cursor.execute('PRAGMA foreign_keys = ON;')

# Create the tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Members (
    member_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE,
    email TEXT UNIQUE NOT NULL,
    phone_number TEXT,
    address TEXT,
    membership_plan_id INTEGER,
    join_date DATE DEFAULT CURRENT_DATE,
    emergency_contact TEXT,
    FOREIGN KEY (membership_plan_id) REFERENCES MembershipPlans(plan_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Staff (
    staff_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT,
    email TEXT UNIQUE,
    phone_number TEXT,
    hire_date DATE DEFAULT CURRENT_DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Classes (
    class_id INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT NOT NULL,
    description TEXT,
    schedule TEXT NOT NULL,
    instructor_id INTEGER,
    capacity INTEGER,
    location TEXT,
    FOREIGN KEY (instructor_id) REFERENCES Staff(staff_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS MembershipPlans (
    plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL,
    duration INTEGER NOT NULL,
    price REAL NOT NULL,
    benefits TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Payments (
    payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date DATE DEFAULT CURRENT_DATE,
    payment_method TEXT,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (plan_id) REFERENCES MembershipPlans(plan_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    enrollment_date DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Attendance (
    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES Members(member_id),
    FOREIGN KEY (class_id) REFERENCES Classes(class_id)
)
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

conn = sqlite3.connect('gym_management.db')
cursor = conn.cursor()

# Insert a membership plan
cursor.execute('''
INSERT INTO MembershipPlans (plan_name, duration, price, benefits)
VALUES ('Standard Plan', 12, 299.99, 'Access to all equipment and classes')
''')

# Insert a member
cursor.execute('''
INSERT INTO Members (first_name, last_name, email, membership_plan_id)
VALUES ('John', 'Doe', 'john.doe@example.com', 1)
''')

# Commit and close
conn.commit()
conn.close()