import sqlite3
from datetime import datetime
from bcrypt import hashpw, gensalt
from pydantic import BaseModel, Field
from typing import Optional, List
from sentence_transformers import SentenceTransformer, util
import os
from pathlib import Path

# Get the directory where the database.py file is located
current_dir = Path(__file__).parent
# Define the path to the database file
DB_PATH = current_dir / 'app.db'
# Define the path to the knowledge base file
KB_PATH = current_dir / 'knowledge_base' / 'fitness_faq.txt'

def update_settings(user_id, notifications=None, units=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO settings (user_id, notifications, units) VALUES (?, ?, ?)",
                        (user_id, notifications, units))
    else:
        updates = []
        values = []
        if notifications is not None:
            updates.append("notifications = ?")
            values.append(notifications)
        if units is not None:
            updates.append("units = ?")
            values.append(units)
        values.append(user_id)
        if updates:
            query = f"UPDATE settings SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return get_settings(user_id)

def get_settings(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT notifications, units FROM settings WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return {"notifications": row[0], "units": row[1]} if row else {"notifications": None, "units": None}

def update_goals(user_id, weight_goal=None, calorie_goal=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO goals (user_id, weight_goal, calorie_goal) VALUES (?, ?, ?)",
                        (user_id, weight_goal, calorie_goal))
    else:
        updates = []
        values = []
        if weight_goal is not None:
            updates.append("weight_goal = ?")
            values.append(weight_goal)
        if calorie_goal is not None:
            updates.append("calorie_goal = ?")
            values.append(calorie_goal)
        values.append(user_id)
        if updates:
            query = f"UPDATE goals SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, tuple(values))
    conn.commit()
    conn.close()
    return get_goals(user_id)

def get_goals(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT weight_goal, calorie_goal FROM goals WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    return {"weight_goal": row[0], "calorie_goal": row[1]} if row else {"weight_goal": None, "calorie_goal": None}

def log_weight(user_id, weight):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weights (user_id, date, weight) VALUES (?, ?, ?)",
                    (user_id, datetime.now().strftime('%Y-%m-%d'), weight))
    conn.commit()
    conn.close()
    return True

def add_food(name, calories):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO foods (name, calories) VALUES (?, ?)", (name, calories))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False
    except sqlite3.OperationalError as e:
        print(f"Database error: {e}")
        conn.close()
        return False

def get_foods():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM foods")
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def log_food(user_id, food_id, quantity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO food_logs (user_id, date, food_id, quantity) VALUES (?, ?, ?, ?)",
                    (user_id, datetime.now().strftime('%Y-%m-%d'), food_id, quantity))
    conn.commit()
    conn.close()
    return True

def get_profile(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, age, height, weight_goal FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        columns = ['id', 'username', 'email', 'age', 'height', 'weight_goal']
        return dict(zip(columns, user))
    return None

def update_profile(user_id, gender=None, age=None, height=None, weight_goal=None, activity_level=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    updates = []
    values = []
    if gender is not None:
        updates.append("gender = ?")
        values.append(gender)
    if activity_level is not None:
        updates.append("activity_level = ?")
        values.append(activity_level)
    if age is not None:
        updates.append("age = ?")
        values.append(age)
    if height is not None:
        updates.append("height = ?")
        values.append(height)
    if weight_goal is not None:
        updates.append("weight_goal = ?")
        values.append(weight_goal)
    values.append(user_id)
    if updates:
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, tuple(values))
        conn.commit()
        conn.close()
    return get_profile(user_id)

def get_user(username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    columns = [description[0] for description in cursor.description]
    conn.close()
    return dict(zip(columns, user)) if user else None

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        hashed_password = hashpw(password.encode(), gensalt()).decode()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        columns = [description[0] for description in cursor.description]
        conn.close()
        return dict(zip(columns, user)) if user else None
    except sqlite3.IntegrityError:
        conn.close()
        return None

def get_workouts(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM workouts WHERE user_id = ? ORDER BY date DESC", (user_id,))
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def log_workout(user_id, exercise, sets, reps, weight):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO workouts (user_id, date, exercise, sets, reps, weight) VALUES (?, ?, ?, ?, ?, ?)",
                    (user_id, datetime.now().strftime('%Y-%m-%d'), exercise, sets, reps, weight))
    conn.commit()
    conn.close()
    return True

def get_food_logs(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM food_logs WHERE user_id = ? ORDER BY date DESC", (user_id,))
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def get_weights(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weights WHERE user_id = ? ORDER BY date DESC", (user_id,))
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def log_bmi(user_id, weight, height):
    bmi = weight / ((height / 100) ** 2) if height > 0 else 0
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bmi_records (user_id, date, bmi) VALUES (?, ?, ?)",
                    (user_id, datetime.now().strftime('%Y-%m-%d'), bmi))
    conn.commit()
    conn.close()
    return True

def get_bmi_records(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bmi_records WHERE user_id = ? ORDER BY date DESC", (user_id,))
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

class KnowledgeBaseTool(BaseModel):
    name: str = "knowledge_base"
    description: str = "Retrieves information from the fitness and nutrition knowledge base."
    model: Optional[SentenceTransformer] = Field(default=None)

    class Config:
        arbitrary_types_allowed = True  # Allow arbitrary types

    def __init__(self, **kwargs):
        self.model = None  # Explicitly setting model to None here, though might be redundant
        super().__init__(**kwargs)
        self.kb_entries: List[str] = self.load_knowledge_base()
        self.kb_embeddings = None

    def load_knowledge_base(self):
        """Loads fitness and nutrition knowledge entries from a text file."""
        try:
            with open(KB_PATH, 'r', encoding='utf-8') as f:
                content = f.read().splitlines()
            return [line for line in content if line.strip()]
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return []

    def initialize_embeddings(self):
        """Initializes sentence embeddings for the knowledge base entries."""
        if self.kb_entries and self.model is not None: # Check if model is not None before using
            self.kb_embeddings = self.model.encode(self.kb_entries, convert_to_tensor=True)
        else:
            print("Knowledge base entries are empty or SentenceTransformer model is not initialized.")
            self.kb_embeddings = None

    def retrieve_knowledge(self, query: str, top_k: int = 3) -> List[str]:
        """
        Retrieves top_k most relevant knowledge entries for a given query.
        Returns: A list of strings representing knowledge entries.
        """
        if self.kb_embeddings is None or self.model is None: # Check both embeddings and model
            print("Knowledge base embeddings are not initialized. Please call initialize_embeddings().")
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        cos_scores = util.cos_sim(query_embedding, self.kb_embeddings)[0]
        top_results = sorted(range(len(cos_scores)), key=lambda i: cos_scores[i], reverse=True)[:top_k]
        return [self.kb_entries[i] for i in top_results]

    def run(self, query: str) -> str:
        """Tool execution method to retrieve knowledge based on a query."""
        knowledge = self.retrieve_knowledge(query)
        if knowledge:
            return " \n".join(knowledge) # Return knowledge entries separated by newline
        else:
            return "No relevant information found in the knowledge base."

    async def arun(self, query: str) -> str:
        """Async version of run, if needed for async environments."""
        return self.run(query)

if __name__ == '__main__':
    # Example usage of database functions (for testing purposes)
    # You can uncomment and run this section to test individual functions

    # Example: Create a user
    new_user = create_user("testuser4", "password123")
    if new_user:
        print("New user created:", new_user)
    else:
        print("Failed to create user (username might be taken).")

    # Example: Get user profile
    user_profile = get_profile(1) # Assuming user ID 1 exists
    if user_profile:
        print("User profile:", user_profile)
    else:
        print("User profile not found.")

    # Example: Add a food
    food_added = add_food("Apple", 52)
    if food_added:
        print("Food added successfully.")
    else:
        print("Failed to add food (name might be duplicate).")

#    Example: Get all foods
    foods = get_foods()
    print("All foods:", foods)

    # Example: Log a workout
    workout_logged = log_workout(1, "Running", 1, 30, 0) # User ID 1, Running for 30 mins
    if workout_logged:
        print("Workout logged.")

    # Example: KnowledgeBaseTool Test (Requires SentenceTransformer and knowledge_base.txt setup)
    tool = KnowledgeBaseTool()
    tool.model = SentenceTransformer('all-MiniLM-L6-v2') # Initialize the model
    tool.initialize_embeddings() # Initialize embeddings AFTER setting the model
    query = "best exercises for weight loss"
    knowledge_results = tool.run(query)
    print(f"Knowledge base results for query '{query}':\n{knowledge_results}")

    pass # No default action when the script is run directly, only example usages above