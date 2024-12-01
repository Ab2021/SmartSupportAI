from agents.base import Agent
from database.db import db
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class KnowledgeBaseAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()

    def process(self, ticket_title: str, ticket_description: str):
        # Get relevant knowledge base entries
        kb_entries = db.get_knowledge_base_entries()
        
        if not kb_entries:
            return None
        
        # Create embedding search prompt
        search_text = preprocess_text(f"{ticket_title} {ticket_description}")
        
        prompt = f"""Given this support ticket:
        Title: {ticket_title}
        Description: {ticket_description}
        
        Find the most relevant solution from these knowledge base entries:
        {[entry['content'] for entry in kb_entries]}
        
        Return only the most relevant solution.
        """
        
        relevant_solution = self.groq_service.get_completion(prompt)
        print(f"[DEBUG] KnowledgeBaseAgent raw API response: {relevant_solution}")
        return relevant_solution

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
