from typing import Protocol, runtime_checkable


@runtime_checkable
class Tree(Protocol):

    def __init__(self, left_node, right_node):
        pass

    def __str__(self):
        pass

    def evaluate(self, environment):
        pass
