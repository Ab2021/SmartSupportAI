from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class AutomatedResolutionAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()
        self.automatable_categories = [
            "password_reset",
            "account_activation",
            "system_status",
            "basic_troubleshooting",
            "documentation_request"
        ]

    def process(self, title: str, description: str, category: str, priority: int):
        try:
            # Preprocess the input text
            preprocessed_text = preprocess_text(f"{title} {description}")
            
            prompt = f"""Analyze this support ticket and determine if it can be automated:
            
            Ticket:
            Title: {title}
            Description: {description}
            Category: {category}
            Priority: {priority}
            
            Determine:
            1. Can this be automated?
            2. What automated steps can be taken?
            3. Success probability
            4. Required API actions
            
            Respond in format:
            can_automate|automation_steps|success_probability|required_apis
            Where:
            - can_automate is 'yes' or 'no'
            - automation_steps are comma-separated steps
            - success_probability is a percentage (0-100)
            - required_apis are comma-separated API endpoints needed
            """
            
            response = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] AutomatedResolutionAgent raw API response: {response}")
            
            try:
                automate, steps, probability, apis = response.strip().split("|")
                return {
                    'can_automate': automate.strip().lower() == 'yes',
                    'automation_steps': [step.strip() for step in steps.split(",") if step.strip()],
                    'success_probability': int(probability.strip().replace("%", "")),
                    'required_apis': [api.strip() for api in apis.split(",") if api.strip()]
                }
            except (ValueError, AttributeError) as e:
                print(f"Error parsing API response: {str(e)}")
                return {
                    'can_automate': False,
                    'automation_steps': [],
                    'success_probability': 0,
                    'required_apis': []
                }
                
        except Exception as e:
            print(f"Unexpected error in automated resolution: {str(e)}")
            return {
                'can_automate': False,
                'automation_steps': [],
                'success_probability': 0,
                'required_apis': []
            }

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
