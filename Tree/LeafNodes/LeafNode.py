from abc import ABC, abstractmethod


class LeafNode(ABC):

    def __init__(self, value):
        self.value = value

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self, environment):
        pass
