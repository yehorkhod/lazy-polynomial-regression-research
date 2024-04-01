import numpy as np
from InitializeCheck.alreadyInitialized import alreadyInitialized


class PolynomialColumnsAdder:

    __powers: np.ndarray = None

    def __init__(self, powers: np.ndarray) -> None:
        self.powers = powers

    def transform(self, X: np.ndarray) -> np.ndarray:
        n_rows, n_columns = X.shape
        self.__equalityCheck(n_columns)
        X_preprocessed = np.zeros([n_rows, self.__powers.sum()])
        columns_preprocessed = iter(range(self.__powers.sum()))

        for column in range(n_columns):
            for power in range(self.__powers[column]):
                X_preprocessed[::, next(columns_preprocessed)] = X[::, column] ** (power + 1)

        return X_preprocessed

    def __equalityCheck(self, n_columns) -> None:
        if not (n_columns == len(self.__powers)):
            raise Exception('Number of X\'s columns and number of powers in an array do not match.')

    @property
    def powers(self):
        return self.__powers

    @powers.setter
    def powers(self, powers: np.ndarray):
        alreadyInitialized(self.__powers, 'powers')

        if not isinstance(powers, np.ndarray):
            raise Exception('Wrong "powers" value, must be an array containing integers.')

        for power in powers:
            if not (power % 1 == 0):
                raise Exception('Wrong "powers" value, must be an array containing integers.')

        self.__powers = powers
