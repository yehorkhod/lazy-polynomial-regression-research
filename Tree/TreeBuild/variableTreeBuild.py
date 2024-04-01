from Tree.BranchNodes.Sum import Sum
from Tree.BranchNodes.Product import Product
from Tree.BranchNodes.Power import Power
from Tree.LeafNodes.Constant import Constant
from Tree.LeafNodes.Variable import Variable
from Tree.TreeBuild.randomNumber import randomNumber


def variableTreeBuild(power: int, name: str):
    if power == 1:
        return Product(Constant(randomNumber()),
                       Power(Variable(name),
                             Constant(power)))

    return Sum(Product(Constant(randomNumber()),
                       Power(Variable(name),
                             Constant(power))),
               variableTreeBuild(power - 1, name))
