import os
import requests
from typing import Optional

class GroqService:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "mixtral-8x7b-32768"
    
    def get_completion(self, prompt: str, max_tokens: Optional[int] = 1000) -> str:
        try:
            headers = {
                "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": max_tokens,
                "temperature": 0.7
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()
            
            return response.json()["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.RequestException as e:
            print(f"API Request Error: {str(e)}")
            return "Error: Unable to process request"
        except (KeyError, IndexError) as e:
            print(f"API Response Format Error: {str(e)}")
            return "Error: Invalid response format"
        except Exception as e:
            print(f"Unexpected Error: {str(e)}")
            return "Error: An unexpected error occurred"
