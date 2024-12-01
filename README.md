# AI-Powered Customer Support System

An intelligent customer support system that leverages AI to automate ticket handling and provide smart assistance. The system uses advanced natural language processing and machine learning techniques to process, classify, and respond to support tickets efficiently.

## System Architecture

The system is built with a modular agent-based architecture:

```
┌─────────────────┐
│  Web Interface  │
│   (Streamlit)   │
└────────┬────────┘
         │
┌────────┴────────┐
│   Main System   │
│  Orchestrator   │
└────────┬────────┘
         │
    ┌────┴────┐
    │  Agents │
    └────┬────┘
┌───────┴──────────────────┐
│ ┌─────────┐ ┌─────────┐ │
│ │ Intent  │ │ Ticket  │ │
│ │Extract. │ │Class.   │ │
│ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ │
│ │Language │ │Priority │ │
│ │Semantics│ │Analysis │ │
│ └─────────┘ └─────────┘ │
│ ┌─────────┐ ┌─────────┐ │
│ │Knowledge│ │Content  │ │
│ │Base     │ │Generate │ │
│ └─────────┘ └─────────┘ │
└────────────┬────────────┘
             │
    ┌────────┴────────┐
    │  Message Bus &  │
    │ Error Handling  │
    └────────┬────────┘
             │
    ┌────────┴────────┐
    │   Database &    │
    │    Storage      │
    └────────────────┘
```

## Key Features

- Intelligent ticket classification and prioritization
- Natural language intent extraction
- Automated response generation
- Knowledge base integration
- Real-time language sentiment analysis
- Screenshot capture functionality
- Message bus for inter-agent communication
- Robust error handling and retry mechanisms

## Tech Stack

- **Backend**: Python 3.11
- **Web Framework**: Streamlit
- **Database**: PostgreSQL
- **AI/ML**: 
  - Groq API Integration
  - Natural Language Processing
- **Error Handling**: Custom implementation with retry mechanisms
- **Message Bus**: In-memory event system
- **Monitoring**: Built-in logging and debugging

## Agent Ecosystem

### Base Agent
All agents inherit from the base Agent class which provides:
- Async processing capabilities
- Error handling and retries
- Message bus integration
- Response validation

```python
class Agent(ABC):
    def __init__(self):
        self.message_bus = MessageBus()
        self._retries = 3
        self._retry_delay = 1

    async def process_async(self, *args, **kwargs):
        return await self._execute_with_retry(self.process, *args, **kwargs)
```

### Available Agents
1. **IntentExtractionAgent**: Determines ticket intent and routing
2. **TicketClassificationAgent**: Categorizes and prioritizes tickets
3. **LanguageSemanticsAgent**: Analyzes text sentiment and urgency
4. **PriorityUnderstandingAgent**: Determines SLA and business impact
5. **KnowledgeBaseAgent**: Searches for relevant solutions
6. **ContentGenerationAgent**: Generates response templates

## Installation Instructions

1. Clone the repository
2. Install dependencies:
```bash
pip install streamlit psycopg2-binary requests pillow
```

3. Set up environment variables:
```bash
GROQ_API_KEY=your_api_key
DATABASE_URL=your_postgresql_url
```

4. Initialize the database:
```bash
python -c "from database.db import Database; Database()"
```

## Usage Guide

1. Start the application:
```bash
streamlit run main.py --server.port 5000
```

2. Access the web interface at `http://localhost:5000`
3. Submit a ticket through the form
4. View the processed results including:
   - Classification and priority
   - Intent analysis
   - Language sentiment
   - Automated response
   - Knowledge base matches

## Directory Structure

```
├── agents/
│   ├── base.py
│   ├── content_generation.py
│   ├── intent_extraction.py
│   ├── knowledge_base.py
│   ├── language_semantics.py
│   ├── priority_understanding.py
│   └── ticket_classification.py
├── database/
│   └── db.py
├── models/
│   └── ticket.py
├── services/
│   └── groq_service.py
├── utils/
│   └── text_processing.py
└── main.py
```

## API Documentation (Groq Integration)

The system integrates with Groq API for AI processing:

```python
class GroqService:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-70b-versatile"
    
    def get_completion(self, prompt: str, max_tokens: Optional[int] = 1000) -> str:
        # API call implementation
```

### Authentication
- Uses API key authentication
- Key should be set in GROQ_API_KEY environment variable

### Error Handling
The system implements multiple layers of error handling:

1. **Agent Level**:
   - Retry mechanism for failed operations
   - Response validation
   - Error propagation

2. **Service Level**:
   - API error handling
   - Network error recovery
   - Response format validation

3. **System Level**:
   - Database connection management
   - Input validation
   - Response sanitization

4. **Web Interface**:
   - User input validation
   - Error display
   - Graceful degradation

Example error handling implementation:
```python
async def _execute_with_retry(self, func, *args, **kwargs):
    for attempt in range(self._retries):
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                self.executor, func, *args, **kwargs
            )
            return AgentResponse(success=True, data=result)
        except Exception as e:
            if attempt == self._retries - 1:
                return AgentResponse(success=False, error=str(e))
            await asyncio.sleep(self._retry_delay)
```
