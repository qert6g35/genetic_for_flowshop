import numpy as np

######################################3#
#
#   Słowniczek
#
#   population - lista permutacji
#   candidate - osobnik, permutacja zadań
#

def initializePopulation(_size,_n):
    """inicjalizuje populacje dla algorytmu genetycznego

    Args:
        _size (int): rozmiar populacji
        _n (int): ilość zadań 

    Returns:
        array: populacja niepowtarzających się osobników
    """
    population = []
    population_size = 0
    while population_size < _size:
        candidate = list(np.random.permutation(_n))
        if candidate not in population:
            population.append(candidate)
            population_size += 1
    return population


# algorytm genetyczny - opis jeszcze moze sie zmieni
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
