import sqlite3
from pathlib import Path

# Get the directory where this file is located
current_dir = Path(__file__).parent
# Define the path to the database file
DB_PATH = current_dir / 'app.db'

def init_db():
    """Initialize the database with necessary tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        age INTEGER,
        height REAL,
        weight_goal REAL,
        gender TEXT,
        activity_level TEXT
    )
    ''')
    
    # Create settings table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        notifications BOOLEAN,
        units TEXT,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create goals table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        weight_goal REAL,
        calorie_goal INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create weights table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        weight REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create foods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        calories INTEGER NOT NULL
    )
    ''')
    
    # Create food_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        food_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (food_id) REFERENCES foods (id)
    )
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
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Create bmi_records table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS bmi_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date TEXT,
        bmi REAL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Add some sample foods
    try:
        sample_foods = [
            ('Apple', 95),
            ('Banana', 105),
            ('Chicken Breast', 165),
            ('Brown Rice (1 cup)', 216),
            ('Egg', 78),
            ('Salmon (100g)', 206),
            ('Broccoli (1 cup)', 55),
            ('Sweet Potato', 112),
            ('Greek Yogurt (1 cup)', 130),
            ('Oatmeal (1 cup)', 166)
        ]
        cursor.executemany('INSERT OR IGNORE INTO foods (name, calories) VALUES (?, ?)', sample_foods)
    except sqlite3.IntegrityError:
        pass  # Ignore if foods already exist
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

if __name__ == "__main__":
    init_db() 