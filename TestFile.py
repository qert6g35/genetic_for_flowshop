from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
from TestingEssentials import getMakData as get_data_from_file


data_pack_num = 0
data_mega_pack = get_data_from_file(10)
data_pack = data_mega_pack[1]
print(" ")
print("         Started data pack:" + str(data_pack_num))
J = data_pack[0]
# Parametry algorytmu genetycznego
population_size = 50
mutation_rate = 0.5
generations = 1000

# Uruchomienie algorytmu genetycznego
ga = GeneticAlgorithm(J, 
                        population_size, 
                        mutation_rate, 
                        generations,
                        mutation_type="mid", 
                        crossover_type="nearest", 
                        selection_type="roulette")

best_solutions = ga.Genetic()

best_solution = best_solutions[-1]
best_solution_Cmax = C_Max(J,best_solution)
best_solution = [elem + 1 for elem in best_solution]

print("Best genetic: " + str(best_solution))
print("Gen Cmax: " + str(best_solution_Cmax))
print("Neh algoritm: " + str(data_pack[2]))
print("Neh Cmax: " + str(data_pack[1]))

print([C_Max(J,best_solutions[i]) for i in range(len(best_solutions))])

#plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 
