from Tree.LeafNodes.LeafNode import LeafNode


class Constant(LeafNode):

    def __str__(self):
        return f'({self.value})'

    def evaluate(self, environment):
        return self.value
