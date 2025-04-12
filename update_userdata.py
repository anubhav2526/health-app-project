import sqlite3

DB_PATH = r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db'  # Update if needed

def initialize_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        age INTEGER,
        height REAL,
        weight_goal REAL,
        gender TEXT,
        activity_level TEXT
    );
    ''')

    # Create workouts table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS workouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        exercise TEXT,
        sets INTEGER,
        reps INTEGER,
        weight REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # Create foods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        calories REAL
    );
    ''')

    # Create food_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        food_id INTEGER,
        quantity REAL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (food_id) REFERENCES foods(id)
    );
    ''')

    # Create weights table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        weight REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # Create settings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        user_id INTEGER PRIMARY KEY,
        notifications INTEGER,
        units TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # Create goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        user_id INTEGER PRIMARY KEY,
        weight_goal REAL,
        calorie_goal INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    # Create bmi_records table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        bmi REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Database initialized and all necessary tables created.")

def check_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in database:", tables)
    conn.close()

if __name__ == "__main__":
    initialize_database()
    check_tables()
