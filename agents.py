import os
from dotenv import load_dotenv
from pathlib import Path
import streamlit as st

# Load environment variables
load_dotenv()

# Flag to use CrewAI or fallback implementation
USE_CREWAI = False

# Get API key from multiple sources
def get_api_key():
    # Try to get from Streamlit secrets
    if 'api_keys' in st.secrets:
        return st.secrets['api_keys']['google']
    
    # Try to get from config.py
    try:
        from config import GOOGLE_API_KEY
        return GOOGLE_API_KEY
    except ImportError:
        pass
    
    # Try to get from environment variables
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        return api_key
    
    # Default to a placeholder (this will cause the LLM to fail gracefully)
    return "api-key-not-found"

# Try to import CrewAI
if USE_CREWAI:
    try:
        from crewai import Agent, LLM
        CREWAI_AVAILABLE = True
    except ImportError:
        CREWAI_AVAILABLE = False
else:
    CREWAI_AVAILABLE = False

def get_unified_llm():
    """Create and return the unified LLM instance."""
    if not CREWAI_AVAILABLE:
        return None
        
    try:
        api_key = get_api_key()
        return LLM(
            model="gemini/gemini-1.5-flash",
            api_key=api_key,
            temperature=0.1
        )
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        # Return a minimal placeholder that won't break the code
        return None

def get_health_assistant(user_id):
    """
    Create and return the Health Assistant agent or a fallback implementation.
    """
    from database import get_workouts, get_food_logs, get_weights, get_bmi_records, get_profile

    # Fetch user data from the database.
    workouts = get_workouts(user_id) or []
    food_logs = get_food_logs(user_id) or []
    weights = get_weights(user_id) or []
    bmi_records = get_bmi_records(user_id) or []
    profile = get_profile(user_id) or {}

    # Aggregate user data into a consistent textual summary.
    user_data_summary = []
    # Profile section:
    if profile:
        user_data_summary.append("=== User's Profile ===")
        user_data_summary.append(
            f"Username: {profile.get('username', 'N/A')} | Age: {profile.get('age', 'N/A')} | Height: {profile.get('height', 'N/A')} | Weight Goal: {profile.get('weight_goal', 'N/A')}"
        )
    # Workouts section:
    if workouts:
        user_data_summary.append("=== User's Workouts ===")
        for w in workouts:
            exercise = w.get('exercise', '').strip() or 'N/A'
            user_data_summary.append(
                f"Date: {w.get('date', 'N/A')} | Exercise: {exercise} | Sets: {w.get('sets', 'N/A')} | Reps: {w.get('reps', 'N/A')} | Weight: {w.get('weight', 'N/A')}"
            )
    # Food logs section:
    if food_logs:
        user_data_summary.append("=== User's Food Logs ===")
        for f in food_logs:
            food_name = f.get('name', 'Unknown Food').strip() or 'Unknown Food'
            user_data_summary.append(
                f"Date: {f.get('date', 'N/A')} | Food: {food_name} | Calories: {f.get('calories', 'Unknown Calories')} | Quantity: {f.get('quantity', 'Unknown Quantity')}"
            )
    # Weight logs section:
    if weights:
        user_data_summary.append("=== User's Weight Logs ===")
        for w in weights:
            user_data_summary.append(
                f"Date: {w.get('date', 'N/A')} | Weight: {w.get('weight', 'N/A')}"
            )
    # BMI records section:
    if bmi_records:
        user_data_summary.append("=== User's BMI Records ===")
        for b in bmi_records:
            user_data_summary.append(
                f"Date: {b.get('date', 'N/A')} | BMI: {b.get('bmi', 'N/A')}"
            )
    user_data_text = "\n".join(user_data_summary) if user_data_summary else "No user data logged yet."

    # Write the aggregated user data to the knowledge base file.
    current_dir = Path(__file__).parent
    faq_file_path = current_dir / "knowledge_base" / "fitness_faq.txt"
    try:
        with open(faq_file_path, "w", encoding="utf-8") as faq_file:
            faq_file.write(user_data_text)
        print(f"User data written to {faq_file_path}")
    except Exception as e:
        print(f"Error writing to {faq_file_path}: {e}")

    # Return fallback implementation
    return FallbackHealthAssistant(user_data_text)

def get_reminders_agent(user_id):
    """Create and return the Reminders Agent with tools or fallback."""
    return FallbackRemindersAgent()

# Fallback implementation classes
class FallbackHealthAssistant:
    def __init__(self, user_data):
        self.user_data = user_data
        self.role = "Health Assistant"
        
    def execute_task(self, task):
        query = task.description if hasattr(task, 'description') else str(task)
        return f"""I'm a simple health assistant. AI-powered features are currently unavailable.

Your data summary:
{self.user_data}

For your query: "{query}", I recommend consulting with a health professional or referring to verified health resources.
"""

class FallbackRemindersAgent:
    def __init__(self):
        self.role = "Reminders Agent"
        
    def execute_task(self, task):
        return "I'm a simple reminders agent. AI-powered features are currently unavailable."
