import numpy as np
import random
import math
from TestingEssentials import C_Max


'''Słowniczek

  population - lista permutacji
  candidate - osobnik, permutacja zadań
'''

class GeneticAlgorithm:
    def __init__(self, J, population_size, mutation_rate, generations):
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.jobs = J
        self.permutation_size = len(J)
        self.population_size = min(population_size, np.math.factorial(self.permutation_size))
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
        # Cmax
        makespan = C_Max(self.jobs, solution)
        return makespan

    # Operatory genetyczne

    # Krzyżowanie (crossover)
    def crossover(self, parent1, parent2):
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
    
    # Mutacja
    def mutate(self, solution, i):
        """Mutacja osobnika. w  funkcji dobierana jest jedna z metod mutacji w zależności od stopnia rzadkości losowania

        Args:
            solution (list): Osobnik, czyli permutacja zadań.

        Returns:
            list: Zmutowany osobnik.
        """
        mutation_occurance_chance = random.random()
        #algorytm mutacji (HARD) zamiana ciągów miejscami
        if mutation_occurance_chance < (self.mutation_rate ** 2):
            print("HARD_!_!_!_"+ str(i))
            newchild = solution[random.randint(1, int(len(solution) - 1)):]
            newchild += [gene for gene in solution if gene not in newchild]
            return newchild
        #algorytm mutacji (MID) zamiana losowych elementów
        if mutation_occurance_chance < self.mutation_rate:
            print("MID_____"+ str(i))
            idx1, idx2 = random.sample(range(len(solution)), 2)
            solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
            return solution
        #algorytm mutacji (SOFT) zamiana sąsiadów
        if mutation_occurance_chance < math.sqrt(self.mutation_rate):
            print("SOFT_____"+ str(i))
            point = random.randint(1, int(len(solution) - 2))
            solution[point], solution[point+1] = solution[point+1], solution[point]
            return solution
        
        return solution
    
    


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
            selected_parents = self.TournamentSelection(3,evaluated_population) #[solution for solution, _ in evaluated_population[:self.population_size // 2]]

            # Krzyżowanie i mutacja
            children = []
            while len(children) < self.population_size:
                parent1 = random.choice(selected_parents)
                parent2 = random.choice(selected_parents)
                child = self.crossover_by_section(parent1, parent2)
                if random.random() < self.mutation_rate:
                    child = self.mutate(child,i)
                children.append(child)

            # Aktualizacja populacji
            population = children

            # Wybór najlepszego rozwiązania
            if len(best_solutions) > 0:
                best_solution, _ = evaluated_population[0]
                if(C_Max(self.jobs,best_solutions[-1]) > C_Max(self.jobs,best_solution)):
                    print("We got _new_ best Cmax:" + str(C_Max(self.jobs,best_solution)))
                    best_solutions.append(best_solution)
            else:
                best_solution, _ = evaluated_population[0]
                print("We got first best Cmax:" + str(C_Max(self.jobs,best_solution)))
                best_solutions.append(best_solution)

        return best_solutions