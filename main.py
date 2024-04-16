from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm

# Przykładowe użycie
J = [[1, 3, 2], [2, 2, 3], [3, 1, 1]]
ga = GeneticAlgorithm(J, population_size=30, mutation_rate=0.1, generations=10)
best_solution = ga.Genetic()
print("Najlepsze rozwiązanie:", best_solution)

plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 