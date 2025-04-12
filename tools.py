from crewai.tools import BaseTool
from typing import List, Optional, Any
import os
from sentence_transformers import SentenceTransformer, util
from pydantic import PrivateAttr

class KnowledgeBaseTool(BaseTool):
    name: str = "knowledge_base"
    description: str = "Retrieves information from the aggregated user data in the fitness_faq.txt file."

    # Use PrivateAttr so these runtime attributes are not included in the schema.
    _kb_entries: List[str] = PrivateAttr(default_factory=list)
    _model: Optional[SentenceTransformer] = PrivateAttr(default=None)
    _kb_embeddings: Optional[Any] = PrivateAttr(default=None)

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        self._kb_entries = self.load_knowledge_base()
        self._model = None
        self._kb_embeddings = None

    def load_knowledge_base(self) -> List[str]:
        # Load aggregated user data from "knowledge_base/fitness_faq.txt"
        knowledge_base_path = os.path.join("knowledge_base", "fitness_faq.txt")
        try:
            with open(knowledge_base_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return [content] if content else []
        except FileNotFoundError:
            print(f"Knowledge base file not found at: {knowledge_base_path}")
            return []

    def initialize_embeddings(self):
        if self._kb_entries:
            if self._model is None:
                self._model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Initializing embeddings for", len(self._kb_entries), "entries.")
            self._kb_embeddings = self._model.encode(self._kb_entries, convert_to_tensor=True)
        else:
            print("No knowledge base entries found to embed.")
            self._kb_embeddings = None

    def _run(self, query: str) -> str:
        self.initialize_embeddings()
        query_embedding = self._model.encode(query, convert_to_tensor=True)
        similarities = [util.pytorch_cos_sim(query_embedding, kb_emb).item() 
                        for kb_emb in self._kb_embeddings]
        max_index = similarities.index(max(similarities))
        return self._kb_entries[max_index]


class ActivityCheckerTool(BaseTool):
    name: str = "activity_checker"
    description: str = "Checks user's recent activity for reminders."

    def _run(self, query: str) -> str:
        from database import get_workouts
        user_id = "placeholder_user_id"
        workouts = get_workouts(user_id)
        if not workouts:
            return "You haven't logged any workouts recently. Time to get moving!"
        return "Great job staying active recently!"


class WorkoutDataTool(BaseTool):
    name: str = "workout_data"
    description: str = "Fetches user's workout data from the database."

    def _run(self, query: str) -> str:
        from database import get_workouts
        user_id = "placeholder_user_id"
        workouts = get_workouts(user_id)
        return "\n".join([f"{w['date']}: {w['exercise']}" for w in workouts]) or "No workouts found."


class NutritionDataTool(BaseTool):
    name: str = "nutrition_data"
    description: str = "Fetches user's nutrition data from the database."

    def _run(self, query: str) -> str:
        from database import get_food_logs
        user_id = "placeholder_user_id"
        logs = get_food_logs(user_id)
        return "\n".join([f"{l['date']}: {l['name']} - {l['calories']} cal" for l in logs]) or "No food logs found."


class DatabaseQueryTool(BaseTool):
    name: str = "database_query"
    description: str = "Executes SQL queries on app.db to fetch user data."

    def _run(self, query: str) -> str:
        import sqlite3
        db_path = r"D:\GenerativeAI_Projects\Health APP\fitness_app\app.db"
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
            if rows:
                return "\n".join(str(row) for row in rows)
            else:
                return "No results found."
        except Exception as e:
            return f"Error executing query: {e}"
