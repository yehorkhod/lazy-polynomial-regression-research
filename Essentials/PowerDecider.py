import numpy as np
from InitializeCheck.alreadyInitialized import alreadyInitialized


class PowerDecider:

    __alpha: int = None
    __divisions: int = None
    __n_bins: int = None
    __power_decider_parameter: str = None
    __n_columns: int = None
    __columns_boundaries: np.ndarray = None
    __bins_boundaries: np.ndarray = None
    __indexes_hash: dict[int, np.ndarray] = None
    __powers: np.ndarray = None

    def __init__(self, alpha: int, divisions: int, power_decider_parameter: str) -> None:
        self.alpha = alpha
        self.divisions = divisions
        self.__n_bins = 2 ** divisions
        self.power_decider_parameter = power_decider_parameter

    def fit(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        data = np.concatenate([X, y.reshape(-1, 1)], axis=1)
        _, self.__n_columns = X.shape
        self.__powers = np.zeros([self.__n_columns]) + self.__alpha
        self.__columns_boundaries = np.array([np.min(X, axis=0), np.max(X, axis=0)]).T
        self.__binsBoundariesSetter()
        self.__indexesHashSetter()
        self.__powerTest(data)

        return self.__powers.astype(int)

    def __powerTest(self, data: np.ndarray) -> None:
        for column in range(self.__n_columns):
            column_bins = self.__binner(data, column)
            column_up_down = PowerDecider.upDownDecider(column_bins, column)
            column_power = self.__powerDecider(column_up_down)
            self.__powers[column] += column_power

    def __binner(self, data: np.ndarray, column: int) -> np.ndarray:
        column_bins = [data.copy()]
        columns = self.__indexes_hash.get(column)

        for i, column in enumerate(columns):
            temporary = np.zeros([self.__n_bins**(i + 1)], dtype=object)
            index = 0

            for j in range(self.__n_bins ** i):
                for bin_ in range(self.__n_bins):
                    bins = column_bins[j][(column_bins[j][::, column] >= self.__bins_boundaries[column][bin_][0]) &
                                          (column_bins[j][::, column] <= self.__bins_boundaries[column][bin_][1])]
                    temporary[index] = bins
                    index += 1

            column_bins = temporary.copy()

        return column_bins

    def __powerDecider(self, up_down: list) -> int:
        powers = []

        for i in range(0, len(up_down), self.__n_bins):
            up_down_chunk = up_down[i:i + self.__n_bins]
            power = PowerDecider.powerDecider(up_down_chunk)
            powers.append(power)

        column_power = self.__powerVoter(powers)

        return column_power

    def __powerVoter(self, powers: list) -> int:
        if self.__power_decider_parameter == 'mode':
            return (lambda x: max(set(x), key=powers.count))(powers)
        if self.__power_decider_parameter == 'median':
            return int(np.median(powers))
        if self.__power_decider_parameter == 'mean':
            return int(np.mean(powers))
        if self.__power_decider_parameter == 'maximum':
            return int(np.max(powers))

    @staticmethod
    def upDownDecider(column_bins: np.ndarray, column: int) -> list:
        up_down = []

        for i in range(len(column_bins)):
            value = PowerDecider.upDownVoter(column_bins[i], column)
            up_down.append(value)

        return up_down

    @staticmethod
    def upDownVoter(bin_: np.ndarray, column: int) -> int | None:
        try:
            max_index = bin_[::, -1].argmax()
            min_index = bin_[::, -1].argmin()
        except ValueError:
            return None  # if bin is empty

        if bin_[max_index, column] > bin_[min_index, column]:
            return 1
        elif bin_[max_index, column] < bin_[min_index, column]:
            return 0

        return None  # if there is only one element in a bin

    @staticmethod
    def powerDecider(up_down_chunk: list) -> int:
        result_list = []

        for item in up_down_chunk:
            if (len(result_list) == 0 or item != result_list[-1]) and item is not None:
                result_list.append(item)

        power = len(result_list)

        return power

    def __binsBoundariesSetter(self) -> None:
        self.__bins_boundaries = np.zeros([self.__n_columns, self.__n_bins + 1, 2])

        for column, [minimum, maximum] in enumerate(self.__columns_boundaries):
            for bin_ in range(self.__n_bins):
                left_limit = ((self.__n_bins - bin_) * minimum + bin_ * maximum) / self.__n_bins
                right_limit = ((self.__n_bins - bin_ - 1) * minimum + (bin_ + 1) * maximum) / self.__n_bins

                self.__bins_boundaries[column][bin_][0] = left_limit
                self.__bins_boundaries[column][bin_][1] = right_limit

    def __indexesHashSetter(self) -> None:
        columns = np.arange(0, self.__n_columns)
        columns_twice = np.concatenate([columns, columns])
        self.__indexes_hash = {i: columns_twice[1 + i:1 + self.__n_columns + i] for i in range(self.__n_columns)}

    @property
    def alpha(self):
        return self.__alpha

    @alpha.setter
    def alpha(self, alpha: int):
        alreadyInitialized(self.__alpha, 'alpha')

        if not (alpha % 1 == 0):
            raise Exception('Wrong "alpha" value, must be an integer.')

        self.__alpha = alpha

    @property
    def divisions(self):
        return self.__divisions

    @divisions.setter
    def divisions(self, divisions: int):
        alreadyInitialized(self.__divisions, 'divisions')

        if not (divisions >= 0 and divisions % 1 == 0):
            raise Exception('Wrong "divisions" value, must be a positive integer.')

        self.__divisions = divisions

    @property
    def n_bins(self):
        return self.__n_bins

    @property
    def power_decider_parameter(self):
        return self.__power_decider_parameter

    @power_decider_parameter.setter
    def power_decider_parameter(self, power_decider_parameter):
        alreadyInitialized(self.__power_decider_parameter, 'power_decider_parameter')

        possible_parameters = ['mode', 'median', 'mean', 'maximum']

        if not (power_decider_parameter in possible_parameters):
            raise Exception(f'Wrong "power_decider_parameter" value, must be in {possible_parameters}.')

        self.__power_decider_parameter = power_decider_parameter
