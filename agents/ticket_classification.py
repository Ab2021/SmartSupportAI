from typing import Dict, Any
from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class TicketClassificationAgent(Agent):
    def __init__(self):
        super().__init__()
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
        self.default_category = "General Inquiry"
        self.default_priority = 2

    def validate_input(self, title: str, description: str) -> bool:
        if not isinstance(title, str) or not title.strip():
            return False
        if not isinstance(description, str) or not description.strip():
            return False
        return True

    def sanitize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        # Ensure category is valid
        if response['category'] not in self.categories:
            response['category'] = self.default_category
            
        # Ensure priority is valid
        if not isinstance(response['priority'], int) or response['priority'] not in self.priority_levels:
            response['priority'] = self.default_priority
            
        return response

    def process(self, title: str, description: str) -> Dict[str, Any]:
        # Validate input
        if not self.validate_input(title, description):
            raise ValueError("Invalid input parameters")

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
        
        if response.startswith("Error:"):
            raise Exception(f"API Error: {response}")
        
        try:
            category, priority = response.strip().split("|")
            priority = int(priority)
            
            result = {
                'category': category.strip(),
                'priority': priority,
                'confidence': 0.8,  # Added for tracking purposes
                'raw_response': response
            }
            
            # Sanitize and validate the response
            return self.sanitize_response(result)
            
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Error parsing API response: {str(e)}")

    def train(self, training_data) -> Dict[str, Any]:
        # Training implementation would go here
        return {"status": "success", "message": "Training not implemented yet"}
