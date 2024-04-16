from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm

# Przykładowe użycie
J, _  = GenerateJ(15,3,5)

print(J)
# Parametry algorytmu genetycznego
population_size = 10
mutation_rate = 0.1
generations = 20

# Wielkość problemu (liczba elementów w permutacji)
n = 10

# Uruchomienie algorytmu genetycznego
ga = GeneticAlgorithm(J, population_size, mutation_rate, generations)
best_solutions = ga.Genetic()

best_solution = best_solutions[-1]
print(best_solution)
plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 
