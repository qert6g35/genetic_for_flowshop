from RandomGenerator import RandomGenerator 
from matplotlib.ticker import MaxNLocator
import copy 
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

def start_t(pi, C):
    return [[C[i][j] - pi[i][j] for j in range(len(C[i]))] for i in range(len(C))]


def generate_random_color(rng):
    r = rng.nextInt(0, 255)
    g = rng.nextInt(0, 255)
    b = rng.nextInt(0, 255)
    color_hex = '#{:02x}{:02x}{:02x}'.format(r, g, b)
    return color_hex    

def tasks_df(pi,start_times,Tasks):
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

def GenerateJ(_n,_M,_seed):     # Generuje nam J wypełnione _n zadaniami na _M maszyn z ziarnem _seed
    rng = RandomGenerator(_seed)
    n = _n
    M  = _M
    J =[]
    for i in range(n):
        p_ij = [rng.nextInt(1, 9) for _ in range(M)]
        J.append(copy.deepcopy(p_ij))
    return J

def EvaluateC(_J):           # Oblicza nam C dla kolejności zadań w podanym _J, rozszerzalne na wiele maszyn
    n = len(_J)
    m = len(_J[0])
    C = [[0] * m for _ in range(n)]

    C[0][0] = _J[0][0]  # Czas zakończenia 1. zadania na 1. maszynie
    for i in range(1,m):
        C[0][i] = _J[0][i]+C[0][i-1] # Obliczamy czasy zakończenia 1. zadania na reszcie maszyn

    # Czasy zakończenia pozostałych zadań
    for j in range(1, n): 
        for i in range(m):
            C[j][i] = max(C[j-1][i], C[j][i-1]) + _J[j][i] # zadanie moze zacząć się dopiero jak jego część na poprzedniej maszynie zostanie zrealizowana oraz aktualna maszyna sie zwolni. 
                                                           # Aby uzyskać czas ukończenia musimy dodać jeszcze czas trwania
    return C

def GetListOfTasks(_J, _numeration):    # daje liste zadań
    pi = [_J[i-1] for i in _numeration]
    return pi

def GetNumeration(_J, _pi):             # daje numeracje 
    numeration = [_J.index(x) for x in _pi]
    return numeration
