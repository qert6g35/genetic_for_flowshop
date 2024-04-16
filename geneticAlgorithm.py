import numpy as np

# Słowniczek
# population - lista permutacji
# candidate - osobnik, permutacja zadań

# inicjalizuje populacje dla algorytmu genetycznego
# Przyjmowane zmienne
# _size         - rozmiar populacji
# _n            - ilość zadań 
# 
# Zwracane zmienne
# population    - populacja niepowtarzających się osobników

def initializePopulation(_size,_n):
    population = []
    population_size = 0
    while population_size < _size:
        candidate = list(np.random.permutation(_n))
        if candidate not in population:
            population.append(candidate)
            population_size += 1
    return population


# algorytm genetyczny
# Przyjmowane zmienne
# data          - 
# generations   - 
# _size         - rozmiar populacji
# _n            - ilość zadań 
# 
# Zwracane zmienne
# ?

def Genetic(data, generations, _size, _n):
    print(str(data),generations)

    #GENEROWANIE 1. POKOLENIA
    initializePopulation(_size,_n)
    
    for _ in range(0,generations):
        print("need to work on thoes:")
        #przetrwanie, eliminacja jednostek w pokoleniu, robimy przetrwanie z losowaniem

        #krzyżowanie osobników, sugestia prow:/krzyżówka klasyczna/

        #mutacja osobników

        #DODATKOWO warunek zakończenia np ilosć iteracji bez poprawy
