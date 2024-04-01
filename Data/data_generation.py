import os
from Data.DataGenerator import DataGenerator

# Files
directory: str = 'Data'

file_1: str = os.path.join(directory, 'dataset0.csv')
file_2: str = os.path.join(directory, 'dataset1.csv')

# Generating 2D data
powers: list[int] = [3]
noise_amount: int = 2
domain_of_definition: tuple[int, int] = (-10, 10)
points_per_variable: int = 2 * (abs(domain_of_definition[0]) + abs(domain_of_definition[1])) + 1

data_generator: DataGenerator = DataGenerator(powers, noise_amount, domain_of_definition, points_per_variable)
data_generator.generateData(file_1)

# Generating 3D data
powers: list[int] = [3, 2]
noise_amount: int = 1
domain_of_definition: tuple[int, int] = (-5, 5)
points_per_variable: int = 2 * (abs(domain_of_definition[0]) + abs(domain_of_definition[1])) + 1
data_generator: DataGenerator = DataGenerator(powers, noise_amount, domain_of_definition, points_per_variable)

data_generator.generateData(file_2)
