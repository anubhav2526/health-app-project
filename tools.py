from crewai.tools import BaseTool
from typing import List
import os
from sentence_transformers import SentenceTransformer, util

class KnowledgeBaseTool(BaseTool):
    name: str = "knowledge_base"
    description: str = "Retrieves information from the fitness and nutrition knowledge base."

    def __init__(self):
        super().__init__()
        self.model = None
        self.kb_entries: List[str] = self.load_knowledge_base()
        self.kb_embeddings = None

    def load_knowledge_base(self) -> List[str]:
        entries = []
        knowledge_base_dir = "knowledge_base"
        if not os.path.exists(knowledge_base_dir):
            return ["No knowledge base found. Please add text files to the 'knowledge_base' directory."]
        
        for file in os.listdir(knowledge_base_dir):
            if file.endswith(".txt"):
                with open(os.path.join(knowledge_base_dir, file), "r", encoding="utf-8") as f:
                    entries.append(f.read().strip())
        return entries if entries else ["Default response: No specific information available."]

    def load_model(self):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            self.kb_embeddings = self.model.encode(self.kb_entries, convert_to_tensor=True)

    def _run(self, query: str) -> str:
        self.load_model()
        query_embedding = self.model.encode(query, convert_to_tensor=True)
        similarities = [util.pytorch_cos_sim(query_embedding, kb_emb).item() 
                       for kb_emb in self.kb_embeddings]
        max_index = similarities.index(max(similarities))
        return self.kb_entries[max_index]

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