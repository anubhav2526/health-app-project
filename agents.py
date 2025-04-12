from crewai import Agent, LLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_unified_llm():
    """Create and return the unified LLM instance."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    return LLM(
        model="gemini/gemini-1.5-flash",
        api_key=api_key,
        temperature=0.1
    )

def get_health_assistant(user_id):
    """
    Create and return the Health Assistant agent with tools.
    This version aggregates the user's logged data (workouts, food logs, weight logs, BMI records, and profile data)
    from app.db, writes a combined summary to 'knowledge_base/fitness_faq.txt' (overwriting previous content),
    and loads that file into the KnowledgeBaseTool. It also includes a DatabaseQueryTool for direct access to app.db.
    """
    from tools import KnowledgeBaseTool, WorkoutDataTool, NutritionDataTool, DatabaseQueryTool
    from database import get_workouts, get_food_logs, get_weights, get_bmi_records, get_profile

    # 1. Create the unified LLM.
    unified_llm = get_unified_llm()

    # 2. Create specialized tools.
    workout_tool = WorkoutDataTool(user_id=user_id)
    nutrition_tool = NutritionDataTool(user_id=user_id)
    # Direct DB query tool.
    db_query_tool = DatabaseQueryTool()
    knowledge_tool = KnowledgeBaseTool()  # This loads aggregated data from file.

    # 3. Fetch user data from the database.
    workouts = get_workouts(user_id) or []
    food_logs = get_food_logs(user_id) or []
    weights = get_weights(user_id) or []
    bmi_records = get_bmi_records(user_id) or []
    profile = get_profile(user_id) or {}

    # 4. Aggregate user data into a consistent textual summary.
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

    # 5. Write the aggregated user data to the knowledge base file.
    faq_file_path = os.path.join("knowledge_base", "fitness_faq.txt")
    try:
        with open(faq_file_path, "w", encoding="utf-8") as faq_file:
            faq_file.write(user_data_text)
        print(f"User data written to {faq_file_path}")
    except Exception as e:
        print(f"Error writing to {faq_file_path}: {e}")

    # 6. Reload the KnowledgeBaseTool to update its entries and embeddings.
    knowledge_tool._kb_entries = knowledge_tool.load_knowledge_base()
    knowledge_tool.initialize_embeddings()

    # 7. Create and return the Health Assistant agent with all tools.
    return Agent(
        role="Health Assistant",
        goal="Assist users with customized fitness and nutrition queries, and provide personalized answers based on your logged data.",
        backstory=(
            "You are an AI health assistant specialized in fitness and nutrition. All user data—including workouts, food logs, weight logs, "
            "BMI records, and profile information—is stored in app.db and aggregated in a file named 'fitness_faq.txt' within the 'knowledge_base' folder. "
            "You can also directly query the database if needed. Use this data to provide detailed, personalized answers."
        ),
        tools=[knowledge_tool, workout_tool, nutrition_tool, db_query_tool],
        verbose=True,
        llm=unified_llm
    )

def get_reminders_agent(user_id):
    """Create and return the Reminders Agent with tools."""
    from tools import ActivityCheckerTool
    unified_llm = get_unified_llm()
    tool = ActivityCheckerTool(user_id=user_id)
    return Agent(
        role="Reminders Agent",
        goal="Generate reminders, exercise suggestions, diet suggestions, and motivational quotes.",
        backstory="You are an AI that helps users stay on track with their fitness goals.",
        tools=[tool],
        verbose=True,
        llm=unified_llm
    )
