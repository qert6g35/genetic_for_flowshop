from RandomGenerator import RandomGenerator 
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import pandas as pd
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

# zwraca dataframe z taskami do wykresu
# Przyjmowane zmienne
# J             - lista zadań
# pi            - permutacja
# start_times   - harmonogram czasów rozpoczęcia
#
# Zwracane zmienne
# df            - dataframe potrzebny do wygenerowania wykresu

def tasks_df(pi, J, start_times):
    n = len(J)  # liczba zadań
    m = len(J[0])  # liczba mapipszyn
    data = []
    Tasks = [J[pi[i]] for i in range(len(pi))]
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

# Wyświetla poglądowy wykres ganta dla ulozonych zadań
# Przyjmowane zmienne
# df            - dataframe generowany przez funckje task_df

def plot_schedule(df):
    fig, ax = plt.subplots(1, figsize=(16,6))
    ax.barh(df.Maszyna, df.Czas_Trwania, left=df.Czas_Rozpoczęcia,color=df.Color)
    plt.show()

# Wyświetla wykres ganta dla ulozonych zadań
# Przyjmowane zmienne
# J             - lista zadań
# pi            - permutacja
# start_times   - harmonogram czasów rozpoczęcia
#

def plot_schedule_fancy(pi, J, start_times):
    n = len(J)  # liczba zadań
    m = len(J[0])  # liczba mapipszyn
    Tasks = [J[pi[i]] for i in range(len(pi))]
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
# _M        - ilość maszyn
# _seed     - seed dla generatora pseudolosowego
#
# Zwracane zmienne
# J         - lista zadań
# pi        - permutacja

def GenerateJ(_n,_M,_seed):     
    rng = RandomGenerator(_seed)
    n = _n
    M  = _M
    J = []
    pi = []
    for i in range(n):
        p_ij = [rng.next_int(1, 9) for _ in range(M)]
        pi.append(i);
        J.append(copy.deepcopy(p_ij))
    return J, pi

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista zadań
# _pi       - permutacja
#
# Zwracane zmienne
# C         - harmonogram czasów zakończenia


def EvaluateC(_J, _pi):           
    J_matrix = [_J[_pi[i]] for i in range(len(_pi))]
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
# _J        - lista zadań
# _pi       - permutacja
#
# Zwracane zmienne
# Cmax      - czas zakończenia ostatniego zadania

def CalculateCmax( _J, _pi):
    Cmax = EvaluateC(_J, _pi)
    return Cmax[-1][-1]

# Oblicza C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
# Przyjmowane zmienne
# _J        - lista zadań
# _C        - harmonogram czasów zakończenia
# _pi       - permutacja
#
# Zwracane zmienne
# _         - lista z listami czasów rozpoczęcia obiektów

def start_t(_J, _pi, _C):
    J_matrix = [_J[_pi[i]] for i in range(len(_pi))]
    return [[_C[i][j] - J_matrix[i][j] for j in range(len(_C[i]))] for i in range(len(_C))]