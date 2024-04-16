from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt


# Przykładowe użycie
J, _  = GenerateJ(10,3,5)

print(J)
# Parametry algorytmu genetycznego
population_size = 50
mutation_rate = 0.1
generations = 20

# Wielkość problemu (liczba elementów w permutacji)
n = 10

# Uruchomienie algorytmu genetycznego
ga = GeneticAlgorithm(J, population_size, mutation_rate, generations)
best_solutions = ga.Genetic()
print(best_solutions)
