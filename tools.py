from crewai.tools import BaseTool
from typing import List, Optional, Any
import os
from sentence_transformers import SentenceTransformer, util
from pydantic import PrivateAttr
from pathlib import Path

# Get the current directory
current_dir = Path(__file__).parent
kb_path = current_dir / "knowledge_base" / "fitness_faq.txt"
db_path = current_dir / "app.db"

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
        # Load aggregated user data from knowledge base file
        try:
            with open(kb_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                return [content] if content else []
        except FileNotFoundError:
            print(f"Knowledge base file not found at: {kb_path}")
            return []

    def initialize_embeddings(self):
        if self._kb_entries:
            if self._model is None:
                try:
                    self._model = SentenceTransformer("all-MiniLM-L6-v2")
                    print("Initialized SentenceTransformer model.")
                except Exception as e:
                    print(f"Error initializing SentenceTransformer: {e}")
                    return
            print("Initializing embeddings for", len(self._kb_entries), "entries.")
            try:
                self._kb_embeddings = self._model.encode(self._kb_entries, convert_to_tensor=True)
            except Exception as e:
                print(f"Error encoding embeddings: {e}")
                self._kb_embeddings = None
        else:
            print("No knowledge base entries found to embed.")
            self._kb_embeddings = None

    def _run(self, query: str) -> str:
        try:
            self.initialize_embeddings()
            if self._model is None or self._kb_embeddings is None:
                return "Knowledge base not properly initialized or empty."
                
            query_embedding = self._model.encode(query, convert_to_tensor=True)
            similarities = [util.pytorch_cos_sim(query_embedding, kb_emb).item() 
                            for kb_emb in self._kb_embeddings]
            max_index = similarities.index(max(similarities))
            return self._kb_entries[max_index]
        except Exception as e:
            return f"Error processing query: {e}"


class ActivityCheckerTool(BaseTool):
    name: str = "activity_checker"
    description: str = "Checks user's recent activity for reminders."
    user_id: str = None

    def __init__(self, user_id=None, **data):
        super().__init__(**data)
        self.user_id = user_id

    def _run(self, query: str) -> str:
        from database import get_workouts
        workouts = get_workouts(self.user_id)
        if not workouts:
            return "You haven't logged any workouts recently. Time to get moving!"
        return "Great job staying active recently!"


class WorkoutDataTool(BaseTool):
    name: str = "workout_data"
    description: str = "Fetches user's workout data from the database."
    user_id: str = None

    def __init__(self, user_id=None, **data):
        super().__init__(**data)
        self.user_id = user_id

    def _run(self, query: str) -> str:
        from database import get_workouts
        workouts = get_workouts(self.user_id)
        return "\n".join([f"{w['date']}: {w['exercise']}" for w in workouts]) or "No workouts found."


class NutritionDataTool(BaseTool):
    name: str = "nutrition_data"
    description: str = "Fetches user's nutrition data from the database."
    user_id: str = None

    def __init__(self, user_id=None, **data):
        super().__init__(**data)
        self.user_id = user_id

    def _run(self, query: str) -> str:
        from database import get_food_logs
        logs = get_food_logs(self.user_id)
        return "\n".join([f"{l['date']}: {l['food_id']} - Quantity: {l['quantity']}" for l in logs]) or "No food logs found."


class DatabaseQueryTool(BaseTool):
    name: str = "database_query"
    description: str = "Executes SQL queries on app.db to fetch user data."

    def _run(self, query: str) -> str:
        import sqlite3
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
