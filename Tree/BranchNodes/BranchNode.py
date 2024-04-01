from abc import ABC, abstractmethod


class BranchNode(ABC):
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def evaluate(self, environment):
        pass
