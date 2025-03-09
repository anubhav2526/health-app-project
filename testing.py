
import sqlite3

conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
cursor = conn.cursor()
cursor.execute("SELECT username, password_hash FROM users")
print("Users table data:", cursor.fetchall())
conn.close()