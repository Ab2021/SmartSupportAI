from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class PriorityUnderstandingAgent(Agent):
    def __init__(self):
        super().__init__()
        self.groq_service = GroqService()
        self.sla_requirements = {
            4: "1 hour",   # Critical
            3: "4 hours",  # High
            2: "24 hours", # Medium
            1: "48 hours"  # Low
        }

    def process(self, title: str, description: str, current_priority: int = None):
        try:
            # Preprocess the input text
            preprocessed_text = preprocess_text(f"{title} {description}")
            
            prompt = f"""Analyze this support ticket and determine:
            1. SLA requirement based on urgency and impact
            2. Business impact level
            3. User frustration level
            
            Ticket:
            Title: {title}
            Description: {description}
            Current Priority: {current_priority if current_priority else 'Not set'}
            
            Respond in format:
            priority_level|sla_requirement|business_impact|user_frustration
            Where:
            - priority_level is a number 1-4 (1=Low, 2=Medium, 3=High, 4=Critical)
            - sla_requirement is the time within which this should be resolved
            - business_impact is a brief description of the impact
            - user_frustration is a level (Low/Medium/High)
            """
            
            response = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] PriorityUnderstandingAgent raw API response: {response}")
            
            try:
                priority, sla, impact, frustration = response.strip().split("|")
                return {
                    'priority': int(priority),
                    'sla_requirement': sla.strip(),
                    'business_impact': impact.strip(),
                    'user_frustration': frustration.strip()
                }
            except (ValueError, AttributeError) as e:
                print(f"Error parsing API response: {str(e)}")
                return {
                    'priority': current_priority or 2,
                    'sla_requirement': self.sla_requirements[2],
                    'business_impact': "Unable to determine",
                    'user_frustration': "Medium"
                }
                
        except Exception as e:
            print(f"Unexpected error in priority understanding: {str(e)}")
            return {
                'priority': current_priority or 2,
                'sla_requirement': self.sla_requirements[2],
                'business_impact': "Unable to determine",
                'user_frustration': "Medium"
            }

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
