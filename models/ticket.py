from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Ticket:
    title: str
    description: str
    category: Optional[str] = None
    priority: Optional[int] = None
    created_at: datetime = datetime.now()
    id: Optional[int] = None

@dataclass
class KnowledgeBaseEntry:
    title: str
    content: str
    category: str
    tags: list[str]
    id: Optional[int] = None
