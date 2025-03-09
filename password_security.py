import sqlite3
from bcrypt import hashpw, gensalt

def hash_password(password):
    return hashpw(password.encode(), gensalt()).decode()




conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
cursor = conn.cursor()
cursor.execute("SELECT id, username, password_hash FROM users")
users = cursor.fetchall()
for user in users:
    user_id, username, password_hash = user
    try:
        # Test if the hash is valid by attempting to hash a dummy password with it
        hashpw(b"test", password_hash.encode())  # This will raise ValueError if invalid
        print(f"User {username} has valid hash: {password_hash}")
    except ValueError:
        new_hash = hashpw(b"password123", gensalt()).decode()  # Default password
        cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        print(f"Rehashed password for {username} to {new_hash}")
conn.commit()
conn.close()

def add_user(username, password):
    conn = sqlite3.connect(r'D:\GenerativeAI_Projects\Health APP\fitness_app\app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        print(f"Username '{username}' already exists!")
        conn.close()
        return False
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print(f"User '{username}' added with hashed password!")
        conn.close()
        return True
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        conn.close()
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        conn.close()
        return False

if __name__ == "__main__":
    add_user("testuser2", "password123")  # Use a new username to avoid duplicate