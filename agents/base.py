from abc import ABC, abstractmethod

class Agent(ABC):
    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    @abstractmethod
    def train(self, *args, **kwargs):
        pass
