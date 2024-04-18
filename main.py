from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
from TestingEssentials import getMakData as get_data_from_file

# Przykładowe użycie
J, _  = GenerateJ(15,3,5)

data_pack = get_data_from_file()
J = data_pack[0]
#print(str(data_pack))
# Parametry algorytmu genetycznego
population_size = 10
mutation_rate = 0.1
generations = 10

# Wielkość problemu (liczba elementów w permutacji)
n = 10

# Uruchomienie algorytmu genetycznego
ga = GeneticAlgorithm(data_pack[0], population_size, mutation_rate, generations)
best_solutions = ga.Genetic()

best_solution = best_solutions[-1]
print(best_solution)
print(C_Max(data_pack[0],best_solution))
plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 
