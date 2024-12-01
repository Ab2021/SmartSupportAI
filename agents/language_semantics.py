from agents.base import Agent
from services.groq_service import GroqService
from utils.text_processing import preprocess_text

class LanguageSemanticsAgent(Agent):
    def __init__(self):
        self.groq_service = GroqService()
        self.sentiment_levels = ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
        self.urgency_levels = ['Low', 'Medium', 'High', 'Critical']

    def process(self, title: str, description: str):
        try:
            # Preprocess the input text
            preprocessed_text = preprocess_text(f"{title} {description}")
            
            prompt = f"""Analyze the language and semantics of this support ticket:
            Title: {title}
            Description: {description}
            
            Provide analysis in the following format:
            sentiment|urgency|key_phrases|technical_terms
            
            Where:
            - sentiment is one of: Very Negative, Negative, Neutral, Positive, Very Positive
            - urgency is one of: Low, Medium, High, Critical
            - key_phrases are the most important phrases (comma-separated)
            - technical_terms are any technical terms used (comma-separated)
            """
            
            response = self.groq_service.get_completion(prompt)
            print(f"[DEBUG] LanguageSemanticsAgent raw API response: {response}")
            
            try:
                sentiment, urgency, phrases, terms = response.strip().split("|")
                return {
                    'sentiment': sentiment.strip(),
                    'urgency': urgency.strip(),
                    'key_phrases': [p.strip() for p in phrases.split(",")],
                    'technical_terms': [t.strip() for t in terms.split(",")]
                }
            except (ValueError, AttributeError) as e:
                print(f"Error parsing API response: {str(e)}")
                return {
                    'sentiment': 'Neutral',
                    'urgency': 'Medium',
                    'key_phrases': [],
                    'technical_terms': []
                }
                
        except Exception as e:
            print(f"Unexpected error in language semantics analysis: {str(e)}")
            return {
                'sentiment': 'Neutral',
                'urgency': 'Medium',
                'key_phrases': [],
                'technical_terms': []
            }

    def train(self, training_data):
        # Training would be implemented here in a production system
        pass
