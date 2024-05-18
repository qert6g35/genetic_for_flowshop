import numpy as np
import random
import math
from TestingEssentials import C_Max, EvaluateC, C_MaxFromC, C_Append


'''Słowniczek

  population - lista permutacji
  candidate - osobnik, permutacja zadań
'''

class GeneticAlgorithm:
    def __init__(self, J, population_size, mutation_rate, generations,mutation_type = "soft",crossover_type = "simple", selection_type = "tournament", register_all = False):
        self.mutation_type = mutation_type
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.jobs = J
        self.permutation_size = len(J)
        self.population_size = min(population_size, np.math.factorial(self.permutation_size))
        self.crossover_type = crossover_type
        self.selection_type = selection_type
        self.solution_cache = {}
        self.register_all = register_all
        #print("Rozmiar populacji jest ustawiony na: ",self.population_size)

    def initializePopulation(self):
        """inicjalizuje populacje dla algorytmu genetycznego
        Returns:
            array: populacja niepowtarzających się osobników
        """
        population = []
        population_size = 0
        while population_size < self.population_size:
            candidate = list(np.random.permutation(self.permutation_size))
            if candidate not in population:
                population.append(candidate)
                population_size += 1
        return population

        # Definicja funkcji oceny (fitness)
    def evaluate(self, solution):
        """Ocena rozwiązania.

        Args:
            solution (list): Osobnik, czyli permutacja zadań.

        Returns:
            int: Wartość funkcji celu (makespan).
        """
        # Sprawdzenie, czy wynik już istnieje w pamięci
        if tuple(solution) in self.solution_cache:
            return self.solution_cache[tuple(solution)]

        # Obliczenie wartości funkcji celu (makespan)
        makespan = C_Max(self.jobs, solution)
        
        # Zapisanie wyniku do pamięci
        self.solution_cache[tuple(solution)] = makespan
        return makespan

    # Operatory genetyczne

    def crossover(self,parent1,parent2):
        types = ["simple", "section","sectionSP","greedy"]
        assert self.crossover_type in types, "Invalid crossover type, possible options are: " + str(types)
        if self.crossover_type == "simple":
            return self.crossover_simple(parent1,parent2)
        if self.crossover_type == "section":
            return self.crossover_by_section(parent1,parent2)
        if self.crossover_type == "sectionSP":
            return self.crossover_by_section_save_placment(parent1,parent2)
        if self.crossover_type == "greedy":
            return self.crossover_with_nn(parent1,parent2)

            
        
    # Krzyżowanie (crossover)
    def crossover_simple(self, parent1, parent2):
        """Krzyżowanie dwóch rodziców.

        Args:
            parent1 (list): Pierwszy rodzic.
            parent2 (list): Drugi rodzic.

        Returns:
            list: Potomek.
        """
        # jakaś metoda krzyżowania
        crossover_point = random.randint(1, len(parent1) - 1)
        child = parent1[:crossover_point] + [gene for gene in parent2 if gene not in parent1[:crossover_point]]
        return child
    
        # Krzyżowanie (crossover)
    def crossover_by_section(self, parent1, parent2):
        """krzyżowanie rodziców w którym rodzić1 daje ciąg swojej premutacji o długości 1/2 całego ciągu, a reszta jest uzupełniana gnamy z rodzica2. pkt startowy i końcowy ciągu jest wybierany losowo

        Args:
            parent1 (list): Pierwszy rodzic/ten którego ciąg wybierany jest mniej zniekształcany.
            parent2 (list): Drugi rodzic.

        Returns:
            list: Potomek.
        """
        start_crossover_point = random.randint(0, int(len(parent1) /2))
        end_crossover_point = start_crossover_point + int(len(parent1) /2)
        if end_crossover_point > (len(parent1) -1):
            end_crossover_point = len(parent1) -1
        child = parent1[start_crossover_point:end_crossover_point] 
        child += [gene for gene in parent2 if gene not in child]
        return child
    
        # Krzyżowanie (crossover)
    def crossover_by_section_save_placment(self, parent1, parent2):
        """krzyżowanie rodziców w którym rodzić1 daje ciąg swojej premutacji o długości 1/2 całego ciągu, a reszta jest uzupełniana gnamy z rodzica2. pkt startowy i końcowy ciągu jest wybierany losowo. ciąg z rodzica 1 ma zachwać swoje połorzenie

        Args:
            parent1 (list): Pierwszy rodzic/ten którego ciąg wybierany jest mniej zniekształcany.
            parent2 (list): Drugi rodzic.

        Returns:
            list: Potomek.
        """
        crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]

        while crossover_points[0]==crossover_points[1]:
            crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
            
        crossover_points.sort()
        child = parent1[crossover_points[0]:crossover_points[-1]] 
        not_in_child = []
        not_in_child += [gene for gene in parent2 if gene not in child]

        temp = []
        for _ in range(0,crossover_points[0]):
            temp.append(not_in_child[0])
            not_in_child.pop(0)

        child = temp + child

        while len(not_in_child) > 0:
            child.append(not_in_child[0])
            not_in_child.pop(0)
        
        return child
    
    # Krzyżowanie (crossover)
    def crossover_with_nnbf(self, parent1, parent2):
        """krzyżowanie wybierające losowy ciąg z permutacji rodzica a reszte uzupełnia dobierając kolejno najlepsze z możliwych kombinacji element po elemencie

        Args:
            parent1 (list): Pierwszy rodzic/ten którego ciąg wybierany jest mniej zniekształcany.
            parent2 (list): Drugi rodzic - nie ma wkładu w wartości dziecka

        Returns:
            list: Potomek.
        """
        
        crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
        
        while crossover_points[0]==crossover_points[1]:
            crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
            
        crossover_points.sort()
        child = parent1[crossover_points[0]:crossover_points[1]] 
        notchild = parent1[0:crossover_points[0]]+parent1[crossover_points[1]:len(parent1)]
        
        while len(child) < crossover_points[1]:
            bestcmax = -1
            for i in range(0,len(notchild)):
                cmax = self.evaluate([notchild[i]] + child)
                if cmax < bestcmax or bestcmax == -1:
                    bestcmax = cmax
                    j = i
            child.insert(0,notchild[j])
            notchild.pop(j)

        while len(child) < len(parent1):
            bestcmax = -1
            for i in range(0,len(notchild)):
                cmax = self.evaluate(child + [notchild[i]])
                if cmax < bestcmax or bestcmax == -1:
                    bestcmax = cmax
                    j = i
            child.append(notchild[j])
            notchild.pop(j)
            
        return child
    
        # Krzyżowanie (crossover)
    def crossover_with_nn(self, parent1, parent2):
        """krzyżowanie wybierające losowy ciąg z permutacji rodzica a reszte uzupełnia na zasadzie greedy

        Args:
            parent1 (list): Pierwszy rodzic/ten którego ciąg wybierany jest mniej zniekształcany.
            parent2 (list): Drugi rodzic - nie ma wkładu w wartości dziecka

        Returns:
            list: Potomek.
        """
        
        crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
        
        while crossover_points[0]==crossover_points[1]:
            crossover_points = [random.randint(0, int(len(parent1)-1)), random.randint(0, int(len(parent1)-1))]
            
        crossover_points.sort()
        child = parent1[crossover_points[0]:crossover_points[1]] 
        notchild = parent1[0:crossover_points[0]]+parent1[crossover_points[1]:len(parent1)]
        notchild.sort(key=lambda x: self.jobs[x][0]) 
        child = notchild[0:crossover_points[0]]+child+notchild[crossover_points[0]:]
            
        return child
    
    
    # Mutacja
    def mutate(self, solution):
        """Mutacja osobnika. w  funkcji dobierana jest jedna z metod mutacji w zależności od stopnia rzadkości losowania

        Args:
            solution (list): Osobnik, czyli permutacja zadań.

        Returns:
            list: Zmutowany osobnik.
        """
        mutation_occurance_chance = random.random()
        types = ["hard", "mid","soft"]
        assert self.mutation_type in types, "Invalid mutation type, possible options are: " + str(types)
        #algorytm mutacji (HARD) zamiana ciągów miejscami
        if self.mutation_type == "hard" and mutation_occurance_chance < self.mutation_rate: #mutation_occurance_chance < (self.mutation_rate ** 2)
            newchild = solution[random.randint(1, int(len(solution) - 1)):]
            newchild += [gene for gene in solution if gene not in newchild]
            return newchild
        #algorytm mutacji (MID) zamiana losowych elementów
        if self.mutation_type == "mid" and mutation_occurance_chance < self.mutation_rate: #mutation_occurance_chance < self.mutation_rate
            idx1, idx2 = random.sample(range(len(solution)), 2)
            solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
            return solution
        #algorytm mutacji (SOFT) zamiana sąsiadów
        if self.mutation_type == "soft" and mutation_occurance_chance < self.mutation_rate: #mutation_occurance_chance < math.sqrt(self.mutation_rate)
            point = random.randint(1, int(len(solution) - 2))
            solution[point], solution[point+1] = solution[point+1], solution[point]
            return solution
        
        return solution
    
    def Selection(self,evaluated_population):
        types = ["roulette", "tournament"]
        assert self.selection_type in types, "Invalid selection type, possible options are: " + str(types)
        if self.selection_type == "tournament":
            return self.TournamentSelection(int(math.sqrt(self.population_size)),evaluated_population) #[solution for solution, _ in evaluated_population[:self.population_size // 2]]
        if self.selection_type == "roulette":
            return self.RouletteSelection(int(math.sqrt(self.population_size)),evaluated_population)



    def TournamentSelection(self,group_size,_evaluated_population:list):
        """Implementacja selekcji turniejowej   

        Args:
            group_size (Int): wielkość grupy turniejowej / ilosć osobników spadnie ! group_size KROTNIE !   
            _evaluated_population (lista tupli {permutacji,C_max_permutacji}): populacja z policzonymi czasami wykonywania

        Returns:
            survivors ([permutacje]):nowa populacja składająca się z osobników które przetrwały turnieje
        """
        survivors = []
        evaluated_population = _evaluated_population
        while len(evaluated_population)>0:
            tournament_grup = []
            if len(evaluated_population) > group_size :
                for _ in range(0,group_size):
                    individual = random.choice(evaluated_population)
                    evaluated_population.remove(individual)
                    tournament_grup.append(individual)
            else:
                tournament_grup = evaluated_population
                evaluated_population = []
            tournament_grup.sort(key=lambda x: x[1])
            survivors.append(tournament_grup[0][0])
        return survivors
        
    def RouletteSelection(self, num_survivors, evaluated_population):
        """Selekcja ruletkowa.

        Args:
            population (list): Lista osobników w populacji.
            fitness_values (list): Wartości dopasowania dla osobników.

        Returns:
            list: Osobnik wybrany za pomocą selekcji ruletkowej.
        """
        population, fitness_values = zip(*evaluated_population)
        total_fitness = sum(fitness_values)
        selection_probabilities = [fitness / total_fitness for fitness in fitness_values]


        # Wybór osobników, którzy przetrwają
        survivors = []
        for _ in range(num_survivors):
            roulette_value = random.uniform(0, 1)
            cumulative_probability = 0
            for i, probability in enumerate(selection_probabilities):
                cumulative_probability += probability
                if roulette_value <= cumulative_probability:
                    survivors.append(population[i])
                    break

        return survivors

    def Genetic(self):
        """Implementacja genetycznego algorytmu optymalizacji.

        Returns:
            list: Lista najlepszych rozwiązań w kolejnych generacjach.
        """
        best_solutions = []

        # Generowanie 1. pokolenia
        population = self.initializePopulation()

        for i in range(self.generations):
            # Ocena populacji
            evaluated_population = [(solution, self.evaluate(solution)) for solution in population]
            evaluated_population.sort(key=lambda x: x[1])

            # Wybór najlepszych osobników do reprodukcji (selekcja)
            # selected_parents = self.TournamentSelection(int(math.sqrt(self.population_size)),evaluated_population) #[solution for solution, _ in evaluated_population[:self.population_size // 2]]
            selected_parents = self.Selection(evaluated_population)
            # Krzyżowanie i mutacja
            children = []
            while len(children) < self.population_size:
                parent1 = random.choice(selected_parents)
                parent2 = random.choice(selected_parents)
                child = self.crossover(parent1, parent2)
                if random.random() < self.mutation_rate:
                    child = self.mutate(child)
                children.append(child)

            # Aktualizacja populacji
            population = children

            # Wybór najlepszego rozwiązania
            if len(best_solutions) > 0:
                best_solution, _ = evaluated_population[0]
                if(C_Max(self.jobs,best_solutions[-1]) > C_Max(self.jobs,best_solution) or self.register_all):
                    #print("We got _new_ best Cmax:" + str(C_Max(self.jobs,best_solution)))
                    best_solutions.append(best_solution)
                else:
                    best_solutions.append(best_solutions[-1])
            else:
                best_solution, _ = evaluated_population[0]
                #print("We got first best Cmax:" + str(C_Max(self.jobs,best_solution)))
                best_solutions.append(best_solution)

        return best_solutions