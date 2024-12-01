from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime
import json
from dataclasses import dataclass, asdict
import asyncio
from concurrent.futures import ThreadPoolExecutor

@dataclass
class AgentResponse:
    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    timestamp: datetime = datetime.now()
    agent_name: Optional[str] = None
    execution_time: Optional[float] = None

    def to_dict(self):
        return asdict(self)

    def validate(self) -> bool:
        if not self.success and not self.error:
            return False
        if self.success and not self.data:
            return False
        return True

class MessageBus:
    _instance = None
    _messages = []
    _subscribers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MessageBus, cls).__new__(cls)
        return cls._instance

    def publish(self, topic: str, message: Dict):
        message['timestamp'] = datetime.now().isoformat()
        self._messages.append((topic, message))
        if topic in self._subscribers:
            for callback in self._subscribers[topic]:
                callback(message)

    def subscribe(self, topic: str, callback):
        if topic not in self._subscribers:
            self._subscribers[topic] = []
        self._subscribers[topic].append(callback)

    def get_messages(self, topic: Optional[str] = None) -> list:
        if topic:
            return [msg for t, msg in self._messages if t == topic]
        return self._messages

class Agent(ABC):
    def __init__(self):
        self.message_bus = MessageBus()
        self.executor = ThreadPoolExecutor(max_workers=3)
        self._retries = 3
        self._retry_delay = 1  # seconds

    async def _execute_with_retry(self, func, *args, **kwargs) -> AgentResponse:
        for attempt in range(self._retries):
            try:
                start_time = datetime.now()
                result = await asyncio.get_event_loop().run_in_executor(
                    self.executor, func, *args, **kwargs
                )
                execution_time = (datetime.now() - start_time).total_seconds()
                
                response = AgentResponse(
                    success=True,
                    data=result,
                    agent_name=self.__class__.__name__,
                    execution_time=execution_time
                )
                
                if not response.validate():
                    raise ValueError("Invalid response format")
                
                self.message_bus.publish(
                    f"{self.__class__.__name__}.success",
                    response.to_dict()
                )
                return response
                
            except Exception as e:
                if attempt == self._retries - 1:
                    error_response = AgentResponse(
                        success=False,
                        error=str(e),
                        agent_name=self.__class__.__name__
                    )
                    self.message_bus.publish(
                        f"{self.__class__.__name__}.error",
                        error_response.to_dict()
                    )
                    return error_response
                await asyncio.sleep(self._retry_delay)

    async def process_async(self, *args, **kwargs) -> AgentResponse:
        return await self._execute_with_retry(self.process, *args, **kwargs)

    @abstractmethod
    def process(self, *args, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def train(self, *args, **kwargs) -> Dict[str, Any]:
        pass

    def validate_input(self, *args, **kwargs) -> bool:
        """Override this method to implement input validation"""
        return True

    def sanitize_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Override this method to implement response sanitization"""
        return response
