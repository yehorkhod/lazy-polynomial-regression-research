from Tree.BranchNodes.Sum import Sum
from Tree.TreeBuild.variableTreeBuild import variableTreeBuild


def baseTreeBuild(powers: list[int], i: int = 0):
    if i == len(powers) - 1:
        return variableTreeBuild(powers[i], f'x{i}')

    return Sum(variableTreeBuild(powers[i], f'x{i}'),
               baseTreeBuild(powers, i + 1))
