from agents.base import Agent
from services.groq_service import GroqService

class ContentGenerationAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()

    def process(self, ticket_title: str, ticket_description: str, knowledge_base_solution: str = None):
        prompt = f"""Generate a professional and helpful response for this support ticket:
        Title: {ticket_title}
        Description: {ticket_description}
        
        Additional Context: {knowledge_base_solution if knowledge_base_solution else 'No knowledge base solution available'}
        
        Requirements:
        1. Be professional and empathetic
        2. Address the specific issue
        3. Provide clear next steps
        4. Include relevant solution if available
        """
        
        response = self.groq_service.get_completion(prompt)
        return response

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
