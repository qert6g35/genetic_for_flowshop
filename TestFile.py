from TestingEssentials import GenerateJ, EvaluateC, C_Max, C_MaxFromC, start_t
from DataVisualization import plot_schedule_fancy
from GeneticAlgorithm import GeneticAlgorithm
from TestingEssentials import getMakData as get_data_from_file
import pandas as pd
import matplotlib.pyplot as plt

data_pack_num = 0
data_mega_pack = get_data_from_file(100)
data_pack = data_mega_pack[1]
print(" ")
print("         Started data pack:" + str(data_pack_num))
J = data_pack[0]
# Parametry algorytmu genetycznego
population_sizes = [50, 100, 200, 300]
mutation_rates = [0.1, 0.2, 0.3, 0.4, 0.5]
generations = [500, 1000, 1500, 2000]


# population_sizes = [50]
# mutation_rates = [0.1]
# generations = [500]

results = []

for pop_size in population_sizes:
    for mut_rate in mutation_rates:
        for gen in generations:
            ga = GeneticAlgorithm(J, 
                        pop_size, 
                        mut_rate, 
                        gen,
                        mutation_type="mid", 
                        crossover_type="nearest", 
                        selection_type="roulette")
            best_solutions = ga.Genetic()

            best_solution = best_solutions[-1]
            best_solution_Cmax = C_Max(J,best_solution)
            results.append({'Population Size': pop_size, 'Mutation Rate': mut_rate, 'Generations': gen, 'Cmax': best_solution_Cmax})




best_solution_Cmax = C_Max(J,best_solution)
best_solution = [elem + 1 for elem in best_solution]


# Zapisz wyniki do dataframe
df = pd.DataFrame(results)

# Wyświetl wyniki
print(df)
#plot_schedule_fancy(best_solution, J, start_t(J, best_solution,(EvaluateC(J,best_solution)))) 

import seaborn as sns

# Ustawienie stylu wykresów
sns.set(style="whitegrid")

# Utwórz siatkę wykresów
fig, axes = plt.subplots(1, 3, figsize=(18, 10))

# Wykres zależności Cmax od parametru population_size
sns.scatterplot(ax=axes[0], x='Population Size', y='Cmax', data=df)
axes[0].set_title('Wpływ parametru population_size na Cmax')
axes[0].set_xlabel('Population Size')
axes[0].set_ylabel('Cmax')

# Wykres zależności Cmax od parametru mutation_rate
sns.scatterplot(ax=axes[1], x='Mutation Rate', y='Cmax', data=df)
axes[1].set_title('Wpływ parametru mutation_rate na Cmax')
axes[1].set_xlabel('Mutation Rate')
axes[1].set_ylabel('Cmax')

# Wykres zależności Cmax od parametru generations
sns.scatterplot(ax=axes[2], x='Generations', y='Cmax', data=df)
axes[2].set_title('Wpływ parametru generations na Cmax')
axes[2].set_xlabel('Generations')
axes[2].set_ylabel('Cmax')

# Wyświetl wykresy
plt.tight_layout()
plt.show()