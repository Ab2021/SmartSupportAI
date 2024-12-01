from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class SolutionRecommendationAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()

    def process(self, title: str, description: str, kb_solution: str = None, category: str = None):
        try:
            # Preprocess the input text
            preprocessed_text = preprocess_text(f"{title} {description}")
            
            prompt = f"""Given this support ticket and knowledge base solution, recommend the best approach to resolve the issue:
            
            Ticket:
            Title: {title}
            Description: {description}
            Category: {category if category else 'Unknown'}
            
            Known Solution: {kb_solution if kb_solution else 'No direct knowledge base match'}
            
            Provide recommendations in this format:
            primary_solution|alternative_approaches|estimated_resolution_time|confidence_level
            Where:
            - primary_solution is the main recommended solution
            - alternative_approaches are comma-separated alternative solutions
            - estimated_resolution_time is in minutes
            - confidence_level is a percentage (0-100)
            """
            
            response = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] SolutionRecommendationAgent raw API response: {response}")
            
            try:
                solution, alternatives, time_est, confidence = response.strip().split("|")
                return {
                    'primary_solution': solution.strip(),
                    'alternative_approaches': [a.strip() for a in alternatives.split(",") if a.strip()],
                    'estimated_resolution_time': int(time_est.strip()),
                    'confidence_level': int(confidence.strip().replace("%", ""))
                }
            except (ValueError, AttributeError) as e:
                print(f"Error parsing API response: {str(e)}")
                return {
                    'primary_solution': "Unable to determine best solution",
                    'alternative_approaches': [],
                    'estimated_resolution_time': 30,
                    'confidence_level': 0
                }
                
        except Exception as e:
            print(f"Unexpected error in solution recommendation: {str(e)}")
            return {
                'primary_solution': "Error generating solution recommendation",
                'alternative_approaches': [],
                'estimated_resolution_time': 30,
                'confidence_level': 0
            }

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
