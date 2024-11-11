from abc import ABC, abstractmethod

class Terminator(ABC):
    def __init__(self):
        pass
    
    @abstractmethod
    def check_terminate(self, fitness:[float], generation:int)->bool:
        pass