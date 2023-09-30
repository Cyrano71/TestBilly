from abc import ABC, abstractmethod

class BaseData(ABC):
    @staticmethod
    @abstractmethod
    def read(self, path: str):
        pass
    
    @staticmethod
    @abstractmethod
    def convert(self, l: list):
        pass