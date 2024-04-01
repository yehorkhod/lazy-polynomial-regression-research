import numpy as np


def generateCombinations(variables: list[str], domain_of_definition: np.ndarray) -> np.ndarray:
    if len(variables) == 0:
        return np.array([[]])

    remaining_variables = variables[1:]
    combinations = []

    for value in domain_of_definition:
        sub_combinations = generateCombinations(remaining_variables, domain_of_definition)
        new_combinations = np.concatenate((value * np.ones((sub_combinations.shape[0], 1)), sub_combinations), axis=1)
        combinations.append(new_combinations)

    return np.vstack(combinations)
