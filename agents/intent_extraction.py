from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text
from concurrent.futures import ThreadPoolExecutor

class IntentExtractionAgent(Agent):
    def __init__(self):
        super().__init__()
        self.groq_service = GroqService()
        self.intent_types = [
            'technical_support',
            'account_management',
            'billing_inquiry',
            'feature_request',
            'bug_report',
            'general_inquiry',
            'product_guidance',
            'service_outage'
        ]

    def process(self, title: str, description: str):
        try:
            # Preprocess the input text
            preprocessed_text = preprocess_text(f"{title} {description}")
            
            prompt = f"""Analyze this support ticket and determine:
            1. Primary intent
            2. Secondary intents (if any)
            3. Required actions
            4. Routing suggestion
            
            Ticket:
            Title: {title}
            Description: {description}
            
            Available intent types: {', '.join(self.intent_types)}
            
            Respond in format:
            primary_intent|secondary_intents|required_actions|routing
            Where:
            - primary_intent is one of the available intent types
            - secondary_intents are comma-separated intents (if any)
            - required_actions are comma-separated actions needed
            - routing is the suggested department/team
            """
            
            response = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] IntentExtractionAgent raw API response: {response}")
            
            try:
                primary, secondary, actions, routing = response.strip().split("|")
                return {
                    'primary_intent': primary.strip(),
                    'secondary_intents': [i.strip() for i in secondary.split(",") if i.strip()],
                    'required_actions': [a.strip() for a in actions.split(",") if a.strip()],
                    'routing': routing.strip()
                }
            except (ValueError, AttributeError) as e:
                print(f"Error parsing API response: {str(e)}")
                return {
                    'primary_intent': 'general_inquiry',
                    'secondary_intents': [],
                    'required_actions': ['review_ticket'],
                    'routing': 'general_support'
                }
                
        except Exception as e:
            print(f"Unexpected error in intent extraction: {str(e)}")
            return {
                'primary_intent': 'general_inquiry',
                'secondary_intents': [],
                'required_actions': ['review_ticket'],
                'routing': 'general_support'
            }

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
