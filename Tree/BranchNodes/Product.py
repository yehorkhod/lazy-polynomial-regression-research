from Tree.BranchNodes.BranchNode import BranchNode


class Product(BranchNode):
    def __str__(self):
        return f'{self.left_node} * {self.right_node}'

    def evaluate(self, environment):
        return self.left_node.evaluate(environment) * self.right_node.evaluate(environment)
