import os
import numpy as np
import pandas as pd
from Tree import Tree
from Tree.TreeBuild.treeBuild import treeBuild
from InitializeCheck.alreadyInitialized import alreadyInitialized
from Data.generateCombinations import generateCombinations


class DataGenerator:

    __powers: list[int] = None
    __noise_amount: int = None
    __boundaries: tuple[int, int] = None
    __points_per_variable: int = None
    __tree: Tree = None
    __variables: list[str] = None
    __columns: list[str] = None

    def __init__(self, powers: list[int], noise_amount: int, boundaries: tuple[int, int], points_per_variable: int) -> None:
        self.powers = powers
        self.noise_amount = noise_amount
        self.boundaries = boundaries
        self.points_per_variable = points_per_variable
        self.__treeSetter()


    def generateData(self, path: str) -> None:
        data = self.__generateData()
        noised_data = self.__noiseData(data)
        self.__columnsSetter()

        if not os.path.exists(path):
            pd.DataFrame(noised_data, columns=self.__columns).to_csv(path, index=False)
            return None

        raise Exception('File already exists!')


    def __generateData(self) -> np.ndarray:
        self.__variables = [f'x{i}' for i in range(len(self.__powers))]
        domain_of_definition = np.linspace(self.__boundaries[0], self.__boundaries[1], self.__points_per_variable)
        combinations = generateCombinations(self.__variables, domain_of_definition)
        targets = []

        for points in combinations:
            environ = {f'x{i}': value for i, value in enumerate(points)}
            target = self.__tree.evaluate(environ)
            targets.append(target)

        targets = np.array(targets)
        data = np.hstack((combinations, targets.reshape(-1, 1)))

        return data

    def __noiseData(self, data: np.ndarray) -> np.ndarray:
        for _ in range(self.__noise_amount):
            shape = data.shape
            noise = np.random.normal(0, 1, shape)
            noised_data = data + noise
            data = np.concatenate([data, noised_data], axis=0)

        return data

    def __columnsSetter(self) -> None:
        self.__columns = self.__variables.copy().append('target')

    def __treeSetter(self) -> None:
        self.__tree = treeBuild(self.__powers)


    @property
    def powers(self):
        return self.__powers

    @powers.setter
    def powers(self, powers):
        alreadyInitialized(self.__powers, 'powers')

        if len(powers) == 0:
            raise Exception('Wrong "powers" value, powers must contain positive integers.')

        for power in powers:
            if not (power >= 1 and power % 1 == 0):
                raise Exception('Wrong "powers" value, powers must contain positive integers.')

        self.__powers = powers


    @property
    def noise_amount(self):
        return self.__noise_amount

    @noise_amount.setter
    def noise_amount(self, noise_amount: int):
        alreadyInitialized(self.__noise_amount, 'noise_amount')

        if not (noise_amount >= 0 and noise_amount % 1 == 0):
            raise Exception('Wrong "noise_amount" value, must be a not negative integer.')

        self.__noise_amount = noise_amount


    @property
    def boundaries(self):
        return self.__boundaries

    @boundaries.setter
    def boundaries(self, boundaries: tuple[int, int]):
        alreadyInitialized(self.__boundaries, 'boundaries')

        if not len(boundaries) == 2:
            raise Exception('Wrong "boundaries" value, must be a tuple of two integers, '
                            'where boundaries[1] > boundaries[0].')

        if not (boundaries[0] % 1 == 0 and
                boundaries[1] % 1 == 0 and
                boundaries[1] > boundaries[0]):
            raise Exception('Wrong "boundaries" value, must be a tuple of two integers, '
                            'where boundaries[1] > boundaries[0].')

        self.__boundaries = boundaries
        

    @property
    def points_per_variable(self):
        return self.__points_per_variable

    @points_per_variable.setter
    def points_per_variable(self, points_per_variable: int):
        alreadyInitialized(self.__points_per_variable, 'points_per_variable')

        if not (points_per_variable > 2 and points_per_variable % 1 == 0):
            raise Exception('Wrong "boundaries" value, must be a integer higher then 2.')

        self.__points_per_variable = points_per_variable


    @property
    def tree(self):
        return self.__tree
