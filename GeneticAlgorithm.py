import numpy as np
import random
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
        print("Rozmiar populacji jest ustawiony na: ",self.population_size)

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

    # Mutacja
    def mutate(self, solution):
        """Mutacja osobnika.

        Args:
            solution (list): Osobnik, czyli permutacja zadań.

        Returns:
            list: Zmutowany osobnik.
        """
        # jakiś tam algorytm mutacji
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(solution)), 2)
            solution[idx1], solution[idx2] = solution[idx2], solution[idx1]
        return solution


    # Algorytm genetyczny
    def Genetic(self):
        """Implementacja genetycznego algorytmu optymalizacji.

        Returns:
            list: Najlepsze rozwiązanie.
        """
        # GENEROWANIE 1. POKOLENIA
        population = self.initializePopulation()
        for _ in range(self.generations):
            # Ocena populacji
            evaluated_population = [(solution, self.evaluate(solution)) for solution in population]
            evaluated_population.sort(key=lambda x: x[1])

            # Wybór najlepszych osobników do reprodukcji (selekcja)
            selected_parents = [solution for solution, _ in evaluated_population[:self.population_size // 2]]

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
        best_solution, best_fitness = evaluated_population[0]
        return best_solution
