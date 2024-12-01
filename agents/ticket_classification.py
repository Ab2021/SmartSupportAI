from typing import Tuple
from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class TicketClassificationAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()
        self.categories = [
            "Technical Issue",
            "Account Related",
            "Billing",
            "Feature Request",
            "General Inquiry"
        ]
        self.priority_levels = {
            1: "Low",
            2: "Medium",
            3: "High",
            4: "Critical"
        }

    def process(self, title: str, description: str) -> Tuple[str, int]:
        # Preprocess the input text
        preprocessed_text = preprocess_text(f"{title} {description}")
        
        # Use Groq to classify the ticket
        prompt = f"""Analyze this support ticket and provide:
        1. The most appropriate category from: {', '.join(self.categories)}
        2. Priority level (1-4) based on urgency and impact
        
        Ticket:
        Title: {title}
        Description: {description}
        
        Respond in format: category|priority_number
        """
        
        response = self.groq_service.get_completion(prompt)
        category, priority = response.strip().split("|")
        return category, int(priority)

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
