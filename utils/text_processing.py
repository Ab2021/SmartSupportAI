import re
from typing import List

def preprocess_text(text: str) -> str:
    """
    Preprocess text for NLP tasks
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and extra whitespace
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

def extract_keywords(text: str) -> List[str]:
    """
    Extract important keywords from text
    """
    # Simple keyword extraction based on word frequency
    words = text.split()
    # Remove common stop words (simplified version)
    stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but'}
    keywords = [word for word in words if word not in stop_words]
    return keywords
