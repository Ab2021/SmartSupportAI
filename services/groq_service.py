import os
import requests
from typing import Optional

class GroqService:
    def __init__(self):
        self.api_url = "https://api.groq.com/v1/completions"
        self.model = "mixtral-8x7b-32768"  # Using Mixtral model for better performance
    
    def get_completion(self, prompt: str, max_tokens: Optional[int] = 1000) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            return response.json()["choices"][0]["text"].strip()
            
        except Exception as e:
            print(f"Error calling Groq API: {str(e)}")
            return "Error generating response"
