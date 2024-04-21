import random
parent1 = [g for g in range(0,16)]
parent2 = [g for g in range(0,16)]

print(parent1)
print(parent2)



# jakaś metoda krzyżowania
start_crossover_point = random.randint(0, int(len(parent1) /2))
end_crossover_point = start_crossover_point + int(len(parent1) /2)
if end_crossover_point > (len(parent1) -1):
    end_crossover_point = len(parent1) -1
child = parent1[start_crossover_point:end_crossover_point] 
child += [gene for gene in parent2 if gene not in child]

