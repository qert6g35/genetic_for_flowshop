from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import random


# # Przykładowe użycie
J, parent1  = GenerateJ(10,3,5)

# print(J)
# # Parametry algorytmu genetycznego
# population_size = 50
# mutation_rate = 0.1
# generations = 20

# # Wielkość problemu (liczba elementów w permutacji)
# n = 10

# # Uruchomienie algorytmu genetycznego
# ga = GeneticAlgorithm(J, population_size, mutation_rate, generations)
# best_solutions = ga.Genetic()
# print(best_solutions)
# random.seed(1)

crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
while crossover_points[0]==crossover_points[1]:
    crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]

crossover_points.sort()
child = parent1[crossover_points[0]:crossover_points[1]] 
notchild = parent1[0:crossover_points[0]]+parent1[crossover_points[1]:len(parent1)]

while len(child) < crossover_points[1]:
    bestcmax = -1
    for i in range(0,len(notchild)):
        cmax = C_Max(J, [notchild[i]] + child)
        if cmax < bestcmax or bestcmax == -1:
            bestcmax = cmax
            j = i
    child.insert(0,notchild[j])
    notchild.pop(j)

while len(child) < len(parent1):
    bestcmax = -1
    for i in range(0,len(notchild)):
        cmax = C_Max(J, child + [notchild[i]])
        if cmax < bestcmax or bestcmax == -1:
            bestcmax = cmax
            j = i
    child.append(notchild[j])
    notchild.pop(j)
