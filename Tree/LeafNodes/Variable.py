from Tree.LeafNodes.LeafNode import LeafNode


class Variable(LeafNode):

    def __str__(self):
        return self.value

    def evaluate(self, environment):
        return environment.get(self.value)
