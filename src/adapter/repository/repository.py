from abc import ABC, abstractmethod


class Repository(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def save(self, entity):
        pass

    @abstractmethod
    def find_all(self):
        pass
