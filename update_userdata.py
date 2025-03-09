# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # # cursor.execute("ALTER TABLE food_logs ADD COLUMN name TEXT")
# # # # cursor.execute("ALTER TABLE food_logs ADD COLUMN calories REAL")
# # # # cursor.execute("ALTER TABLE food_logs ADD COLUMN weight REAL")
# # # # cursor.execute("ALTER TABLE food_logs ADD COLUMN height REAL")
# # # # cursor.execute("ALTER TABLE food_logs ADD COLUMN age REAL")
# # # conn.commit()
# # # conn.close()
# # # print("Added 'weight' and 'height' and 'age'  columns to food_logs table!")

# # # # Update testing.py
# # # import sqlite3

# # # try:
# # #     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # #     cursor = conn.cursor()
# # #     cursor.execute("INSERT INTO food_logs (user_id, date, name, quantity, calories) VALUES (?, ?, ?, ?, ?)",
# # #                    (1, "2025-03-09", "Apple", 100, 95))
# # #     cursor.execute("INSERT INTO food_logs (user_id, date, name, quantity, calories) VALUES (?, ?, ?, ?, ?)",
# # #                    (1, "2025-03-08", "Chicken Breast", 200, 165))
# # #     conn.commit()
# # #     print("Sample data inserted into food_logs!")
# # #     conn.close()
# # # except sqlite3.OperationalError as e:
# # #     print(f"Database error: {e}")
# # # except Exception as e:
# # #     print(f"Unexpected error: {e}")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS users (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     username TEXT UNIQUE,
# # #     password TEXT
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Users table created!")


# # # add test user

# # # import sqlite3

# # # try:
# # #     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # #     cursor = conn.cursor()
# # #     cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("testuser", "password123"))
# # #     conn.commit()
# # #     print("Test user added!")
# # #     conn.close()
# # # except sqlite3.OperationalError as e:
# # #     print(f"Database error: {e}")
# # # except Exception as e:
# # #     print(f"Unexpected error: {e}")


# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute("PRAGMA table_info(users)")
# # # columns = cursor.fetchall()
# # # print("Columns in users table:", columns)
# # # conn.close()

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
# # # cursor.execute("ALTER TABLE users ADD COLUMN height REAL")
# # # cursor.execute("ALTER TABLE users ADD COLUMN weight_goal REAL")
# # # conn.commit()
# # # conn.close()
# # # print("Added profile columns to users table!")

# # # from database import update_profile

# # # update_profile(1, email="test@example.com", age=30, height=175.5, weight_goal=70.0)
# # # print("Profile updated!")


# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS workouts (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     user_id INTEGER,
# # #     date TEXT,
# # #     exercise TEXT,
# # #     sets INTEGER,
# # #     reps INTEGER
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Workouts table created!")

# # # from database import log_workout

# # # log_workout(1, "Push-ups", 3, 10)
# # # print("Workout logged!")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS foods (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     name TEXT UNIQUE,
# # #     calories REAL
# # # )''')
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS food_logs (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     user_id INTEGER,
# # #     date TEXT,
# # #     food_id INTEGER,
# # #     quantity REAL,
# # #     FOREIGN KEY (food_id) REFERENCES foods(id)
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Foods and food_logs tables created!")

# # # from database import add_food, log_food

# # # add_food("Apple", 95)
# # # log_food(1, 1, 100)  # Log 100g of Apple for user_id 1
# # # print("Food added and logged!")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute("PRAGMA table_info(weights)")
# # # print("Columns in weights table:", cursor.fetchall())
# # # conn.close()

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS weights (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     user_id INTEGER,
# # #     date TEXT,
# # #     weight REAL
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Weights table created!")

# # # from database import log_weight

# # # log_weight(1, 70.5)  # Log 70.5 kg for user_id 1
# # # print("Weight logged!")
# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_records (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     user_id INTEGER,
# # #     date TEXT,
# # #     bmi REAL
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("BMI records table created!")

# # # from database import log_bmi

# # # log_bmi(1, 70.5, 175.5)  # Log BMI for user_id 1 with 70.5 kg and 175.5 cm height
# # # print("BMI logged!")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS weights (
# # #     id INTEGER PRIMARY KEY AUTOINCREMENT,
# # #     user_id INTEGER,
# # #     date TEXT,
# # #     weight REAL
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Weights table created!")

# # # # 
# # # from database import log_weight

# # # log_weight(1, 70.5)  # Log 70.5 kg for user_id 1
# # # print("Weight logged!")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
# # #     user_id INTEGER PRIMARY KEY,
# # #     notifications INTEGER,
# # #     units TEXT,
# # #     FOREIGN KEY (user_id) REFERENCES users(id)
# # # )''')
# # # cursor.execute('''CREATE TABLE IF NOT EXISTS goals (
# # #     user_id INTEGER PRIMARY KEY,
# # #     weight_goal REAL,
# # #     calorie_goal INTEGER,
# # #     FOREIGN KEY (user_id) REFERENCES users(id)
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Settings and goals tables created!")
# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # # Add notifications column if not exists
# # # # cursor.execute("ALTER TABLE settings ADD COLUMN notifications INTEGER")
# # # # Add units column if not exists
# # # # cursor.execute("ALTER TABLE settings ADD COLUMN units TEXT")
# # # conn.commit()
# # # conn.close()
# # # print("Settings table updated with notifications and units columns!")

# # # from database import update_settings, update_goals

# # # update_settings(1, notifications=1, units="metric")
# # # update_goals(1, weight_goal=70.0, calorie_goal=2000)
# # # print("Settings and goals updated!")

# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute("DROP TABLE IF EXISTS settings")
# # # cursor.execute('''CREATE TABLE settings (
# # #     user_id INTEGER PRIMARY KEY,
# # #     notifications INTEGER,
# # #     units TEXT,
# # #     FOREIGN KEY (user_id) REFERENCES users(id)
# # # )''')
# # # conn.commit()
# # # conn.close()
# # # print("Settings table recreated with correct schema!")

# # # Save as check_password_hash.py
# # # import sqlite3

# # # conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
# # # cursor = conn.cursor()
# # # cursor.execute("SELECT username, password_hash FROM users LIMIT 1")
# # # row = cursor.fetchone()
# # # print(f"Username: {row[0]}, Password Hash: {row[1]}")
# # # conn.close()

# # import sqlite3

# def check_tables():
#     conn = sqlite3.connect('app.db')
#     cursor = conn.cursor()
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()
#     print("Tables in database:", tables)
#     conn.close()

# # # check_tables()

# # def initialize_database():
# #     conn = sqlite3.connect('app.db')  # Update with your database path
# #     cursor = conn.cursor()
    
# #     # Create users table
# #     cursor.execute('''
# #     CREATE TABLE IF NOT EXISTS users (
# #         id INTEGER PRIMARY KEY AUTOINCREMENT,
# #         username TEXT NOT NULL UNIQUE,
# #         password_hash TEXT NOT NULL
# #     );
# #     ''')
    
# #     conn.commit()
# #     conn.close()
# #     print("Database initialized and users table created.")

# # if __name__ == "__main__":
# #     initialize_database()



# # check_tables()

# import sqlite3

# def initialize_database():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()

#     # Create users table with activity_level column
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     username TEXT NOT NULL UNIQUE,
#     password_hash TEXT NOT NULL,
#     age INTEGER,
#     height REAL,
#     weight_goal REAL,
#     gender TEXT,
#     activity_level TEXT
# );
# ''')

#     # Create workouts table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS workouts (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     date TEXT,
#     exercise TEXT,
#     sets INTEGER,
#     reps INTEGER,
#     weight REAL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# ''')

#     # Create foods table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS foods (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE,
#     calories REAL
# );
# ''')

#     # Create food_logs table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS food_logs (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     date TEXT,
#     food_id INTEGER,
#     quantity REAL,
#     FOREIGN KEY (food_id) REFERENCES foods(id)
# );
# ''')

#     # Create weights table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS weights (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     date TEXT,
#     weight REAL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# ''')

#     # Create settings table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS settings (
#     user_id INTEGER PRIMARY KEY,
#     notifications INTEGER,
#     units TEXT,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# ''')

#     # Create goals table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS goals (
#     user_id INTEGER PRIMARY KEY,
#     weight_goal REAL,
#     calorie_goal INTEGER,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# ''')

#     # Create bmi_records table
#     cursor.execute('''
# CREATE TABLE IF NOT EXISTS bmi_records (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     user_id INTEGER,
#     date TEXT,
#     bmi REAL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# );
# ''')

#     conn.commit()
#     conn.close()
#     print("Database initialized and all necessary tables created.")

# if __name__ == "__main__":
#     initialize_database()



# check_tables()

# def add_columns_to_users():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()
    
#     # Add height column if it doesn't exist
#     try:
#         cursor.execute("ALTER TABLE users ADD COLUMN height REAL")
#     except sqlite3.OperationalError:
#         print("Column 'height' already exists or another error occurred.")
    
#     # Add age column if it doesn't exist
#     try:
#         cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
#     except sqlite3.OperationalError:
#         print("Column 'age' already exists or another error occurred.")
    
#     # Add weight_goal column if it doesn't exist
#     try:
#         cursor.execute("ALTER TABLE users ADD COLUMN weight_goal REAL")
#     except sqlite3.OperationalError:
#         print("Column 'weight_goal' already exists or another error occurred.")

#     conn.commit()
#     conn.close()
#     print("Columns added to users table if they did not exist.")

# if __name__ == "__main__":
#     add_columns_to_users()

# def add_gender_column():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("ALTER TABLE users ADD COLUMN gender TEXT")
#     except sqlite3.OperationalError:
#         print("Column 'gender' already exists or another error occurred.")
    
#     conn.commit()
#     conn.close()
#     print("Gender column added to users table if it did not exist.")

# if __name__ == "__main__":
#     add_gender_column()

# def add_activity_level_column():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("ALTER TABLE users ADD COLUMN activity_level TEXT")
#     except sqlite3.OperationalError:
#         print("Column 'activity_level' already exists or another error occurred.")
    
#     conn.commit()
#     conn.close()
#     print("Activity level column added to users table if it did not exist.")

# if __name__ == "__main__":
#     add_activity_level_column()

# def add_weight_column():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("ALTER TABLE workouts ADD COLUMN weight REAL")
#     except sqlite3.OperationalError:
#         print("Column 'weight' already exists or another error occurred.")
    
#     conn.commit()
#     conn.close()
#     print("Weight column added to workouts table if it did not exist.")

# if __name__ == "__main__":
#     add_weight_column()

import sqlite3
# def add_name_column_to_food_logs():
#     conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
#     cursor = conn.cursor()
    
#     try:
#         cursor.execute("ALTER TABLE food_logs ADD COLUMN name TEXT")
#     except sqlite3.OperationalError:
#         print("Column 'name' already exists or another error occurred.")
    
#     conn.commit()
#     conn.close()
#     print("Name column added to food_logs table if it did not exist.")

# if __name__ == "__main__":
#     add_name_column_to_food_logs()

def add_calories_column_to_food_logs():
    conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("ALTER TABLE food_logs ADD COLUMN calories REAL")
    except sqlite3.OperationalError:
        print("Column 'calories' already exists or another error occurred.")
    
    conn.commit()
    conn.close()
    print("Calories column added to food_logs table if it did not exist.")

if __name__ == "__main__":
    add_calories_column_to_food_logs()