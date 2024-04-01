from Tree.LeafNodes.Constant import Constant
from Tree.BranchNodes.Sum import Sum
from Tree.TreeBuild.randomNumber import randomNumber
from Tree.TreeBuild.baseTreeBuild import baseTreeBuild


def treeBuild(powers: list[int]):
    return Sum(Constant(randomNumber()),
               baseTreeBuild(powers))
