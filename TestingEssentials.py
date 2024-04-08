from RandomGenerator import RandomGenerator 
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import pandas as pd
from Task import Task
import copy
from matplotlib.patches import Patch

##########################################################
#
#           Część odpowiedzialna za wykresy - wymaga przerobienia pod nowy typ Task
#
##########################################################

# Generuje losowy kolor dla zadania do wykresu
# Przyjmowane zmienne
# rng       - obiekt RandomGenerator
#
# Zwracane zmienne
# color_hex - kod hex koloru

def generate_random_color(rng):
    r = rng.next_int(0, 255)
    g = rng.next_int(0, 255)
    b = rng.next_int(0, 255)
    color_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return color_hex    
#
#   TO DO 
#
def tasks_df(pi,Tasks, start_times):
    n = len(Tasks)  # liczba zadań
    m = len(Tasks[0])  # liczba mapipszyn
    data = []
    c_dict = {}
    rng = RandomGenerator(1)
    for task in range(n):
        for machine in range(m):
            start_time = start_times[task][machine]
            duration = Tasks[task][machine]
            hlp =  str(pi[task])
            if not hlp in c_dict:
                c_dict[hlp] = generate_random_color(rng)
            color = c_dict[hlp]
            data.append([pi[task], machine+1, start_time, duration, color])

    df = pd.DataFrame(data, columns=['Zadanie', 'Maszyna', 'Czas_Rozpoczęcia', 'Czas_Trwania','Color'])
    return df

def plot_schedule(df):
    fig, ax = plt.subplots(1, figsize=(16,6))
    ax.barh(df.Maszyna, df.Czas_Trwania, left=df.Czas_Rozpoczęcia,color=df.Color)
    plt.show()

#
#   TO DO
#
def plot_schedule_fancy(pi,start_times,Tasks):
    n = len(Tasks)  # liczba zadań
    m = len(Tasks[0])  # liczba mapipszyn
    data = []
    c_dict = {}
    end_set = set()
    rng = RandomGenerator(1)
    for task in range(n):
        for machine in range(m):
            start_time = start_times[task][machine]
            duration = Tasks[task][machine]
            end_set.add(start_time+duration)
            hlp = str(pi[task])
            if not hlp in c_dict:
                c_dict[hlp] = generate_random_color(rng)
            color = c_dict[hlp]
            data.append([pi[task], machine+1, start_time, duration, color])

    df = pd.DataFrame(data, columns=['Zadanie', 'Maszyna', 'Czas_Rozpoczęcia', 'Czas_Trwania','Color'])
    fig, ax = plt.subplots(1, figsize=(16,6))
    ax.barh(df.Maszyna, df.Czas_Trwania, left=df.Czas_Rozpoczęcia,color=df.Color)
    legend_elements = [Patch(facecolor=c_dict[i], label=i)  for i in c_dict]
    plt.legend(handles=legend_elements)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.xlabel('czas')
    plt.ylabel('maszyny')
    plt.xticks(list(end_set))
    plt.show()
    
    
##########################################################
#
#           Część odpowiedzialna za operacje na zbiorze zadań i permutacji
#
##########################################################

# Zwraca listę J obiektów typu Task na podstawie zadanych parametrów
# Przyjmowane zmienne
# _n        - ilość zadań
# _m        - ilość maszyn
# _seed     - seed dla generatora pseudolosowego
#
# Zwracane zmienne
# J         - lista obiektów typu Task

def GenerateJ(_n,_M,_seed):     
    rng = RandomGenerator(_seed)
    n = _n
    M  = _M
    J =[]
    for i in range(n):
        p_ij = [rng.next_int(1, 9) for _ in range(M)]
        J.append(copy.deepcopy(Task(p_ij,i)))
    return J

# Na potrzeby pozostałych funkcji w tym pliku, zmienia listę obiektów typu Task na listę id i listę list czasów J_matrix
# Przyjmowane zmienne
# _J        - lista obiektów typu Task
#
# Zwracane zmienne
# J_matrix  - lista z listami czasów obiektów
# id        - lista z indeksami

def FromTasksToMatrix(_J):
    J_matrix = []
    id = []
    for i in range(len(_J)):
        J_matrix.append(_J[i].times)
        id.append(_J[i].id)
    return id, J_matrix

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista obiektów typu Task
#
# Zwracane zmienne
# C         - lista z listami czasów obiektów

def EvaluateC(_J):           
    _, J_matrix = FromTasksToMatrix(_J)
    n = len(J_matrix)
    m = len(J_matrix[0])
    C = [[0] * m for _ in range(n)]

    C[0][0] = J_matrix[0][0]  # Czas zakończenia 1. zadania na 1. maszynie
    for i in range(1,m):
        C[0][i] = J_matrix[0][i]+C[0][i-1] # Obliczamy czasy zakończenia 1. zadania na reszcie maszyn

    # Czasy zakończenia pozostałych zadań
    for j in range(1, n): 
        for i in range(m):
            C[j][i] = max(C[j-1][i], C[j][i-1]) + J_matrix[j][i] # zadanie moze zacząć się dopiero jak jego część na poprzedniej maszynie zostanie zrealizowana oraz aktualna maszyna sie zwolni. 
                                                           # Aby uzyskać czas ukończenia musimy dodać jeszcze czas trwania
    return C

# Oblicza Cmax dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista obiektów typu Task
#
# Zwracane zmienne
# Cmax      - lista z listami czasów obiektów

def CalculateCmax( _J):
    Cmax = EvaluateC(_J)
    return Cmax[-1][-1]

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista obiektów typu Task
# C         - lista z listami czasów obiektów
#
# Zwracane zmienne
# _         - lista z listami czasów rozpoczęcia obiektów

def start_t(_J, C):
    _, J_matrix = FromTasksToMatrix(_J)
    return [[C[i][j] - J_matrix[i][j] for j in range(len(C[i]))] for i in range(len(C))]