from agents.base import Agent
from database.db import db
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class KnowledgeBaseAgent(Agent):
    def __init__(self):
        super().__init__()
        self.groq_service = GroqService()

    def process(self, ticket_title: str, ticket_description: str):
        try:
            # Get relevant knowledge base entries
            print("[DEBUG] Fetching knowledge base entries...")
            kb_entries = db.get_knowledge_base_entries()
            
            if not kb_entries:
                print("[DEBUG] No knowledge base entries found")
                return None
            
            # Validate KB entries
            valid_entries = []
            for entry in kb_entries:
                if not isinstance(entry, dict) or 'content' not in entry:
                    print(f"[DEBUG] Invalid KB entry format: {entry}")
                    continue
                if not entry['content'] or not isinstance(entry['content'], str):
                    print(f"[DEBUG] Invalid KB entry content: {entry}")
                    continue
                valid_entries.append(entry)
            
            if not valid_entries:
                print("[DEBUG] No valid knowledge base entries found")
                return None
            
            # Create embedding search prompt
            search_text = preprocess_text(f"{ticket_title} {ticket_description}")
            print(f"[DEBUG] Preprocessed search text: {search_text}")
            
            prompt = f"""Given this support ticket:
            Title: {ticket_title}
            Description: {ticket_description}
            
            Find the most relevant solution from these knowledge base entries:
            {[entry['content'] for entry in valid_entries]}
            
            Return only the most relevant solution in a clear, formatted manner.
            If no relevant solution is found, respond with 'NO_RELEVANT_SOLUTION'.
            """
            
            relevant_solution = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] KnowledgeBaseAgent raw API response: {relevant_solution}")
            
            # Validate and format the response
            if relevant_solution.strip() == "NO_RELEVANT_SOLUTION":
                print("[DEBUG] No relevant solution found in knowledge base")
                return None
                
            return relevant_solution.strip()
            
        except Exception as e:
            print(f"[DEBUG] Error in KnowledgeBaseAgent processing: {str(e)}")
            return None

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
