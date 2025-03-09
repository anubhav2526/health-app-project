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
    """Create and return the Health Assistant agent with tools."""
    from tools import KnowledgeBaseTool, WorkoutDataTool, NutritionDataTool
    unified_llm = get_unified_llm()
    workout_tool = WorkoutDataTool(user_id=user_id)
    nutrition_tool = NutritionDataTool(user_id=user_id)
    knowledge_tool = KnowledgeBaseTool()
    return Agent(
        role="Health Assistant",
        goal="Assist users with fitness and nutrition queries",
        backstory="You are an AI health assistant specialized in fitness and nutrition.",
        tools=[knowledge_tool, workout_tool, nutrition_tool],
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
        goal="Generate reminders and motivational messages",
        backstory="You are an AI that helps users stay on track with their fitness goals.",
        tools=[tool],
        verbose=True,
        llm=unified_llm
    )