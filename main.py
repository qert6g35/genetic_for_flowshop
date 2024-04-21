from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
from TestingEssentials import getMakData as get_data_from_file

# Przykładowe użycie
J, _  = GenerateJ(15,3,5)
max_generations = 100000

data_mega_pack = get_data_from_file(2)
for data_pack in data_mega_pack:
    print("Started next data pack")
    J = data_pack[0]
    # Parametry algorytmu genetycznego
    population_size = 10
    mutation_rate = 0.1
    generations = int(10 ** (len(J)/2)) #TODO uwaga to wypadało by dobrać najlepiej jakąś fajną funkcją 
    if generations > max_generations:
        generations = max_generations
    print(generations)

    # Uruchomienie algorytmu genetycznego
    ga = GeneticAlgorithm(J, population_size, mutation_rate, generations)
    best_solutions = ga.Genetic()

    best_solution = best_solutions[-1]
    best_solution_Cmax = C_Max(J,best_solution)
    best_solution = [elem + 1 for elem in best_solution]
    print("Best genetic: " + str(best_solution))
    print("Gen Cmax: " + str(best_solution_Cmax))
    print("Neh algoritm: " + str(data_pack[2]))
    print("Neh Cmax: " + str(data_pack[1]))
#plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 
